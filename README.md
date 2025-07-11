# Samples for the Adobe PDF Services Python SDK

This sample project helps you get started with the Adobe PDF Services Python SDK.

The sample classes illustrate how to perform PDF-related actions (such as converting to and from the PDF format) using
the SDK. **Please note that the Adobe PDF Services Python SDK supports only server side use cases.**

## Prerequisites
The sample application has the following requirements:
* Python : Version 3.10 or above. Python installation instructions can be found [here](https://www.python.org/). 

## Authentication Setup

The credentials file for the samples is ```pdfservices-api-credentials.json```.
Before the samples can be run, set the environment variables `PDF_SERVICES_CLIENT_ID` and `PDF_SERVICES_CLIENT_SECRET` from the `pdfservices-api-credentials.json` file downloaded at the end of creation of credentials via [Get Started](https://www.adobe.io/apis/documentcloud/dcsdk/gettingstarted.html?ref=getStartedWithServicesSdk) workflow by running the following commands:

 1. For MacOS/Linux Users :
 ```$xlst
 export PDF_SERVICES_CLIENT_ID=<YOUR CLIENT ID>
 export PDF_SERVICES_CLIENT_SECRET=<YOUR CLIENT SECRET>
 ```

 2. For Windows Users :
 ```$xlst
 SET PDF_SERVICES_CLIENT_ID=<YOUR CLIENT ID>
 SET PDF_SERVICES_CLIENT_SECRET=<YOUR CLIENT SECRET>
 ```

## Client Configurations

The SDK supports setting up custom socket timeout or connect timeout for the API calls. Please refer this [section](#create-a-pdf-file-from-a-docx-file-by-providing-custom-value-for-timeouts) to know more.

Additionally, SDK can be configured to process the documents in the specified region. Please refer this [section](#export-a-pdf-file-to-a-docx-file-by-providing-the-region) section to know more.

## Quota Exhaustion

If you receive ServiceUsageError during the Samples run, it means that trial credentials have exhausted their usage quota.
Please [contact us](https://www.adobe.com/go/pdftoolsapi_requestform) to get paid credentials.

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

The code itself is in the ```src``` folder. Test files used by the samples can be found in ```resources/```. When executed, all samples create an ```output``` 
child folder under the project root directory to store their results.

### Create a PDF File
These samples illustrate how to convert files of supported formats to PDF.
Refer the [Create PDF API documentation](https://developer.adobe.com/document-services/docs/apis/#tag/Create-PDF/operation/pdfoperations.createpdf) to see the list of all supported media types which can be converted to PDF.

####  Create a PDF File From a DOCX File 

The sample class ```create_pdf_from_docx.py``` creates a PDF file from a DOCX file.

```$xslt
python src/createpdf/create_pdf_from_docx.py
```

####  Create a PDF File From a DOCX File with options 

The sample class ```create_pdf_from_docx_with_options.py``` creates a PDF file from a DOCX file by setting documentLanguage as
the language of input file.

```$xslt
python src/createpdf/create_pdf_from_docx_with_options.py
```

####  Create a PDF File From a PPTX File 

The sample class ```create_pdf_from_pptx.py``` creates a PDF file from a PPTX file.

```$xslt
python src/createpdf/create_pdf_from_pptx.py
```

### Create a PDF File From HTML
These samples illustrate how to convert HTML to PDF. 
Refer the [HTML to PDF API documentation](https://developer.adobe.com/document-services/docs/apis/#tag/Html-to-PDF/operation/pdfoperations.htmltopdf) to see instructions on the structure of the zip file.

#### Create a PDF File From a Static HTML file with inline CSS

The sample class ```html_with_inline_css_to_pdf.py``` creates a PDF file from an input HTML file with inline CSS.

```$xslt
python src/htmltopdf/html_with_inline_css_to_pdf.py
```

#### Create a PDF File From HTML specified via URL

The sample class ```html_to_pdf_from_url.py``` creates a PDF file from an HTML specified via URL.

```$xslt
python src/htmltopdf/html_to_pdf_from_url.py
```

#### Create a PDF File From Static HTML (via Zip Archive)

The sample class ```static_html_to_pdf.py``` creates a PDF file from a zip file containing the input HTML file and its resources.

```$xslt
python src/htmltopdf/static_html_to_pdf.py
```

#### Create a PDF File From Dynamic HTML (via Zip Archive)

The sample class ```dynamic_html_to_pdf.py``` converts a zip file, containing the input HTML file and its resources, along
with the input data to a PDF file. The input data is used by the javascript in the HTML file to manipulate the HTML DOM,
thus effectively updating the source HTML file. This mechanism can be used to provide data to the template HTML
dynamically and then, convert it into a PDF file.

```$xslt
python src/htmltopdf/dynamic_html_to_pdf.py
```

### Export PDF To Other Formats
These samples illustrate how to export PDF files to other formats. Refer [Export PDF API documentation](https://developer.adobe.com/document-services/docs/apis/#tag/Export-PDF/operation/pdfoperations.exportpdf) 
and [Export PDF To Images API documentation](https://developer.adobe.com/document-services/docs/apis/#tag/PDF-To-Images) for supported export formats.

#### Export a PDF File To a DOCX File 

The sample class ```export_pdf_to_docx.py``` converts a PDF file to a DOCX file.

```$xslt
python src/exportpdf/export_pdf_to_docx.py
```

#### Export a PDF file to a DOCX file (apply OCR on the PDF file)

The sample class ```export_pdf_to_docx_with_ocr_option.py``` converts a PDF file to a DOCX file. OCR processing is also performed on the input PDF file to extract text from images in the document.

```$xslt
python src/exportpdf/export_pdf_to_docx_with_ocr_option.py
```

#### Export a PDF File To an Image Format (JPEG)

The sample class ```export_pdf_to_jpeg.py``` converts a PDF file's pages to a list of JPEG images.

```$xslt
python src/exportpdftoimages/export_pdf_to_jpeg.py
```

#### Export a PDF File To a Zip of Images (JPEG)

The sample class ```export_pdf_to_jpeg_zip.py``` converts a PDF file's pages to JPEG images. The resulting file is a ZIP archive containing one image per page of the source PDF file

```$xslt
python src/exportpdftoimages/export_pdf_to_jpeg_zip.py
```

#### Import Form Data Into a PDF File

The sample class ```import_pdf_form_data.py``` imports form data into a PDF file that contains form fields.

```$xslt
python src/importpdfformdata/import_pdf_form_data.py
```

#### Export Form Data From a PDF File

The sample class ```export_pdf_form_data.py``` extracts form data from a PDF file that contains filled form fields and returns the data in JSON format.

```$xslt
python src/exportpdfformdata/export_pdf_form_data.py
```

### Combine PDF Files
These samples illustrate how to combine multiple PDF files into a single PDF file.

#### Combine Multiple PDF Files

The sample class ```combine_pdf.py``` combines multiple PDF files into a single PDF file. The combined PDF file contains all pages
of the source files.

```$xslt
python src/combinepdf/combine_pdf.py
```

#### Combine Specific Pages of Multiple PDF Files

The sample class ```combine_pdf_with_page_ranges.py``` combines specific pages of multiple PDF files into a single PDF file.
 
```$xslt
python src/combinepdf/combine_pdf_with_page_ranges.py
```

### OCR PDF File

These samples illustrate how to apply OCR(Optical Character Recognition) to a PDF file and convert it to a searchable copy of your PDF. 
The supported input format is application/pdf.

#### Convert a PDF File into a Searchable PDF File

The sample class ```ocr_pdf.py``` converts a PDF file into a searchable PDF file.

```$xslt
python src/ocrpdf/ocr_pdf.py
```

#### Convert a PDF File into a Searchable PDF File while keeping the original image

The sample class ```ocr_pdf_with_options.py``` converts a PDF file to a searchable PDF file with maximum fidelity to the original 
image and default en-us locale. Refer to the documentation of OCRSupportedLocale and OCRSupportedType to see 
the list of supported OCR locales and OCR types.

```$xslt
python src/ocrpdf/ocr_pdf_with_options.py
```

### Compress PDF File

These samples illustrate how to reduce the size of a PDF file.

#### Reduce PDF File Size

The sample class ```compress_pdf.py``` reduces the size of a PDF file.

```$xslt
python src/compresspdf/compress_pdf.py
```

####  Reduce PDF File Size on the basis of Compression Level 

The sample class ```compress_pdf_with_options.py``` reduces the size of a PDF file on the basis of provided compression level.
Refer to the documentation of CompressionLevel to see the list of supported compression levels.

```$xslt
python src/compresspdf/compress_pdf_with_options.py
```

### Linearize PDF File

The sample illustrates how to convert a PDF file into a Linearized (also known as "web optimized") PDF file. Such PDF files are 
optimized for incremental access in network environments.

#### Convert a PDF File into a Web Optimized File

The sample class ```linearize_pdf.py``` optimizes the PDF file for a faster Web View.

```$xslt
python src/linearizepdf/linearize_pdf.py
```

### Protect PDF File

These samples illustrate how to secure a PDF file with a password.

#### Convert a PDF File into a Password Protected PDF File

The sample class ```protect_pdf.py``` converts a PDF file into a password protected PDF file.

```$xslt
python src/protectpdf/protect_pdf.py
```

#### Protect a PDF File with an Owner Password and Permissions

The sample class ```protect_pdf_with_owner_password.py``` secures an input PDF file with owner password and allows certain access permissions 
such as copying and editing the contents, and printing of the document at low resolution.

```$xslt
python src/protectpdf/protect_pdf_with_owner_password.py
```

### Remove Protection

The sample illustrates how to remove a password security from a PDF document.

#### Remove Protection from a PDF File

The sample class ```remove_protection.py``` removes a password security from a secured PDF document.

```$xslt
python src/removeprotection/remove_protection.py
```

### Rotate Pages

The sample illustrates how to rotate pages in a PDF file.

#### Rotate Pages in PDF File

The sample class ```rotate_pdf_pages.py``` rotates specific pages in a PDF file.  

```$xslt
python src/rotatepages/rotate_pdf_pages.py
```

### Delete Pages

The sample illustrates how to delete pages in a PDF file.

#### Delete Pages from PDF File

The sample class ```delete_pdf_pages.py``` removes specific pages from a PDF file.

```$xslt
python src/deletepages/delete_pdf_pages.py
```

### Reorder Pages

The sample illustrates how to reorder the pages in a PDF file.

#### Reorder Pages in PDF File

The sample class ```reorder_pdf_pages.py``` rearranges the pages of a PDF file according to the specified order.

```$xslt
python src/reorderpages/reorder_pdf_pages.py
```

### Insert Pages

The sample illustrates how to insert pages in a PDF file.

#### Insert Pages into a PDF File

The sample class ```insert_pdf_pages.py``` inserts pages of multiple PDF files into a base PDF file.

```$xslt
python src/insertpages/insert_pdf_pages.py
```

### Replace Pages

The sample illustrates how to replace pages of a PDF file.

#### Replace PDF File Pages with Multiple PDF Files

The sample class ```replace_pdf_pages.py``` replaces specific pages in a PDF file with pages from multiple PDF files.

```$xslt
python src/replacepages/replace_pdf_pages.py
```

### Split PDF File
These samples illustrate how to split PDF file into multiple PDF files.

#### Split PDF By Number of Pages

The sample class ```split_pdf_by_number_of_pages.py``` splits input PDF into multiple PDF files on the basis of the maximum number
of pages each of the output files can have.

```$xslt
python src/splitpdf/split_pdf_by_number_of_pages.py
```

#### Split PDF Into Number of PDF Files

The sample class ```split_pdf_into_number_of_files.py``` splits input PDF into multiple PDF files on the basis of the number
of documents.
 
```$xslt
python src/splitpdf/split_pdf_into_number_of_files.py
```

#### Split PDF By Page Ranges

The sample class ```split_pdf_by_page_ranges.py``` splits input PDF into multiple PDF files on the basis of page ranges.
Each page range corresponds to a single output file having the pages specified in the page range.

```$xslt
python src/splitpdf/split_pdf_by_page_ranges.py
```

### Document Merge

Adobe Document Merge Operation allows you to produce high fidelity PDF and Word documents with dynamic data inputs.
Using this operation, you can merge your JSON data with Word templates to create dynamic documents for 
contracts and agreements, invoices, proposals, reports, forms, branded marketing documents and more.
To know more about document generation and document templates, please checkout the [documentation](http://www.adobe.com/go/dcdocgen_overview_doc)

#### Merge Document to DOCX

The sample class ```merge_document_to_docx.py``` merges the Word based document template with the input JSON data to generate 
the output document in the DOCX format.

```$xslt
python src/documentmerge/merge_document_to_docx.py
```

#### Merge Document to DOCX with Fragments

The sample class ```merge_document_to_docx_with_fragments.py``` merges the Word based document template with the input JSON data and fragments JSON to generate 
the output document in the DOCX format.

```$xslt
python src/documentmerge/merge_document_to_docx_with_fragments.py
```

#### Merge Document to PDF

The sample class ```merge_document_to_pdf.py``` merges the Word based document template with the input JSON data to generate
the output document in the PDF format.

```$xslt
python src/documentmerge/merge_document_to_pdf.py
```

### PDF Electronic Seal

These samples illustrate how to perform electronic seal over PDF documents like
agreements, invoices, proposals, reports, forms, branded marketing documents and more.
To know more about PDF Electronic Seal, please see the [documentation](https://www.adobe.com/go/dc_eseal_overview_doc).
The following details needs to updated while executing these samples: PROVIDER_NAME, ACCESS_TOKEN, CREDENTIAL_ID and PIN.

#### Apply Electronic Seal

The sample class ```electronic_seal.py``` uses the sealing options with default appearance options to apply electronic seal over the PDF document.

```$xslt
python src/electronicseal/electronic_seal.py
```

#### Apply Electronic Seal With Custom Appearance Options

The sample class ```electronic_seal_with_appearance_options.py``` uses the sealing options with custom appearance options to apply electronic seal over the PDF document.

```$xslt
python src/electronicseal/electronic_seal_with_appearance_options.py
```

#### Apply Electronic Seal With Trusted Timestamp

The sample class ```electronic_seal_with_time_stamp_authority.py``` uses a time stamp authority to apply electronic seal with trusted timestamp over the PDF document.

```$xslt
python src/electronicseal/electronic_seal_with_time_stamp_authority.py
```


### Extract PDF

These samples illustrate extracting content of PDF in a structured JSON format along with the renditions inside PDF. 
The output of SDK extract operation is Zip package. The Zip package consists of following:

* The structuredData.json file with the extracted content & PDF element structure. See the [JSON schema](https://opensource.adobe.com/pdftools-sdk-docs/release/shared/extractJSONOutputSchema.json). Please refer the [Styling JSON schema](https://opensource.adobe.com/pdftools-sdk-docs/release/shared/extractJSONOutputSchemaStylingInfo.json) for a description of the output when the styling option is enabled. 
* A renditions' folder(s) containing renditions for each element type selected as input. 
  The folder name is either "tables" or "figures" depending on your specified element type. 
  Each folder contains renditions with filenames that correspond to the element information in the JSON file. 
  
#### Extract Text Elements

The sample class ```extract_text_info_from_pdf.py``` extracts text elements from PDF document.

```$xslt
python src/extractpdf/extract_text_info_from_pdf.py
```

#### Extract Text, Table Elements

The sample class ```extract_text_table_info_from_pdf.py``` extracts text, table elements from PDF document. 

```$xslt
python src/extractpdf/extract_text_table_info_from_pdf.py
```

#### Extract Text, Table Elements with Renditions of Table Elements

The sample class ```extract_text_table_info_with_renditions_from_pdf.py``` extracts text, table elements along with table renditions
from PDF document. Note that the output is a zip containing the structured information along with renditions as described
in [section](#extract-pdf).

```$xslt
python src/extractpdf/extract_text_table_info_with_renditions_from_pdf.py
```
#### Extract Text, Table Elements with Renditions of Figure, Table Elements

The sample class ```extract_text_table_info_with_figures_tables_renditions_from_pdf.py``` extracts text, table elements along with figure 
and table element's renditions from PDF document. Note that the output is a zip containing the structured information 
along with renditions as described in [section](#extract-pdf).

```$xslt
python src/extractpdf/extract_text_table_info_with_figures_tables_renditions_from_pdf.py
```
#### Extract Text Elements and bounding boxes for Characters present in text blocks

The sample class ```extract_text_info_with_char_bounds_from_pdf.py``` extracts text elements and bounding boxes for characters present in text blocks. Note that the output is a zip containing the structured information 
along with renditions as described in [section](#extract-pdf).

```$xslt
python src/extractpdf/extract_text_info_with_char_bounds_from_pdf.py
```

#### Extract Text, Table Elements and bounding boxes for Characters present in text blocks with Renditions of Table Elements

The sample class ```extract_text_table_info_with_char_bounds_from_pdf.py``` extracts text, table elements, bounding boxes for characters present in text blocks and 
table element's renditions from PDF document. Note that the output is a zip containing the structured information 
along with renditions as described in [section](#extract-pdf).

```$xslt
python src/extractpdf/extract_text_table_info_with_char_bounds_from_pdf.py
```

#### Extract Text, Table Elements with Renditions and CSV's of Table Elements 

The sample class ```extract_text_table_info_with_table_structure_from_pdf.py``` extracts text, table elements, table structures as CSV and 
table element's renditions from PDF document. Note that the output is a zip containing the structured information 
along with renditions as described in [section](#extract-pdf).

```$xslt
python src/extractpdf/extract_text_table_info_with_table_structure_from_pdf.py
```

#### Extract Text, Table Elements with Styling information of text

The sample class ```extract_text_table_info_with_styling_from_pdf.py``` extracts text and table elements along with the styling information of the text blocks.
Note that the output is a zip containing the structured information 
along with renditions as described in [section](#extract-pdf).

```$xslt
python src/extractpdf/extract_text_table_info_with_styling_from_pdf.py
```

##### Extract Text elements (handling error scenarios)

The sample class ```extract_text_from_pdf_exception_sample.py``` highlights how to handle different types of exception. Place the invalid input pdf file in resources/invalidinputs folder.

```$xslt
python src/extractpdf/extract_text_from_pdf_exception_sample.py <input file name>
```

### PDF Properties
This sample illustrates how to fetch properties of a PDF file

#### Fetch PDF Properties

The sample class ```get_pdf_properties.py``` fetches the properties of an input PDF.

```$xslt
python src/pdfproperties/get_pdf_properties.py
```

### Custom Client Configuration

These samples illustrate how to provide a custom client configurations(timeouts, proxy etc.).

#### Create a PDF File From a DOCX File (By providing custom value for timeouts)

The sample class ```create_pdf_with_custom_timeouts.py``` highlights how to provide the custom value for connection timeout and socket timeout.

```$xslt
python src/customconfigurations/create_pdf_with_custom_timeouts.py
```

#### Create a PDF File From a DOCX File (By providing Proxy Server settings)

The sample class ```create_pdf_with_proxy_server.py``` highlights how to provide Proxy Server configurations to allow all API calls via that proxy Server.

```$xslt
python src/customconfigurations/create_pdf_with_proxy_server.py
```

#### Create a PDF File From a DOCX File (By providing Proxy Server settings with authentication)

The sample class ```create_pdf_with_authenticated_proxy_server.py``` highlights how to provide Proxy Server configurations to allow all API calls via that proxy Server that requires authentication.

```$xslt
python src/customconfigurations/create_pdf_with_authenticated_proxy_server.py
```

#### Export a PDF File to a DOCX File (By providing the region)

The sample class ```export_pdf_with_specified_region.py``` highlights how to configure the SDK to process the documents in the specified region.
```$xslt
python src/customconfigurations/export_pdf_with_specified_region.py
```

### Create Tagged PDF

These samples illustrate how to create a PDF document with enhanced readability from existing PDF document. All tags from the input file will be removed except for existing alt-text images and a
new tagged PDF will be created as output. However, the generated PDF is not guaranteed to comply with accessibility standards such as WCAG and PDF/UA as you may need to perform further downstream remediation to meet those standards.

#### Create Tagged PDF from a PDF

The sample project ```autotag_pdf.py``` highlights how to add tags to PDF document to make the PDF more accessible.

```$xslt
python src/autotagpdf/autotag_pdf.py
```

### Create Tagged PDF from a PDF along with a report and shift the headings in the output PDF file

The sample project ```autotag_pdf_with_options.py``` highlights how to add tags to PDF documents to make the PDF more accessible and also shift the headings in the output PDF file.
Also, it generates a tagging report which contains the information about the tags that the tagged output PDF document contains.

```$xslt
python src/autotagpdf/autotag_pdf_with_options.py
```

#### Create Tagged PDF from a PDF by setting options with command line arguments

The sample project ```autotag_pdf_parametrised.py``` highlights how to add tags to PDF documents to make the PDF more accessible by setting options through command line arguments.

Here is a sample list of command line arguments and their description: </br>
--input &lt; input file path &gt; </br>
--output &lt; output file path &gt; </br>
--report { If this argument is present then the output will be generated with the tagging report } </br>
--shift_headings { If this argument is present then the headings will be shifted in the output PDF document } </br>

```$xslt
 python src/autotagpdf/autotag_pdf_parametrised.py --input src/resources/autotagPDFInput.pdf --output output/AutotagPDFParameterised/ --shift_headings --report
```

### External Input / Output Storage
These samples illustrate how to use external input and output storage for the supported operations.

####  Create a PDF File From a DOCX File Using External Input Storage

The sample class ```external_input_create_pdf_from_docx.py``` creates a PDF file from a DOCX file stored at external storage.

```$xslt
python src/externalstorage/external_input_create_pdf_from_docx.py
```

####  Create a PDF File From a DOCX File Using External Input Storage and Store the Result in External Output Storage

The sample class ```external_input_and_output_create_pdf_from_docx.py``` creates a PDF file from a DOCX file stored at external storage and stores the result in external output storage.

```$xslt
python src/externalstorage/external_input_and_output_create_pdf_from_docx.py
```

### Accessibility Checker
This samples illustrate how to check PDF files to see if they meet the machine-verifiable requirements of PDF/UA and WCAG 2.0.

#### Run Accessibility Checker on Input PDF

The sample class ```pdf_accessibility_checker.py``` checks the accessibility of an input PDF.

```$xslt
python src/pdfaccessibilitychecker/pdf_accessibility_checker.py
```

#### Run Accessibility Checker on input PDF file for given page start and page end

This sample class ```pdf_accessibility_checker_with_option.py``` checks the accessibility of an input PDF for given page start and page end.

```$xslt
python src/pdfaccessibilitychecker/pdf_accessibility_checker_with_option.py
```

### PDF Watermark
This sample illustrates how to add watermark to a PDF document.

#### Add watermark to a PDF document

The sample class ```pdf_watermark.py``` adds watermark with default appearance options to apply watermark on the PDF document.

```$xslt
python src/pdfwatermark/pdf_watermark.py
```

#### Run Add watermark to a PDF document with options

This sample class ```pdf_watermark_with_options.py``` adds watermark to a PDF document with custom watermark appearance option and page range options.

```$xslt
python src/pdfwatermark/pdf_watermark_with_options.py
```

### Contributing

Contributions are welcome! Read the [Contributing Guide](.github/CONTRIBUTING.md) for more information.

### Licensing

This project is licensed under the MIT License. See [LICENSE](LICENSE.md) for more information. 
