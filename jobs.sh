#!/bin/sh

#set things up
curr_dir=$PWD
cd /home/msilva/gen-2-triggers/

#initialize the different variables
d_type=$1
d_time=$2
npes=$3
e_time=$4
ndom=$5

#actually run the script
eval `/cvmfs/icecube.opensciencegrid.org/py2-v3.1.0/setup.sh`
bash /data/user/msilva/metaprojects/combo/build/env-shell.sh <<EOF
python extract_triggers_with_cuts.py -dom_type ${d_type} -dom_time ${d_time} -pe_cut ${npes} -event_time ${e_time} -ndom_cut ${ndom} 
EOF
