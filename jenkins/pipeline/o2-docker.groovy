def notifyObj
node("o2.radiantbluecloud.com"){
   env.WORKSPACE=pwd()
   env.DOCKER_HOST_URL="${DOCKER_HOST_URL}"
   try{

     stage("Checkout"){
         dir("omar"){
            git branch: "${OSSIM_GIT_BRANCH}", url: 'https://github.com/ossimlabs/omar.git'
         }
         dir("ossim-ci"){
            git branch: "${OSSIM_GIT_BRANCH}", url: 'https://github.com/ossimlabs/ossim-ci.git'
         }
        notifyObj = load "${env.WORKSPACE}/ossim-ci/jenkins/pipeline/notify.groovy"
    }
     stage("Confiure Docker"){
         //dir("${env.WORKSPACE}/omar/build_scripts/docker"){
             sh """
             ${env.WORKSPACE}/ossim-ci/scripts/linux/o2-docker.sh
             """
         //}
     }
   }
   catch(e)
   {
      println e
      currentBuild.result = "FAILED"
      notifyObj?.notifyFailed()
   }

   stage("Clean Workspace"){
     step([$class: 'WsCleanup'])
  }
}