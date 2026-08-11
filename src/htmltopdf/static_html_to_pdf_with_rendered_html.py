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
from adobe.pdfservices.operation.pdfjobs.jobs.html_to_pdf_job import HTMLtoPDFJob
from adobe.pdfservices.operation.pdfjobs.params.html_to_pdf.html_to_pdf_params import HTMLtoPDFParams
from adobe.pdfservices.operation.pdfjobs.params.html_to_pdf.page_layout import PageLayout
from adobe.pdfservices.operation.pdfjobs.result.html_to_pdf_result import HTMLtoPDFResult

# Initialize the logger
logging.basicConfig(level=logging.INFO)


#
# This sample illustrates how to convert an HTML file to PDF with the include_rendered_html option enabled.
# When include_rendered_html is set to True, the operation returns a ZIP file containing both the generated PDF
# and the rendered HTML content. The HTML file and its associated dependencies must be in a single ZIP file.
#
# Refer to README.md for instructions on how to run the samples.
#
class StaticHTMLtoPDFWithRenderedHTML:
    def __init__(self):
        try:
            file = open('src/resources/createPDFFromStaticHtmlInput.zip', 'rb')
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

            # Create parameters for the job with include_rendered_html enabled
            html_to_pdf_params = self.get_html_to_pdf_params()

            # Creates a new job instance
            html_to_pdf_job = HTMLtoPDFJob(input_asset=input_asset, html_to_pdf_params=html_to_pdf_params)

            # Submit the job and gets the job result
            location = pdf_services.submit(html_to_pdf_job)
            pdf_services_response = pdf_services.get_job_result(location, HTMLtoPDFResult)

            # Get content from the resulting asset(s)
            # When include_rendered_html is True, the result is a ZIP file containing both PDF and HTML
            result_asset: CloudAsset = pdf_services_response.get_result().get_asset()
            stream_asset: StreamAsset = pdf_services.get_content(result_asset)

            # Creates an output stream and copy stream asset's content to it
            # Note: The output file will be a ZIP file containing both the PDF and rendered HTML
            output_file_path = self.create_output_file_path()
            with open(output_file_path, "wb") as file:
                file.write(stream_asset.get_input_stream())

            logging.info(f"Output ZIP file saved to: {output_file_path}")
            logging.info("The ZIP file contains both the generated PDF and the rendered HTML content")

        except (ServiceApiException, ServiceUsageException, SdkException) as e:
            logging.exception(f'Exception encountered while executing operation: {e}')

    # Generates a string containing a directory structure and file name for the output file
    @staticmethod
    def create_output_file_path() -> str:
        now = datetime.now()
        time_stamp = now.strftime("%Y-%m-%dT%H-%M-%S")
        os.makedirs("output/StaticHTMLToPDFWithRenderedHTML", exist_ok=True)
        return f"output/StaticHTMLToPDFWithRenderedHTML/htmltopdf{time_stamp}.zip"

    @staticmethod
    def get_html_to_pdf_params() -> HTMLtoPDFParams:
        # Define the page layout, in this case an 8 x 11.5 inch page (effectively portrait orientation)
        page_layout = PageLayout(page_height=11.5, page_width=8)
        # Set include_rendered_html to True to get both PDF and rendered HTML in a ZIP file
        return HTMLtoPDFParams(
            page_layout=page_layout,
            include_header_footer=True,
            include_rendered_html=True
        )


if __name__ == "__main__":
    StaticHTMLtoPDFWithRenderedHTML()

