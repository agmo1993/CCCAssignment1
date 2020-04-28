# HPC Twitter Processing 

Social media has become an integral part of today’s society, it acts as a medium through which people express their feelings and emotions on any matter publicly. In this project, we have implemented a simple, parallelized application that finds the top 10 most frequently used hashtags and the languages used for tweeting for the twitter dataset of Sydney. This task was executed at the University of Melbourne HPC facility SPARTAN.   

# Message Passing Interface

The Architecture developed is a multiple instruction, single data stream (MISD) program according to Flynn’s Taxonomy. The overall task is broken down into subtasks and assigned to different functional units. The first unit has the responsibility of reading the Twitter JSON file line by line and sends the data that it has read to the second and third units. The second and third unit has the role of string processing on the data that has been read and sent by the first unit.  
 
The second unit parses the data and uses a regular expression to extract tweets from the line of data. It then sends the extracted tweets to the fourth unit. The third unit extracts the language of the tweet and sends it to the fourth unit. The fourth unit is an output data storage, with hashmaps (Python dictionaries) used to store tweets and count the number of times they appeared as well as the languages used for the tweets. It then sorts the hashmaps and outputs the top 10 most frequent tweets and languages used respectively.  
 
Blocking point-to-point communication was used as the method to send and receive data between the units. Therefore, the sending process blocks until the receiving process has correctly received the correct information

# Invocation

Each condition was programmed using Bash Scripts, according to the appropriate Slurm commands. 

### Condition 1 - One node one core

The filename for this script is myjob1.slurm

```sh
#!/bin/bash #SBATCH --partition=cloud 
#SBATCH --time=00:20:00 
#SBATCH --nodes=1 
#SBATCH --ntasks=1 
module load Python/3.4.3-goolf-2015a 
#module load Java/1.8.0_71 
#module load mpj/0.44 
time srun -n 1 python tweetParser_v2.py
```

### Condition 2 - One node eight cores

The filename for this script is myjob2.slurm

```sh
#!/bin/bash 
#SBATCH --partition=cloud 
#SBATCH --time=00:20:00 
#SBATCH --nodes=1 
#SBATCH --ntasks=8
module load Python/3.4.3-goolf-2015a 
#module load Java/1.8.0_71 
#module load mpj/0.44 
time srun -n 8 python tweetParser_v2.py
```

### Condition 3 - Two nodes eight cores

The filename for this script is myjob3.slurm

```sh
#!/bin/bash 
#SBATCH --partition=cloud 
#SBATCH --time=00:20:00 
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=4
module load Python/3.4.3-goolf-2015a 
#module load Java/1.8.0_71 
#module load mpj/0.44 
time srun -n 8 python tweetParser_v2.py
```
