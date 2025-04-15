import sys
import subprocess
import time
import configparser
import os
import logging
from logging.handlers import RotatingFileHandler

# logger 생성 및 설정
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# RotatingFileHandler 설정: 최대 1MB, 백업 파일 5개
handler = RotatingFileHandler('my_log_file.log', maxBytes=1024*1024, backupCount=5)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def get_config_path():
    """
    실행 파일이 빌드된 exe일 경우 sys.frozen 속성이 True가 되므로,
    이때는 sys.executable의 위치(즉, exe가 위치한 디렉토리)를 기준으로 config.ini의 경로를 설정합니다.
    개발 환경에서는 __file__을 기준으로 config.ini의 경로를 설정합니다.
    """
    if getattr(sys, 'frozen', False): # exe로 빌드된 경우
        base_path = os.path.dirname(sys.executable)
    else: # 스크립트 상태인 경우
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, 'config.ini')

def load_config():
    """
    config.ini 파일을 읽어 [Program] 섹션의 설정값을 반환합니다.
    """
    config_path = get_config_path()
    if not os.path.exists(config_path):
        logging.error("설정 파일을 찾을 수 없습니다: %s", config_path)
        sys.exit(1)
    config = configparser.ConfigParser()
    config.read(config_path, encoding='utf-8')
    if 'Program' not in config:
        logging.error("config.ini에 [Program] 섹션이 없습니다.")
        sys.exit(1)
    return config

def run_and_monitor(exe_path, arg_str,monitor_interval):
    """
    exe_path에 지정된 실행 파일과 arg_str(실행 인자)을 사용하여 프로세스를 실행하고,
    monitor_interval 초마다 프로세스가 살아있는지 체크합니다.
    프로세스가 종료되면 재실행합니다.
    """
    while True:
        try:
            if arg_str.strip():
                process = subprocess.Popen([exe_path, arg_str])
            else: 
                process = subprocess.Popen([exe_path])
            logging.info(f"프로세스 시작됨. PID: {process.pid}")
        except Exception as e:
            logging.error("프로세스 실행 실패: %s", e)
            break
        
        # 실행 중인 프로세스를 monitor_interval초 간격으로 모니터링합니다.
        while True:
            time.sleep(monitor_interval)
            # process.poll()이 None이면 프로세스가 여전히 실행 중임을 의미합니다.
            if process.poll() is None:
                logging.info("프로세스 %s 실행 중", process.pid)
            else:
                logging.info("프로세스 %s 종료됨. 재실행합니다...", process.pid)
                break  # 내부 루프 종료 후, 바깥 루프에서 새 프로세스 실행

if __name__ == '__main__':
    config = load_config()

    # config.ini의 [Program] 섹션에서 실행 파일 경로와 실행 인자 읽기
    exe_path = config.get('Program', 'path', fallback='')
    arg_str = config.get('Program', 'args', fallback='')
    monitor_interval = config.getint('Program', 'monitor_interval', fallback=30)

    if not exe_path:
        logging.error("실행 파일 경로가 비어 있습니다. config.ini 파일을 확인하세요.")
        sys.exit(1)

    run_and_monitor(exe_path, arg_str,monitor_interval)
