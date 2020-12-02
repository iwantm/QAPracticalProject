pipeline {
  agent any
  environment {
        TELEGRAM_BOT = credentials('telegram_bot')
  }
  stages {
    stage('Testing') {
      steps {
        sh './scripts/test.sh'
      }
      post{
        success {
          script{
            sh 'curl https://api.telegram.org/bot'+ TELEGRAM_BOT +'/sendMessage?chat_id=539893428\\&text=' + BRANCH_NAME + '%20passed%20tests'
          }
        }
        failure {
          sh 'curl https://api.telegram.org/bot'+ TELEGRAM_BOT +'/sendMessage?chat_id=539893428\\&text=' + BRANCH_NAME + '%20failed%20tests'
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
      post{
        failure {
          sh 'curl https://api.telegram.org/bot'+ TELEGRAM_BOT +'/sendMessage?chat_id=539893428\\&text=' + BRANCH_NAME + '%20failed%20build'
        }
      }
    }

    stage('Setup'){
      when{
        branch "main"
      }
      steps{
        sh './scripts/ansible.sh'
      }
      post{
        failure {
          sh 'curl https://api.telegram.org/bot'+ TELEGRAM_BOT +'/sendMessage?chat_id=539893428\\&text=' + BRANCH_NAME + '%20failed%20ansible%20 config'
        }
      }
    }

    stage('Deploy App') {
      when {
        branch 'main'  
            }
      steps {
        sh './scripts/deploy.sh'
      }
      post{
        success {
          script{
            sh 'curl https://api.telegram.org/bot'+ TELEGRAM_BOT +'/sendMessage?chat_id=539893428\\&text=' + BRANCH_NAME + 'successfully%20deployed'
          }
        }
        failure {
          sh 'curl https://api.telegram.org/bot'+ TELEGRAM_BOT +'/sendMessage?chat_id=539893428\\&text=' + BRANCH_NAME + 'failed%20to%20deploy'
        }
      }
    }

  }
  
}