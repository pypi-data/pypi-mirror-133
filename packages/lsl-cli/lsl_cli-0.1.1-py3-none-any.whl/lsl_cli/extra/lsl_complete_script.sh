#!/usr/bin/env bash

DIR=$(python3 -c "import lsl_cli;print(lsl_cli.__path__[0])")
COMP_FILE="$DIR/extra/lsl-completion"

case $# in 
	0) SH_NAME="$(basename "$SHELL")" ;; 
	1) SH_NAME="$1" ;;
esac

case $SH_NAME in
	bash)
		SHELL_RC="$HOME/.bashrc"
		COMP_FILE="$COMP_FILE.bash"
		;;
	zsh)
		SHELL_RC="$HOME/.zshrc"
		COMP_FILE="$COMP_FILE.zsh"
		;;
	*)	
         echo "Error: Invalid shell name '$SH_NAME'"
         exit
         ;;
esac

echo ""
echo "# >>> lsl_cli autocompletion >>>"
echo "source $COMP_FILE"
echo "# <<< lsl_cli autocompletion <<<"