import configparser
import time
import subprocess
import os
import sys
import psutil

def is_process_running(ps_name, ps_path):
    for proc in psutil.process_iter(['name', 'exe']):
        try:
            if proc.info['name'] == ps_name and proc.info['exe'] == ps_path:
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
    runpath = config['Program']['runpath']
    
    while True:
        if not is_process_running(program_name, program_path):
            subprocess.Popen([runpath])
        time.sleep(10)
if __name__=='__main__':
    main()