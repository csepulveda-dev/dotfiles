function !post --wraps='hugo new content content/posts/' --description 'alias !post=hugo new content content/posts/'
    hugo new content content/posts/ $argv
end
