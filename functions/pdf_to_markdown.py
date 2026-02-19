import os
from google.genai import types
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered
import torch

def pdf_to_markdown(pdf_path):
    try:
        # You can force it to use CPU if you want to keep memory usage low
        # Select "mps" for Apple Silicon, "cuda" for NVIDIA, or "cpu" for CPU-only
        if (torch.backends.mps.is_available()) and (torch.backends.mps.is_built()):
            os.environ["TORCH_DEVICE"] = "mps"
        elif torch.cuda.is_available():
            os.environ["TORCH_DEVICE"] = "cuda"
        else:
            os.environ["TORCH_DEVICE"] = "cpu"
        # Or "cuda" for NVIDIA, "mps" for Apple Silicon

        basedir = os.path.dirname("./")
        pdf_path = os.path.join(basedir, pdf_path)

        # 1. Initialize Marker (This loads the AI models)
        converter = PdfConverter(artifact_dict=create_model_dict())

        # 2. Convert PDF to Markdown
        rendered = converter(pdf_path)
        full_markdown, _, _ = text_from_rendered(rendered)
        return full_markdown
        # 3. Your "Dictionary" Logic
        # Marker's output is so clean you can now split by its 
        # beautiful headers (e.g., "##", "###")
        # sections = full_markdown.split("\n## ") 

        # final_sections = []
        # for section in sections:
        #     # Send this 'clean' section to the agent!
        #     # print(f"Feeding cleaned section to DB: {section}...")
        #     final_sections.append(section)
        # 4. Final Output
        # print("Final Markdown Output:")
        # print(full_markdown)
        # pprint.pprint(final_sections, indent=2, width=80)
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return None


schema_pdf_to_markdown = types.FunctionDeclaration(
    name="pdf_to_markdown",
    description="Converts a PDF file to Markdown format",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "pdf_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the PDF file to be converted to Markdown",
            ),
        },
    ),
)

