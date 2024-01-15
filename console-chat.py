import openai

openai.api_key = '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'

def chat_with_gpt(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        temperature=0.7,
        n=1,
        stop=None,
    )
    return response.choices[0].text.strip()

conversation = ""
try:
	while True:
	    user_input = input("user:")
	    conversation += f"user: {user_input}\n"
	    response = chat_with_gpt(conversation)
	    conversation += f"AI: {response}\n"
	    print("AI:", response)

except KeyboardInterrupt:
	print("\n [+] quitting....\n [+] Good bye mr.snow\n")

