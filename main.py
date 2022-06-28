from ntpath import join
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
import speech_recognition as sr
import pyaudio
import os
import webbrowser
from urllib.parse import quote_plus


# Определение переменных


# Основная функция, запуск UI
def UI():
    app = QApplication(sys.argv)
    global window
    window = QMainWindow()
    window.setWindowTitle("Speech Assistant - Wait...")
    window.setGeometry(300, 300, 400, 300)

    main_text = QLabel(window)
    main_text.setText("Your Command: ")
    main_text.move(10, 200)
    main_text.setFixedWidth(100)

    global user_text
    user_text = QLabel(window)
    user_text.setText("")
    user_text.move(110, 200)

    global butt
    butt = QPushButton("Record", window)
    butt.setText("Record")
    butt.resize(350, 100)
    butt.move(25, 25)
    butt.clicked.connect(progchange)
    window.show()
    app.exec()


# Изменение UI
def progchange():
    butt.setText("Recording...")
    butt.setEnabled(False)
    window.setWindowTitle("Speech Assistant - Process...")
    work()


# Запись
def record():
    with m as source:
        global recognized_data
        recognized_data = ""
        r.adjust_for_ambient_noise(m, duration=4)
        try:
            audio = r.listen(source, phrase_time_limit=7, timeout=1)
            recognized_data = r.recognize_google(audio, language="ru").lower()
        except(sr.WaitTimeoutError, sr.UnknownValueError):
            pass
        else:
            return recognized_data


def get_google(ri, *command: list):
    """
    Поиск видео на YouTube с автоматическим открытием ссылки на список результатов
    :param args: фраза поискового запроса
    """
    a = ' '.join(command)
    url = "https://www.google.com/search?q=" + quote_plus(a)
    webbrowser.get().open(url)
    print(f"Ваша команда: %s" % ri)


def open_finder(ri, *command: list):
    os.chdir('/Users/wasd64/')
    os.system("open `pwd`")
    print(f"Ваша команда: %s" % ri)


def turnon_wifi(ri, *command: list):
    os.system("networksetup -setairportpower airport on")
    print(f"Ваша команда: %s" % ri)


def turnoff_wifi(ri, *command: list):
    os.system("networksetup -setairportpower airport off")
    print(f"Ваша команда: %s" % ri)


def open_sysmon(ri, *command: list):
    os.system(
        "/System/Applications/Utilities/Activity\ Monitor.app/Contents/MacOS/Activity\ Monitor ; exit;")
    print(f"Ваша команда: %s" % ri)


def open_settings(ri, *command: list):
    os.system(
        "/System/Applications/System\ Preferences.app/Contents/MacOS/System\ Preferences ; exit;")
    print(f"Ваша команда: %s" % ri)


def stop(ri, *command: list):
    print(f"Ваша команда: %s" % ri)
    sys.exit()


def get_sum(ri, *command: list):
    a=0
    for x in range(len(command)):
        try:
            a+=int(command[x])
        except:
            pass
    print(f"Ваша команда: %s" % ri)
    print(f"Результат: %a" % a)


# Команды
commands = {
    ("открой проводник", "открой финдер", "запустить проводник", "открыть проводник"): open_finder,
    ("открой диспетчер задач", "открой мониторинг ресурсов", "запусти диспетчер задач", "запусти мониторинг ресурсов"): open_sysmon,
    ("открой настройки системы", "открой настройки", "настройки"): open_settings,
    ("найди в интернете", "поиск в интернете"): get_google,
    ("сложи", "прибавь"): get_sum,
    ("завершение", "выход"): stop
}


def work():
    global r
    global m
    r = sr.Recognizer()
    m = sr.Microphone(device_index=2)
    while True:
        global ri
        ri = record()
        if type(ri) != type(None):
            print(ri)
            if ri == "выключи wi-fi":
                turnoff_wifi(ri)
            elif ri == "включи wi-fi":
                turnon_wifi(ri)
            for key in commands.keys():
                for x in key:
                    if x in ri:
                        global comand
                        command = list(set(tuple(ri.split(" "))) -
                                       set(tuple(x.split(" "))))
                        print("COMAND")
                        print(command)
                        commands[key](ri, *command)
            else:
                continue


# Запуск программы
if __name__ == "__main__":
    UI()
