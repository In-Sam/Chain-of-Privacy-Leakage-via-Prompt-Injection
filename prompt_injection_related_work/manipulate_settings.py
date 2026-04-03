import os
import pickle as pkl
import subprocess
import datetime
import threading

import utilities as ut  # ut.getGlobalVariable / ut.setGlobalVariable 를 쓴다고 가정
import jailbreak_template as jt  # (※ 이 부분 기능 자체는 제가 개선/확장 도움은 못 드립니다)

from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout

import macro as M

# -------------------- init --------------------
# ✅ config 폴더 삭제
# os.makedirs("./config", exist_ok=True)
os.makedirs("./logs", exist_ok=True)
os.makedirs("./global_variable", exist_ok=True)  # ✅ global_variable 폴더 보장(안전)

CLEAR_CMD = "cls" if os.name == "nt" else "clear"

server_state = "off"
server_process: subprocess.Popen | None = None
server_thread: threading.Thread | None = None

server_log = ""
log_lock = threading.Lock()

# enable 할 때 만든 폴더 경로(예: ./logs/2026-01-28_12-34-56)
current_log_dir: str | None = None


def now_stamp() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def safe_append_log(line: str) -> None:
    global server_log
    with log_lock:
        server_log += line


def safe_get_log() -> str:
    with log_lock:
        return server_log


def safe_flush_log() -> str:
    global server_log
    with log_lock:
        data = server_log
        server_log = ""
    return data


def stream_logs(proc: subprocess.Popen) -> None:
    try:
        assert proc.stdout is not None
        for line in iter(proc.stdout.readline, ""):
            if not line:
                break
            safe_append_log(line)
            print(line, end="")
    except Exception as e:
        print(f"[log-thread error] {e!r}")


