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
from adobe.pdfservices.operation.pdfjobs.jobs.eseal_job import PDFElectronicSealJob
from adobe.pdfservices.operation.pdfjobs.params.eseal.appearance_item import AppearanceItem
from adobe.pdfservices.operation.pdfjobs.params.eseal.appearance_options import AppearanceOptions
from adobe.pdfservices.operation.pdfjobs.params.eseal.csc_auth_context import CSCAuthContext
from adobe.pdfservices.operation.pdfjobs.params.eseal.csc_credentials import CSCCredentials
from adobe.pdfservices.operation.pdfjobs.params.eseal.document_level_permission import DocumentLevelPermission
from adobe.pdfservices.operation.pdfjobs.params.eseal.electronic_seal_params import PDFElectronicSealParams
from adobe.pdfservices.operation.pdfjobs.params.eseal.field_location import FieldLocation
from adobe.pdfservices.operation.pdfjobs.params.eseal.field_options import FieldOptions
from adobe.pdfservices.operation.pdfjobs.result.eseal_pdf_result import ESealPDFResult

# Initialize the logger
logging.basicConfig(level=logging.INFO)


#
# This sample illustrates how to apply electronic seal over the PDF document using custom appearance options.
#
# To know more about PDF Electronic Seal, please see the
# <a href="https://www.adobe.com/go/dc_eseal_overview_doc" target="_blank">documentation</a>.
#
# Refer to README.md for instructions on how to run the samples.
#
class ElectronicSealWithAppearanceOptions:
    def __init__(self):
        try:
            pdf_file = open('src/resources/sampleInvoice.pdf', 'rb')
            file_input_stream = pdf_file.read()
            pdf_file.close()

            seal_image_file = open('src/resources/sampleSealImage.png', 'rb')
            seal_image_input_stream = seal_image_file.read()
            seal_image_file.close()

            # Initial setup, create credentials instance
            credentials = ServicePrincipalCredentials(
                client_id=os.getenv('PDF_SERVICES_CLIENT_ID'),
                client_secret=os.getenv('PDF_SERVICES_CLIENT_SECRET')
            )

            # Creates a PDF Services instance
            pdf_services = PDFServices(credentials=credentials)

            # Creates an asset(s) from source file(s) and upload
            asset = pdf_services.upload(input_stream=file_input_stream, mime_type=PDFServicesMediaType.PDF)
            seal_image_asset = pdf_services.upload(input_stream=seal_image_input_stream, mime_type=PDFServicesMediaType.PNG)

            # Create AppearanceOptions and add the required signature display items to it
            appearance_options: AppearanceOptions = AppearanceOptions()
            appearance_options.add_item(AppearanceItem.NAME)
            appearance_options.add_item(AppearanceItem.LABELS)
            appearance_options.add_item(AppearanceItem.DATE)
            appearance_options.add_item(AppearanceItem.SEAL_IMAGE)
            appearance_options.add_item(AppearanceItem.DISTINGUISHED_NAME)

            # Set the document level permission to be applied for output document
            document_level_permission = DocumentLevelPermission.FORM_FILLING

            # Sets the Seal Field Name to be created in input PDF document.
            seal_field_name = "Signature1"

            # Sets the page number in input document for applying seal.
            seal_page_number = 1

            # Sets if seal should be visible or invisible.
            seal_visible = True

            # Creates FieldLocation instance and set the coordinates for applying signature
            field_location = FieldLocation(150, 250, 350, 200)

            # Create FieldOptions instance with required details.
            field_options = FieldOptions(
                field_name=seal_field_name,
                field_location=field_location,
                page_number=seal_page_number,
                visible=seal_visible
            )

            # Sets the name of TSP Provider being used.
            provider_name = "<PROVIDER_NAME>"

            # Sets the access token to be used to access TSP provider hosted APIs.
            access_token = "<ACCESS_TOKEN>"

            # Sets the credential ID.
            credential_id = "<CREDENTIAL_ID>"

            # Sets the PIN generated while creating credentials.
            pin = "<PIN>"

            # Creates CSCAuthContext instance using access token and token type.
            csc_auth_context = CSCAuthContext(
                access_token=access_token,
                token_type="Bearer",
            )

            # Create CertificateCredentials instance with required certificate details.
            certificate_credentials = CSCCredentials(
                provider_name=provider_name,
                credential_id=credential_id,
                pin=pin,
                csc_auth_context=csc_auth_context,
            )

            # Create parameters for the job
            electronic_seal_params = PDFElectronicSealParams(
                seal_certificate_credentials=certificate_credentials,
                seal_appearance_options=appearance_options,
                seal_field_options=field_options,
                document_level_permissions=document_level_permission,
            )

            # Creates a new job instance
            electronic_seal_job = PDFElectronicSealJob(input_asset=asset,
                                                       electronic_seal_params=electronic_seal_params,
                                                       seal_image_asset=seal_image_asset)

            # Submit the job and gets the job result
            location = pdf_services.submit(electronic_seal_job)
            pdf_services_response = pdf_services.get_job_result(location, ESealPDFResult)

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
        os.makedirs("output/ElectronicSeal", exist_ok=True)
        return f"output/ElectronicSeal/sealedOutputWithAppearanceOptions{time_stamp}.pdf"


if __name__ == "__main__":
    ElectronicSealWithAppearanceOptions()
