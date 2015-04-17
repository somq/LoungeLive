#!flask/bin/python

import os
import sys
from tools import *
from redditJob import *
from hltvJob import *

def launchJobs():
    print ' ***** jobs started ***** '
    # proc all the jobs in parallel eg. ProcessParallel(redditJob, hltvJob)
    procs =  ProcessParallel(redditJob, hltvJob)
    procs.fork_processes()
    procs.start_all()
    #wait until all the process got executed
    procs.join_all()
    #finished: continue.
    print ' ***** jobs done ***** '  

if __name__ == '__main__':
    schedJobs(launchJobs)
    launchJobs()
