import time
import config


class bcolors:  # 颜色代码
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    DEBUG = '\033[36m'


if config.LOG not in ['ALL', 'INFO', 'WARN', 'ERROR', 'DEBUG']:
    level = 'ERROR'
    print(bcolors.WARNING + "WARNING: " + bcolors.ENDC + "| " +
          time.strftime('%Y-%m-%d %H:%M:%S') + " | " + str("日志等级配置错误，将默认使用ERROR"))
else:
    level = config.LOG


class logging():  # 自定义日志
    def info(self, text):
        if level in ['INFO', 'DEBUG', 'WARN', 'ERROR', 'ALL']:
            print(bcolors.OKGREEN + "INFO: " + bcolors.ENDC + "| " +
                  time.strftime('%Y-%m-%d %H:%M:%S') + " | " + str(text))

    def warn(self, text):
        if level in ['WARN', 'ERROR', 'DEBUG', 'ALL']:
            print(bcolors.WARNING + "WARNING: " + bcolors.ENDC + "| " +
                  time.strftime('%Y-%m-%d %H:%M:%S') + " | " + str(text))

    def error(self, text):
        if level in ['ERROR', 'DEBUG', 'ALL']:
            print(bcolors.FAIL + "ERROR: " + bcolors.ENDC + "| " +
                  time.strftime('%Y-%m-%d %H:%M:%S') + " | " + str(text))

    def debug(self, text):
        if level in ['DEBUG', 'ALL']:
            print(bcolors.DEBUG + "DEBUG: " + bcolors.ENDC + "| " +
                  time.strftime('%Y-%m-%d %H:%M:%S') + " | " + str(text))
