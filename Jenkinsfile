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
            sh 'echo ' + TELEGRAM_BOT
            sh 'curl https://api.telegram.org/bot'+ TELEGRAM_BOT +'/sendMessage?chat_id=539893428\&text=' + BRANCH_NAME + '%20passed tests'
          }
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