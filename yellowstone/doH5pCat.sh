#!/bin/bash
#
#BSUB -a poe                  # set parallel operating environment
#BSUB -P UJHB0003                 # project code
#BSUB -J h5pC              # job name
#BSUB -W 24:00                 # wall-clock time (hrs:mins)
#BSUB -n 1                    # number of tasks in job
#BSUB -q geyser              # queue
#BSUB -R "span[ptile=1]"
#BSUB -e h5pC.%I.log       # error file name in which %J is replaced by the job ID
#BSUB -o h5pC.%I.log       # output file name in which %J is replaced by the job ID



export ComS="h5pcat.py -eq"
declare -a runs=("p_psInj" "O_psInj" "Hep_psInj" "Hepp_psInj")

export BASE="$HOME/Work/Injection"
export DATA="$BASE/psInj"

echo "Environment ..."
cd $DATA
module restore lfmtp
module list
echo "Running in $PWD"
echo "Running on host `hostname` on `date`"

#Loop through array of runs
for i in "${runs[@]}"
do
	echo "Running $ComS on $i"
	$ComS $i.*.h5part
done
