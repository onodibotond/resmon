#This fil is used for resource monitoring on Linux environments

import psutil
import config
import time
import logging
import tarfile
import os
import sys

logging.basicConfig(filename='/var/log/resmon.log', format='%(asctime)s %(levelname)s %(message)s', filemode='w', level=logging.INFO)

#This function is used for archiving the PID's folders
def make_tarfile(output_filename, source_dir):
    try:
        if os.path.isfile(output_filename):
            logging.info("Archive {0} already exists.".format(output_filename))
        else:
            logging.info("Creating archive {0}".format(output_filename))
            with tarfile.open(output_filename, "w:gz") as tar:
                tar.add(source_dir, arcname=os.path.basename(source_dir))
    except Exception:
        logging.exception("Can't archive folder!")

#This function is used to gather the memory usage in percent
def get_ram_percent():
    try:
        p = psutil.virtual_memory().percent
        logging.debug("Ram usage: {0}".format(p))
        return p
    except Exception:
        logging.exception('get_ram_percent(): Failed to get memory usage in percentage.')

#This function is used to get the list of processes ordered by ram usage
def get_procs_by_usage():
    procs = []
    try:
        for proc in psutil.process_iter():
            p = proc.as_dict(attrs=['pid', 'name', 'username', 'memory_percent'])
            procs.append(p)
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        logging.exception("get_procs_by_usage(): Failed to get processes")
        
    procs = sorted(procs, key=lambda procObj: procObj['memory_percent'], reverse=True)
    return procs

#This function is used to clean older archives the the specified days number
def clean_old_files(days = config.DAYS_TO_KEEP, seconds = config.SECONDS_PER_DAY, path = "/opt/resmon/archives/"):
    now = time.time()
    for f in os.listdir(path):
        try:
            if os.stat(os.path.join(path, f)).st_mtime < now - days * seconds:
                if os.path.isfile(os.path.join(path, f)):
                    logging.info("Removing file: {0} since it is older then {1}".format(os.path.join(path, f), days))
                    os.remove(os.path.join(path, f))
        except (FileNotFoundError, IOError):
            print("Wrong file {0} or file path {1}".format(f, path))

#This is the main function which 
#loops over and monitors the memory usage
def run():
    OCCURENCE = 0
    ALREADY_OCCURED = 0
    while True:
        try:
            if (get_ram_percent() >= config.MAX_MEMORY):
                #in case the memory is heigher for more then 15 seconds we want to increase the log time 
                #to not spam it with the same data
                max_occurence = config.MAX_OCCURENCE * 4 if ALREADY_OCCURED > 0 else config.MAX_OCCURENCE
                if (OCCURENCE >= max_occurence):
                    for p in get_procs_by_usage():
                        if p['memory_percent'] > config.MIN_MEMORY:
                            command = ' '.join(psutil.Process(p['pid']).cmdline())
                            logging.warning(config.WARNING_MESSAGE.format(p['name'], p['pid'], p['memory_percent'], p['username'], command, p['pid']))
                            make_tarfile("/opt/resmon/archives/{0}.tar.gz".format(p['pid']), "/proc/{0}".format(p['pid']))
                            ALREADY_OCCURED = 1
                            OCCURENCE = 0
                            logging.debug("OCCURENCE: {0}, ALREADY_OCCURED: {1}".format(OCCURENCE, ALREADY_OCCURED))
                else:
                    OCCURENCE += 1
            else:
                OCCURENCE = 0
                ALREADY_OCCURED = 0
        except Exception:
            logging.exception("run(): Error in run")

        clean_old_files()
        time.sleep(config.TIMEOUT)


if __name__ == "__main__":
    logging.info("Starting Monitor")
    run()
