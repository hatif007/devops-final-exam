
pipeline {
    agent  {
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
              
                  
                }    
            }    
        }
    
        stage('Install Dependencies') {
            steps {
                 container('python') {
                sh  'pip install -r requirements.txt pytest'
            }
            }
        }

stage('python qa auto test') {
            steps {
                container('python') {
                sh 'python -m pytest -v'
            }
            }
        }
 stage('Parallel  Checks') {       
parallel {
                stage('Linting') {
                    steps {
                        echo  'Linting'
                    }
                }
                stage('Security Scan') {
                    steps {
                        echo  'Security Scan'
                    }
                }
            }
 }
    
stage('finish') {
            steps {
                echo 'finish'
            }

        }

        
    }

