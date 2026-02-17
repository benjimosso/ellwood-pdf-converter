from google.genai import types
from functions.pdf_markd import pdf_to_markdown, schema_get_files_info

available_functions = types.Tool(
    function_declarations=[schema_pdf_to_markdown],
)

def call_function(function_call, verbose=False):
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    print(f" - Calling function: {function_call.name}")
    function_mapping = {
        "pdf_to_markdown": pdf_to_markdown,
    }
    function_name = function_call.name or ""
    if function_name not in function_mapping:
        return types.Content(
            role="tool",
             parts=[
                 types.Part.from_function_response(
                     name=function_name,
                     response={"error": f"Unknown function: {function_name}"},
                 )
             ]
        )
    
    # Call the function
    func = function_mapping[function_name]
    result = func(**function_call.args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result},
            )
        ]
    )