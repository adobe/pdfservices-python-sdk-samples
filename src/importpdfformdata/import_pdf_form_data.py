#!/usr/bin/env python3

"""
Copyright 2024 Adobe
All Rights Reserved.

NOTICE: Adobe permits you to use, modify, and distribute this file in
accordance with the terms of the Adobe license agreement accompanying it.
"""

import logging
import os
from datetime import datetime
from pathlib import Path

from adobe.pdfservices.operation.auth.service_principal_credentials import ServicePrincipalCredentials
from adobe.pdfservices.operation.config.client_config import ClientConfig
from adobe.pdfservices.operation.exception.exceptions import ServiceApiException, ServiceUsageException, SdkException
from adobe.pdfservices.operation.pdf_services import PDFServices
from adobe.pdfservices.operation.pdf_services_media_type import PDFServicesMediaType
from adobe.pdfservices.operation.pdfjobs.jobs.import_pdf_form_data_job import ImportPDFFormDataJob
from adobe.pdfservices.operation.pdfjobs.params.import_pdf_form_data.import_pdf_form_data_params import ImportPDFFormDataParams
from adobe.pdfservices.operation.pdfjobs.result.import_pdf_form_data_result import ImportPDFFormDataResult

# Initialize the logger
logging.basicConfig(level=logging.INFO)


class ImportPDFFormData:
    def __init__(self):
        try:
            file = open('src/resources/importPdfFormDataInput.pdf', 'rb')
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

            # Form data to be imported
            form_data = {
                "option_two": "Yes",
                "option_one": "Yes",
                "name": "garvit",
                "option_three": "Off",
                "age": "24",
                "favorite_movie": "Star Wars Again",
            }

            # Create parameters for the job
            import_pdf_form_data_params = ImportPDFFormDataParams(json_form_fields_data=form_data)

            # Creates a new job instance
            import_pdf_form_data_job = ImportPDFFormDataJob(input_asset=input_asset)

            # Set the parameters for the job
            import_pdf_form_data_job.set_params(import_pdf_form_data_params)

            # Submit the job and gets the job result
            location = pdf_services.submit(import_pdf_form_data_job)
            pdf_services_response = pdf_services.get_job_result(location, ImportPDFFormDataResult)

            # Get content from the resulting asset(s)
            result_asset = pdf_services_response.get_result().get_asset()
            stream_asset = pdf_services.get_content(result_asset)

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
        os.makedirs("output/ImportPDFFormData", exist_ok=True)
        return f"output/ImportPDFFormData/import{time_stamp}.pdf"


if __name__ == "__main__":
    ImportPDFFormData() 
