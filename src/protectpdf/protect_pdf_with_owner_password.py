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
from adobe.pdfservices.operation.pdfjobs.jobs.protect_pdf_job import ProtectPDFJob
from adobe.pdfservices.operation.pdfjobs.params.protect_pdf.content_encryption import ContentEncryption
from adobe.pdfservices.operation.pdfjobs.params.protect_pdf.encryption_algorithm import EncryptionAlgorithm
from adobe.pdfservices.operation.pdfjobs.params.protect_pdf.password_protect_params import PasswordProtectParams
from adobe.pdfservices.operation.pdfjobs.params.protect_pdf.permission import Permission
from adobe.pdfservices.operation.pdfjobs.params.protect_pdf.permissions import Permissions
from adobe.pdfservices.operation.pdfjobs.result.protect_pdf_result import ProtectPDFResult

# Initialize the logger
logging.basicConfig(level=logging.INFO)


#
# This sample illustrates how to secure a PDF file with owner password and allow certain access permissions
# such as copying and editing the contents, and printing of the document at low resolution.
#
# Refer to README.md for instructions on how to run the samples.
#
class ProtectPDFWithOwnerPassword:
    def __init__(self):
        try:
            file = open('src/resources/protectPDFInput.pdf', 'rb')
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

            # Create new permissions instance and add the required permissions
            permissions = Permissions()
            permissions.add_permission(Permission.PRINT_LOW_QUALITY)
            permissions.add_permission(Permission.EDIT_DOCUMENT_ASSEMBLY)
            permissions.add_permission(Permission.COPY_CONTENT)

            # Create parameters for the job
            protect_pdf_params = PasswordProtectParams(
                owner_password='password',
                encryption_algorithm=EncryptionAlgorithm.AES_256,
                permissions=permissions,
                content_encryption=ContentEncryption.ALL_CONTENT_EXCEPT_METADATA,
            )

            # Creates a new job instance
            protect_pdf_job = ProtectPDFJob(input_asset=input_asset, protect_pdf_params=protect_pdf_params)

            # Submit the job and gets the job result
            location = pdf_services.submit(protect_pdf_job)
            pdf_services_response = pdf_services.get_job_result(location, ProtectPDFResult)

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
        os.makedirs("output/ProtectPDFWithOwnerPassword", exist_ok=True)
        return f"output/ProtectPDFWithOwnerPassword/protect{time_stamp}.pdf"


if __name__ == "__main__":
    ProtectPDFWithOwnerPassword()
