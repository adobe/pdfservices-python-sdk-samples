"""
 Copyright 2024 Adobe
 All Rights Reserved.

 NOTICE: Adobe permits you to use, modify, and distribute this file in
 accordance with the terms of the Adobe license agreement accompanying it.
"""

import logging
import os
import time

from adobe.pdfservices.operation.auth.service_principal_credentials import ServicePrincipalCredentials
from adobe.pdfservices.operation.exception.exceptions import ServiceApiException, ServiceUsageException, SdkException
from adobe.pdfservices.operation.io.external_asset import ExternalAsset
from adobe.pdfservices.operation.io.external_storage_type import ExternalStorageType
from adobe.pdfservices.operation.pdf_services import PDFServices
from adobe.pdfservices.operation.pdf_services_job_status import PDFServicesJobStatus
from adobe.pdfservices.operation.pdf_services_job_status_response import PDFServicesJobStatusResponse
from adobe.pdfservices.operation.pdfjobs.jobs.create_pdf_job import CreatePDFJob

# Initialize the logger
logging.basicConfig(level=logging.INFO)


#
# This sample illustrates how to use external storage as input and output in PDF Services.
# For this illustration a PDF file will be created and stored externally from a DOCX file stored externally.
#
# Refer to README.md for instructions on how to run the samples.
#
class ExternalInputAndOutputCreatePDFFromDOCX:
    def __init__(self):
        try:
            # Initial setup, create credentials instance
            credentials = ServicePrincipalCredentials(
                client_id=os.getenv('PDF_SERVICES_CLIENT_ID'),
                client_secret=os.getenv('PDF_SERVICES_CLIENT_SECRET')
            )

            # Creates a PDF Services instance
            pdf_services = PDFServices(credentials=credentials)

            # Creating external assets from pre signed URLs.
            input_pre_signed_url = "INPUT_PRESIGNED_URL"
            output_pre_signed_url = "OUTPUT_PRESIGNED_URL"
            input_external_asset = ExternalAsset(uri=input_pre_signed_url, external_storage_type=ExternalStorageType.S3)
            output_external_asset = ExternalAsset(uri=output_pre_signed_url, external_storage_type=ExternalStorageType.S3)

            # Creates a new job instance
            create_pdf_job = CreatePDFJob(input_asset=input_external_asset, output_asset=output_external_asset)

            # Submit the job and gets the job result
            location = pdf_services.submit(create_pdf_job)

            # Poll to check job status and wait until job is done
            pdf_services_job_status_reposnse: PDFServicesJobStatusResponse = None
            while (pdf_services_job_status_reposnse is None or
                   pdf_services_job_status_reposnse.get_status() == PDFServicesJobStatus.IN_PROGRESS):
                pdf_services_job_status_reposnse = pdf_services.get_job_status(location)
                # get retry interval from response
                retry_after = pdf_services_job_status_reposnse.get_retry_interval()
                time.sleep(retry_after)

            logging.info("Output is now available on the provided output external storage.")

        except (ServiceApiException, ServiceUsageException, SdkException) as e:
            logging.exception(f'Exception encountered while executing operation: {e}')


if __name__ == "__main__":
    ExternalInputAndOutputCreatePDFFromDOCX()
