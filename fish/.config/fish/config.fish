#/opt/homebrew/bin/brew shellenv | source
eval "$(/opt/homebrew/bin/brew shellenv)"

zoxide init fish | source
if status is-interactive
    # Commands to run in interactive sessions can go here
end
starship init fish | source

### MANAGED BY RANCHER DESKTOP START (DO NOT EDIT)
set --export --prepend PATH "/Users/csepulveda-gg/.rd/bin"
### MANAGED BY RANCHER DESKTOP END (DO NOT EDIT)
