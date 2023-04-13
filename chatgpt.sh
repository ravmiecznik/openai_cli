#!/bin/bash

artifacts_base_path=$VIRTUAL_ENV
if [ -z $artifacts_base_path ] 
then
	echo Activate virtual env first ! >&2
	return 1
fi

artifacts_base_path=$artifacts_base_path/conversations

mkdir -p $artifacts_base_path
mkdir -p $artifacts_base_path/responses

export artifacts_base_path

echo Convesration artifacts will be saved in: $artifacts_base_path

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
	ls -tr $artifacts_base_path/responses/response_simple* >/dev/null 2>&1
	status=$?
	if [ $status = 0 ]
	then
		last_resp=$(ls -tr $artifacts_base_path/responses/response_simple*| tail -n 1)
		if [[ $arg == "pop" ]]
		then
			rm $last_resp
			return
		fi
		echo "$(cat $last_resp)"
	fi
}

# Not used yet
function find_conversation {
  keyword=$1
  files_matching="$(grep "$keyword" -il $artifacts_base_path/responses/* | xargs -I {} head -c 40 {})"
  echo $files_matching
#  echo "$files_matching"
}



# Record terminal actions
function record {
        mkdir -p $artifacts_base_path/scripts
        export record_file=$artifacts_base_path/scripts/script_$(date +"%Y-%m-%d_%H-%M-%S").scr
        [ -f $record_file ] || script $record_file

}

function show_record {
        cat $record_file
}

export -f record
export -f show_record
export -f chatsh

echo Use \'last_conversation\' to access last recorded conversation.
echo Use \'record\' command to record terminal actions.
echo \'exit\' to stop recording.
echo Access last record by \'show_record\' command.
