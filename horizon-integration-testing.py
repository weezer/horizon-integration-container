__author__ = 'weez8031'

#!/usr/bin/python

import subprocess
import os
import errno
import yaml


def create_horizon_testing_container():
    CMD = ["lxc-create -t download -n test-container -- --dist ubuntu --release trusty --arch amd64",
           "lxc-start -n test-container -d",
           ]
    for command in CMD:
        subprocess.call(command, shell=True)


def add_testing_container_ip_into_hosts():

    testing_container_ip = subprocess.check_output("lxc-ls -n test-container -iH")
    append_info = "[horizon_testing_container]\n" + testing_container_ip
    filename = "/etc/ansible/hosts"
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    with open(filename, 'a') as f:
        f.write(append_info)


def get_horizon_container_ip(path):
    with open(path, 'r') as f:
        ip_yaml = yaml.load(f)
        for name in ip_yaml.keys():
            if 'horizon' in name:
                horizon_ip = ip_yaml['name']['container_address']
                break

    return horizon_ip

def main():
    pass

if __name__ == "__main__":
    main()
