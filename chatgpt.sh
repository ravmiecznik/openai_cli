#!/bin/bash

export OPENAI_API_KEY=$(cat .token | tr -d '\n')

function chatg { 
	prompt=\""$@\""
	resp=$(openai api chat_completions.create -m gpt-3.5-turbo -g user "$prompt")
	fold -s -w $((2*$COLUMNS/3)) <<< $resp
	echo
}

export -f chatg
