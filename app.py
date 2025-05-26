import time
import os
from fastapi import FastAPI, HTTPException, Depends
from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Load security token from environment variables or config
VALIDATION_TOKEN = os.getenv("API_VALIDATION_TOKEN")
print(VALIDATION_TOKEN)


# Define the request model using Pydantic for validation
class QueryRequest(BaseModel):
    api_key: str  # API key for authentication
    question: str  # User's question/query
    token: str  # Security validation token


# Function to verify the API validation token
def validate_token(token: str) -> bool:
    """
    Checks if the provided token matches the expected validation token.
    Returns True if valid, False otherwise.
    """
    return token == VALIDATION_TOKEN


# Function to validate the provided API key before making a request
def validate_api_key(api_key: str) -> bool:
    """
    Validates the API key by making a lightweight request to OpenRouter.
    Returns True if the API key is valid, otherwise False.
    """
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        client.models.list()  # Attempt to list available models
        return True
    except Exception:
        return False  # Return False if the request fails


# Function to send a query to OpenAI via OpenRouter
def get_openai_response(api_key: str, question: str, token: str):
    """
    Sends a query to OpenAI's API via OpenRouter and returns the response.
    Also measures the response time for monitoring performance.
    """
    MODEL = "meta-llama/llama-3.3-8b-instruct:free"  # Define the model to use

    # Validate API key
    if not validate_api_key(api_key):
        raise HTTPException(status_code=401, detail="Invalid API key")

    # Initialize OpenAI client with the provided API key
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    start_time = time.time()  # Record the start time for response timing

    try:
        # Make the API request
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "<YOUR_SITE_URL>",  # Optional metadata for OpenRouter
                "X-Title": "<YOUR_SITE_NAME>",
            },
            extra_body={},
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "system": "You are FinGraph Sage, an AI specializing in financial data analysis and graph navigation.",
                    "content": question,  # User's query
                },
            ],
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error calling OpenAI API: {str(e)}"
        )

    response_time = time.time() - start_time  # Calculate total response time
    return {
        "response": completion.choices[0].message.content,  # Extract response content
        "response_time_seconds": round(response_time, 2),  # Round response time
	"response_usage": completion.usage,
        "llm_model":completion.model,
        "created": completion.created,
        "system_fingerprint": completion.system_fingerprint,        
    }


# FastAPI endpoint to process queries with token validation
@app.post("/query")
def query_openai(request: QueryRequest):
    """
    FastAPI route to handle POST requests and return AI-generated responses.
    Users must provide an API key, a security token, and a query.
    """
    if not validate_token(request.token):  # Validate token BEFORE calling API
        raise HTTPException(status_code=403, detail="Invalid security token")

    return get_openai_response(request.api_key, request.question, request.token)


# Run the FastAPI server using Uvicorn (for local testing or production)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8888)  # Start the server
