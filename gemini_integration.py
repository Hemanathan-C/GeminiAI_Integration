from google import genai
from env import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)



print("Hey there ! I'm a Gemini AI model.")
print("I can help you with various tasks.")
print("For example, I can generate content for you.")
conversation = []
while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit','quit','stop']:
        print("Exiting the program...")
        print("Thank you for using the Gemini AI model.")
        print("Goodbye!")
        break
    else:
        conversation.append(user_input)
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=conversation,
        )
        conversation.append(response.text)
        print("Gemini: ",response.text)
# print("CONVERSATIONS: ",conversation)
