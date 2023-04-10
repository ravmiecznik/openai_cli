#!/bin/bash

export OPENAI_API_KEY=$(cat .token | tr -d '\n')

function chatg { 
	query=\""$@\""
	resp=$(openai api chat_completions.create -m gpt-3.5-turbo -g user "$query")
	fold -s -w $((2*$COLUMNS/3)) <<< $resp
	echo
}

export -f chatg
