"""
 Copyright 2024 Adobe
 All Rights Reserved.

 NOTICE: Adobe permits you to use, modify, and distribute this file in
 accordance with the terms of the Adobe license agreement accompanying it.
"""

import logging
import os

from adobe.pdfservices.operation.auth.service_principal_credentials import ServicePrincipalCredentials
from adobe.pdfservices.operation.exception.exceptions import ServiceApiException, ServiceUsageException, SdkException
from adobe.pdfservices.operation.pdf_services import PDFServices
from adobe.pdfservices.operation.pdf_services_media_type import PDFServicesMediaType
from adobe.pdfservices.operation.pdfjobs.jobs.pdf_properties_job import PDFPropertiesJob
from adobe.pdfservices.operation.pdfjobs.params.pdf_properties.pdf_properties_params import PDFPropertiesParams
from adobe.pdfservices.operation.pdfjobs.result.pdf_properties_result import PDFPropertiesResult

# Initialize the logger
logging.basicConfig(level=logging.INFO)


#
# This sample illustrates how to retrieve properties of an input PDF file.
#
# Refer to README.md for instructions on how to run the samples.
#
class GetPDFProperties:
    def __init__(self):
        try:
            file = open('src/resources/pdfPropertiesInput.pdf', 'rb')
            input_stream = file.read()
            file.close()

            # Initial setup, create credentials instance
            credentials = ServicePrincipalCredentials(
                client_id=os.getenv('PDF_SERVICES_CLIENT_ID'),
                client_secret=os.getenv('PDF_SERVICES_CLIENT_SECRET')
            )

            # Creates a PDF Services instance
            pdf_services = PDFServices(credentials=credentials)

            # Creates an asset(s) from source file(s) and upload
            input_asset = pdf_services.upload(input_stream=input_stream,
                                              mime_type=PDFServicesMediaType.PDF)

            pdf_properties_params = PDFPropertiesParams(include_page_level_properties=True)

            # Creates a new job instance
            pdf_properties_job = PDFPropertiesJob(input_asset=input_asset, pdf_properties_params=pdf_properties_params)

            # Submit the job and gets the job result
            location = pdf_services.submit(pdf_properties_job)
            pdf_services_response = pdf_services.get_job_result(location, PDFPropertiesResult)

            pdf_properties_result = pdf_services_response.get_result()

            # Fetch the requisite properties of the specified PDF.
            print("Size of the specified PDF file:"
                  + str(pdf_properties_result.get_pdf_properties_dict().get("document").get("file_size")))
            print("Version of the specified PDF file:"
                  + str(pdf_properties_result.get_pdf_properties_dict().get("document").get("pdf_version")))
            print("Page count of the specified PDF file:"
                  + str(pdf_properties_result.get_pdf_properties_dict().get("document").get("page_count")))

        except (ServiceApiException, ServiceUsageException, SdkException) as e:
            logging.exception(f'Exception encountered while executing operation: {e}')


if __name__ == '__main__':
    GetPDFProperties()