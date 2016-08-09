#!/usr/bin/env bash

dir=$(pwd)
source $HOME/.aws_jobs/aws_consts.txt

if [ -e "$dir/run.sh"  ];then
    ssh $AWS_USER@AWS_PUBLIC_DNS 'mkdir =p $HOME/jobs/job_$JOB_NUM'
    chmod u+x run.sh
    scp -r -i $AWS_KEY . $AWS_USER@$AWS_PUBLIC_DNS:~/jobs/job_$JOB_NUM
    JOB_NUM=$((JOB_NUM+1))
    
    echo -e "#If key directory changes or DNS information changes, it can be modified here\nAWS_KEY=$AWS_KEY AWS_USER=$AWS_USER AWS_PUBLIC_DNS=$AWS_PUBLIC_DNS JOB_NUM=$JOB_NUM" > $HOME/.aws_jobs/aws_consts.txt

else
    echo "$dir/run.sh";
    echo "Did not find file"
fi
