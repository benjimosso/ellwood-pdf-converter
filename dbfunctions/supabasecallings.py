import os
from dotenv import load_dotenv
from supabase import create_client, Client
from pydantic import BaseModel



load_dotenv()
url: str= os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# Deterministic 1536-dim sample embedding for testing.
SAMPLE_EMBEDDINGS_1536 = [i / 1536 for i in range(1536)]


def supabase_login():
    
    auth_response = supabase.auth.sign_in_with_password(
        {
            "email": os.environ.get("SUPABASE_EMAIL"),
            "password": os.environ.get("SUPABASE_PASSWORD")
        }
    )
    return auth_response

def supabase_logout():
    supabase.auth.sign_out()

def supabase_get_hoas():
    login_response = supabase_login()
    if not login_response:
        print("Supabase login failed.")
        return None
    response = (
        supabase.table("hoas")
        .select("*")
        .execute()
    )
    return response.data

def supabase_get_rules():
    login_response = supabase_login()
    if not login_response:
        print("Supabase login failed.")
        return None
    response = (
        supabase.table("rules")
        .select("*")
        .execute()
    )
    return response.data

def supabase_get_hoa_id(hoa_name):
    login_response = supabase_login()
    if not login_response:
        print("Supabase login failed.")
        return None
    response = (
        supabase.table("hoas")
        .select("id")
        .eq("name", hoa_name)
        .execute()
    )
    if response.data:
        return response.data[0]["id"]
    else:
        print(f"HOA with name '{hoa_name}' not found.")
        return None

def supabase_insert_rules_table(hoa_id, markdown_content, embeddings, title, metadata):
    login_response = supabase_login()
    try:
        if not login_response:
            print("Supabase login failed.")
            return None
        response = (
            supabase.table("rules")
            .insert(
                {
                    "hoa_id": hoa_id,
                    "content": markdown_content,
                    "embeddings": embeddings,
                    "title": title,
                    "metadata": metadata.model_dump()  # Convert Pydantic model to dict for insertion
                }
            )
            .execute()
        )
        return response.data
    except Exception as e:
        print(f"Error inserting into Supabase: {e}")
        return None
    



# test = supabase_get_rules()
# print(test[1]['title'])
# print(test[1]["embeddings"])