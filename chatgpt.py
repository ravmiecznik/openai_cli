#!/bin/env python
import os
import sys
import textwrap
import select
import shutil
import openai
import datetime
import argparse

This_Path = os.path.dirname(os.path.abspath(__file__))


# Load your API key from an environment variable or secret management service
# openai.api_key = os.getenv("OPENAI_API_KEY")

def get_token():
    with open(os.path.join(This_Path, '.token')) as token:
        return token.read().strip()


def main(question, model="gpt-3.5-turbo"):
    openai.api_key = get_token()
    resp_raw = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "user",
             "content": question,
             }
        ]
    )
    resp_dict = resp_raw.to_dict()
    resp_text = resp_dict['choices'][0]['message']['content']
    return resp_text, resp_raw


def print_wrapped(percent=70):
    terminal_width = shutil.get_terminal_size().columns
    output_width = int(terminal_width * percent/100 + 0.5)

    def print_w(text, *args, **kwargs):
        for line in text.splitlines():
            # will not break source code snippets
            print('\n'.join(textwrap.wrap(line, width=output_width)), *args, **kwargs)
    return print_w


print70w = print_wrapped(70)
#print70w = print

if __name__ == "__main__":
    stdin_pending, _, _ = select.select([sys.stdin], [], [], 0.001)
    if stdin_pending:
        resp_text, resp_raw = main(sys.stdin.read())
        print70w(resp_text)

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
        print(f"start with '^' to refer to previous question like :\n\t{prompt}^ elaborate more")

        question = input(prompt)
        while question:
            question_prev = question
            resp = main(question)[0]
            print70w(f"chatgpt: {resp}")
            question = input(prompt)
            if question.startswith('^'):
                question = question[1:]
                question = f"In regards to question: {question_prev}\nyou answered: {resp}\n{question}"
            elif question == 'end conversation':
                break

    q = ' '.join(args.query)
    resp_txt, resp_raw = main(q)

    if args.save_resp:
        now = datetime.datetime.now()
        date_string = now.strftime("%Y-%m-%d_%H_%M_%S")
        resps_dir = os.getenv("artifacts_base_path", ".")
        resps_dir = os.path.join(resps_dir, "responses")
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
    print70w(resp_txt)
