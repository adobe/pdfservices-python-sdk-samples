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
from adobe.pdfservices.operation.pdfjobs.jobs.combine_pdf_job import CombinePDFJob
from adobe.pdfservices.operation.pdfjobs.params.combine_pdf.combine_pdf_params import CombinePDFParams
from adobe.pdfservices.operation.pdfjobs.params.page_ranges import PageRanges
from adobe.pdfservices.operation.pdfjobs.result.combine_pdf_result import CombinePDFResult

# Initialize the logger
logging.basicConfig(level=logging.INFO)

#
# This sample illustrates how to combine specific pages of multiple PDF files into a single PDF file.
#
# Note that the SDK supports combining upto 20 files in one operation
#
# Refer to README.md for instructions on how to run the samples.
#
class CombinePDFWithPageRanges:
    def __init__(self):
        try:
            file = open('src/resources/combineFilesInput1.pdf', 'rb')
            input_stream_1 = file.read()
            file.close()

            file = open('src/resources/combineFilesInput2.pdf', 'rb')
            input_stream_2 = file.read()
            file.close()

            # Initial setup, create credentials instance
            credentials = ServicePrincipalCredentials(
                client_id=os.getenv('PDF_SERVICES_CLIENT_ID'),
                client_secret=os.getenv('PDF_SERVICES_CLIENT_SECRET')
            )

            # Creates a PDF Services instance
            pdf_services = PDFServices(credentials=credentials)

            # Creates an asset(s) from source file(s) and upload
            stream_assets = [StreamAsset(input_stream_1, PDFServicesMediaType.PDF),
                             StreamAsset(input_stream_2, PDFServicesMediaType.PDF)]

            assets = pdf_services.upload_assets(stream_assets)

            page_ranges_for_first_file = self.get_page_range_for_first_file()
            page_ranges_for_second_file = self.get_page_range_for_second_file()

            # Create parameters for the job
            combine_pdf_params = ((CombinePDFParams()
                                  .add_asset(assets[0],page_ranges=page_ranges_for_first_file))
                                  .add_asset(assets[1],page_ranges=page_ranges_for_second_file))

            # Creates a new job instance
            combine_pdf_job = CombinePDFJob(combine_pdf_params=combine_pdf_params)

            # Submit the job and gets the job result
            location = pdf_services.submit(combine_pdf_job)
            pdf_services_response = pdf_services.get_job_result(location, CombinePDFResult)

            # Get content from the resulting asset(s)
            result_asset: CombinePDFResult = pdf_services_response.get_result().get_asset()
            stream_asset: StreamAsset = pdf_services.get_content(result_asset)

            # Creates an output stream and copy stream asset's content to it
            output_file_path = self.create_output_file_path()
            with open(output_file_path, "wb") as file:
                file.write(stream_asset.get_input_stream())

        except (ServiceApiException, ServiceUsageException, SdkException) as e:
            logging.exception(f'Exception encountered while executing operation: {e}')

    @staticmethod
    def get_page_range_for_first_file() -> PageRanges:
        # Specify which pages of the first file are to be included in the combined file
        page_ranges_for_first_file = PageRanges()
        # Add page 1
        page_ranges_for_first_file.add_single_page(1)
        # Add page 2
        page_ranges_for_first_file.add_single_page(2)
        # Add pages 3 to 4
        page_ranges_for_first_file.add_range(3, 4)
        return page_ranges_for_first_file

    @staticmethod
    def get_page_range_for_second_file() -> PageRanges:
        # Specify which pages of the first file are to be included in the combined file
        page_ranges_for_second_file = PageRanges()
        # Add all pages including and after page 3
        page_ranges_for_second_file.add_all_from(3)
        return page_ranges_for_second_file

    # Generates a string containing a directory structure and file name for the output file
    @staticmethod
    def create_output_file_path() -> str:
        now = datetime.now()
        time_stamp = now.strftime("%Y-%m-%dT%H-%M-%S")
        os.makedirs("output/CombinePDFWithPageRanges", exist_ok=True)
        return f"output/CombinePDFWithPageRanges/combine{time_stamp}.pdf"


if __name__ == "__main__":
    CombinePDFWithPageRanges()
