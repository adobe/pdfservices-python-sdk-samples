# Copyright 2023 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

import logging
import os.path
import sys
import argparse
from pathlib import Path

from adobe.pdfservices.operation.auth.credentials import Credentials
from adobe.pdfservices.operation.exception.exceptions import ServiceApiException, ServiceUsageException, SdkException
from adobe.pdfservices.operation.execution_context import ExecutionContext
from adobe.pdfservices.operation.io.file_ref import FileRef

from adobe.pdfservices.operation.internal.api.dto.request.autotagpdf.autotag_pdf_output import \
    AutotagPDFOutput
from adobe.pdfservices.operation.pdfops.autotag_pdf_operation import AutotagPDFOperation
from adobe.pdfservices.operation.pdfops.options.autotagpdf.autotag_pdf_options import AutotagPDFOptions

logging.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO'))


class AutotagPDFParameterised:

    _input_path: str
    _output_path: str
    _generate_report: bool
    _shift_headings: bool

    base_path = str(Path(__file__).parents[2])

    def __init__(self):
        pass

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

    def get_default_input_file_path(self) -> str:
        return self.base_path + '/resources/autotagPdfInput.pdf'

    def get_default_output_file_path(self) -> str:
        return self.base_path + '/output/AutotagPDFParameterised'

    def get_autotag_pdf_options(self) -> AutotagPDFOptions:
        shift_headings = self._shift_headings
        generate_report = self._generate_report

        builder: AutotagPDFOptions.Builder = AutotagPDFOptions.builder()
        if shift_headings:
            builder.with_shift_headings()
        if generate_report:
            builder.with_generate_report()
        return builder.build()

    def execute(self, *args: str) -> None:
        args = self.parse_args(*args)
        self._input_path = args.input if args.input else self.get_default_input_file_path()
        self._output_path = args.output if args.output else self.get_default_output_file_path()
        self._generate_report = args.report
        self._shift_headings = args.shift_headings

        self.autotag_pdf()

    def autotag_pdf(self):
        try:
            # Initial setup, create credentials instance.
            credentials = Credentials.service_principal_credentials_builder(). \
                with_client_id(os.getenv('PDF_SERVICES_CLIENT_ID')). \
                with_client_secret(os.getenv('PDF_SERVICES_CLIENT_SECRET')). \
                build()

            # Create an ExecutionContext using credentials and create a new operation instance.
            execution_context = ExecutionContext.create(credentials)
            autotag_pdf_operation = AutotagPDFOperation.create_new()

            # Set operation input from a source file.
            source = FileRef.create_from_local_file(self._input_path)
            autotag_pdf_operation.set_input(source)

            # Build AutotagPDF options and set them into the operation
            autotag_pdf_operation.set_options(self.get_autotag_pdf_options())

            # Execute the operation.
            autotag_pdf_output: AutotagPDFOutput = autotag_pdf_operation.execute(execution_context)

            input_file_name = Path(self._input_path).stem
            base_output_path = self._output_path

            Path(base_output_path).mkdir(parents=True, exist_ok=True)

            # Save the result to the specified location.
            tagged_pdf_path = f'{base_output_path}/{input_file_name}-tagged.pdf'
            autotag_pdf_output.get_tagged_pdf().save_as(tagged_pdf_path)
            if self._generate_report:
                report_path = f'{base_output_path}/{input_file_name}-report.xlsx'
                autotag_pdf_output.get_report().save_as(report_path)

        except (ServiceApiException, ServiceUsageException, SdkException) as e:
            logging.exception(f'Exception encountered while executing operation: {e}')


if __name__ == "__main__":
    autotag_pdf_parameterised = AutotagPDFParameterised()
    autotag_pdf_parameterised.execute()
