function !tsh --wraps='tsh login --proxy=glossgenius.teleport.sh:443 glossgenius.teleport.sh --auth okta' --description 'alias !tsh=tsh login --proxy=glossgenius.teleport.sh:443 glossgenius.teleport.sh --auth okta'
    tsh login --proxy=glossgenius.teleport.sh:443 glossgenius.teleport.sh --auth okta $argv
end
