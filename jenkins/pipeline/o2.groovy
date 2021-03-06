def notifyObj
node {
   env.WORKSPACE=pwd()
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
     stage("Download Artifacts"){
         dir("${env.WORKSPACE}"){
             step ([$class: 'CopyArtifact',
                projectName: "ossim-${OSSIM_GIT_BRANCH}",
                filter: "artifacts/*.jar",
                flatten: true])
         }
     }
     stage("Build"){
         sh """
           ${env.WORKSPACE}/ossim-ci/scripts/linux/o2-build.sh
           ${env.WORKSPACE}/ossim-ci/scripts/linux/o2-install.sh
         """
     }
     
     stage("Archive"){
       dir("${env.WORKSPACE}"){
           sh "tar cvfz install.tgz install"
       }
       dir("${env.WORKSPACE}/artifacts"){
           sh "mv ${env.WORKSPACE}/install.tgz ."
       }
       archiveArtifacts 'artifacts/*'
    }

    stage("Clean Workspace"){
      step([$class: 'WsCleanup'])
    }

   }
    catch(e)
    {
      currentBuild.result = "FAILED"
      notifyObj?.notifyFailed()
    }
}