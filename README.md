### OPENAI Command line


## setup
```bash
python3 -m venv OPENAI
python -m pip install openai
pip install openai --upgrade
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