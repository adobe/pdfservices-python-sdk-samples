"""
 Copyright 2024 Adobe
 All Rights Reserved.

 NOTICE: Adobe permits you to use, modify, and distribute this file in
 accordance with the terms of the Adobe license agreement accompanying it.
"""

import json
import logging
import os
from datetime import datetime

from adobe.pdfservices.operation.auth.service_principal_credentials import ServicePrincipalCredentials
from adobe.pdfservices.operation.exception.exceptions import ServiceApiException, ServiceUsageException, SdkException
from adobe.pdfservices.operation.io.cloud_asset import CloudAsset
from adobe.pdfservices.operation.io.stream_asset import StreamAsset
from adobe.pdfservices.operation.pdf_services import PDFServices
from adobe.pdfservices.operation.pdf_services_media_type import PDFServicesMediaType
from adobe.pdfservices.operation.pdfjobs.jobs.html_to_pdf_job import HTMLtoPDFJob
from adobe.pdfservices.operation.pdfjobs.params.html_to_pdf.html_to_pdf_params import HTMLtoPDFParams
from adobe.pdfservices.operation.pdfjobs.params.html_to_pdf.page_layout import PageLayout
from adobe.pdfservices.operation.pdfjobs.result.html_to_pdf_result import HTMLtoPDFResult

# Initialize the logger
logging.basicConfig(level=logging.INFO)


#
# This sample illustrates how to provide data inputs to an HTML file before converting it to PDF. The data input is
# used by the javascript in the HTML file to manipulate the HTML DOM, thus effectively updating the source HTML file.
# This mechanism can be used to provide data to the template HTML dynamically and convert it into a PDF file.
#
# Refer to README.md for instructions on how to run the samples.
#
class DynamicHTMLToPDF:
    def __init__(self):
        try:
            file = open('src/resources/createPDFFromDynamicHtmlInput.zip', 'rb')
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
            input_asset = pdf_services.upload(input_stream=input_stream, mime_type=PDFServicesMediaType.ZIP)

            # Create parameters for the job
            html_to_pdf_params = self.get_html_to_pdf_params()

            # Creates a new job instance
            html_to_pdf_job = HTMLtoPDFJob(input_asset=input_asset, html_to_pdf_params=html_to_pdf_params)

            # Submit the job and gets the job result
            location = pdf_services.submit(html_to_pdf_job)
            pdf_services_response = pdf_services.get_job_result(location, HTMLtoPDFResult)

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
        os.makedirs("output/DynamicHTMLToPDF", exist_ok=True)
        return f"output/DynamicHTMLToPDF/htmltopdf{time_stamp}.pdf"

    @staticmethod
    def get_html_to_pdf_params() -> HTMLtoPDFParams:
        # Define the page layout, in this case an 8 x 11.5 inch page (effectively portrait orientation)
        page_layout = PageLayout(page_height=11.5, page_width=8)
        # Sets the dataToMerge field that needs to be populated in the HTML before its conversion
        data_to_merge = {
            "title": "Create, Convert PDFs and More!",
            "sub_title": "Easily integrate PDF actions within your document workflows."
        }
        return HTMLtoPDFParams(page_layout=page_layout, json=json.dumps(data_to_merge))


if __name__ == "__main__":
    DynamicHTMLToPDF()
