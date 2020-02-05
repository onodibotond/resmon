from configparser import ConfigParser
import math

parser = ConfigParser()
parser.read('/etc/resmon/monitor.conf')

DAYS_TO_KEEP = parser.getint('user_config', 'days_to_keep')
COLLECT = parser.getboolean('user_config', 'do_collection')
MAX_MEMORY = parser.getint('user_config', 'trigger_collection')

TIMEOUT = parser.getint('app_config', 'check_cycle_time')
MIN_MEMORY = parser.getint('app_config', 'min_memory_to_be_sampled')
MAX_OCCURENCE = math.ceil(parser.getint('app_config', 'min_sample_period') / TIMEOUT)

SECONDS_PER_DAY = 86400
WARNING_MESSAGE = "The process {0} with PID: {1} uses {2}% memory, is executed by {3} with the initial command: {4} \nMore info at /opt/resmon/archives/{0}.tar.gz"
