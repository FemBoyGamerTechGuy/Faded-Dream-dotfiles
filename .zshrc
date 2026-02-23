# =============================================================================
# Faded Dream - ZSH Configuration
# =============================================================================

# -----------------------------------------------------------------------------
# History
# -----------------------------------------------------------------------------
HISTFILE=~/.zsh-history
HISTSIZE=99999
SAVEHIST=99999

setopt HIST_IGNORE_DUPS      # don't record duplicate commands
setopt HIST_IGNORE_SPACE     # don't record commands starting with a space
setopt HIST_VERIFY           # show history expansion before running
setopt SHARE_HISTORY         # share history across all zsh sessions

# -----------------------------------------------------------------------------
# Completion
# -----------------------------------------------------------------------------
zstyle :compinstall filename "$HOME/.zshrc"
autoload -Uz compinit
compinit

zstyle ':completion:*' menu select          # arrow key menu for completion
zstyle ':completion:*' matcher-list 'm:{a-z}={A-Z}'  # case insensitive completion

# -----------------------------------------------------------------------------
# Options
# -----------------------------------------------------------------------------
unsetopt beep                # no beep on error
setopt AUTO_CD               # type a directory name to cd into it
setopt CORRECT               # suggest corrections for mistyped commands

# -----------------------------------------------------------------------------
# Keybindings
# -----------------------------------------------------------------------------
bindkey '^[[A' history-search-backward   # up arrow searches history
bindkey '^[[B' history-search-forward    # down arrow searches history

# -----------------------------------------------------------------------------
# Oh My Posh
# -----------------------------------------------------------------------------
eval "$($HOME/.zsh/posh-linux-amd64 init zsh --config $HOME/.zsh/themes/if_tea.omp.json)"

# -----------------------------------------------------------------------------
# Plugins
# -----------------------------------------------------------------------------
source "$HOME/.zsh/zsh-autosuggestions/zsh-autosuggestions.zsh"
source "$HOME/.zsh/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh"

# -----------------------------------------------------------------------------
# Aliases
# -----------------------------------------------------------------------------
alias ls='ls --color=auto'
alias ll='ls -lah --color=auto'
alias la='ls -A --color=auto'
alias grep='grep --color=auto'
alias cls='clear'
alias update='sudo pacman -Syu --noconfirm'
alias paru='paru --noconfirm'
alias vim='nvim'
alias cat='bat --style=plain' # requires bat package
