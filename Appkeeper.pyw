import configparser
import time
import subprocess
import os
import sys
import psutil

def is_process_running(ps_name):
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] == ps_name:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def main():
    config = configparser.ConfigParser()
    script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    ini_path = os.path.join(script_dir,'config.ini')
    config.read(ini_path, encoding='utf-8')
    
    program_name = config['Program']['name']
    program_path = config['Program']['path']
    
    while True:
        if not is_process_running(program_name):
            subprocess.Popen([program_path])
        time.sleep(5)
if __name__=='__main__':
    main()