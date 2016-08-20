#!/usr/bin/env bash
# Created by Connor Murray (connormurray7@gmail.com) on 8/8/2016
#
# Requires two arguments, the full path to the .pem key for the AWS instance
# and the public DNS address for the AWS instance
#
# For each job that you want to run, create a a shell script named "run.sh"
# and then type "pushjob". This will copy all of the contents 
# of the current directory and place them in a folder on the AWS instance.
# The job scheduler will run the script, and save the output in the same folder.

#Read user input
AWS_KEY=$1
AWS_PUBLIC_DNS=$2
AWS_USER="ubuntu"
JOB_NUM=0

#Give the full path to the .pem key file and the AWS public DNS address 
if [ "$#" -ne  "2" ]; then
    echo "Two arguments required, .pem full path and AWS Public DNS address "
    exit 1
fi

# aws_jobs folder stores the pushjob script, and stores the path to the .pem, and the DNS address.
chmod u+x push_job.sh
mkdir $HOME/.aws_jobs
cp push_job.sh $HOME/.aws_jobs/push_job.sh

#Can be changed at anytime and still should work.
echo -e "#If key directory changes or DNS information changes, it can be modified here\nAWS_KEY=$AWS_KEY AWS_USER=$AWS_USER AWS_PUBLIC_DNS=$AWS_PUBLIC_DNS JOB_NUM=$JOB_NUM" > $HOME/.aws_jobs/aws_consts.txt
echo "alias pushjob=$HOME/.aws_jobs/push_job.sh" >> $HOME/.bashrc
source $HOME/.bashrc

scp -r -i $AWS_KEY ./util $AWS_USER@$AWS_PUBLIC_DNS:~/
ssh -i $AWS_KEY $AWS_USER@$AWS_PUBLIC_DNS << EOF
mkdir jobs; 
sudo apt-get -qq update; 
sudo apt-get -qq upgrade;
sudo apt-get -qq install build-essential;
gcc -v;
make -v;
python util/dir_watcher.py start;
EOF

echo "----------------------------------"
echo "Finished installing environment."
echo "Type \"pushjob\" when inside directory containing a run script \"run.sh\" to push the contents of the directory to the box and begin executing the script"
echo "There are logs contained in ~/util/logs "
