pipeline {
  agent any
  stages {
    stage('Testing') {
      steps {
        sh './scripts/test.sh'
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