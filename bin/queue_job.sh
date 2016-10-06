#PBS -S /bin/bash
#PBS -q batch
#PBS -N MSMA_runs
#PBS -l nodes=1:ppn=4:AMD
#PBS -l walltime=48:00:00
#PBS -l mem=20gb
#PBS -M sukrit@uga.edu 
#PBS -m ae


module load java/jdk1.8.0_20

module load octave/4.0.3


cd $PBS_O_WORKDIR
touch "filename"
 
# CALLS PERMUTE_RUNS.SH SCRIPT 
./permute_runs.sh