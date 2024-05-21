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
from adobe.pdfservices.operation.pdfjobs.jobs.replace_pages_job import ReplacePagesJob
from adobe.pdfservices.operation.pdfjobs.params.page_ranges import PageRanges
from adobe.pdfservices.operation.pdfjobs.params.replace_pages.replace_pages_params import ReplacePagesParams
from adobe.pdfservices.operation.pdfjobs.result.replace_page_result import ReplacePagesResult

# Initialize the logger
logging.basicConfig(level=logging.INFO)


#
# This sample illustrates how to replace specific pages in a PDF file.
#
# Refer to README.md for instructions on how to run the samples.
#
class ReplacePDFPages:
    def __init__(self):
        try:
            base_file = open('src/resources/baseInput.pdf', 'rb')
            base_input_stream = base_file.read()
            base_file.close()

            file_1 = open('src/resources/replacePagesInput1.pdf', 'rb')
            input_stream_1 = file_1.read()
            file_1.close()

            file_2 = open('src/resources/replacePagesInput2.pdf', 'rb')
            input_stream_2 = file_2.read()
            file_2.close()

            # Initial setup, create credentials instance
            credentials = ServicePrincipalCredentials(
                client_id=os.getenv('PDF_SERVICES_CLIENT_ID'),
                client_secret=os.getenv('PDF_SERVICES_CLIENT_SECRET')
            )

            # Creates a PDF Services instance
            pdf_services = PDFServices(credentials=credentials)

            # Creates an asset(s) from source file(s) and upload
            base_asset = pdf_services.upload(input_stream=base_input_stream,
                                              mime_type=PDFServicesMediaType.PDF)
            asset_1 = pdf_services.upload(input_stream=input_stream_1,
                                         mime_type=PDFServicesMediaType.PDF)
            asset_2 = pdf_services.upload(input_stream=input_stream_2,
                                          mime_type=PDFServicesMediaType.PDF)

            page_ranges = self.get_page_range_for_first_file()

            # Create parameters for the job
            replace_pages_params = ReplacePagesParams(base_asset=base_asset)

            # Add the first asset as input to the params, along with its page ranges and base page
            replace_pages_params.add_pages_to_replace(input_asset=asset_1, page_ranges=page_ranges, base_page=1)

            # Add the second asset as input to the params, along with base page
            replace_pages_params.add_pages_to_replace(input_asset=asset_2, base_page=3)

            # Creates a new job instance
            replace_pages_job = ReplacePagesJob(replace_pages_params=replace_pages_params)

            # Submit the job and gets the job result
            location = pdf_services.submit(replace_pages_job)
            pdf_services_response = pdf_services.get_job_result(location, ReplacePagesResult)

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
        os.makedirs("output/ReplacePDFPages", exist_ok=True)
        return f"output/ReplacePDFPages/replace{time_stamp}.pdf"

    @staticmethod
    def get_page_range_for_first_file() -> PageRanges:
        # Specify page ranges
        page_ranges = PageRanges()
        # Add pages 1 to 3
        page_ranges.add_range(1, 3)
        # Add page 4
        page_ranges.add_single_page(4)
        return page_ranges


if __name__ == "__main__":
    ReplacePDFPages()
