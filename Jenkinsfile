
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

    - name: docker
      image: docker:29-dind
      securityContext:
        privileged: true
      env:
        - name: DOCKER_HOST
          value: unix:///var/run/docker.sock
      volumeMounts:
        - name: docker-storage
          mountPath: /var/lib/docker

  volumes:
    - name: docker-storage
      emptyDir: {}
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
                sh  'pip install -r requirements.txt pytest bandit flake8'
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
                stage('Flake8') {
                    steps {
                        catchError(
            buildResult: 'SUCCESS',
            stageResult: 'UNSTABLE',
            message: 'Flake8 linting issues found'
        ) {
                        container('python') {
                    sh 'python -m flake8 app.py tests'
                    }
        }
                }
                }
                stage('Security Scan') {
                    steps {
                        catchError(
            buildResult: 'SUCCESS',
            stageResult: 'UNSTABLE',
            message: 'Bandit found security findings'
        ) {
                        container('python') {
                        sh 'python -m bandit -r app.py tests'
                    }
                }
                
}
            }
            }
 }
 
stage('Check Docker Engine') {
    steps {
        container('docker') {
            echo 'Waiting for Docker daemon...'
            sleep 5
            sh 'docker version'
        }
    }
}
stage('finish') {
            steps {
                echo 'finish'
            }

        }

        
    }

}