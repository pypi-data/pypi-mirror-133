_lsl_completion()
{
    local cur prev
	
	cur=${COMP_WORDS[COMP_CWORD]}
	prev=${COMP_WORDS[COMP_CWORD-1]}

	if [[ ! -n $(command -v lsl) ]]; then
		return 0 
	fi 

	local COMMANDS=(
		"list"
		"echo"
		"show"
		"find"
		"complete"
		"stub"
		"rate"
		"delay"
		"xdf"
	)

	local command i
    for (( i=0; i < $COMP_CWORD; i++ )); do
        if [[ ${COMMANDS[@]} =~ ${COMP_WORDS[i]} ]]; then
            command=${COMP_WORDS[i]}
            break
        fi
    done

    local subcommand j SUBCOMMANDS
    if [[ "$command" == "xdf" ]]; then
		SUBCOMMANDS=(
    		"rate"
    		"info"
    		"play"
    	)
    	for (( j=$i+1; j < $COMP_CWORD; j++ )); do
    		if [[ ${COMMANDS[@]} =~ ${COMP_WORDS[i]} ]]; then
    			subcommand=${COMP_WORDS[j]}
    			break
    		fi
    	done
    fi

    if [[ "$cur" == -* ]]; then
    	case $command in
			list) 
				COMPREPLY=($(compgen -W '--all
				 	--list --timeout
				 	--name --type 
				 	--source_id --channel_count 
				 	--channel_format --nominal_srate 
				 	--hostname --uid 
				 	--version --session_id 
				 	--created_at' -- ${cur}))
				return 0
				;;
			echo) 
				COMPREPLY=($(compgen -W "--timeout" -- ${cur}))
				return 0
				;;
			show) 
				COMPREPLY=($(compgen -W "--timeout" -- ${cur}))
				return 0
				;;
			find) 
				COMPREPLY=($(compgen -W '
				 	--name --type 
				 	--source_id --channel_count 
				 	--channel_format --nominal_srate 
				 	--hostname --uid 
				 	--version --session_id 
				 	--created_at' -- ${cur}))
				return 0
				;;
			complete)
				COMPREPLY=($(compgen -W '
					--bash --zsh' -- ${cur} ))
				;;
			stub)
				COMPREPLY=($(compgen -W '
					--channel_count --nominal_srate 
					--chunk_size' -- ${cur}))
				;;
			rate) 
				COMPREPLY=($(compgen -W '
					--count --timeout' -- ${cur}))
				;;
			delay) 
				COMPREPLY=($(compgen -W '
					--count --timeout' -- ${cur}))
				;;
		esac
    fi

    if [[ -n $command ]]; then
    	case $command in 
    		echo|show|rate|delay)
				COMPREPLY=( $( compgen -W "$( lsl list | xargs echo )" -- ${cur} ) )
				;;
			xdf)
				if [[ -n $subcommand ]]; then
					COMPREPLY=($(compgen -f -X '!*.xdf' -- ${cur}; compgen -o nospace -d -S / -- ${cur} ))
				else
					COMPREPLY=( $( compgen -W "$(echo ${SUBCOMMANDS[@]})" -- ${cur} ) )
				fi
				;;
		esac
	fi

	if [[ "$command" == "" ]]; then
		COMPREPLY=( $( compgen -W "$(echo ${COMMANDS[@]})" -- ${cur} ) )
	fi

	return 0
} &&


complete -F _lsl_completion lsl