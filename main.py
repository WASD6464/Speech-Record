from ntpath import join
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
import speech_recognition as sr
import pyaudio
import os
import webbrowser
from subprocess import call



### Определение переменных
r = sr.Recognizer()
m = sr.Microphone(device_index=0)


### Основная функция, запуск UI
def UI():
    app = QApplication(sys.argv)
    global window
    window = QMainWindow()
    window.setWindowTitle("Speech Assistant - Wait...")
    window.setGeometry(300,300,400,300)

    main_text = QLabel(window)
    main_text.setText("Your Command: ")
    main_text.move(10,200)
    main_text.setFixedWidth(100)

    global user_text
    user_text = QLabel(window)
    user_text.setText("")
    user_text.move(110,200)


    global butt 
    butt = QPushButton("Record", window)
    butt.setText("Record")
    butt.resize(350,100)
    butt.move(25,25)
    butt.clicked.connect(progchange and record)
    window.show()
    app.exec()
    


### Изменение UI
def progchange():
    butt.setText("Recording...")
    butt.setEnabled(False)
    window.setWindowTitle("Speech Assistant - Process...")



### Запись
def record(*args: tuple):
    with m as source:
        global recognized_data
        recognized_data = ""
        r.adjust_for_ambient_noise(m, duration=2)
        try:
            audio = r.listen(source, phrase_time_limit=5, timeout=5)
            recognized_data = r.recognize_google(audio, language="ru").lower()
            print(recognized_data)
        except(sr.WaitTimeoutError,sr.UnknownValueError):
            pass
        except (sr.RequestError):
            user_text.setText("!!Check Internet Connetion!!")
        else:
            return recognized_data


def get_google(*args: tuple):
    """
    Поиск видео на YouTube с автоматическим открытием ссылки на список результатов
    :param args: фраза поискового запроса
    """
    if not args[0]: return
    search_term = " ".join(args[0])
    url = "https://www.google.com/search?q=" + search_term
    webbrowser.get().open(url)


def open_finder():
    targetDirectory = "~/Desktop"
    call(["open", targetDirectory])


def turnon_wifi():
    os.system("networksetup -setairportpower airport on")

def turnoff_wifi():
    os.system("networksetup -setairportpower airport off")

def open_sysmon():
    os.system("/System/Applications/Utilities/Activity\ Monitor.app/Contents/MacOS/Activity\ Monitor ; exit;")

def open_settings():
    os.system("/System/Applications/System\ Preferences.app/Contents/MacOS/System\ Preferences ; exit;")


def stop():
    sys.exit()

# def get_sum():
#     d




### Команды 
commands = {
    ("открой проводник", "открой файндер", "запусти проводник"): open_finder,
    ("выключи вайфай", "выключи вифи"): turnoff_wifi,
    ("включи вайфай", "включи вифи"): turnon_wifi,
    ("открой диспетчер задач", "открой мониторинг ресурсов", "запусти диспетчер задач", "запусти мониторинг ресурсов"): open_sysmon,
    ("открой настройки системы", "открой настройки", "настройки"): open_settings,
    ("найди в интернете", "поиск в интернете"): get_google,
    # ("сложи", "прибавь"): get_sum,
    ("завершение", "выход"): stop
}


### Поиск команды из записи в словаре
# def execute_command_with_name(command_name: str, *args: list):
#     """
#     Выполнение заданной пользователем команды с дополнительными аргументами
#     :param command_name: название команды
#     :param args: аргументы, которые будут переданы в функцию
#     :return:
#     """
#     for key in commands.keys():
#         if command_name in key:
#             commands[key](*args)
#             user_text.setText(command_name)
#         else:
#             pass


### Запуск программы
if __name__=="__main__":
    UI()
    while True:
        recognize_input = record()
        # отделение комманд от дополнительной информации (аргументов)
        # recognize_input = recognize_input.split(" ")
        print(recognize_input)
        command = recognize_input
        command_options = [str(input_part) for input_part in recognize_input[1:len(recognize_input)]]
        if command in commands.key:
            commands[commands.key](*args)
            user_text.setText(command)
        else:
            continue