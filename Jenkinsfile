
pipeline {
    agent {
        kubernetes {
            yaml '''
apiVersion: v1
kind: Pod
spec:
  containers:
    - name: python
      image: python:3.13-slim
      command:
        - cat
      tty: true
'''
        }
    }

    stages {
        stage('python') {
            steps {
                container('python') {
                 sh   'python --version'
                   sh 'python -m pip --version'
                }        
                }    
        }

        stage('Finish') {
            steps {
                echo 'MY APP IS WORKING   completed successfully'
            }
        }
    }
}
