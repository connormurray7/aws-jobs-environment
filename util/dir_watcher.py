import time
import os
import Queue
import threading
import subprocess
import sys
from daemon import Daemon

class DirectoryWatcher:
    DIRECTORY = "/home/ubuntu/jobs"
    num_dir = 0

    def changed(self):
        dir_list = os.listdir(self.DIRECTORY)
        delta = len(dir_list) - self.num_dir
        if(delta > 0):  #New file in directory!
            self.num_dir = len(dir_list)
            return (True,sorted(dir_list)[-delta:]) #return newest entries
        return (False,)

    def __init__(self):
        self.num_dir = len(os.listdir(self.DIRECTORY))

class ApplicationRunner: 

    def __init__(self):
        self.q = Queue.Queue()
        self.t = threading.Thread(target=self.worker)

    def worker(self):
        directory = DirectoryWatcher.DIRECTORY + "/" + self.q.get()
        sys.stdout.write("Running this job: " + directory)
        if(os.path.isfile(directory + "/run.sh")):
            subprocess.call(directory + "/run.sh")
        else:
            sys.stderr.write("no run script here")
        self.q.task_done()

    def try_running(self):
        if(not(self.q.empty()) and not(self.t.is_alive())):
            sys.stdout.write("running job")
            self.t = threading.Thread(target=self.worker)
            self.t.start()


def monitor_dir():
    dir_watcher = DirectoryWatcher()
    app_runner = ApplicationRunner()
    while True:
        tup = dir_watcher.changed()
        if(tup[0]):
            #sys.stdout.write(tup[1])
            for d in tup[1]:
                app_runner.q.put(d)

        app_runner.try_running()
        time.sleep(60)

class DirWatcherDaemon(Daemon):
	def run(self):
        	monitor_dir()

if __name__ == "__main__":
    #logging.basicConfig(filename='./log/dir_watcher.log',level=logging.DEBUG)
    daemon = DirWatcherDaemon('/tmp/dir_watcher.pid','/home/ubuntu/util/log/dir_watcher_stdin.log','home/ubuntu/util/log/dir_watcher_stdout.log','/home/ubuntu/util/log/dir_watcher_stderr.log')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
