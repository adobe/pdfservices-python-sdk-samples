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
from adobe.pdfservices.operation.pdfjobs.jobs.export_pdf_to_images_job import ExportPDFtoImagesJob
from adobe.pdfservices.operation.pdfjobs.params.pdf_to_image.export_pdf_to_images_output_type import \
    ExportPDFToImagesOutputType
from adobe.pdfservices.operation.pdfjobs.params.pdf_to_image.export_pdf_to_images_params import \
    ExportPDFtoImagesParams
from adobe.pdfservices.operation.pdfjobs.params.pdf_to_image.export_pdf_to_images_target_format import \
    ExportPDFToImagesTargetFormat
from adobe.pdfservices.operation.pdfjobs.result.export_pdf_to_images_result import ExportPDFtoImagesResult

# Initialize the logger
logging.basicConfig(level=logging.INFO)


#
# This sample illustrates how to export a PDF file to a list of JPEG files.
#
# Refer to README.md for instructions on how to run the samples.
#
class ExportPDFtoJPEG:
    def __init__(self):
        try:
            file = open('src/resources/exportPDFToImageInput.pdf', 'rb')
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

            # Create parameters for the job
            export_pdf_to_images_params = ExportPDFtoImagesParams(
                export_pdf_to_images_target_format=ExportPDFToImagesTargetFormat.JPEG,
                export_pdf_to_images_output_type=ExportPDFToImagesOutputType.LIST_OF_PAGE_IMAGES
            )

            # Creates a new job instance
            export_pdf_to_images_job = ExportPDFtoImagesJob(
                input_asset=input_asset,
                export_pdf_to_images_params=export_pdf_to_images_params
            )

            # Submit the job and gets the job result
            location = pdf_services.submit(export_pdf_to_images_job)
            pdf_services_response = pdf_services.get_job_result(location, ExportPDFtoImagesResult)

            # Get content from the resulting asset(s)
            result_assets = pdf_services_response.get_result().get_assets()

            output_file_path = self.create_output_file_path()

            for(asset_index, asset) in enumerate(result_assets):
                save_output_file_path = f"{output_file_path}_{asset_index}.jpeg"
                stream_asset: StreamAsset = pdf_services.get_content(asset)
                # Creates an output stream and copy stream asset's content to it
                with open(save_output_file_path, "wb") as file:
                    file.write(stream_asset.get_input_stream())

        except (ServiceApiException, ServiceUsageException, SdkException) as e:
            logging.exception(f'Exception encountered while executing operation: {e}')

    # Generates a string containing a directory structure and file name for the output file
    @staticmethod
    def create_output_file_path() -> str:
        now = datetime.now()
        time_stamp = now.strftime("%Y-%m-%dT%H-%M-%S")
        os.makedirs("output/ExportPDFToImages", exist_ok=True)
        return f"output/ExportPDFToImages/export{time_stamp}"


if __name__ == "__main__":
    ExportPDFtoJPEG()
