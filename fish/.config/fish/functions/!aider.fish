function !aider --wraps='aider --no-auto-commits' --description 'alias !aider=aider --no-auto-commits'
    aider --no-auto-commits --chat-mode ask $argv
end
