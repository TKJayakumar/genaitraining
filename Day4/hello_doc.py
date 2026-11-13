from pathlib import Path
from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import InputFormat
from docling.document_converter import (
    DocumentConverter,
    PdfFormatOption
)

from docling.datamodel.pipeline_options import PdfPipelineOptions

from docling.datamodel.pipeline_options import PdfPipelineOptions

from docling_core.types.doc import (ImageRefMode,  PictureItem,  TableItem)


pipeline_options = PdfPipelineOptions(
    do_ocr=True,
    do_table_structure=True,
    generate_picture_images=True,
    generate_page_images=True,
    images_scale=2.0
)
 
pdf_path = "ai_agents_2026_brief.pdf"

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

#converter = DocumentConverter()
converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(
            pipeline_options=pipeline_options
        )
    }
)

 
result = converter.convert(pdf_path)



doc = result.document
 
# markdown_content = doc.export_to_markdown()

# output_file = output_dir / "parsed_document.md"

# output_file.write_text(markdown_content, encoding="utf-8")

# print("PDF parsing completed!")

# print(markdown_content)
 
doc.save_as_markdown(

    output_dir / "parsed_document.md",

    image_mode=ImageRefMode.REFERENCED

)
 
picture_count = 0
 
for element, level in doc.iterate_items():

    if isinstance(element, PictureItem):

         picture_count += 1

         image = element.get_image(doc)

         if image:

            image.save(output_dir / f"picture_{picture_count}.png")

         print(f"Extracted picture: {picture_count}")
 
print(f"total extracted images are : {picture_count}")            

 
