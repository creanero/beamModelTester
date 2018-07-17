#!/bin/bash

#a script to wrap beamModelTester, dreamBeam and iLiSA together

#Created on Tue Jul 17 17:26:54 2018
#author: creanero

ACC_FOLDER=$1
frequency=$2

#sets a variable for ilisa directory
if [[ -z "${ILISA_DIR}" ]]; then
  ILISA_DIR="${HOME}/iLiSA"
  echo "iLiSA directory enviroment variable not specified.  Defaulting to ${ILISA_DIR}"
fi


#checks the ACC Folder has been specified
#if not, exits
if [[ -z "${ACC_FOLDER}" ]]; then
  echo "ACC file directory variable not specified.  Terminating"
  exit 1

#if it is, runs the acc2bst script on that directory
else
  ${ILISA_DIR}/scripts/acc2bst.py $ACC_FOLDER
fi

#SE607_20180406T090614_rcu3_CygA_dur86147_ct20170403_acc2bst.hdf5

DB_OUT_TYPE="print"
telescope="LOFAR" 
band="LBA" 
stnID="SE607" 
beammodel="Hamaker"
beginUTC="20180406T090614" #need to calculate this
duration="86147" #need to calculate this 
timeStep=519 #should put some checks onto this, but this is a good start  
pointingRA="350.85"
pointingDEC="58.815" 
#frequency=$frequency #no point running this step, but good as an illustration

./dreamBeam/scripts/pointing_jones.py $DB_OUT_TYPE telescope band stnID beammodel beginUTC duration timeStep pointingRA pointingDEC [frequency]
