import PySimpleGUI as sg
from form_login import *
from form_datphong import *

def main():
    layout = [
        [sg.Text('Ứng dụng Quản Lý Khách Sạn', size=(30, 1), font=('Helvetica', 20), text_color='red')],
        [sg.Button('Đăng nhập', key='-LOGIN-', size=(15, 2)), sg.Button('Thoát', size=(15, 2)),sg.Button('Đặt Phòng',key = '-ORDER-', size=(15, 2)), sg.Button('In', size=(15, 2))]
    ]


    window = sg.Window('Ứng dụng Quản Lý Khách Sạn', layout, size=(1080,720))

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Thoát':
            break
        #goi form login
        elif event == '-LOGIN-':
            show_login_window()
        elif event == '-ORDER-':
            show_booking_window()

    window.close()

if __name__ == '__main__':
    main()
