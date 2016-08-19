---
layout: post
title: AWS Jobs Environment
---
### _Introduction_
This offers an easy lightweight way to submit "jobs" from your local machine to an Amazon EC2 instance. This is not meant for queuing jobs in a production environment, but rather is a convenient tool for submitting jobs to another instance. Written in Python, this sets up a job queue on the AWS instance and has a simple way of submitting jobs from your local machine.

### _Some simple use cases_
1. If you have ever been on the go or on a low powered laptop and needed to do some cpu intensive job. You can submit these tasks as "jobs" to the EC2 instance and be on your way.
2. Need to run a benchmark or a comparison between pieces of code, but your local machine has a lot of programs or other processing that can interupt the test.
3. Submitting a batch of jobs and check back later.

### _Installation_
	git clone https://github.com/connormurray7/aws-jobs-environment.git
	chmod u+x install.sh push_job.sh
	
Run the install
	
	./install.sh <full path to .pem> <public dns address>
	
If you use bash, 
	
	source ~/.bashrc

If you use another type of shell then you will need to add the following line to your respective .rc 

	alias pushjob=<path to home dir>/.aws_jobs/push_job.sh
	
### _Usage_
For every job that you want to submit, you will need to create a "run.sh" file that contains what you want to run. The `pushjob` command will copy the contents of the directory that you're currently in and push it to the server. It will be placed into the job queue and run sequentially.