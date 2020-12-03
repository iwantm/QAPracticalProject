#! /bin/bash
ssh jenkins@persongen-manager -o StrictHostKeyChecking=no	 << EOF
export API_CODE={env.$API_CODE}
echo $API_CODE
if [ -d "QAPracticalProject" ]; then
    cd QAPracticalProject
    git pull
else
    git clone git@github.com:iwantm/QAPracticalProject.git
    cd QAPracticalProject/
fi
docker-compose pull
docker stack deploy --compose-file docker-compose.yaml PersonGenerator

EOF