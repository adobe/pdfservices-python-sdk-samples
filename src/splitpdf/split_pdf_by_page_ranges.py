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
from adobe.pdfservices.operation.io.stream_asset import StreamAsset
from adobe.pdfservices.operation.pdf_services import PDFServices
from adobe.pdfservices.operation.pdf_services_media_type import PDFServicesMediaType
from adobe.pdfservices.operation.pdfjobs.jobs.split_pdf_job import SplitPDFJob
from adobe.pdfservices.operation.pdfjobs.params.page_ranges import PageRanges
from adobe.pdfservices.operation.pdfjobs.params.split_pdf.split_pdf_params import SplitPDFParams
from adobe.pdfservices.operation.pdfjobs.result.split_pdf_result import SplitPDFResult

# Initialize the logger
logging.basicConfig(level=logging.INFO)


#
# This sample illustrates how to create a PDF file from a DOCX file.
#
# Refer to README.md for instructions on how to run the samples.
#
class SplitPDFByPageRanges:
    def __init__(self):
        try:
            file = open('src/resources/splitPDFInput.pdf', 'rb')
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

            page_ranges = self.get_page_ranges()

            # Create parameters for the job
            split_pdf_params = SplitPDFParams(page_ranges=page_ranges)

            # Creates a new job instance
            split_pdf_job = SplitPDFJob(input_asset, split_pdf_params)

            # Submit the job and gets the job result
            location = pdf_services.submit(split_pdf_job)
            pdf_services_response = pdf_services.get_job_result(location, SplitPDFResult)

            # Get content from the resulting asset(s)
            result_assets = pdf_services_response.get_result().get_assets()

            # Creates an output stream and copy stream asset's content to it
            output_file_path = self.create_output_file_path()

            for i, result_asset in enumerate(result_assets):
                stream_asset: StreamAsset = pdf_services.get_content(result_asset)
                with open(f"{output_file_path}_{i}.pdf", "wb") as file:
                    file.write(stream_asset.get_input_stream())

        except (ServiceApiException, ServiceUsageException, SdkException) as e:
            logging.exception(f'Exception encountered while executing operation: {e}')

    @staticmethod
    def create_output_file_path() -> str:
        now = datetime.now()
        time_stamp = now.strftime("%Y-%m-%dT%H-%M-%S")
        os.makedirs("output/SplitPDFByPageRanges", exist_ok=True)
        return f"output/SplitPDFByPageranges/split{time_stamp}.pdf"

    @staticmethod
    def get_page_ranges() -> PageRanges:
        # Specify page ranges
        page_ranges = PageRanges()
        # Add page 1
        page_ranges.add_single_page(1)
        # Add pages 3 to 4
        page_ranges.add_range(3, 4)
        return page_ranges


if __name__ == "__main__":
    SplitPDFByPageRanges()
