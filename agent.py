from typing import Optional

from google import genai
from openai import OpenAI
from env import GEMINI_API_KEY
import requests
import json
from pydantic import BaseModel, Field

client = OpenAI(
    api_key=GEMINI_API_KEY, 
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

SYSTEM_PROMPT = """
    You're an expert AI Assistant in resolving user queries using chain of thought.
    You work on START, PLAN and OUTPUT steps.
    You need to first PLAN what needs to be done. The PLAN can be multiple steps.
    Once you think enough PLAN has been done, finally you can give an OUTPUT. 
    you can also use available tools if you think it is necessary to resolve the query.
    for every tool call, wait for the OBSERVE step, which is the output from the called tool.

    Rules:
    - Strictly Follow the given JSON output format.
    - Only run one step at a time.
    - The sequence of steps is START (where user gives an input), PLAN (that can be multiple times) and finally OUTPUT (which is going to be displayed to the user).

    Output JSON Format:
    { "step": "START" | "PLAN" | "OUTPUT" | "TOOL", "content": "string", "tool": "string", "input": "string" }

    available Tools:
    - get_weather_info(location): This tool takes a location as input and returns the current weather information for that location.

    Example 1:
    START: Hey, can you solve 2 + 3 * 5 / 10
    PLAN: { "step": "PLAN": "content": "Seems like user is interested in math problem" }
    PLAN: { "step": "PLAN": "content": "looking at the problem, we should solve this using BODMAS method" }
    PLAN: { "step": "PLAN": "content": "first we must multiply 3 * 5 which is 15" }
    PLAN: { "step": "PLAN": "content": "Yes, The BODMAS is correct thing to be done here" }
    PLAN: { "step": "PLAN": "content": "Now the new equation is 2 + 15 / 10" }
    PLAN: { "step": "PLAN": "content": "We must perform divide that is 15 / 10 = 1.5" }
    PLAN: { "step": "PLAN": "content": "Now the new equation is 2 + 1.5" }
    PLAN: { "step": "PLAN": "content": "Now finally lets perform the add 3.5" }
    PLAN: { "step": "PLAN": "content": "Great, we have solved and finally left with 3.5 as answer" }
    OUTPUT: { "step": "OUTPUT": "content": "Great, we have solved and finally left with 3.5 as answer" }

    Example 2:
    START: What is the weather of Delhi?
    PLAN: { "step": "PLAN": "content": "Seems like user is interested in getting weather of Delhi in India" }
    PLAN: { "step": "PLAN": "content": "Lets see if we have any available tool from the list of available tools" }
    PLAN: { "step": "PLAN": "content": "Great, we have weather available tool for this query" }
    PLAN: { "step": "PLAN": "content": "I need to call the get_weather_info tool with Delhi as the location" }
    PLAN: { "step": "TOOL": "tool": "get_weather_info", "input": "delhi" }
    PLAN: { "step": "OBSERVE": "tool": "get_weather_info", "output": "the temperature in Delhi is cloudy with 25°C" }
    PLAN: { "step": "PLAN": "content": "Great, I got the weather info about Delhi" }
    OUTPUT: { "step": "OUTPUT": "content": "The current weather in Delhi is cloudy with 25°C" }
"""

class MyOutputFormat(BaseModel):
    step: str = Field(..., description="The current step in the process. Example: START, PLAN, OUTPUT, TOOL.")
    content: Optional[str] = Field(None, description="The content of the message. This can be any string that provides information about the current step.")
    tool: Optional[str] = Field(None, description="The name of the tool to be used. This field is only relevant when the step is TOOL.")
    input: Optional[str] = Field(None, description="The input for the tool. This field is only relevant when the step is TOOL.")


def get_weather_info(location):
    
    url = f"https://wttr.in/{location}?format=%C+%t"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return "Something Went Wrong! Unable to fetch weather information."

avl_tool_map = {
    "get_weather_info": get_weather_info
}

message_history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

while True:

    user_input = input("Enter Text:  ")
    message_history.append({"role": "user", "content": user_input})

    while True:
        response = client.chat.completions.parse(
            model="gemini-2.5-flash", 
            response_format=MyOutputFormat,
            messages=message_history
        )
        assistant_message = response.choices[0].message.content
        message_history.append({"role": "assistant", "content": assistant_message})
        assistant_response_json = response.choices[0].message.parsed
        if assistant_response_json.step == "START":
            print("Getting Started: ", assistant_response_json.content)
            continue
        if assistant_response_json.step == "TOOL":
            tool_name = assistant_response_json.tool
            tool_input = assistant_response_json.input
            tool_response = avl_tool_map[tool_name](tool_input)
            print(f"Calling Tool: {tool_name} with input: {tool_input} = {tool_response}")
            message_history.append({"role": "developer", "content": json.dumps(
                {"step": "OBSERVE", "tool": tool_name, "input": tool_input, "output": tool_response}
            )})
            continue
        if assistant_response_json.step == "PLAN":
            print("Planning: ", assistant_response_json.content)
            continue
        if assistant_response_json.step == "OUTPUT":
            print("Output: ", assistant_response_json.content)
            break
