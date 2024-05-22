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
from adobe.pdfservices.operation.pdfjobs.jobs.insert_pages_job import InsertPagesJob
from adobe.pdfservices.operation.pdfjobs.params.insert_pages.insert_pages_params import InsertPagesParams
from adobe.pdfservices.operation.pdfjobs.params.page_ranges import PageRanges
from adobe.pdfservices.operation.pdfjobs.result.insert_pages_result import InsertPagesResult

# Initialize the logger
logging.basicConfig(level=logging.INFO)


#
# This sample illustrates how to insert specific pages of multiple PDF files into a single PDF file.
#
# Refer to README.md for instructions on how to run the samples.
#
class InsertPDFPages:
    def __init__(self):
        try:
            base_file = open('src/resources/baseInput.pdf', 'rb')
            base_input_stream = base_file.read()
            base_file.close()

            first_file_to_insert = open('src/resources/firstFileToInsertInput.pdf', 'rb')
            first_input_stream_to_insert = first_file_to_insert.read()
            first_file_to_insert.close()

            second_file_to_insert = open('src/resources/secondFileToInsertInput.pdf', 'rb')
            second_input_stream_to_insert = second_file_to_insert.read()
            second_file_to_insert.close()

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
            first_asset_to_insert = pdf_services.upload(input_stream=first_input_stream_to_insert,
                                          mime_type=PDFServicesMediaType.PDF)
            second_asset_to_insert = pdf_services.upload(input_stream=second_input_stream_to_insert,
                                          mime_type=PDFServicesMediaType.PDF)

            page_ranges = self.get_page_range_for_first_file()

            # Create parameters for the job
            insert_pages_params = InsertPagesParams(base_asset=base_asset)

            # Add the first asset as input to the params, along with its page ranges and base page
            insert_pages_params.add_pages_to_insert(input_asset=first_asset_to_insert, page_ranges=page_ranges, base_page=2)

            # Add the second asset as input to the params, along with base page
            insert_pages_params.add_pages_to_insert(input_asset=second_asset_to_insert, base_page=3)

            # Creates a new job instance
            insert_pages_job = InsertPagesJob(insert_pages_params=insert_pages_params)

            # Submit the job and gets the job result
            location = pdf_services.submit(insert_pages_job)
            pdf_services_response = pdf_services.get_job_result(location, InsertPagesResult)

            # Get content from the resulting asset(s)
            result_asset: CloudAsset = pdf_services_response.get_result().get_asset()
            stream_asset: StreamAsset = pdf_services.get_content(result_asset)

            # Creates an output stream and copy stream asset's content to it
            output_file_path = "insertpagesOutput.pdf"
            with open(output_file_path, "wb") as file:
                file.write(stream_asset.get_input_stream())

        except (ServiceApiException, ServiceUsageException, SdkException) as e:
            logging.exception(f'Exception encountered while executing operation: {e}')

    @staticmethod
    def get_page_range_for_first_file() -> PageRanges:
        # Specify which pages of the first file are to be included in the combined file
        page_ranges_for_first_file = PageRanges()
        # Add pages 1 to 3
        page_ranges_for_first_file.add_range(1, 3)
        # Add single page 1
        page_ranges_for_first_file.add_single_page(1)
        return page_ranges_for_first_file


if __name__ == "__main__":
    InsertPDFPages()
