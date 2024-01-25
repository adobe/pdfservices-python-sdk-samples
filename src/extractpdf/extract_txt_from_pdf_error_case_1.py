# Copyright 2021 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

import logging
import os.path

from adobe.pdfservices.operation.auth.credentials import Credentials
from adobe.pdfservices.operation.exception.exceptions import ServiceApiException, ServiceUsageException, SdkException
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_pdf_options import ExtractPDFOptions
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_element_type import ExtractElementType
from adobe.pdfservices.operation.execution_context import ExecutionContext
from adobe.pdfservices.operation.io.file_ref import FileRef
from adobe.pdfservices.operation.pdfops.extract_pdf_operation import ExtractPDFOperation

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


def handle_exception(exception_type, exception_message):
    logging.info(exception_type)
    logging.info(exception_message)
    return exception_type, exception_message


try:
    # get base path.
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # Initial setup, create credentials instance.
    credentials = Credentials.service_principal_credentials_builder(). \
        with_client_id(os.getenv('PDF_SERVICES_CLIENT_ID')). \
        with_client_secret(os.getenv('PDF_SERVICES_CLIENT_SECRET')). \
        build()

    # Create an ExecutionContext using credentials and create a new operation instance.
    execution_context = ExecutionContext.create(credentials)
    extract_pdf_operation = ExtractPDFOperation.create_new()

    # Set operation input from a source file.
    source = FileRef.create_from_local_file(base_path + "/resources/removeProtectionInput.pdf")
    extract_pdf_operation.set_input(source)

    # Build ExtractPDF options and set them into the operation
    extract_pdf_options: ExtractPDFOptions = ExtractPDFOptions.builder() \
        .with_element_to_extract(ExtractElementType.TEXT) \
        .build()
    extract_pdf_operation.set_options(extract_pdf_options)

    # Execute the operation.
    result: FileRef = extract_pdf_operation.execute(execution_context)

    # Save the result to the specified location.
    result.save_as(base_path + "/output/ExtractTextInfoFromPDF.zip")
except ServiceApiException as serviceApiException:
    # ServiceApiException is thrown when an underlying service API call results in an error.
    handle_exception("ServiceApiException", serviceApiException.message)
except ServiceUsageException as serviceUsageException:
    # ServiceUsageError is thrown when either service usage limit has been reached or credentials quota has been
    # exhausted.
    handle_exception("ServiceUsageException", serviceUsageException.message)
except SdkException as sdkException:
    # SdkException is typically thrown for client-side or network errors.
    handle_exception("SdkException", sdkException.message)

