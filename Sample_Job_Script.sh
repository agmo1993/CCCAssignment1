#!/bin/bash
#SBATCH --partition=cloud
#SBATCH --time=00:04:00
#SBATCH --nodes=1
#SBATCH --ntasks=3
#SBATCH --cpus-per-task=1
module load Python/3.4.3-goolf-2015a
#module load Java/1.8.0_71
#module load mpj/0.44
srun -n 3 tweetParser_v2.py


