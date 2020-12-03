#! /bin/bash
sudo apt install python3 python3-pip python3-venv -y
python3 -m venv testing-venv

. testing-venv/bin/activate

pip3 install -r tests/requirements.txt
export API_CODE=tetststs
pytest --cov=service1
pytest --cov=service2
pytest --cov=service3
pytest --cov=service4

deactivate

rm -rf testing-venv