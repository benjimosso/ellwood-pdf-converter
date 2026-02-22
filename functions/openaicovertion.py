import os
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
from pprint import pprint

class Metadata(BaseModel):
    associated_hoa: str
    CC_R_reference: str
    document_name: str
    pages: int
    effective_date: str
    category: str
    tags: list[str]

class GPTOutput(BaseModel):
    title: str
    metadata: Metadata


def convert_to_supabase_format(markdown_content: str) -> tuple[list[GPTOutput], list[float], str]:
    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable not set")
    client = OpenAI(api_key=api_key)  # Initialize OpenAI client with API key

    
    response_embeddings = client.embeddings.create(
        model="text-embedding-3-small",
        input=markdown_content,
        encoding_format="float"
    )
    embeddings = response_embeddings.data[0].embedding
    response_json = client.responses.parse(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": "You are a helpful assistant that converts markdown content into a format suitable for Supabase."},
            {"role": "user", "content": f"""Convert the following markdown content into a JSON format with title and metadata: {markdown_content}

The title should be a concise summary of the content.

The metadata should include any relevant tags or categories looking something like this:
{{  
    associated_hoa: "Sunrise Village",
    CC_R_reference: "6.6.g",
    document_name: "Sunrise_Village_Guidelines", 
    pages: 1,
    effective_date: "2017-06-27",
    category: "Landscaping",
    tags: ["encroachment", "common area", "maintenance"]
}}

Adapt the field names and values to match the content provided."""}
        ],
        text_format=GPTOutput
    )

    event = response_json.output_parsed
    if not event:
        raise ValueError("Failed to parse GPT response into the expected format.")
    print("GPT Output Parsed Successfully!... Preparing data for Supabase insertion.")
    return ([
        GPTOutput(
            title=event.title,
            metadata=event.metadata
        ),
    ], embeddings, markdown_content)