pipeline {
  agent any
  stages {
    stage('Testing') {
      steps {
        sh './scripts/test.sh'
      }
    }

    stage('Build') {
      steps {
        sh './scripts/build-images.sh'
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
  environment {
    API_CODE = 'iw455756477'
  }
}