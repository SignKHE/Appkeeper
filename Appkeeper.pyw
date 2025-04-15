import sys
import subprocess
import time
import configparser
import os

def get_config_path():
    """
    실행 파일이 빌드된 exe일 경우 sys.frozen 속성이 True가 되므로,
    이때는 sys.executable의 위치(즉, exe가 위치한 디렉토리)를 기준으로 config.ini의 경로를 설정합니다.
    개발 환경에서는 __file__을 기준으로 config.ini의 경로를 설정합니다.
    """
    if getattr(sys, 'frozen', False):
        # exe로 빌드된 경우
        base_path = os.path.dirname(sys.executable)
    else:
        # 스크립트 상태인 경우
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, 'config.ini')

def load_config():
    """
    config.ini 파일을 읽어 [Program] 섹션의 설정값을 반환합니다.
    """
    config_path = get_config_path()
    config = configparser.ConfigParser()
    # 파일이 없으면 예외 발생하거나 기본값을 설정할 수 있으므로, 필요에 따라 예외처리하세요.
    config.read(config_path, encoding='utf-8')
    return config

def run_and_monitor(exe_path, arg_str):
    while True:
        # 실행파일과 실행 인자를 함께 실행합니다.
        process = subprocess.Popen([exe_path, arg_str])
        print(f"프로세스 시작됨. PID: {process.pid}")
        
        # 실행 중인 프로세스를 30초 간격으로 모니터링합니다.
        while True:
            time.sleep(30)
            # process.poll()이 None이면 프로세스가 여전히 실행 중임을 의미합니다.
            if process.poll() is None:
                print(f"프로세스 {process.pid} 가 실행 중입니다.")
            else:
                print(f"프로세스 {process.pid} 가 종료되었습니다. 재실행합니다...")
                break  # 내부 루프 종료 후, 바깥 루프에서 새 프로세스 실행

if __name__ == '__main__':
    config = load_config()

    # 실행할 실행파일의 전체 경로를 지정합니다.
    exe_path = config.get('Program', 'path', fallback='')
    # 실행 인자로 전달할 문자열을 지정합니다.
    arg_str = config.get('Program', 'args', fallback='')

    run_and_monitor(exe_path, arg_str)
