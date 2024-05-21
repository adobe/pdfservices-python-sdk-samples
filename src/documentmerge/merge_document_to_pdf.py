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
from adobe.pdfservices.operation.pdfjobs.jobs.document_merge_job import DocumentMergeJob
from adobe.pdfservices.operation.pdfjobs.params.documentmerge.document_merge_params import DocumentMergeParams
from adobe.pdfservices.operation.pdfjobs.params.documentmerge.output_format import OutputFormat
from adobe.pdfservices.operation.pdfjobs.result.document_merge_result import DocumentMergePDFResult

# Initialize the logger
logging.basicConfig(level=logging.INFO)


#
# This sample illustrates how to merge the Word based document template with the input JSON data to generate
# the output document in the PDF format.
#
# To know more about document generation and document templates, please see the
# <a href="http://www.adobe.com/go/dcdocgen_overview_doc">documentation</a>
#
# Refer to README.md for instructions on how to run the samples.
#
class MergeDocumentToPDF:
    def __init__(self):
        try:
            file = open('src/resources/salesOrderTemplate.docx', 'rb')
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
                                              mime_type=PDFServicesMediaType.DOCX)

            # Setup input data for the document merge process
            with open('src/resources/salesOrder.json', 'r') as file:
                content_string = file.read()
            json_data_for_merge = json.loads(content_string)

            # Create parameters for the job
            document_merge_params = DocumentMergeParams(json_data_for_merge=json_data_for_merge,
                                                        output_format=OutputFormat.PDF)

            # Creates a new job instance
            document_merge_job = DocumentMergeJob(input_asset=input_asset,
                                                  document_merge_params=document_merge_params)

            # Submit the job and gets the job result
            location = pdf_services.submit(document_merge_job)
            pdf_services_response = pdf_services.get_job_result(location, DocumentMergePDFResult)

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
        os.makedirs("output/MergeDocumentToPDF", exist_ok=True)
        return f"output/MergeDocumentToPDF/merge{time_stamp}.pdf"


if __name__ == "__main__":
    MergeDocumentToPDF()
