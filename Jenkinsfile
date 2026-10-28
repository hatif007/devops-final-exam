
pipeline {
    agent {
        kubernetes {
            yaml '''
apiVersion: v1
kind: Pod
spec:
  containers:
    - name: inspector
      image: busybox:1.36
      command:
        - cat
      tty: true
'''
        }
    }

    stages {
        stage('SystemInfo') {
            steps {
                container('inspector') {
                    sh 'hostname'
sh 'uname -a'
sh 'whoami'
sh 'pwd'
                }        
                }    
        }

        stage('Finish') {
            steps {
                echo 'Linux inspection completed successfully'
            }
        }
    }
}
