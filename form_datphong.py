import PySimpleGUI as sg
from conc import*

def check_booking(ma_khach, ma_phong, ngay_vao, ngay_ra, dat_coc):
        conn = connect_to_database()
        cursor = conn.cursor()

        # Gọi stored procedure để kiểm tra thông tin đặt phòng
        cursor.callproc('DatPhong', (ma_khach, ma_phong, ngay_vao, ngay_ra, dat_coc))
        conn.commit()

        # Kiểm tra kết quả trả về từ stored procedure
        cursor.execute("SELECT @result")
        result = cursor.fetchone()[0]

        if result == 1:
            print('Đặt phòng thành công!')
            return True
        else:
            print('Đặt phòng không thành công! Vui lòng kiểm tra lại thông tin đặt phòng.')
            return False


#
def show_booking_window():
    layout = [
        [sg.Text('Mã khách hàng:', size=(15, 1)), sg.InputText(key='-MA_KHACH-')],
        [sg.Text('Mã phòng:', size=(15, 1)), sg.InputText(key='-MA_PHONG-')],
        [sg.Text('Ngày vào :', size=(15, 1)), sg.InputText(key='-NGAY_VAO-')],
        [sg.Text('Ngày ra :', size=(15, 1)), sg.InputText(key='-NGAY_RA-')],
        [sg.Text('Đặt cọc:', size=(15, 1)), sg.InputText(key='-DAT_COC-')],
        [sg.Button('Đặt phòng'), sg.Button('Thoát')]
    ]

    window = sg.Window('Đặt phòng', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Thoát':
            break
        elif event == 'Đặt phòng':
            ma_khach = values['-MA_KHACH-']
            ma_phong = values['-MA_PHONG-']
            ngay_vao = values['-NGAY_VAO-']
            ngay_ra = values['-NGAY_RA-']
            dat_coc = values['-DAT_COC-']
            if check_booking(ma_khach, ma_phong, ngay_vao, ngay_ra, dat_coc):
                sg.popup('Đặt phòng thành công!')
            else:
                sg.popup('Đặt phòng không thành công! Vui lòng kiểm tra lại thông tin đặt phòng.')

    window.close()

if __name__ == '__main__':
    show_booking_window()
