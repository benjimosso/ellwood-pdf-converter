import os
import argparse
from functions.pdf_to_markdown import pdf_to_markdown
from functions.openaicovertion import convert_to_supabase_format
from functions.tokencounter import num_tokens_from_string, num_tokens_from_messages
from pprint import pprint

def main():
#     markdown_example = """# Sample Title
# This is some sample content extracted from the PDF. It includes various sections and details.
# ## Subsection
# More detailed content goes here.
# """
#     convert_to_supabase_format(markdown_example)
    parser = argparse.ArgumentParser(description="Convert PDF to Markdown")
    parser.add_argument("pdf_path", help="Path to the PDF file")
    args = parser.parse_args()

    # load_dotenv()
    # api_key = os.environ.get("GEMINI_API_KEY")
    # if not api_key:
    #     raise RuntimeError("GEMINI_API_KEY environment variable not set")
    # client = genai.Client(api_key=api_key)

    # token_count = num_tokens_from_string("Esto es una prueba", "o200k_base")
    # print(f"Number of tokens in the string: {token_count}")
    # models_tokens = num_tokens_from_messages(
    #     [
    #         {"role": "system", "content": "You are a helpful assistant."},
    #         {"role": "user", "content": "Hello, how are you?"},
    #         {"role": "assistant", "content": "I'm good, thank you! How can I assist you today?"}
    #     ],
    #     model="gpt-4o-mini-2024-07-18"
    # )
    # print(f"Number of tokens in the messages: {models_tokens}")
    markdown_output = pdf_to_markdown(args.pdf_path)
    if markdown_output:
        print("Markdown conversion successful.")
        # Now you can pass this markdown_output to your conversion function
        amount_of_tokens = num_tokens_from_string(markdown_output, "o200k_base")
        print(f"Number of tokens in the markdown content: {amount_of_tokens}")
    else:
        print("Markdown conversion failed.")

if __name__ == "__main__":
    main()
    