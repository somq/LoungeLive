#!/usr/bin/env python2.7

from multiprocessing import Process
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
import time
import logging



#Subprocesses Join
class ProcessParallel(object):
    def __init__(self, *jobs):
        self.jobs = jobs
        self.processes = []

    def fork_processes(self):
        for job in self.jobs:
            proc  = Process(target=job)
            self.processes.append(proc)

    def start_all(self):
        for proc in self.processes:
            proc.start()

    def join_all(self):
        for proc in self.processes:
            proc.join()

#scheduler
mainSchedJobsInterval = 15 #minutes
def schedJobs(funcToRun):
    logging.basicConfig()
    scheduler = BlockingScheduler()
    datenow = datetime.datetime.now()
    print("main scheduler started for jobs @" + str(datenow))

#    rs = scheduler.add_job(subtwo, 'interval', id="MainTaskid", name="maintask", start_date=datetime.datetime.now(), seconds=3, jobstore='default')
    rs = scheduler.add_job(funcToRun, trigger="interval", id="mainSchedJobID", name="mainSchedJob", jobstore='default', executor='default', replace_existing=False, minutes=mainSchedJobsInterval)
    print("Running Tasks")
    scheduler.start()
