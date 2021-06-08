# Samples for the Adobe PDFServices Python SDK

This sample project helps you get started with the Adobe PDFServices Python SDK which currently has only Extract PDF Operation.

The sample classes illustrate how to perform PDF-related extraction (extracting content of PDF in user friendly 
structured format) using the SDK.

## Prerequisites
The sample application has the following requirements:
* Python : Version 3.6 or above. Python installation instructions can be found [here](https://www.python.org/). 

## Authentication Setup

The api credentials file and corresponding private key file for the samples is ```pdfservices-api-credentials.json``` and ```private.key``` 
respectively. Before the samples can be run, replace both the files with the ones present in the downloaded zip file at 
the end of creation of credentials via [Get Started](https://www.adobe.io/apis/documentcloud/dcsdk/gettingstarted.html?ref=getStartedWithServicesSdk) workflow.

The SDK also supports providing the authentication credentials at runtime, without storing them in a config file. Please
refer this [section](#extract-text-elements-by-providing-in-memory-authentication-credentials) to 
know more.

## Installation

Install the dependencies for the samples as listed in the ```requirements.txt``` file with this command: 

    pip install -r requirements.txt

## A Note on Logging

The SDK uses the Python standard logging module. Customize the logging settings as needed.

Default Logging Config:

    logging.getLogger(__name__).addHandler(logging.NullHandler())


## Running the samples
The following sub-sections describe how to run the samples. Prior to running the samples, check that the credentials 
file is set up as described above and that the project has been built.

The code itself is in the ```extractpdf``` folder. Test files used by the samples can be found in ```resources/```. When executed, all samples create an ```output``` 
child folder under the project root directory to store their results.

### Extract PDF

#### Structured Information Output Format
The output of SDK extract operation is Zip package. The Zip package consists of following:

* The structuredData.json file with the extracted content & PDF element structure. 
  See the [JSON schema](https://opensource.adobe.com/pdftools-sdk-docs/release/shared/extractJSONOutputSchema.json).
  Please refer the [Styling JSON schema](https://opensource.adobe.com/pdftools-sdk-docs/release/shared/extractJSONOutputSchemaStylingInfo.json) for a description of the output when the styling option is enabled. 
* A renditions folder(s) containing renditions for each element type selected as input. 
  The folder name is either “tables” or “figures” depending on your specified element type. 
  Each folder contains renditions with filenames that correspond to the element information in the JSON file. 

#### Extract Elements Information and Renditions from a PDF File
These samples illustrate how to extract PDF elements from PDF Document.

##### Extract Text Elements

The sample class ```extract_txt_from_pdf.py``` extracts text elements from PDF Document.

```$xslt
python src/extractpdf/extract_txt_from_pdf.py
```

##### Extract Text, Table Elements

The sample class ```extract_txt_table_info_from_pdf.py``` extracts text, table elements from PDF Document. 

```$xslt
python src/extractpdf/extract_txt_table_info_from_pdf.py
```
##### Extract Text, Table Elements with Renditions of Table Elements

The sample class ```extract_txt_table_info_with_rendition_from_pdf.py``` extracts text, table elements along with table renditions
from PDF Document. Note that the output is a zip containing the structured information along with renditions as described
in [section](#structured-information-output-format).

```$xslt
python src/extractpdf/extract_txt_table_info_with_rendition_from_pdf.py
```
##### Extract Text, Table Elements with Renditions of Figure, Table Elements

The sample class ```extract_txt_table_info_with_figure_tables_rendition_from_pdf.py``` extracts text, table elements along with figure 
and table element's renditions from PDF Document. Note that the output is a zip containing the structured information 
along with renditions as described in [section](#structured-information-output-format).

```$xslt
python src/extractpdf/extract_txt_table_info_with_figure_tables_rendition_from_pdf.py
```

##### Extract Text Elements (By providing in-memory Authentication credentials)

The sample class ```extract_txt_from_pdf_with_in_memory_auth_credentials.py``` extracts text elements from PDF Document. 
This sample highlights how to provide in-memory auth credentials for performing an operation. 
This enables the clients to fetch the credentials from a secret server during runtime, instead of storing them in a file.

```$xslt
python src/extractpdf/extract_txt_from_pdf_with_in_memory_auth_credentials.py
```

##### Extract Text Elements and bounding boxes for Characters present in text blocks

The sample class ```extract_txt_with_char_bounds_from_pdf.py``` extracts text elements and bounding boxes for characters present in text blocks. 
Note that the output is a zip containing the structured information 
along with renditions as described in [section](#structured-information-output-format).

```$xslt
python src/extractpdf/extract_txt_with_char_bounds_from_pdf.py
```

##### Extract Text, Table Elements and bounding boxes for Characters present in text blocks with Renditions of Table Elements

The sample class ```extract_txt_table_info_with_char_bounds_from_pdf.py``` extracts text, table elements, bounding boxes for characters present in text blocks and table element's renditions from PDF Document. 
Note that the output is a zip containing the structured information 
along with renditions as described in [section](#structured-information-output-format).

```$xslt
python src/extractpdf/extract_txt_table_info_with_char_bounds_from_pdf.py
```

##### Extract Text, Table Elements with Renditions and CSV's of Table Elements

The sample class ```extract_txt_table_info_with_table_structure_from_pdf.py``` extracts text, table elements, table structures as CSV and table element's renditions from PDF Document.  
Note that the output is a zip containing the structured information 
along with renditions as described in [section](#structured-information-output-format).

```$xslt
python src/extractpdf/extract_txt_table_info_with_table_structure_from_pdf.py
```

##### Extract Text with Styling Info

The sample class ```extract_txt_with_styling_info_from_pdf.py``` extracts text along with Styling Info.  
Note that the output is a zip containing the structured information 
along with renditions as described in [section](#structured-information-output-format).

```$xslt
python src/extractpdf/extract_txt_with_styling_info_from_pdf.py
```

### Contributing

Contributions are welcome! Read the [Contributing Guide](.github/CONTRIBUTING.md) for more information.

### Licensing

This project is licensed under the Apache2 License. See [LICENSE](LICENSE.md) for more information.