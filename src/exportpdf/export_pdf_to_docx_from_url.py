"""
 Copyright 2024 Adobe
 All Rights Reserved.

 NOTICE: Adobe permits you to use, modify, and distribute this file in
 accordance with the terms of the Adobe license agreement accompanying it.

 CONTRIBUTED BY : MOHAMMAD PRINCE (https://github.com/mprince2k18)
"""

import logging
import os
import sys
from datetime import datetime
import requests
from adobe.pdfservices.operation.auth.service_principal_credentials import ServicePrincipalCredentials
from adobe.pdfservices.operation.exception.exceptions import ServiceApiException, ServiceUsageException, SdkException
from adobe.pdfservices.operation.io.cloud_asset import CloudAsset
from adobe.pdfservices.operation.io.stream_asset import StreamAsset
from adobe.pdfservices.operation.pdf_services import PDFServices
from adobe.pdfservices.operation.pdf_services_media_type import PDFServicesMediaType
from adobe.pdfservices.operation.pdfjobs.jobs.export_pdf_job import ExportPDFJob
from adobe.pdfservices.operation.pdfjobs.params.export_pdf.export_pdf_params import ExportPDFParams
from adobe.pdfservices.operation.pdfjobs.params.export_pdf.export_pdf_target_format import ExportPDFTargetFormat
from adobe.pdfservices.operation.pdfjobs.result.export_pdf_result import ExportPDFResult
from dotenv import load_dotenv

# Initialize the logger
logging.basicConfig(level=logging.INFO)


class ExportPDFToDOCX:
    def __init__(self):
        # Load environment variables
        load_dotenv()

        self.client_id = os.getenv('PDF_SERVICES_CLIENT_ID')
        self.client_secret = os.getenv('PDF_SERVICES_CLIENT_SECRET')

    def export_pdf_from_url_to_docx(self, pdf_url: str):
        try:
            logging.info("Starting the PDF to DOCX export process from URL.")

            # Fetch the PDF from the URL
            response = requests.get(pdf_url)
            response.raise_for_status()  # Raise an exception if the request failed
            input_stream = response.content
            logging.info("PDF downloaded successfully from URL.")

            # Create credentials instance
            credentials = ServicePrincipalCredentials(
                client_id=self.client_id,
                client_secret=self.client_secret
            )
            logging.info("Credentials created successfully.")

            # Create a PDF Services instance
            pdf_services = PDFServices(credentials=credentials)
            logging.info("PDFServices instance created.")

            # Upload the input file
            input_asset = pdf_services.upload(input_stream=input_stream, mime_type=PDFServicesMediaType.PDF)
            logging.info("Input file uploaded successfully.")

            # Create parameters for the job
            export_pdf_params = ExportPDFParams(target_format=ExportPDFTargetFormat.DOCX)

            # Create and submit export job
            export_pdf_job = ExportPDFJob(input_asset=input_asset, export_pdf_params=export_pdf_params)
            location = pdf_services.submit(export_pdf_job)
            logging.info("Export job submitted successfully.")

            # Get job result
            pdf_services_response = pdf_services.get_job_result(location, ExportPDFResult)
            result_asset: CloudAsset = pdf_services_response.get_result().get_asset()
            stream_asset: StreamAsset = pdf_services.get_content(result_asset)
            logging.info("Job completed successfully. Retrieving content.")

            # Save the output to file
            output_file_path = self.create_output_file_path()
            with open(output_file_path, "wb") as file:
                file.write(stream_asset.get_input_stream())
            logging.info(f"Successfully exported PDF to DOCX: {output_file_path}")

        except (requests.RequestException, ServiceApiException, ServiceUsageException, SdkException) as e:
            logging.exception(f"Exception encountered while executing operation: {e}")

    @staticmethod
    def create_output_file_path() -> str:
        now = datetime.now()
        time_stamp = now.strftime("%Y-%m-%dT%H-%M-%S")
        os.makedirs("output/ExportPDFToDOCX", exist_ok=True)
        return f"output/ExportPDFToDOCX/export_{time_stamp}.docx"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        logging.error("Usage: python export_pdf_to_docx.py <PDF_URL>")
        sys.exit(1)

    # Get the PDF URL from the command line arguments
    pdf_url = sys.argv[1]

    # Initialize the ExportPDFToDOCX instance and run the export method for URL
    exporter = ExportPDFToDOCX()
    exporter.export_pdf_from_url_to_docx(pdf_url)
