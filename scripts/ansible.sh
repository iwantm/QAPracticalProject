#! /bin/bash
mkdir -p ~/.local/bin

pip3 install --user ansible
/home/jenkins/.local/bin/ansible-playbook -i ansible/Inventory ansible/playbook.yaml

