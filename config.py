DEFAULT_SERVICES_LINUX = ['sshd', 'nginx', 'docker', 'cron', 'vsftpd']
DEFAULT_SERVICES_WINDOWS = ['wuauserv', 'EventLog', 'Winmgmt', 'Dnscache']

DEFAULT_PORTS_LINUX = [22, 80, 443, 3306, 21]
DEFAULT_PORTS_WINDOWS = [135, 445, 3389]

LOG_WHEN = 'midnight'
LOG_INTERVAL = 1 
LOG_BACKUP_COUNT = 7
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'