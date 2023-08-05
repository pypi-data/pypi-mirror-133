# AUTOGENERATED! DO NOT EDIT! File to edit: 00_core.ipynb (unless otherwise specified).

__all__ = ['pdf_to_img', 'extract_images_from_pdfs']

# Cell
def pdf_to_img(pdf_path: Path, destination_path: Path, img_type: str, export_quality_factor=2.0) -> None:
    """Converts a PDF file into a series of image files.

    Each image file is labelled with its page number"""
    destination_path.mkdir(parents=True, exist_ok=True) # create the destination directory if it doesn't already exist
    pdf_obj = fitz.open(file)
    mat = fitz.Matrix(export_quality_factor, export_quality_factor)
    for page_number in range(len(pdf_obj)):
        page = pdf_obj.load_page(page_number)
        pix = page.get_pixmap(matrix=mat)  # use 'mat' instead of the identity matrix
        pix.save(f"{str(destination_path)}/{file.name[:-4]}-{page_number + 1}.{img_type}")

# Cell
def extract_images_from_pdfs(source_folder: Path, destination_folder: Path, img_type: str, export_quality_factor=2.0):
    """Converts all PDF files inside a particular source folder into individual image files.

    Each PDF file exports a single image for each page.
    You can specify the type of image you want. See
    https://pymupdf.readthedocs.io/en/latest/faq.html#how-to-convert-images for
    a full list of support export options."""
    files = list(source_folder.glob("*.pdf"))
    for file in files:
        pdf_to_img(file, destination_folder, "png")