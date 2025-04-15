import subprocess
import time
import configparser
import os

def load_program_config(config_path):
    """
    주어진 config.ini 파일 경로에서 [Program] 섹션의 정보를 읽어와
    실행 파일 경로와 실행 인자를 반환하는 함수입니다.
    
    반환 예시:
      {
         "path": "C:\\Windows\\System32\\notepad.exe",
         "args": "a=실행인자 b=예제"
      }
    """
    config = configparser.ConfigParser()
    config.read(config_path, encoding='utf-8')
    
    # [Program] 섹션에서 path와 args 값을 가져옴
    path_value = config.get('Program', 'path', fallback=None)
    args_value = config.get('Program', 'args', fallback="")

    # args 값이 큰따옴표로 둘러싸여 있으면 제거
    if args_value.startswith('"') and args_value.endswith('"'):
        args_value = args_value[1:-1]
    
    return {"path": path_value, "args": args_value}

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
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(script_dir, 'config.ini')

    program_config = load_program_config(config_file)

    # 실행할 실행파일의 전체 경로를 지정합니다.
    exe_path = program_config["path"]
    # 실행 인자로 전달할 문자열을 지정합니다.
    arg_str = program_config["args"]

    run_and_monitor(exe_path, arg_str)
