#!/bin/env python
import os
import sys
import select

import openai
import datetime
import argparse

This_Path = os.path.dirname(os.path.abspath(__file__))


# Load your API key from an environment variable or secret management service
# openai.api_key = os.getenv("OPENAI_API_KEY")

def get_token():
    with open(os.path.join(This_Path, '.token')) as token:
        return token.read().strip()


def main(question):
    openai.api_key = get_token()
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

    stdin_pending, _, _ = select.select([sys.stdin], [], [], 0.001)

    if stdin_pending:
        resp_text, resp_raw = main(sys.stdin.read())
        print(resp_text)

    parser = argparse.ArgumentParser()

    parser.add_argument('-r', '--save-resp', action='store_true', help='save detailed response')
    parser.add_argument('-t', '--get-token', action='store_true', help='retrieves token from .token file')
    parser.add_argument('-i', '--interactive', action='store_true', help='interactive mode')
    parser.add_argument('query', nargs='*', help='chatgpt question')
    args = parser.parse_args()

    if args.get_token:
        print(get_token())
        sys.exit(0)

    if args.interactive:
        prompt = "?> "
        print("---INTERACTIVE MODE---")
        print("'CTRL-C or 'end conversation' to stop")
        print(f"start with '^' to refer to previous question: {prompt}^ elaborate more")

        question = input(prompt)
        while question:
            question_prev = question
            resp = main(question)[0]
            print(f"chatgpt: {resp}")
            question = input(prompt)
            if question.startswith('^'):
                question = question[1:]
                question = f"In regards to question: {question_prev}\nyou answered: {resp}\n{question}"
                print(question)
            elif question == 'end conversation':
                break

    q = ' '.join(args.query)
    resp_txt, resp_raw = main(q)

    if args.save_resp:
        now = datetime.datetime.now()
        date_string = now.strftime("%Y-%m-%d_%H_%M_%S")

        resps_dir = "responses"
        os.makedirs(resps_dir, exist_ok=True)
        target_file = os.path.join(resps_dir, f'response{date_string}.txt')
        target_file_simple = os.path.join(resps_dir, f'response_simple{date_string}.txt')
        with open(target_file, 'w') as resp, open(target_file_simple, 'w') as resp_simple:
            resp.write(f"question: '{q}'\n")
            resp.write(f"response:{resp_txt}\n")
            resp.write('\n' + 30 * '-')
            resp.write(str(resp_raw))

            resp_simple.write(f"question: {q}\n")
            resp_simple.write(f"answer: {resp_txt}")
    print()
    print(resp_txt)
