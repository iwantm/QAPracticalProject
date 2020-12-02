#! /bin/bash

sudo apt install python3 python3-pip -y
mkdir -p ~/.local/bin
echo 'PATH=$PATH:~/.local/bin' >> ~/.bashrc
source ~/.bashrc
pip install --user ansible
ansible --version

ansible-playbook -i ansible/Inventory ansible/playbook.yaml

