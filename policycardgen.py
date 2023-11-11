import json
import requests
from apikey import apikey
YOUR_OPENAI_API_KEY = apikey


# Define the function for generating a policy card
def generate_policy_card(user_needs_rankings):
    # Implement the logic to create the policy card based on user needs and rankings
    return {
        "policy_card_prompt": "Policy for addressing user needs",
        "policy_card_description": "This policy aims to address the top ranked user needs such as " + ", ".join(user_needs_rankings.keys()),
        "corresponding_user_needs": list(user_needs_rankings.keys()),
        "policy_category": "Urban Development"  # Example category
    }

# Function specifications for the API
functions = [
    {
        "name": "generate_policy_card",
        "description": "Generate a policy card based on user needs and rankings",
        "parameters": {
            "type": "object",
            "properties": {
                "user_needs_rankings": {
                    "type": "object",
                    "description": "A dictionary of user needs and their rankings"
                }
            },
            "required": ["user_needs_rankings"]
        }
    }
]


# Function to send request to Chat Completion API
def chat_completion_request(messages, functions=None, function_call=None, model="gpt-4"):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + YOUR_OPENAI_API_KEY,
    }
    json_data = {"model": model, "messages": messages}
    if functions is not None:
        json_data.update({"functions": functions})
    if function_call is not None:
        json_data.update({"function_call": function_call})

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print("Request failed:", e)
        print("Response:", response.text)
        return None

# Example conversation with dummy data
dummy_user_needs = {
    "Transportation": 5,
    "Healthcare": 3,
    "Education": 4
}
messages = [
    {"role": "system", "content": "Use the generate_policy_card function to create a policy card."},
    {"role": "user", "content": "I need a policy card for our city's needs survey."},
    {"role": "assistant", "content": "Generating policy card...", "function_call": {"name": "generate_policy_card", "arguments": json.dumps({"user_needs_rankings": dummy_user_needs})}}
]


# Send request and get response
response = chat_completion_request(messages, functions=functions)

if response:
    try:
        if "function_call" in response["choices"][0]["message"]:
            function_call = response["choices"][0]["message"]["function_call"]
            user_needs_rankings = json.loads(function_call["arguments"])["user_needs_rankings"]
            policy_card = generate_policy_card(user_needs_rankings)
            print(policy_card)
        else:
            print("No function call generated. Check the input or conversation flow.")
    except KeyError as e:
        print("KeyError occurred:", e)
        print("Response structure:", response)
else:
    print("Failed to get a valid response.")

# Replace YOUR_OPENAI_API_KEY with your actual OpenAI API key
