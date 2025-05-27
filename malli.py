from groq import Groq

# Set the Groq API key
groq_client = Groq(add Your API)

# Function to send user's message to Groq for response
def send_to_groq(messages, model="llama3-8b-8192"):
    response = groq_client.chat.completions.create(messages=messages, model=model)
    return response.choices[0].message.content

# Main loop for conversation
messages = []

print("Type 'exit' to end the conversation.")

while True:
    user_text = input("You: ")
    if user_text.lower() == "exit":
        print("Goodbye!")
        break
    messages.append({"role": "user", "content": user_text})
    response_text = send_to_groq(messages)
    print(f"Assistant: {response_text}")
    messages.append({"role": "assistant", "content": response_text})  # Ensure there's no non-breaking space here
