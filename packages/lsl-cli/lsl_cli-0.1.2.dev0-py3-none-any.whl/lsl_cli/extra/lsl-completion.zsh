autoload -U +X compinit && compinit
autoload -U +X bashcompinit && bashcompinit

CURDIR=`cd $(dirname $0); pwd`
source $CURDIR/$(basename $0 .zsh).bash