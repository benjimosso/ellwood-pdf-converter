import os
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
from pprint import pprint

class GPTOutput(BaseModel):
    title: str
    content: str
    metadata: list[str]

# def convert_to_supabase_format(markdown_content: str) -> tuple[list[GPTOutput], list[float], str]:
def convert_to_supabase_format(markdown_content: str):
    # This is a placeholder function. You would implement your logic to parse the markdown
    # and create GPTOutput instances based on the content.
    # For example, you might split the markdown into sections and create an output for each section.
    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable not set")
    client = OpenAI(api_key=api_key)  # Initialize OpenAI client with API key

    #testing a simple response: 
    response = client.responses.create(
        model="gpt-4o-mini",
        input="Who won the last world cup?"
    )
    print(response.output_text)
    # response_embeddings = client.embeddings.create(
    #     model="text-embedding-ada-002",
    #     input=markdown_content,
    #     encoding_format="float"
    # )
    # embeddings = response_embeddings.data[0].embedding
    # response_json = client.responses.parse(
    #     model="gpt-4o-mini",
    #     input=[
    #         {"role": "system", "content": "You are a helpful assistant that converts markdown content into a format suitable for Supabase."},
    #         {"role": "user", "content": f"Convert the following markdown content into a JSON format with title, content, and metadata: {markdown_content}"}
    #     ],
    # )

    # event = response_json.output_parsed
    # pprint(f"Parsed GPT Output: {event}", indent=2, width=80)
    # pprint(f"Generated Embeddings: {embeddings[:5]}...")  # Print the first 5 dimensions of the embedding for verification
    # return ([
    #     GPTOutput(
    #         title=event.title,
    #         metadata={"source": "pdf_to_markdown"}
    #     ),
    # ], embeddings, markdown_content)