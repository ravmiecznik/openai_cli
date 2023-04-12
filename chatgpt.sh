#!/bin/bash


export OPENAI_API_KEY=$(chatgpt --get-token)

function chatsh {
	query=\""$@\""
	resp=$(openai api chat_completions.create -m gpt-3.5-turbo -g user "$query")
	fold -s -w $((2*$COLUMNS/3)) <<< $resp
	echo
}

# Access last conversation, to keep thread use ./chatgpt.py -r some question
function last_conversation {
	arg=$1
	ls -tr responses/response_simple* >/dev/null 2>&1
	status=$?
	if [ $status = 0 ]
	then
		last_resp=$(ls -tr responses/response_simple*| tail -n 1)
		if [[ $arg == "pop" ]]
		then
			rm $last_resp
			return
		fi
		echo "$(cat $last_resp)"
	fi
}

function find_conversation {
  keyword=$1
  files_matching="$(grep "$keyword" -il responses/* | xargs -I {} head -c 40 {})"
  echo $files_matching
#  echo "$files_matching"
}

export -f chatsh
