import os

from groq import Groq
from env import GROQ_API_KEY

client = Groq(
    api_key=GROQ_API_KEY
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "Explain the importance of fast language models",
        }
    ],
    model="llama-3.3-70b-versatile",
)

print("Hey there ! I'm a Groq AI model.")
print("I can help you with various tasks.")
print("For example, I can generate content for you.")
conversation = []
while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit','quit','stop']:
        print("Exiting the program...")
        print("Thank you for using the Groq AI model.")
        print("Goodbye!")
        break
    else:
        conversation.append({
                    "role": "system",
                    "content": user_input
                },)
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": conversation
                },
            ],
            model="llama-3.3-70b-versatile",
        )
    assistant_reply = chat_completion.choices[0].message.content
    print(assistant_reply)
    conversation.append({"role": "assistant", "content": assistant_reply})


#     system_message = {
#     "role": "system",
#     "content": "You are a helpful assistant."
# }
# conversation = []

# while True:
#     user_input = input("You: ")
#     if user_input.lower() in ['exit', 'quit', 'stop']:
#         print("Exiting the program...")
#         print("Thank you for using the Groq AI model.")
#         print("Goodbye!")
#         break
#     else:
#         conversation.append({"role": "user", "content": user_input})
#         messages = [system_message] + conversation
#         chat_completion = client.chat.completions.create(
#             messages=messages,
#             model="llama-3.3-70b-versatile",
#         )
#         assistant_reply = chat_completion.choices[0].message.content
#         print(assistant_reply)
#         conversation.append({"role": "assistant", "content": assistant_reply})
