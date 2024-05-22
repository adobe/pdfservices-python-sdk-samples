"""
 Copyright 2024 Adobe
 All Rights Reserved.

 NOTICE: Adobe permits you to use, modify, and distribute this file in
 accordance with the terms of the Adobe license agreement accompanying it.
"""

import argparse
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

from adobe.pdfservices.operation.auth.service_principal_credentials import ServicePrincipalCredentials
from adobe.pdfservices.operation.exception.exceptions import ServiceApiException, ServiceUsageException, SdkException
from adobe.pdfservices.operation.io.cloud_asset import CloudAsset
from adobe.pdfservices.operation.io.stream_asset import StreamAsset
from adobe.pdfservices.operation.pdf_services import PDFServices
from adobe.pdfservices.operation.pdf_services_media_type import PDFServicesMediaType
from adobe.pdfservices.operation.pdfjobs.jobs.autotag_pdf_job import AutotagPDFJob
from adobe.pdfservices.operation.pdfjobs.params.autotag_pdf.autotag_pdf_params import AutotagPDFParams
from adobe.pdfservices.operation.pdfjobs.result.autotag_pdf_result import AutotagPDFResult

# Initialize the logger
logging.basicConfig(level=logging.INFO)


#
# This sample illustrates how to generate a tagged PDF by setting options with command line arguments.
#
# Refer to README.md for instructions on how to run the samples.
#
class AutotagPDFParameterised:
    _input_path: str
    _output_path: str
    _generate_report: bool
    _shift_headings: bool

    def __init__(self):
        pass

    def execute(self, *args: str) -> None:
        args = self.parse_args(*args)
        self._input_path = args.input if args.input else self.get_default_input_file_path()
        self._output_path = args.output if args.output else self.get_default_output_file_path()
        self._generate_report = args.report
        self._shift_headings = args.shift_headings

        self.autotag_pdf()

    def autotag_pdf(self):
        try:
            file = open(self._input_path, 'rb')
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
                                              mime_type=PDFServicesMediaType.PDF)

            # Create parameters for the job
            autotag_pdf_params = self.get_autotag_pdf_options()

            # Creates a new job instance
            autotag_pdf_job = AutotagPDFJob(input_asset=input_asset,
                                            autotag_pdf_params=autotag_pdf_params)

            # Submit the job and gets the job result
            location = pdf_services.submit(autotag_pdf_job)
            pdf_services_response = pdf_services.get_job_result(location, AutotagPDFResult)

            # Get content from the resulting asset(s)
            result_asset: CloudAsset = pdf_services_response.get_result().get_tagged_pdf()
            stream_asset: StreamAsset = pdf_services.get_content(result_asset)

            # Create output directory if not present
            self.create_output_file_path(self._output_path)

            # Creates an output stream and copy stream asset's content to it
            with open(f'{self._output_path}/autotagPDFInput-tagged.pdf', "wb") as file:
                file.write(stream_asset.get_input_stream())

            if self._generate_report:
                result_asset_report: CloudAsset = pdf_services_response.get_result().get_report()
                stream_asset_report: StreamAsset = pdf_services.get_content(result_asset_report)
                with open(f'{self._output_path}/autotagPDFInput-report.xlsx', "wb") as file:
                    file.write(stream_asset_report.get_input_stream())

        except (ServiceApiException, ServiceUsageException, SdkException) as e:
            logging.exception(f'Exception encountered while executing operation: {e}')

    @staticmethod
    def parse_args(*args: str):
        if not args:
            args = sys.argv[1:]
        parser = argparse.ArgumentParser(description='Autotag PDF')

        parser.add_argument('--input', help='Input file path', type=Path, metavar='input')
        parser.add_argument('--output', help='Output path', type=Path, dest='output')
        parser.add_argument('--report', dest='report', action='store_true', help='Generate report(in XLSX format)',
                            default=False)
        parser.add_argument('--shift_headings', dest='shift_headings', action='store_true', help='Shift headings',
                            default=False)

        return parser.parse_args(args)

    @staticmethod
    def get_default_input_file_path() -> str:
        return 'src/resources/autotagPdfInput.pdf'

    @staticmethod
    def get_default_output_file_path() -> str:
        now = datetime.now()
        time_stamp = now.strftime("%Y-%m-%dT%H-%M-%S")
        os.makedirs("output/AutotagPDFParameterised", exist_ok=True)
        return f"output/AutotagPDFParameterised/autotag-tagged{time_stamp}"

    @staticmethod
    def create_output_file_path(path) -> None:
        os.makedirs(path, exist_ok=True)

    def get_autotag_pdf_options(self) -> AutotagPDFParams:
        return AutotagPDFParams(
            shift_headings=self._shift_headings,
            generate_report=self._generate_report
        )


if __name__ == "__main__":
    autotag_pdf_parameterised = AutotagPDFParameterised()
    autotag_pdf_parameterised.execute()
