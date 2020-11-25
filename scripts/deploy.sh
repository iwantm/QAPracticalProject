#! /bin/bash
ssh google_iwantm_me@persongen-manager	 << EOF
if [ -d "QAPracticalProject" ]; then
    cd QAPracticalProject
    git pull
else
    git clone https://github.com/iwantm/QAPracticalProject.git
    cd QAPracticalProject/
fi
docker-compose pull
docker stack deploy --compose-file docker-compose.yaml AnimalApp

EOF