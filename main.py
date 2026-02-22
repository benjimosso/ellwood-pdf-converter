import os
import argparse
from functions.pdf_to_markdown import pdf_to_markdown
from functions.openaicovertion import convert_to_supabase_format
from functions.tokencounter import num_tokens_from_string, num_tokens_from_messages
from dbfunctions.supabasecallings import supabase_insert_rules_table
from pprint import pprint

def main():

    parser = argparse.ArgumentParser(description="Convert PDF to Markdown")
    # parser.add_argument("pdf_path", help="Path to the PDF file")
    args = parser.parse_args()

    pdf_folder = "./pdfs"
    if os.path.isdir(pdf_folder):
        print(f"PDF folder '{pdf_folder}' exists. Processing PDFs...")
        for filename in os.listdir(pdf_folder):
            if filename.endswith(".pdf"):
                pdf_path = os.path.join(pdf_folder, filename)
                print(f"Processing PDF: {pdf_path}")
                markdown_output = pdf_to_markdown(pdf_path)
                if markdown_output:
                    print("Markdown conversion successful.")
                    # Now you can pass this markdown_output to your conversion function
                    gpt_output, embeddings, original_markdown = convert_to_supabase_format(markdown_output)
                    pprint(f"Metadata Extracted from Markdown text: {gpt_output[0].metadata}", indent=2, width=80)
                    hoa_id = os.environ.get("HOA_ID")  # Replace with the actual HOA ID from environment variable
                    if gpt_output and embeddings:
                        insert_response = supabase_insert_rules_table(hoa_id, original_markdown, embeddings, gpt_output[0].title, gpt_output[0].metadata)
                        if not insert_response:
                            print("Failed to insert data into Supabase.")
                        else:
                            print("Data inserted into Supabase successfully.")
                            print(f"Filename '{filename}' processed and stored in database.")
                    
                else:
                    print("Markdown conversion failed.")

    else:
        print(f"PDF folder '{pdf_folder}' does not exist. Please create the folder and add PDF files to process.")
    # Old usage single file processing:
    # markdown_output = pdf_to_markdown(args.pdf_path)
    # if markdown_output:
    #     print("Markdown conversion successful.")
    #     # Now you can pass this markdown_output to your conversion function
    #     gpt_output, embeddings, original_markdown = convert_to_supabase_format(markdown_output)
    #     pprint(f"GPT Output: {gpt_output}", indent=2, width=80)
    #     hoa_id = "ef6de8fc-39d0-4607-a053-88b69f7a34b3"  # Replace with the actual HOA ID
    #     if gpt_output and embeddings:
    #         insert_response = supabase_insert_rules_table(hoa_id, original_markdown, embeddings, gpt_output[0].title, gpt_output[0].metadata)
    #         pprint(f"Supabase Insert Response: {insert_response}", indent=2, width=80)
        
    # else:
    #     print("Markdown conversion failed.")

if __name__ == "__main__":
    main()
    