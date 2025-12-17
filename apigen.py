##### Generate the question and answers dataset for 
from fastapi import FastAPI, HTTPException, Depends

from fastapi.security import OAuth2PasswordBearer

from pydantic import BaseModel
import openai

# Set your OpenAI API key or make .env file
# As well check out the openai documentation
openai.api_key = ""
# OAuth2 configuration
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Hardcoded username and token for simplicity
VALID_USERNAME = "medical_user"
VALID_TOKEN = "secure_token_1234"

# Initialize FastAPI app
app = FastAPI()

# Request schema
class ChatRequest(BaseModel):
    username: str
    query: str

def verify_user(username: str, token: str):
    """
    Verifies the username and token.
    """
    if username != VALID_USERNAME or token != VALID_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

def ask_medical_bot(user_query: str) -> str:
    """
    Calls OpenAI API to generate a medical bot response.
    """
    try:
        # Define the messages for the chat-based model
        messages = [
            {"role": "system", "content": (
                "You are a highly knowledgeable, empathetic, and professional medical assistant. "
                "Your primary goal is to provide accurate and helpful information about diseases, their symptoms, and solutions. "
                "You can also suggest alternative medicines and offer practical advice for managing stress. "
                "If a user asks something unrelated to medical topics, kindly let them know that you specialize in medical queries only. "
                "Always respond politely, concisely, and professionally, offering support and encouragement."
            )},
            {"role": "user", "content": user_query},
        ]

        # Call the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use gpt-4 if desired
            messages=messages,
            temperature=0.7,
        )

        # Return the generated response
        return response['choices'][0]['message']['content'].strip()

    except openai.error.OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")

@app.post("/chat/")
def chat(request: ChatRequest, token: str = Depends(oauth2_scheme)):
    """
    API endpoint to interact with the medical chatbot.
    """
    # Verify user credentials
    verify_user(request.username, token)

    # Get the bot's response
    bot_response = ask_medical_bot(request.query)
    return {"username": request.username, "response": bot_response}
