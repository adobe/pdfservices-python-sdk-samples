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
from adobe.pdfservices.operation.io.stream_asset import StreamAsset
from adobe.pdfservices.operation.pdf_services import PDFServices
from adobe.pdfservices.operation.pdf_services_media_type import PDFServicesMediaType
from adobe.pdfservices.operation.pdfjobs.jobs.autotag_pdf_job import AutotagPDFJob
from adobe.pdfservices.operation.pdfjobs.params.autotag_pdf.autotag_pdf_params import AutotagPDFParams
from adobe.pdfservices.operation.pdfjobs.result.autotag_pdf_result import AutotagPDFResult

# Initialize the logger
logging.basicConfig(level=logging.INFO)


#
# This sample illustrates how to generate a tagged PDF along with a report and shift the headings in
# the output PDF file.
#
# Refer to README.md for instructions on how to run the samples.
#
class AutotagPDFWithOptions:
    def __init__(self):
        try:
            file = open('src/resources/autotagPDFInput.pdf', 'rb')
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

            # Create parameters for the job
            autotag_pdf_params = AutotagPDFParams(
                generate_report=True,
                shift_headings=True
            )

            # Creates a new job instance
            autotag_pdf_job = AutotagPDFJob(input_asset=input_asset,
                                            autotag_pdf_params=autotag_pdf_params)

            # Submit the job and gets the job result
            location = pdf_services.submit(autotag_pdf_job)
            pdf_services_response = pdf_services.get_job_result(location, AutotagPDFResult)

            # Get content from the resulting asset(s)
            result_asset: CloudAsset = pdf_services_response.get_result().get_tagged_pdf()
            result_asset_report: CloudAsset = pdf_services_response.get_result().get_report()
            stream_asset: StreamAsset = pdf_services.get_content(result_asset)
            stream_asset_report: StreamAsset = pdf_services.get_content(result_asset_report)

            # Creates an output stream and copy stream asset's content to it
            output_file_path = self.create_output_file_path()
            output_file_path_report = self.create_output_file_path_for_tagging_report()
            with open(output_file_path, "wb") as file:
                file.write(stream_asset.get_input_stream())
            with open(output_file_path_report, "wb") as file:
                file.write(stream_asset_report.get_input_stream())

        except (ServiceApiException, ServiceUsageException, SdkException) as e:
            logging.exception(f'Exception encountered while executing operation: {e}')

    # Generates a string containing a directory structure and file name for the output file
    @staticmethod
    def create_output_file_path() -> str:
        now = datetime.now()
        time_stamp = now.strftime("%Y-%m-%dT%H-%M-%S")
        os.makedirs("output/AutotagPDF", exist_ok=True)
        return f"output/AutotagPDF/autotag-tagged{time_stamp}.pdf"

    # Generates a string containing a directory structure and file name for the tagging report output
    @staticmethod
    def create_output_file_path_for_tagging_report() -> str:
        now = datetime.now()
        time_stamp = now.strftime("%Y-%m-%dT%H-%M-%S")
        os.makedirs("output/AutotagPDF", exist_ok=True)
        return f"output/AutotagPDF/autotag-tagged{time_stamp}.xlsx"


if __name__ == "__main__":
    AutotagPDFWithOptions()
