#!/bin/env python
import sys
import openai
import datetime
import argparse


# Load your API key from an environment variable or secret management service
# openai.api_key = os.getenv("OPENAI_API_KEY")

def main(question):
    with open('.token') as token:
        openai.api_key = token.read().strip()

    resp_raw = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user",
             "content": question,
             }
        ]
    )
    resp_dict = resp_raw.to_dict()
    resp_text = resp_dict['choices'][0]['message']['content']
    return resp_text, resp_raw


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-r', '--save-resp', action='store_true', help='save detailed response')
    parser.add_argument('query', nargs='*', help='chatgpt question')
    args = parser.parse_args()
    # print(args.query)
    q = ' '.join(args.query)
    resp_txt, resp_raw = main(q)

    if args.save_resp:
        now = datetime.datetime.now()
        date_string = now.strftime("%Y-%m-%d_%H_%M_%S")
        with open(f'response{date_string}.txt', 'w') as resp:
            resp.write(f"question: '{q}'\n")
            resp.write("response:\n")
            resp.write(resp_txt)
            resp.write('\n' + 30 * '-')
            resp.write(str(resp_raw))

    print(resp_txt)
