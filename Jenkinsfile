pipeline {
    agent any

   environment {
     def scanner = tool "sonarQubeScanner";
     SONAR_CRED = credentials('sonarqube-login')
   }

    stages {

        stage('Sonarqube Analysis') {
            steps {
                withSonarQubeEnv("sonarQubeServer") {
                    sh('${scanner}/bin/sonar-scanner \
                              -Dsonar.projectKey=OpenAPI \
                              -Dsonar.login=$SONAR_CRED_USR \
                              -Dsonar.password=$SONAR_CRED_PSW \
                              -Dsonar.sources=./')
                }
            }
        }

        stage('Seed Database') {
            steps {

                withCredentials([string(credentialsId: 'MONGO_CONNECTION_STRING', variable: 'MONGO_CONNECTION_STRING')]) {
                    dir('data_test') {
                        sh "chmod +x ./seed-db.sh"
                        sh "./seed-db.sh"
                    }
                }
            }
        }

        stage('Install python dependencies') {
            steps {
                 sh '''
                  # Crear el entorno virtual
                  python3 -m venv myenv

                  # Activar el entorno virtual
                  . myenv/bin/activate

                  # Instalar dependencias
                  pip install -r requirements.txt
                '''
            }
        }

        stage('Run Test') {
            steps {
                withCredentials([string(credentialsId: 'MONGO_CONNECTION_STRING', variable: 'MONGO_CONNECTION_STRING')]) {
                    script {
                        catchError (buildResult: 'FAILURE', stageResult: 'FAILURE') {
                             sh '''
                                chmod +x ./autotest.sh
                                . myenv/bin/activate
                                ./autotest.sh
                            '''
                        }
                    }
                }
            }
        }

        stage('Report') {
            steps {
                publishHTML(target: [
                    allowMissing: false,
                    alwaysLinkToLastBuild: false,
                    keepAll: false,
                    reportDir: '../reports',
                    reportFiles: 'report.html',
                    reportName: 'API Test Report'
                ])
            }
        }
    }
}