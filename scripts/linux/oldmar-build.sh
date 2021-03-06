#!/bin/bash
pushd `dirname $0` >/dev/null
OSSIMCI_SCRIPT_DIR=`pwd -P`
pushd $OSSIMCI_SCRIPT_DIR/../../.. >/dev/null
popd > /dev/null
popd >/dev/null

source $OSSIMCI_SCRIPT_DIR/ossim-env.sh

if [ ! -f "$OSSIM_DEV_HOME/joms-$OSSIM_VERSION.jar" ]; then
   echo "ERROR: $OSSIM_DEV_HOME/joms-$OSSIM_VERSION.jar is not found in the install artifact and OMAR can't be built."
   exit 1
fi
# make sure the joms jar is in the local maven repo
mvn install:install-file -Dfile=$OSSIM_DEV_HOME/joms-$OSSIM_VERSION.jar -DgroupId=org.ossim -DartifactId=joms -Dversion=$OSSIM_VERSION -Dpackaging=jar
if [ $? -ne 0 ]; then
 echo; echo "ERROR: MVN install failed for joms."
 exit 1
fi

if [ -d $OSSIM_DEV_HOME/ossim-install ] ; then
   rm -rf $OSSIM_DEV_HOME/ossim-install
fi

mv $OSSIM_INSTALL_PREFIX ossim-install


$OSSIM_DEV_HOME/omar/build_scripts/linux/build.sh
if [ $? -ne 0 ]; then
 echo; echo "ERROR: OMAR failed to build."
 exit 1
fi

