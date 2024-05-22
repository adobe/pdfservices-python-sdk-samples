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
from adobe.pdfservices.operation.pdfjobs.jobs.reorder_pages_job import ReorderPagesJob
from adobe.pdfservices.operation.pdfjobs.params.page_ranges import PageRanges
from adobe.pdfservices.operation.pdfjobs.params.reorder_pages.reorder_pages_params import ReorderPagesParams
from adobe.pdfservices.operation.pdfjobs.result.reorder_pages_result import ReorderPagesResult

# Initialize the logger
logging.basicConfig(level=logging.INFO)


#
# This sample illustrates how to reorder the pages in a PDF file.
#
# Refer to README.md for instructions on how to run the samples.
#
class ReorderPDFPages:
    def __init__(self):
        try:
            file = open('src/resources/reorderPagesInput.pdf', 'rb')
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
            input_asset = pdf_services.upload(input_stream=input_stream, mime_type=PDFServicesMediaType.PDF)

            pages_to_reorder = self.get_page_range_for_reorder()

            # Create parameters for the job
            reorder_pages_params = ReorderPagesParams(asset=input_asset, page_ranges=pages_to_reorder)

            # Creates a new job instance
            reorder_pages_job = ReorderPagesJob(reorder_pages_params=reorder_pages_params)

            # Submit the job and gets the job result
            location = pdf_services.submit(reorder_pages_job)
            pdf_services_response = pdf_services.get_job_result(location, ReorderPagesResult)

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
        os.makedirs("output/ReorderPDFPages", exist_ok=True)
        return f"output/ReorderPDFPages/reorder{time_stamp}.pdf"

    @staticmethod
    def get_page_range_for_reorder() -> PageRanges:
        # Specify order of the pages for an output document
        page_ranges = PageRanges()
        # Add pages 3 to 4
        page_ranges.add_range(3, 4)
        # Add page 1
        page_ranges.add_single_page(1)
        return page_ranges


if __name__ == "__main__":
    ReorderPDFPages()
