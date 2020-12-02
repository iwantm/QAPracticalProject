#! /bin/bash

source ~/.bashrc
pip3 install --user ansible
ansible-playbook -i ansible/Inventory ansible/playbook.yaml

