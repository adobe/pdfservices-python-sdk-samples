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
from adobe.pdfservices.operation.pdfjobs.jobs.delete_pages_job import DeletePagesJob
from adobe.pdfservices.operation.pdfjobs.params.delete_pages.delete_pages_params import DeletePagesParams
from adobe.pdfservices.operation.pdfjobs.params.page_ranges import PageRanges
from adobe.pdfservices.operation.pdfjobs.result.delete_pages_result import DeletePagesResult

# Initialize the logger
logging.basicConfig(level=logging.INFO)


#
# This sample illustrates how to delete pages in a PDF file.
#
# Refer to README.md for instructions on how to run the samples.
#
class DeletePDFPages:
    def __init__(self):
        try:
            file = open('src/resources/deletePagesInput.pdf', 'rb')
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

            # Delete pages of the document (as specified by PageRanges).
            page_ranges_for_deletion = self.get_page_ranges_for_deletion()

            # Create parameters for the job
            delete_pages_params = DeletePagesParams(page_ranges=page_ranges_for_deletion)

            # Creates a new job instance
            delete_pages_job = DeletePagesJob(input_asset=input_asset,
                                              delete_pages_params=delete_pages_params)

            # Submit the job and gets the job result
            location = pdf_services.submit(delete_pages_job)
            pdf_services_response = pdf_services.get_job_result(location, DeletePagesResult)

            # Get content from the resulting asset(s)
            result_asset: CloudAsset = pdf_services_response.get_result().get_asset()
            stream_asset: StreamAsset = pdf_services.get_content(result_asset)

            # Creates an output stream and copy stream asset's content to it
            output_file_path = self.create_output_file_path()
            with open(output_file_path, "wb") as file:
                file.write(stream_asset.get_input_stream())

        except (ServiceApiException, ServiceUsageException, SdkException) as e:
            logging.exception(f'Exception encountered while executing operation: {e}')

    @staticmethod
    def create_output_file_path() -> str:
        now = datetime.now()
        time_stamp = now.strftime("%Y-%m-%dT%H-%M-%S")
        os.makedirs("output/DeletePDFPages", exist_ok=True)
        return f"output/DeletePDFPages/delete{time_stamp}.pdf"

    @staticmethod
    def get_page_ranges_for_deletion() -> PageRanges:
        # Specify pages for deletion
        page_range_for_deletion = PageRanges()
        # Add page 1
        page_range_for_deletion.add_single_page(1)
        # Add pages 3 to 4
        page_range_for_deletion.add_range(3, 4)
        return page_range_for_deletion


if __name__ == "__main__":
    DeletePDFPages()
