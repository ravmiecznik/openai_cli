### OPENAI Command line


## setup

1. Access https://platform.openai.com/account/api-keys to create a token
2. Store token in `.token` file.
3. Configure python venv and install openai Python API and command line tools.
```bash
python3 -m venv OPENAI
source OPENAI/bin/activate
python -m pip install openai
pip install openai --upgrade
```

>Having CLI for openai makes some things easier as you can simply provide some commands output to Chat.<br>
>It is also quite simple to pass a file to a query:
> 
> ```chatg review this script: "$(cat chatgpt.sh)"```
> 
> Use quotation marks in bash shell to keep file formating.
```
~/openai$ chatg fix this sentence: my english bad is very very
My English is very, very bad.
```


## usage (self explained)

```bash
~/openai$ source chatgpt.sh

~/openai$ chatg what is this code: "$(cat chatgpt.sh)"
This code is a bash shell script that defines a chatbot function called "chatg" which uses the OpenAI GPT-3 API to generate responses 
to user input. The script also exports the API key from a file named ".token" and defines the function to be used globally (-f 
option). The prompt for the chatbot function is passed as an argument to the function. The script is executed by the bash shell at the 
beginning of the file (#!"usr/bin/bash").

```

```bash

~/openai$ chatg what is this code: "$(cat chatgpt.py)"

This is a Python script that uses OpenAI's Chat API to generate responses to user questions. It takes a single command line argument 
as the input question and creates a text file with the response and timestamped name. The script loads the API key from a hidden file 
named `.token`. The `main()` function creates a chat message with the input question and sends it to the GPT-3.5-Turbo model to 
generate a response. The response is saved in a text file along with the original question and API response.

```

```commandline
~/openai$ chatg find problems in "$(cat chatgpt.py)"
1. API key is not securely loaded:
The API key is currently loaded from a file named '.token', which could be compromised if someone gains access to the file system. It 
would be better to load the key from an environment variable or secret management service.

2. No error handling for file access:
The program opens and reads from the '.token' file without any error handling, which could result in a crash if the file does not 
exist or cannot be read.

3. No input validation:
The 'question' variable is used as is, without validation or sanitization, which could allow for malicious input to affect the 
behavior of the program.

4. Hard-coded model name:
The model name is currently hard-coded as "gpt-3.5-turbo", which could become outdated or less effective over time. It would be better 
to load the model name from a configuration file or environment variable.

5. No return value:
The 'main' function does not return any value, which may limit the flexibility of the program to be used as a module in other 
applications.

6. No unit tests:
The code lacks unit tests, making it hard to ensure that it works as intended and to detect errors or regressions.

```