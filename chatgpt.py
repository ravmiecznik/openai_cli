#!/bin/env python
import os
import sys
import textwrap
import select
import shutil
import openai
import datetime
import argparse
import json
from pprint import pformat

# This_Path = os.path.dirname(os.path.abspath(__file__))

This_Path = os.path.dirname(os.path.abspath(__file__))

Responses_dir = os.getenv("artifacts_base_path", ".")
Responses_dir = os.path.join(Responses_dir, "responses")
os.makedirs(Responses_dir, exist_ok=True)


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
    output_width = int(terminal_width * percent / 100 + 0.5)

    def print_w(text, *args, **kwargs):
        for line in text.splitlines():
            # will not break source code snippets
            print('\n'.join(textwrap.wrap(line, width=output_width)), *args, **kwargs)

    return print_w


def save_json(data: dict, filename: str):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def save_last_resp(question: str, response: dict, target_file: str = None):
    """
    Saves last response to json file
    :param question: string of question
    :param response: a full dict of response
    :param target_file: filename to save to, if None, will create a new file else will append to existing
    :return: None
    """

    if target_file is not None:
        # load json from target_file
        target_file = os.path.join(Responses_dir, target_file)
        with open(target_file) as f:
            _data = json.load(f)
            _data.append({
                "question": question,
                "response": response
            })

    else:
        _data = [
            {
                "question": question,
                "response": response
            }
        ]
        now = datetime.datetime.now()
        date_string = now.strftime("%Y-%m-%d_%H_%M_%S")
        target_file = os.path.join(Responses_dir, f'response{date_string}.json')
    save_json(_data, target_file)


def get_last_resp():
    data, last_file = None, None

    try:
        files = os.listdir(Responses_dir)
        files.sort(key=lambda x: os.path.getmtime(os.path.join(Responses_dir, x)))
        last_file = files[-1]
        with open(os.path.join(Responses_dir, last_file)) as f:
            data = json.load(f)
    except Exception as e:
        print(f"No conversations found", file=sys.stderr)
    return data, last_file


print70w = print_wrapped(70)
# print70w = print

if __name__ == "__main__":
    stdin_pending, _, _ = select.select([sys.stdin], [], [], 0.001)
    if stdin_pending:
        resp_text, resp_raw = main(sys.stdin.read())
        print70w(resp_text)

    parser = argparse.ArgumentParser()

    parser.add_argument('-r', '--save-resp', action='store_true', help='save detailed response')
    parser.add_argument('-g', '--get-last-resp', action='store_true', help='gets last response, '
                                                                           'allows to continue a conversation')
    parser.add_argument('-G', '--get-last-resp-full', action='store_true', help='gets last full response')
    parser.add_argument('-t', '--get-token', action='store_true', help='retrieves token from .token file')
    parser.add_argument('-i', '--interactive', action='store_true', help='interactive mode')
    parser.add_argument('-v', '--verbose', action='store_true', help='print verbose conversation')
    parser.add_argument('query', nargs='*', help='chatgpt question')
    args = parser.parse_args()

    if args.get_token:
        print(get_token())
        sys.exit(0)

    if args.get_last_resp_full:
        data, rest_file = get_last_resp()
        print(f"last response file: {rest_file}")
        print70w(pformat(data))
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

    question = ' '.join(args.query)
    response_file = None
    if args.get_last_resp:
        data, response_file = get_last_resp()
        conversation = ''
        if data:
            for thread in data:
                conversation += f"\nquestion': {thread['question']}\n"
                conversation += f"answer: {thread['response']['choices'][0]['message']['content']}\n"
        conversation = f"In regards to previous conversation: {conversation}\n{question}"
        if args.verbose or not question:
            print70w(conversation)
        if not question:
            sys.exit(0)
        resp_txt, resp_raw = main(conversation)
    else:
        resp_txt, resp_raw = main(question)

    if args.save_resp:
        save_last_resp(question, resp_raw, response_file)

    print()
    print70w(resp_txt)
