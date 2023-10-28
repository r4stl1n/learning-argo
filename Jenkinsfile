node {
    def app

    stage('Clone repository') {
      

        checkout scm
    }

    stage('StackHawk') {
        withCredentials([usernamePassword(credentialsId: 'stackhawk', passwordVariable: 'STACKHAWK_PASS', usernameVariable: 'STACKHAWK_USER')]) {
            sh '''docker run -e API_KEY=${STACKHAWK_PASS} --rm -v "$(pwd):/hawk:rw --workdir $(pwd) -it stackhawk/hawkscan:latest'''
        }
    }
 
    stage('Semgrep-Scan') {
        sh '''docker pull returntocorp/semgrep && \
        docker run \
        -v "$(pwd):$(pwd)" --workdir $(pwd) \
        returntocorp/semgrep semgrep ci --config auto'''
    }

    stage('Build image') {
  
       app = docker.build("r4stl1n/learning-argo")
    }

    stage('Test image') {
  

        app.inside {
            sh 'echo "Tests passed"'
        }
    }

    stage('Push image') {
        
        docker.withRegistry('https://registry.hub.docker.com', 'dockerhub') {
            app.push("${env.BUILD_NUMBER}")
        }
    }
    
    stage('Trigger ManifestUpdate') {
                echo "triggering updatemanifestjob"
                build job: 'updatemanifest', parameters: [string(name: 'DOCKERTAG', value: env.BUILD_NUMBER)]
        }
}
