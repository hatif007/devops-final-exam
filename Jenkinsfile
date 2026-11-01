
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

    - name: trivy
      image: aquasec/trivy:0.76.0
      command:
        - cat
      tty: true

    - name: git
      image: alpine/git:latest
      command:
        - cat
      tty: true

    - name: tools
      image: mikefarah/yq:4
      command:
        - cat
      tty: true

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
                catchError(
                    buildResult: 'SUCCESS',
                    stageResult: 'UNSTABLE',
                    message: 'Trivy found image vulnerabilities'
                ) {
                    container('docker') {
                        sh '''
                            docker run --rm \
                              -v /var/run/docker.sock:/var/run/docker.sock \
                              aquasec/trivy:0.76.1 image \
                              --image-src docker \
                              --scanners vuln \
                              --severity HIGH,CRITICAL \
                              --exit-code 1 \
                              devops-final-exam:$BUILD_NUMBER
                        '''
                    }
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
                            docker tag devops-final-exam:$BUILD_NUMBER \
                              $DOCKER_USERNAME/devops-final-exam:$BUILD_NUMBER

                            printf '%s' "$DOCKER_PASSWORD" | \
                              docker login -u "$DOCKER_USERNAME" --password-stdin

                            docker push $DOCKER_USERNAME/devops-final-exam:$BUILD_NUMBER
                        '''
                    }
                }
            }
        }

        stage('Update GitOps Repository') {
            steps {
                dir('gitops-config') {

                    // 1. Checkout GitOps repository
                    container('git') {
                        git branch: 'main',
                            credentialsId: 'github-gitops',
                            url: 'https://github.com/hatif007/devops-final-exam-gitops.git'

                        sh 'git config --global --add safe.directory "$PWD"'
                        sh 'git status -sb'
                    }

                    // 2. Update DEV image tag only when needed
                    container('tools') {
                        sh 'yq --version'
                        sh '''
                            FILE=environments/dev/values.yaml
                            CURRENT_TAG=$(yq -r '.pods.tag' "$FILE")

                            if [ "$CURRENT_TAG" != "$BUILD_NUMBER" ]; then
                                yq -i '.pods.tag = strenv(BUILD_NUMBER)' "$FILE"
                            else
                                echo "DEV image tag already up to date."
                            fi
                        '''
                    }

                    // 3. Review, commit and push
                    container('git') {
                        echo 'Reviewing GitOps changes...'

                        sh 'git diff -- environments/dev/values.yaml'

                        sh 'git config user.name "hatif007"'
                        sh 'git config user.email "yoav.barel1@gmail.com"'

                        sh 'git add -- environments/dev/values.yaml'
                        sh 'git diff --cached --check'

                        def diffStatus = sh(
                            script: 'git diff --cached --quiet',
                            returnStatus: true
                        )

                        if (diffStatus == 1) {
                            sh 'git commit -m "Update DEV image tag to $BUILD_NUMBER"'

                            withCredentials([
                                gitUsernamePassword(credentialsId: 'github-gitops')
                            ]) {
                                sh 'git push origin main'
                            }

                            echo 'GitOps push completed.'

                        } else if (diffStatus == 0) {
                            echo 'No changes to commit. Skipping push.'

                        } else {
                            error "Git diff failed with exit code ${diffStatus}"
                        }
                    }
                }
            }
        }

        stage('finish') {
            steps {
                echo 'Pipeline completed.'
            }
        }
    }
}
