import PySimpleGUI as sg
from conc import*



def check_login(username, password):
    conn = connect_to_database()
    cursor = conn.cursor()

    # Thực hiện truy vấn để kiểm tra thông tin đăng nhập
    cursor.execute("SELECT * FROM Account WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        return True
    else:
        return False

def show_login_window():
    layout = [
        [sg.Text('Tên đăng nhập:', size=(15, 1)), sg.InputText(key='-USERNAME-')],
        [sg.Text('Mật khẩu:', size=(15, 1)), sg.InputText(key='-PASSWORD-', password_char='*')],
        [sg.Button('Đăng nhập'), sg.Button('Thoát')]
    ]

    window = sg.Window('Đăng nhập', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Thoát':
            break
        elif event == 'Đăng nhập':
            username = values['-USERNAME-']
            password = values['-PASSWORD-']
            if check_login(username, password):
                sg.popup('Đăng nhập thành công!')
            else:
                sg.popup('Đăng nhập không thành công! Vui lòng kiểm tra lại tên đăng nhập và mật khẩu.')

    window.close()