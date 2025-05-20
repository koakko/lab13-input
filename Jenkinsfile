properties ([
    parameters ([
        choice( name: 'StagSvr', choices: ['Yes', 'No'], description: 'Deploy container in Staging Server?')
        string( name: 'IMGVer', defaultValue: 'v1', description: 'Add Docker image version')
    ])
])
node('!master') {
    def dhreg = 'docker.io'
    def dhauth = 'dh-credentials'
    def stauth = 'st-ssh'
    def psauth = 'ps-ssh'
    def fimg, bimg
    def stssh = 'ssh -i /${SSH_KEY} /${SSH_USER}@192.168.0.181 << 'EOF''
    def psssh = 'ssh -i /${SSH_KEY} /${SSH_USER}@192.168.0.182 << 'EOF''
    def deploycmd = '''
    docker rmi -f lab13-frontend:${IMGVer} || true
    docker rmi -f lab13-backend:${IMGVer} || true
    docker stop cfend || true
    docker stop cbend || true
    docker rm -f cfend || true
    docker rm -f cbend || true
    docker pull lab13-frontend:${IMGVer}
    docker pull lab13-frontend:${IMGVer}
    docker run -d -p 8181:80 --name cfend lab13-frontend:${IMGVer}
    docker run -d -p 5000:5000 --name cbend lab13-backend:${IMGVer} 
    '''

    try {
        stage('Pull Resource') {
            node('frontend-agent') {
                git checkout scm
            }
        }

        stage('Build Images') {
            node('frontend-agent') {
            fimg = docker.build("lab13-frontend:${IMGVer}")
            bimg = docker.build("lab13-backend:${IMGVer}")
            }
        }    

        stage('Push Image To Registory') {
            node('frontend-agent') {
            docker.withRegistry("https://${dhreg}", dhauth) {
                fimg.push()
                bimg.push()
                }
            }
        }

        stage('Test Image') {
            node('frontend-agent') {
                parallel(
                    'Test Frontend': {
                        sh 'curl -f http://localhost:8181 || exit 1'
                    },
                    'Test Backend': {
                        sh 'curl -f http://localhost:5000 || exit 1'
                    }
                )
            }
        }
        stage('Deploy Container') {
            node('frontend-agent') {
            if (params.StagSvr == 'Yes') {
                withCredentials([sshUserPrivateKey:(credentialsId: st-ssh, keyFileVariable: 'SSH_KEY', usernameVariable: 'SSH_USER')]) {
                    sh '${stssh}'
                    sh '${deploycmd}'
                }
            } else {
                def deployps = input message: "Deploy Container to Production Server?",
    parameters: [choice(name: 'PS', choices: ['Yes', 'No'], description: 'Deploy Frontend and Backend!')]
             if (params.deployps == 'Yes') {
                withCredentials([sshUserPrivateKey:(credentialsId: 'ps-ssh', keyFileVariable: 'SSH_KEY', usernameVariable: 'SSH_USER')]) {
                    sh '${ps-ssh}'
                    sh '${deploycmd}'
                }
             } else {
                echo "There is no Server for deploy container!"   
             }
            }
        }
    }
            } catch (e) {
                echo "Pipeline fail!"
                throw e
            } finally {
                stage('Pipeline Status') {
                    if ( currentBuild.result == 'SUCCESS') {
                        echo "Your pipeline is Successful!"
                    } else {
                        echo "Your pipeline is fail!"
                    }
                }
            }
        }