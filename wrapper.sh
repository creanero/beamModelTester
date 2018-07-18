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

#sets a variable for dreamBeam directory
if [[ -z "${DB_DIR}" ]]; then
	DB_DIR="${HOME}/dreamBeam"
	echo "iLiSA directory enviroment variable not specified.  Defaulting to ${ILISA_DIR}"
fi

#checks the ACC Folder has been specified
#if not, exits
if [[ -z "${ACC_FOLDER}" ]]; then
	echo "ACC file directory variable not specified.  Terminating"
	exit 1


else
	#if it is, runs the acc2bst script on that directory
	${ILISA_DIR}/scripts/acc2bst.py $HOME/$ACC_FOLDER 2> /dev/null


	#then runs the code to generate inputs for dreamBeam

	#TODO: Soft code in the positions
	POS_STNID=1
	POS_DATE=2
	POS_TIME=3
	POS_RCU=4
	POS_DUR=5
	POS_SRC=6

	#for this output, will always want "print"
	DB_OUT_TYPE="print"
	#so far, will always want LOFAR and Hamaker
	telescope="LOFAR" 
	beammodel="Hamaker"
	#ACC operations should always have a cadence of 519 seconds.
	timeStep=519 #should put some checks onto this, but this is a good start  

	#parse the filename using awk
	ACC_FILE=`echo "${ACC_FOLDER}" | awk -F "/" '{print $NF}'`

	#finds the station ID
	stnID=`echo "${ACC_FILE}" | awk -F "_" '{print $1}'`

	#finds the date
	ACC_DATE=`echo "${ACC_FILE}" | awk -F "_" '{print $2}'`
	YEAR="${ACC_DATE:0:4}"
	MONTH="${ACC_DATE:4:2}"
	DAY="${ACC_DATE:6:2}"

	#finds the time
	ACC_TIME=`echo "${ACC_FILE}" | awk -F "_" '{print $3}'`
	HOUR="${ACC_TIME:0:2}"
	MINUTE="${ACC_TIME:2:2}"
	SECOND="${ACC_TIME:4:2}"

	#creates the dreamBeam friendly time
	beginUTC="${YEAR}-${MONTH}-${DAY}T${HOUR}:${MINUTE}:${SECOND}"

	#finds the RCU
	ACC_RCU=`echo "${ACC_FILE}" | awk -F "_" '{print $4}'`
	RCU="${ACC_RCU:3:1}"

	#uses RCU to find the LOFAR band
	if [ "$RCU" == "3" ]; then
		band="LBA" 
	elif [ "$RCU" == "5" ]; then
		band="HBA" 
	elif [ "$RCU" == "7" ]; then
		band="HBA" 
	fi

	#finds the duration of the run
	ACC_DUR=`echo "${ACC_FILE}" | awk -F "_" '{print $5}'`
	duration=`echo "${ACC_DUR}" | sed 's/dur//g'`

	#finds the source
	ACC_SRC=`echo "${ACC_FILE}" | awk -F "_" '{print $6}'`

	#uses a short script to find the source coordinates
	SRC_COORDS=`./source_conv.py $ACC_SRC`

	#could probably use the coordinates directly, but this makes the dreamBeam call clearer
	pointingRA=`echo "${SRC_COORDS}" | awk -F " " '{print $1}'`
	pointingDEC=`echo "${SRC_COORDS}" | awk -F " " '{print $2}'`

	#no need to calculate frequency
	#frequency=$frequency 
	#works out frequency name if needed
	if [[ -z "${frequency}" ]]; then
		echo "Frequency not specified."
		FREQ_NAME=""
	else
		FREQ_NAME="_${frequency}Hz"
	fi

	CSV_FILE="${stnID}_${ACC_DATE}T${ACC_TIME}_${ACC_RCU}_${ACC_SRC}_${ACC_DUR}_${beammodel}_model${FREQ_NAME}.csv"

	#calls the dreamBeam file
	${DB_DIR}/scripts/pointing_jones.py $DB_OUT_TYPE $telescope $band $stnID $beammodel $beginUTC $duration $timeStep $pointingRA $pointingDEC $frequency > $CSV_FILE 2> /dev/null
	echo "created file: ${CSV_FILE}"

fi


