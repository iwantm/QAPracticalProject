pipeline {
  agent any
  stages {
    stage('Testing') {
      steps {
        sh './scripts/test.sh'
      }
      post{
        success {
            curl 'https://api.telegram.org/bot'+ credentials('telegram_bot')'/sendMessage?chat_id=539893428&text=idk'
        }
        failure {
          telegramSend env.BRANCH_NAME + ' failed tests'
        }
      }
    }

    stage('Build') {
      when {
        branch 'main'  
            }
      steps {
        sh './scripts/build-images.sh'
      }
    }

    stage('Setup'){
      when{
        branch "main"
      }
      steps{
        sh './scripts/ansible.sh'
      }
    }

    stage('Deploy App') {
      when {
        branch 'main'  
            }
      steps {
        sh './scripts/deploy.sh'
      }
    }

  }
  
}