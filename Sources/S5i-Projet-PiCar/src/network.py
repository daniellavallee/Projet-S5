import os

def get_ip_address(ifname:str):
    return os.popen('ip addr show '+ ifname +' | grep "\<inet\>" | awk \'{ print $2 }\' | awk -F "/" \'{ print $1 }\'').read().strip()