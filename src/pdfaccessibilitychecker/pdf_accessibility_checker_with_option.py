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
from adobe.pdfservices.operation.exception.exceptions import ServiceApiException, SdkException, ServiceUsageException
from adobe.pdfservices.operation.io.cloud_asset import CloudAsset
from adobe.pdfservices.operation.io.stream_asset import StreamAsset
from adobe.pdfservices.operation.pdf_services import PDFServices
from adobe.pdfservices.operation.pdf_services_media_type import PDFServicesMediaType
from adobe.pdfservices.operation.pdfjobs.jobs.pdf_accessibility_checker_job import PDFAccessibilityCheckerJob
from adobe.pdfservices.operation.pdfjobs.params.pdf_accessibility_checker.pdf_accessibility_checker_params import \
    PDFAccessibilityCheckerParams
from adobe.pdfservices.operation.pdfjobs.result.pdf_accessibility_checker_result import PDFAccessibilityCheckerResult

# Initialize the logger
logging.basicConfig(level=logging.INFO)

#
# This sample illustrates how to generate an accessibility check report of input PDF
# file for given page start and page end.
#
# Refer to README.md for instructions on how to run the samples.
#
class PDFAccessibilityChecker:
    def __init__(self):
        try:
            pdf_file = open("src/resources/CheckerPDFInput.pdf", 'rb')
            input_stream = pdf_file.read()
            pdf_file.close()

            # Initial setup, create credentials instance
            credentials = ServicePrincipalCredentials(
                client_id=os.getenv('PDF_SERVICES_CLIENT_ID'),
                client_secret=os.getenv('PDF_SERVICES_CLIENT_SECRET'))

            # Creates a PDF Services instance
            pdf_services = PDFServices(credentials=credentials)

            # Creates an asset(s) from source file(s) and upload
            input_asset = pdf_services.upload(input_stream=input_stream, mime_type=PDFServicesMediaType.PDF)

            # Create parameters for the job
            pdf_accessibility_checker_params = PDFAccessibilityCheckerParams(page_start=1, page_end=2)

            # Creates a new job instance
            pdf_accessibility_checker_job = PDFAccessibilityCheckerJob(input_asset=input_asset,
                                                                       pdf_accessibility_checker_params=pdf_accessibility_checker_params)
            # Submit the job and gets the job result
            location = pdf_services.submit(pdf_accessibility_checker_job)
            pdf_services_response = pdf_services.get_job_result(location, PDFAccessibilityCheckerResult)

            # Get content from the resulting asset(s)
            result_asset: CloudAsset = pdf_services_response.get_result().get_asset()
            stream_asset: StreamAsset = pdf_services.get_content(result_asset)

            report_asset: CloudAsset = pdf_services_response.get_result().get_report()
            stream_report: StreamAsset = pdf_services.get_content(report_asset)

            output_file_path = self.create_pdf_output_file_path()

            with open(output_file_path, "wb") as file:
                file.write(stream_asset.get_input_stream())

            output_file_path_json = self.create_json_output_file_path()
            with open(output_file_path_json, "wb") as file:
                file.write(stream_report.get_input_stream())

        except (ServiceApiException, ServiceUsageException, SdkException) as e:
            logging.exception(f'Exception encountered while executing operation: {e}')

    # Generates a string containing a directory structure and file name for the output file

    def create_pdf_output_file_path(self) -> str:
        now = datetime.now()
        time_stamp = now.strftime("%Y-%m-%dT%H-%M-%S")
        os.makedirs("output/PDFAccessibilityCheckerWithOptions", exist_ok=True)
        return f"output/PDFAccessibilityCheckerWithOptions/accessibilitychecker{time_stamp}.pdf"

    def create_json_output_file_path(self) -> str:
        now = datetime.now()
        time_stamp = now.strftime("%Y-%m-%dT%H-%M-%S")
        os.makedirs("output/PDFAccessibilityCheckerWithOptions", exist_ok=True)
        return f"output/PDFAccessibilityCheckerWithOptions/accessibilitychecker{time_stamp}.json"

if __name__ == "__main__":
    PDFAccessibilityChecker()
