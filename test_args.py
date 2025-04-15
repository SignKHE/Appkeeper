# test_args.py
import sys

def main():
    print("전달된 인자:")
    for i, arg in enumerate(sys.argv):
        print(f"argv[{i}]: {arg}")
    input("\n출력을 확인하려면 엔터 키를 누르세요...")  # 사용자 입력 대기

if __name__ == '__main__':
    main()
