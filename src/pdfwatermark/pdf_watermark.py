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
from adobe.pdfservices.operation.pdfjobs.jobs.pdf_watermark_job import PDFWatermarkJob
from adobe.pdfservices.operation.pdfjobs.result.pdf_watermark_result import PDFWatermarkResult

# Initialize the logger
logging.basicConfig(level=logging.INFO)

#
# This sample illustrates how to apply watermark to a PDF file.
#
# Note that PDF Watermark operation on a PDF file results in a PDF file.
# Refer to README.md for instructions on how to run the samples.
#

class PDFWatermark:
    def __init__(self):
        try:
            pdf_file = open("src/resources/PDFwatermarkInput.pdf", 'rb')
            source_file_input_stream = pdf_file.read()
            pdf_file.close()

            pdf_file = open("src/resources/watermark.pdf", 'rb')
            watermark_file_input_stream = pdf_file.read()
            pdf_file.close()

            # Initial setup, create credentials instance
            credentials = ServicePrincipalCredentials(
                client_id=os.getenv('PDF_SERVICES_CLIENT_ID'),
                client_secret=os.getenv('PDF_SERVICES_CLIENT_SECRET'))

            # Creates a PDF Services instance
            pdf_services = PDFServices(credentials=credentials)

            # Creates an asset(s) from source file(s) and upload
            input_asset = pdf_services.upload(input_stream=source_file_input_stream, mime_type=PDFServicesMediaType.PDF)
            watermark_asset = pdf_services.upload(input_stream=watermark_file_input_stream, mime_type=PDFServicesMediaType.PDF)

            # Creates a new job instance
            pdf_watermark_job = PDFWatermarkJob(input_asset=input_asset, watermark_asset=watermark_asset)

            # Submit the job and gets the job result
            location = pdf_services.submit(pdf_watermark_job)
            pdf_services_response = pdf_services.get_job_result(location, PDFWatermarkResult)

            # Get content from the resulting asset(s)
            pdf_watermark_result: CloudAsset = pdf_services_response.get_result().get_asset()
            stream_asset: StreamAsset = pdf_services.get_content(pdf_watermark_result)

            # Creates an output stream and copy stream asset's content to it
            output_file_path = self.create_output_file_path()
            with open(output_file_path, "wb") as file:
                file.write(stream_asset.get_input_stream())
        except (ServiceApiException, ServiceUsageException, SdkException) as e:
            logging.exception(f'Exception encountered while executing operation: {e}')

            # Generates a string containing a directory structure and file name for the output file

    def create_output_file_path(self) -> str:
        now = datetime.now()
        time_stamp = now.strftime("%Y-%m-%dT%H-%M-%S")
        os.makedirs("output/PDFWatermark", exist_ok=True)
        return f"output/PDFWatermark/pdfwatermark{time_stamp}.pdf"

if __name__ == "__main__":
    PDFWatermark()
