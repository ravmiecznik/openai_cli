### OPENAI Command Line Interface
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

## setup

1. Access https://platform.openai.com/account/api-keys to create a token
2. Store token in `.token` file.
3. Configure python venv and install openai Python API and command line tools.

```bash
env=OPENAI
python3 -m venv $env
ln -sf $PWD/chatgpt.py $PWD/$env/bin/chatgpt
ln -sf $PWD/.token $PWD/$env/bin/.token
source $env/bin/activate
python -m pip install openai
pip install openai --upgrade
```

>`chatgpt` calls python script via link<br>
>`chatg` calls shell script, must be sourced first

## usage (self explained)

```commandline
~/openai$ chatgpt --help
usage: chatgpt [-h] [-r] [-t] [query [query ...]]

positional arguments:
  query            chatgpt question

optional arguments:
  -h, --help       show this help message and exit
  -r, --save-resp  save detailed response
  -t, --get-token  retrieves token from .token file

```

```commandline
~/openai$ source chatgpt.sh

~/openai$ chatg what is this code: "$(cat chatgpt.sh)"
This code is a bash shell script that defines a chatbot function called "chatg" which uses the OpenAI GPT-3 API to generate responses 
to user input. The script also exports the API key from a file named ".token" and defines the function to be used globally (-f 
option). The prompt for the chatbot function is passed as an argument to the function. The script is executed by the bash shell at the 
beginning of the file (#!"usr/bin/bash").

```

```commandline

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

```commandline
~/openai$ chatg explain output: "$(python -c "print(4/0)" 2>&1)"
This is a Python error message that occurs when the code is trying to perform a division operation with a divisor of zero. In this 
case, the error message is indicating that there is a ZeroDivisionError on line 1 of the code. The traceback is presenting the error 
message from the most recent call in the program, which in this case is line 1. 

In simpler terms, the code tried to divide a number by 0, which is impossible, and this error message is informing us that this 
operation caused an issue in the code that we need to fix.

```

```commandline
~/openai$ chatg check this error "$(./chatgpt.py -r 2>&1)" from script "$(cat chatgpt.py)"
The error is in the line:


parser.add_argument('-r', '--save-resp', action='store true', 
help='save detailed response')


The correct value for the `action` argument should be 
`'store_true'` (with an underscore), not `'store true'`. Change it 
to:

parser.add_argument('-r', '--save-resp', action='store_true', 
help='save detailed response')


```

## The current version of the API does not support referencing a thread, but it will be added in a future update.
## Solution is to store responses with '-r' option and access it with a bash function 'last_conversation'

```commandline
~/openai$ ./chatgpt.py -r  shortly explain what is discus fish

Discus fish is a type of freshwater fish that is native to the Amazon River basin in South America. They are known for their circular and flat shaped body and vibrant coloration, which can vary from yellow, blue, green, and red. Discus fish require a specific water condition, temperature, and diet to thrive, and they are often kept in aquariums as pets for their beauty and unique behaviors. They are a popular choice among experienced fish keepers due to their challenging care requirements.

~/openai$ ./chatgpt.py -r elaborate more on $(last_conversation)

Discus fish are also known for their social behavior and will often form groups in the wild. They communicate with each other through a series of grunts and whistles and are capable of recognizing individual members of their species. Discus fish are also territorial and can become aggressive if they feel their space is being invaded. In the wild, they primarily feed on small invertebrates and are known for their ability to sift through sand and gravel to find food. In aquariums, they can be fed a variety of foods including flakes, pellets, and frozen or live foods. Due to their sensitive nature, it is important for owners to keep their tanks clean and maintain a stable environment. Overall, discus fish are prized for their unique beauty, social behavior, and challenging care requirements.

```