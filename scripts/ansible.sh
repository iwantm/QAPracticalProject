#! /bin/bash

sudo apt install python3 python3-pip -y
pip install --user ansible
source ~/.bashrc

ansible-playbook -i ansible/Inventory ansible/playbook.yaml

