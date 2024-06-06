import datetime
import os
import time
import subprocess
import webbrowser


def getCurrentTimeStamp():
    times = str(time.time() * 1000).split(".")[0]
    return times


def startNginx():
    program_path = "./nginx/nginx.exe"
    arguments = []
    try:
        # 调用系统命令行并运行指定的程序
        process = subprocess.Popen([program_path] + arguments)
        # 等待子进程结束
        process.wait()
    except Exception as e:
        print("startNginx Error!!!：", str(e))


def openBrowser():
    webbrowser.open('http://localhost:8080/#/')


def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created successfully.")
    else:
        print(f"Folder '{folder_path}' already exists.")


def makeDirNameByDate():
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    return f'{year}_{month}_{day}'
