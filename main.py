import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from form_login import show_login_window
from form_datphong import show_booking_window
from datphong import*

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1080, 650)

        # Tạo layout chính
        main_layout = QVBoxLayout()

        # Thanh điều hướng
        button_layout = QHBoxLayout()

        login_button = QPushButton('Đăng nhập', self)
        login_button.clicked.connect(self.show_login)
        button_layout.addWidget(login_button)

        exit_button = QPushButton('Thoát', self)
        exit_button.clicked.connect(self.close)
        button_layout.addWidget(exit_button)

        order_button = QPushButton('Đặt Phòng', self)
        order_button.clicked.connect(self.show_thue_phong)
        button_layout.addWidget(order_button)

        print_button = QPushButton('In', self)
        button_layout.addWidget(print_button)

        # Thêm thanh điều hướng vào layout chính
        main_layout.addLayout(button_layout)

        # Tạo widget để chứa tiêu đề và các phần còn lại
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_widget.setLayout(content_layout)


        # Thêm widget chứa tiêu đề và các phần còn lại vào layout chính
        main_layout.addWidget(content_widget)

        # Thiết lập layout chính cho cửa sổ
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def show_login(self):
        show_login_window()

    def show_thue_phong(self):
        self.thue_phong_window = ThuePhongWindow()
        self.setCentralWidget(ThuePhongWindow())

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
