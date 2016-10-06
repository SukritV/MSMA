#PBS -S /bin/bash
#PBS -q batch
#PBS -N MSMA_permute_runs
#PBS -l nodes=1:ppn=4:AMD
#PBS -l walltime=48:00:00
#PBS -l mem=20gb
#PBS -M sukrit@uga.edu 
#PBS -m ae


# CALLS PERMUTE_RUNS.SH SCRIPT 
./permute_runs.sh