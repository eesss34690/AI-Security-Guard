import PySimpleGUI as sg
from os import path
import numpy as np
import requests
import PIL.Image
from cv2 import waitKey
import time
import line_bot as bot

name = [['a', 'b', 'c', 'd'],
        ['e', 'f', 'g', 'h'],
        ['i', 'j', 'k', 'l']]


def try_again_GUI():
    sg.theme('Dark Blue 17')
    layout = [
        [sg.Text('Please try again.',
                 size=(25, 1),  font=("Calibri", 50))],
        [sg.Cancel(font=("Calibri", 20))]

    ]

    return sg.Window('AI Security Guard', layout)


def accepted_GUI():
    sg.theme('Dark Blue 17')
    layout = [
        [sg.Text('Your request has been accepted.',
                 size=(27, 1),  font=("Calibri", 50))],
    ]
    return sg.Window('AI Security Guard', layout)


def GUI():
    sg.theme('Dark Blue 17')
    layout = [
        [sg.Text('Please finish the form.', size=(
            30, 2),  font=("Calibri", 20))],
        [sg.Text('Destination floor', size=(30, 2), font=("Calibri", 20)),
         sg.InputText('', size=(30, 2), font=("Calibri", 20))],
        [sg.Text('Who do you want to visit?', size=(30, 2), font=(
            "Calibri", 20)), sg.InputText('', size=(30, 2), font=("Calibri", 20))],
        [sg.Text('Your name', size=(30, 2), font=("Calibri", 20)),
         sg.InputText('', size=(30, 2), font=("Calibri", 20))],
        [sg.Submit(font=("Calibri", 20)), sg.Cancel(font=("Calibri", 20))]
    ]

    return sg.Window('AI Security Guard', layout)


def confirm_GUI():

    layout = [
        [sg.Text('Confirming......', size=(12, 1),  font=("Calibri", 50))],
    ]

    return sg.Window('AI Security Guard', layout)


def validate(value1, value2):
    # print(value1)
    for i in range(5):
        if i <= 3:
            if name[value1-2][i] == value2:
                bot.send_message(value1-2)
                sg.popup_auto_close(
                    'Your request has been accepted.', auto_close_duration=3)
                sg.popup_auto_close(
                    'elevator destination:' + str(value1-2), auto_close_duration=2)
                return 1
                # if xx:
                #     return 1
                # elif yy:
                #     return 2

        else:
            return 3


def accepted_GUI():
    sg.theme('Dark Blue 17')
    layout = [
        [sg.Text('Your request has been accepted.',
                 size=(27, 1),  font=("Calibri", 50))],
    ]
    return sg.Window('AI Security Guard', layout)


def denied_GUI():
    sg.theme('Dark Blue 17')
    layout = [
        [sg.Text('Your request has been rejected.',
                 size=(27, 1),  font=("Calibri", 50))],
    ]

    return sg.Window('AI Security Guard', layout)


def main():
    window = None
    count = 0
    c = 0
    while True:             # Event Loop
        # window = None
        if window is None:
            window = GUI()

        event, values = window.read()
        if event == None:
            break
        if event == 'Submit':

            if values[0] != "" and values[1] != "" and values[2] != "":

                window.close()

                if validate(int(values[0]), values[1]) == 1:
                    continue
                   # window = accepted_GUI()
                   # sg.popup_auto_close(
                   #     'Your request has been accepted.', auto_close_duration = 5)

                elif validate(int(values[0]), values[1]) == 2:
                    window = denied_GUI()
                    bot.guard_message()
                    break

                elif validate(int(values[0]), values[1]) == 3:
                    window = try_again_GUI()
                    event = window.read()
                    window.close()
                    window = None
                    count = count+1
                    if count == 3:
                        count = 0
                        break

            else:
                window = GUI()
        if event == 'Cancel':
            window.close()
            window = None
            break


main()