# -------------------- file I/O --------------------
def readFile(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


# -------------------- config keys --------------------
main_format_py = readFile("./main_format.py")

ADDITIONAL_TASK_PATH = "additional_task_path"
ADDITIONAL_TASK_KEY = "additional_task_key"
HONEY_POT_PATH = "honey_pot_path"
HONEY_POT_KEY = "honey_pot_key"

defaults = {
    ADDITIONAL_TASK_PATH: "additional_task",
    ADDITIONAL_TASK_KEY: "key1",
    HONEY_POT_PATH: "more_info",
    HONEY_POT_KEY: "key2",
    "blog_path": "blog",
    "blog_key": "pageid",
}

# ✅ 기존 config bootstrap을 global_variable로 교체
for k, v in defaults.items():
    try:
        ut.getGlobalVariable(k)
    except FileNotFoundError:
        ut.setGlobalVariable(k, v)


def applyFormat() -> None:
    main_py = main_format_py
    main_py = M.applyMacros(main_py)
    with open("./main.py", "w", encoding="utf-8") as f:
        f.write(main_py)


# -------------------- logging (new) --------------------
def ensure_log_dir_for_enable() -> str:
    """서버 enable 시점에 log 디렉터리 생성하고 경로 반환"""
    global current_log_dir
    if current_log_dir is not None:
        return current_log_dir

    enable_ts = now_stamp()
    d = os.path.join("./logs", enable_ts)
    os.makedirs(d, exist_ok=True)
    current_log_dir = d

    # enable marker
    with open(os.path.join(d, f"{enable_ts}_enabled_server.txt"), "w", encoding="utf-8") as f:
        f.write("Enabled the server.")

    return d


def saveServerLog_on_disable() -> None:
    """서버 disable 시점: 끈 시각을 파일명으로 해서 enable 디렉터리에 저장"""
    global current_log_dir

    if current_log_dir is None:
        current_log_dir = "./logs"

    data = safe_flush_log()
    disable_ts = now_stamp()

    # disable marker
    with open(os.path.join(current_log_dir, f"{disable_ts}_disabled_server.txt"), "w", encoding="utf-8") as f:
        f.write("Disabled the server.")

    if data:
        with open(os.path.join(current_log_dir, f"{disable_ts}.txt"), "w", encoding="utf-8") as f:
            f.write(data)


def flushLog_in_terminal_only() -> None:
    """메뉴 8번: 지금 터미널에서 보이는 로그를 파일로 저장하고 비우기(현재 enable 디렉터리 사용)"""
    global current_log_dir

    if current_log_dir is None:
        os.makedirs("./logs/manual", exist_ok=True)
        current_log_dir = "./logs/manual"

    data = safe_flush_log()
    if not data:
        return

    ts = now_stamp()
    with open(os.path.join(current_log_dir, f"{ts}_manual_flush.txt"), "w", encoding="utf-8") as f:
        f.write(data)


# -------------------- server control --------------------
def start_server() -> None:
    global server_state, server_process, server_thread
    jt.makePrompt()

    if server_state == "on":
        return

    applyFormat()
    ensure_log_dir_for_enable()

    server_process = subprocess.Popen(
        ["python", "-u", "main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    server_thread = threading.Thread(target=stream_logs, args=(server_process,), daemon=True)
    server_thread.start()

    server_state = "on"


def stop_server() -> None:
    global server_state, server_process, server_thread, current_log_dir

    if server_state == "off":
        return

    saveServerLog_on_disable()

    if server_process is not None:
        try:
            server_process.terminate()
            server_process.wait(timeout=5)
        except Exception:
            try:
                server_process.kill()
                server_process.wait(timeout=5)
            except Exception:
                pass
        finally:
            try:
                if server_process.stdout:
                    server_process.stdout.close()
            except Exception:
                pass

    server_process = None
    server_thread = None
    server_state = "off"
    current_log_dir = None


def switchServerState() -> None:
    if server_state == "off":
        start_server()
    else:
        stop_server()


def restart_server() -> None:
    stop_server()
    start_server()


# -------------------- UI --------------------
def printPresentConfig(config: str) -> None:
    print("==================================================== present config ====================================================")
    if config == "all":
        print(f"blog path: {ut.getGlobalVariable("blog_path")}")
        print(f"blog key: {ut.getGlobalVariable("blog_key")}")
        print(f"{ADDITIONAL_TASK_PATH}: {ut.getGlobalVariable(ADDITIONAL_TASK_PATH)}")
        print(f"{ADDITIONAL_TASK_KEY}: {ut.getGlobalVariable(ADDITIONAL_TASK_KEY)}")
        print(f"{HONEY_POT_PATH}: {ut.getGlobalVariable(HONEY_POT_PATH)}")
        print(f"{HONEY_POT_KEY}: {ut.getGlobalVariable(HONEY_POT_KEY)}")
    elif config == "blog_path":
        print(f"blog path: {ut.getGlobalVariable("blog_path")}")
    elif config == "blog_key":
        print(f"blog key: {ut.getGlobalVariable("blog_key")}")
    elif config == ADDITIONAL_TASK_PATH:
        print(f"{ADDITIONAL_TASK_PATH}: {ut.getGlobalVariable(ADDITIONAL_TASK_PATH)}")
    elif config == ADDITIONAL_TASK_KEY:
        print(f"{ADDITIONAL_TASK_KEY}: {ut.getGlobalVariable(ADDITIONAL_TASK_KEY)}")
    elif config == HONEY_POT_PATH:
        print(f"{HONEY_POT_PATH}: {ut.getGlobalVariable(HONEY_POT_PATH)}")
    elif config == HONEY_POT_KEY:
        print(f"{HONEY_POT_KEY}: {ut.getGlobalVariable(HONEY_POT_KEY)}")
    print("==================================================== present config ====================================================")


def setConfig(config: str) -> None:
    os.system(CLEAR_CMD)
    printPresentConfig(config)
    new = input(f"new {config} (just enter to escape): ").strip()
    if new == "":
        return
    ut.setGlobalVariable(config, new)


def printMenu() -> None:
    printPresentConfig("all")
    print("-2. set blog path")
    print("-1. set blog key")
    print("1. set additional task path")
    print("2. set additional task key")
    print("3. set more info path")
    print("4. set more info key")
    print("")
    print(f"5. switch server state (current state: {server_state})")
    print("6. reload server")
    print("7. (omitted here)")  # ※ jailbreak 관련 기능은 제가 개선/확장 형태로 도와드릴 수 없습니다.
    print("")
    print("==================================================== server log ====================================================")
    print(safe_get_log(), end="")


# -------------------- main --------------------
if __name__ == "__main__":
    print(ut.getGlobalVariable("url"))
    start_server()
    session = PromptSession()

    with patch_stdout():
        while True:
            try:
                os.system(CLEAR_CMD)
                printMenu()

                s = session.prompt(
                    "\n==================================================== server log ====================================================\n"
                    "8. clear logs in this terminal (save, flush)\n"
                    "\nYour Choice (Just enter to exit): "
                ).strip()

                if s == "":
                    break

                menu = int(s)

                if menu == -2:
                    setConfig("blog_path")
                if menu == -1:
                    setConfig("blog_key")
                if menu == 1:
                    setConfig(ADDITIONAL_TASK_PATH)
                elif menu == 2:
                    setConfig(ADDITIONAL_TASK_KEY)
                elif menu == 3:
                    setConfig(HONEY_POT_PATH)
                elif menu == 4:
                    setConfig(HONEY_POT_KEY)
                elif menu == 5:
                    switchServerState()
                elif menu == 6:
                    restart_server()
                elif menu == 7:
                    jt.main()
                elif menu == 8:
                    flushLog_in_terminal_only()
                elif menu//10 == 7:
                    commandMapping = jt.commandMapping
                    commandMapping[menu%10 - 1]()

            except ValueError:
                continue
            except Exception as e:
                print(f"[error] {e!r}")

    stop_server()
