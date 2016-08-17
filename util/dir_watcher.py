"""
Created by Connor Murray (connormurray7@gmail.com)
on 8/8/2016

It uses Daemon.py which was created by Sander Marechal found at
https://web.archive.org/web/20160305151936/http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python
"""

import time
import os
import Queue
import threading
import sys
import subprocess
from daemon import Daemon

class DirectoryWatcher(object):
    """Watches DIRECTORY for any new directories (i.e jobs)

    Assumes that new directories are in the form "job_XXXXX"
    Where XXXXX is a monotonically increasing integer based on job number.

    Attributes:
        DIRECTORY: Static String of the full path to jobs directory
        num_dir: integer of the current number of directories in DIRECTORY
    """

    DIRECTORY = "/home/ubuntu/jobs"
    num_dir = 0

    def __init__(self):
        self.num_dir = len(os.listdir(self.DIRECTORY))

    def changed(self):
        """Checks if new jobs have been added to directory.

        Returns:
            Sorted list of jobs in ascending order (job_0,job_1...)
        """
        dir_list = os.listdir(self.DIRECTORY)
        delta = len(dir_list) - self.num_dir
        if delta > 0:  #New file in directory!
            self.num_dir = len(dir_list)
            return sorted(dir_list)[-delta:] #return newest entries
        return None

class ApplicationRunner:
    """Driver for running the jobs.
    
    When "try_running()" is called, this class checks the queue for 
    jobs to execute and then sychrnously (for now) executes the job.

    Attributes:
        queue: queue of strings for each job.
    """

    def __init__(self):
        self.queue = Queue.Queue()

    def try_running(self):
        """Runs job if queue isn't empty."""
        if self.queue.empty(): 
            return
        directory = DirectoryWatcher.DIRECTORY + "/" + self.queue.get()
        if os.path.isfile(directory + "/run.sh"):
            subprocess.call(["bash", directory + "/run.sh"])
        else:
            sys.stderr.write("no run script here")
        self.queue.task_done()


def driver():
    """The daemonized function that monitors the jobs directory.
    
    Main loop that drivers the program.
    Creates two singletons, DirectoryWatcher and ApplicationRunner.
    """
    dir_watcher = DirectoryWatcher()
    app_runner = ApplicationRunner()
    while True:
        jobs = dir_watcher.changed()
        if jobs is not None:
            for j in jobs:
                app_runner.queue.put(j)

        app_runner.try_running()
        time.sleep(60)

class DirWatcherDaemon(Daemon):
    """ Derives from Daemon, overrides the run method. """ 
    def run(self):
        driver()

if __name__ == "__main__":
    daemon = DirWatcherDaemon('/tmp/dir_watcher.pid',
                              '/home/ubuntu/util/log/dir_watcher_stdin.log',
                              '/home/ubuntu/util/log/dir_watcher_stdout.log',
                              '/home/ubuntu/util/log/dir_watcher_stderr.log')
    if len(sys.argv) == 2:
        if sys.argv[1] == 'start':
            daemon.start()
        elif sys.argv[1] == 'stop':
            daemon.stop()
        elif sys.argv[1] == 'restart':
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
