import os
import time
import psutil

from colorama import Fore

# getters
def get_time() -> str:
    return time.strftime('%H:%M:%S')

def parse(content:str) -> str:
    return content.replace("\n", "\n\t\t     ")

# classes
class bprint():
    def success(content:str) -> None:
        print(f'[{Fore.LIGHTBLACK_EX}{get_time()}{Fore.RESET}] [{Fore.LIGHTGREEN_EX}success{Fore.RESET}] {parse(content)}')

    def error(content:str) -> None:
        print(f'[{Fore.LIGHTBLACK_EX}{get_time()}{Fore.RESET}] [{Fore.LIGHTRED_EX}error{Fore.RESET}] {parse(content)}')

    def critical(content:str) -> None:
        print(f'[{Fore.LIGHTBLACK_EX}{get_time()}{Fore.RESET}] [{Fore.LIGHTRED_EX}critical{Fore.RESET}] {parse(content)}')

    def warning(content:str) -> None:
        print(f'[{Fore.LIGHTBLACK_EX}{get_time()}{Fore.RESET}] [{Fore.LIGHTRED_EX}warning{Fore.RESET}] {parse(content)}')

    def info(content:str) -> None:
        print(f'[{Fore.LIGHTBLACK_EX}{get_time()}{Fore.RESET}] [{Fore.YELLOW}info{Fore.RESET}] {parse(content)}')

    def input(content:str) -> str:
        print(f'[{Fore.LIGHTBLACK_EX}{get_time()}{Fore.RESET}] [{Fore.CYAN}input{Fore.RESET}] {parse(content)} ', end='')
        item = input()
        return item

    def pause() -> None:
        print(f'[{Fore.LIGHTBLACK_EX}{get_time()}{Fore.RESET}] [{Fore.CYAN}pause{Fore.RESET}] Press any key...')
        os.system('pause >nul')

    def center(var:str) -> None:
        col = os.get_terminal_size().columns
        varl = var.splitlines()
        nvarl = max(len(v) for v in varl if v.strip())
        spaces = int((col - nvarl) / 2)
        print('\n'.join((' ' * spaces) + var for var in var.splitlines()))

    def start(content:str="process") -> int:
        print(f'[{Fore.LIGHTBLACK_EX}{get_time()}{Fore.RESET}] Starting {content}...')
        return time.time()

    def finish(starting_time:int, ending_time:int=time.time, content:str="Process") -> None:
        print(f'[{Fore.LIGHTBLACK_EX}{get_time()}{Fore.RESET}] {content} finished after {round(starting_time - ending_time, 3)} seconds...')

class system:
    def init() -> None:
        os.system('')

    def clear() -> None:
        os.system('cls')

    def title(title:str='') -> None:
        os.system(f'title {title}')

    def size(x:int, y:int) -> None:
        os.system('mode ' + str(x) + ',' + str(y))
        os.system('powershell -command "&{$w=(get-host).ui.rawui;$w.buffersize=@{width=' + str(x) + ';height=9001};$w.windowsize=@{width=' + str(x) + ';height=' + str(y) + '};}"')

    def ppid() -> str:
        return psutil.Process(os.getppid()).parent().name()

    def command(command:str) -> None:
        os.system(command)

    def exit(sleep:int=1, val:bool=True) -> None:
        print(f"[{Fore.LIGHTBLACK_EX}{get_time()}{Fore.RESET}] Exiting...")
        if val:
            time.sleep(sleep)
        exit()