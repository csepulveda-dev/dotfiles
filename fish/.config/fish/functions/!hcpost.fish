function !hcpost --wraps='hugo new content content/posts/' --description 'alias !hcpost=hugo new content content/posts/'
    hugo new content content/posts/ $argv
end
