
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

    - name: docker
      image: docker:29-dind
      securityContext:
        privileged: true
      

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
                    sh 'python --version'
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                container('python') {
                    sh 'pip install -r requirements.txt pytest bandit flake8'
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

        stage('Parallel Checks') {
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

        stage('Build Docker Image') {
            steps {
                container('docker') {
                    sh 'docker build -t devops-final-exam:$BUILD_NUMBER .'
                }
            }
        }

        stage('Scan Docker Image') {
            steps {
                container('docker') {
                    sh '''
                        docker run --rm \
                          -v /var/run/docker.sock:/var/run/docker.sock \
                          aquasec/trivy:0.76.1 image \
                          --image-src docker \
                          --scanners vuln \
                          --severity HIGH,CRITICAL \
                          --exit-code 0 \
                          devops-final-exam:$BUILD_NUMBER
                    '''
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                container('docker') {
                    withCredentials([usernamePassword(
                        credentialsId: 'Docker_hub',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )]) {
                        sh '''
                            docker tag devops-final-exam:$BUILD_NUMBER $DOCKER_USERNAME/devops-final-exam:$BUILD_NUMBER

                            printf '%s' "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin

                            docker push $DOCKER_USERNAME/devops-final-exam:$BUILD_NUMBER
                        '''
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
}
