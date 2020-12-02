#! /bin/bash

sudo apt install python3 python3-pip -y
mkdir -p ~/.local/bin

pip install --user ansible
ansible --version
echo 'PATH=$PATH:~/.local/bin' >> ~/.bashrc
source ~/.bashrc
ansible-playbook -i ansible/Inventory ansible/playbook.yaml

