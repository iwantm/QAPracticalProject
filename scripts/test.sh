#! /bin/bash
sudo apt install python3 python3-pip python3-venv -y
python3 -m venv testing-venv

. testing-venv/bin/activate

pip3 install -r tests/requirements.txt
export API_CODE=tetststs
pytest --suppress-no-test-exit-code




deactivate

rm -rf testing-venv