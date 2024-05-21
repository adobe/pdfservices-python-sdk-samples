"""
 Copyright 2024 Adobe
 All Rights Reserved.

 NOTICE: Adobe permits you to use, modify, and distribute this file in
 accordance with the terms of the Adobe license agreement accompanying it.
"""

import logging
import os
from datetime import datetime

from adobe.pdfservices.operation.auth.service_principal_credentials import ServicePrincipalCredentials
from adobe.pdfservices.operation.exception.exceptions import ServiceApiException, ServiceUsageException, SdkException
from adobe.pdfservices.operation.io.cloud_asset import CloudAsset
from adobe.pdfservices.operation.io.external_asset import ExternalAsset
from adobe.pdfservices.operation.io.external_storage_type import ExternalStorageType
from adobe.pdfservices.operation.io.stream_asset import StreamAsset
from adobe.pdfservices.operation.pdf_services import PDFServices
from adobe.pdfservices.operation.pdfjobs.jobs.create_pdf_job import CreatePDFJob
from adobe.pdfservices.operation.pdfjobs.result.create_pdf_result import CreatePDFResult

# Initialize the logger
logging.basicConfig(level=logging.INFO)


#
# This sample illustrates how to use external storage as input in PDF Services.
# For this illustration a PDF file will be created from a DOCX file stored externally.
#
# Refer to README.md for instructions on how to run the samples.
#
class ExternalInputCreatePDFFromDOCX:
    def __init__(self):
        try:
            # Initial setup, create credentials instance
            credentials = ServicePrincipalCredentials(
                client_id=os.getenv('PDF_SERVICES_CLIENT_ID'),
                client_secret=os.getenv('PDF_SERVICES_CLIENT_SECRET')
            )

            # Creates a PDF Services instance
            pdf_services = PDFServices(credentials=credentials)

            # Creating external asset from pre signed URL.
            input_pre_signed_url = "INPUT_PRESIGNED_URL"
            input_external_asset = ExternalAsset(uri=input_pre_signed_url, external_storage_type=ExternalStorageType.S3)

            # Creates a new job instance
            create_pdf_job = CreatePDFJob(input_asset=input_external_asset)

            # Submit the job and gets the job result
            location = pdf_services.submit(create_pdf_job)
            pdf_services_response = pdf_services.get_job_result(location, CreatePDFResult)

            # Get content from the resulting asset(s)
            result_asset: CloudAsset = pdf_services_response.get_result().get_asset()
            stream_asset: StreamAsset = pdf_services.get_content(result_asset)

            # Creates an output stream and copy stream asset's content to it
            output_file_path = self.create_output_file_path()
            with open(output_file_path, "wb") as file:
                file.write(stream_asset.get_input_stream())
        except (ServiceApiException, ServiceUsageException, SdkException) as e:
            logging.exception(f'Exception encountered while executing operation: {e}')

    # Generates a string containing a directory structure and file name for the output file
    @staticmethod
    def create_output_file_path() -> str:
        now = datetime.now()
        time_stamp = now.strftime("%Y-%m-%dT%H-%M-%S")
        os.makedirs("output/ExternalInputCreatePDFFromDOCX", exist_ok=True)
        return f"output/ExternalInputCreatePDFFromDOCX/create{time_stamp}.pdf"


if __name__ == "__main__":
    ExternalInputCreatePDFFromDOCX()
