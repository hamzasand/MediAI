import openai
openai.api_key = ""
def ask_medical_bot(user_query):
    """
    This function takes the user's query and generates a response using OpenAI's GPT model.
    Args:
        user_query (str): The user's question or query.
    Returns:
        str: The chatbot's response.
    """
    try:
        # Define the messages for the chat-based  model
        # Can be change according your requirements as want assign a role for your purpose
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
        
        # Call the OpenAI API using ChatCompletion
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use gpt-4 if available and desired
            messages=messages,
            temperature=0.7,  # Adjust creativitylevel
        )
        
        # Extract and return the response text
        return response['choices'][0]['message']['content'].strip()

    except openai.error.OpenAIError as e:
        return f"An error occurred: {str(e)}"

# Chatbot Interface
if __name__ == "__main__":
    print("Welcome to the Medical Chatbot!")
    print("You can ask about diseases, symptoms, alternative medicines, or stress-related issues.")
    print("Type 'exit' to end the conversation.")
    
    while True:
        # Take user input
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'exit':
            print("Goodbye! Stay healthy!")
            break

        
        # Get response from the bot
        bot_response = ask_medical_bot(user_input)
        print(f"Bot: {bot_response}")
