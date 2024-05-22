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
from adobe.pdfservices.operation.pdfjobs.jobs.rotate_pages_job import RotatePagesJob
from adobe.pdfservices.operation.pdfjobs.params.page_ranges import PageRanges
from adobe.pdfservices.operation.pdfjobs.params.rotate_pages.angle import Angle
from adobe.pdfservices.operation.pdfjobs.params.rotate_pages.rotate_pages_params import RotatePagesParams
from adobe.pdfservices.operation.pdfjobs.result.rotate_pages_result import RotatePagesResult

# Initialize the logger
logging.basicConfig(level=logging.INFO)


#
# This sample illustrates how to rotate pages in a PDF file.
#
# Refer to README.md for instructions on how to run the samples.
#
class RotatePDFPages:
    def __init__(self):
        try:
            file = open('src/resources/rotatePagesInput.pdf', 'rb')
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

            # First set of page ranges for rotating the specified pages of the input PDF file.
            first_page_range: PageRanges = self.get_first_page_range_for_rotation()

            # Second set of page ranges for rotating the specified pages of the input PDF file.
            second_page_range: PageRanges = self.get_second_page_range_for_rotation()

            # Create parameters for the job
            rotate_pages_params = RotatePagesParams()
            rotate_pages_params.add_angle_to_rotate_for_page_ranges(angle=Angle.ANGLE_90, page_ranges=first_page_range)
            rotate_pages_params.add_angle_to_rotate_for_page_ranges(angle=Angle.ANGLE_180, page_ranges=second_page_range)

            # Creates a new job instance
            reorder_pages_job = RotatePagesJob(input_asset=input_asset, rotate_pages_params=rotate_pages_params)

            # Submit the job and gets the job result
            location = pdf_services.submit(reorder_pages_job)
            pdf_services_response = pdf_services.get_job_result(location, RotatePagesResult)

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
        os.makedirs("output/RotatePDF", exist_ok=True)
        return f"output/RotatePDF/rotate{time_stamp}.pdf"

    @staticmethod
    def get_first_page_range_for_rotation() -> PageRanges:
        # Specify pages for rotation
        first_page_range = PageRanges()
        # Add page 1
        first_page_range.add_single_page(1)
        # Add pages 3 to 4
        first_page_range.add_range(3, 4)
        return first_page_range

    @staticmethod
    def get_second_page_range_for_rotation() -> PageRanges:
        # Specify pages for rotation
        second_page_range = PageRanges()
        # Add page 2
        second_page_range.add_single_page(2)
        return second_page_range


if __name__ == "__main__":
    RotatePDFPages()
