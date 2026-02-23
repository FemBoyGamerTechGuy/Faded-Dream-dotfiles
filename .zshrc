# Lines configured by zsh-newuser-install
HISTFILE=~/.zsh-history
HISTSIZE=99999
SAVEHIST=99999
unsetopt beep
# End of lines configured by zsh-newuser-install
# The following lines were added by compinstall
zstyle :compinstall filename '/home/FemBoyGamerTechGuy/.zshrc'

autoload -Uz compinit
compinit
# End of lines added by compinstall
eval "$($HOME/.zsh/posh-linux-amd64 init zsh --config $HOME/.zsh/themes/if_tea.omp.json)"
source $HOME/.zsh/zsh-autosuggestions/zsh-autosuggestions.zsh
source $HOME/.zsh/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
