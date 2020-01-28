#!/bin/bash

usage_exit() {
        echo "Usage: $cmdname -y YAML [-d EXEC_DATE] [-w WORKING_DIR]" 1>&2
        exit 1
}
cmdname=`basename $0`

while getopts y:d:w: OPT
do
  case $OPT in
    y) flg_y=true; yaml=$OPTARG;;
    d) flg_d=true; date=$OPTARG;;
    w) flg_w=true; wdir=$OPTARG;;
    *) usage_exit
  esac
done

shift $((OPTIND - 1))

pycmd="python3 /opt/app/jetline/kicker.py"

if [ ! $flg_y ]; then
  usage_exit
fi

pycmd="${pycmd} -y ${yaml}"

if [ $flg_d ]; then
  pycmd="${pycmd} -d ${date}"
fi

if [ $flg_w ]; then
  pycmd="${pycmd} -w ${wdir}"
fi

# get job definition file
aws s3 cp s3://jetline-job/ /opt/app/jobs/ --recursive

echo "executing ${pycmd}"
eval $pycmd
