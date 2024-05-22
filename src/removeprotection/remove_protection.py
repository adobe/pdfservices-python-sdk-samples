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
from adobe.pdfservices.operation.pdfjobs.jobs.remove_protection_job import RemoveProtectionJob
from adobe.pdfservices.operation.pdfjobs.params.remove_protection.remove_protection_params import RemoveProtectionParams
from adobe.pdfservices.operation.pdfjobs.result.remove_protection_result import RemoveProtectionResult

# Initialize the logger
logging.basicConfig(level=logging.INFO)


#
# This sample illustrates how to remove password security from a PDF document.
#
# Refer to README.md for instructions on how to run the samples.
#
class RemoveProtection:
    def __init__(self):
        try:
            file = open('src/resources/removeProtectionInput.pdf', 'rb')
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
            remove_protection_params = RemoveProtectionParams(password="password")

            # Creates a new job instance
            remove_protection_job = RemoveProtectionJob(input_asset=input_asset,
                                                        remove_protection_params=remove_protection_params)

            # Submit the job and gets the job result
            location = pdf_services.submit(remove_protection_job)
            pdf_services_response = pdf_services.get_job_result(location, RemoveProtectionResult)

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
        os.makedirs("output/RemoveProtection", exist_ok=True)
        return f"output/RemoveProtection/removeProtection{time_stamp}.pdf"


if __name__ == "__main__":
    RemoveProtection()
