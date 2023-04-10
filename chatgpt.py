#!/bin/env python
import sys
import openai
import datetime


# Load your API key from an environment variable or secret management service
# openai.api_key = os.getenv("OPENAI_API_KEY")

def main(question):
    with open('.token') as token:
        openai.api_key = token.read().strip()

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user",
             "content": question,
             }
        ]
    )

    resp_dict = response.to_dict()

    now = datetime.datetime.now()
    date_string = now.strftime("%Y-%m-%d_%H_%M_%S")

    resp_text = resp_dict['choices'][0]['message']['content']
    print(resp_text)

    with open(f'response{date_string}.txt', 'w') as resp:
        resp.write(f"question: '{question}'\n")
        resp.write("response:\n")
        resp.write(resp_text)
        resp.write('\n' + 30 * '-')
        resp.write(str(response))


if __name__ == "__main__":
    q = ' '.join(sys.argv[1:])
    main(q)
