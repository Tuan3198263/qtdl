import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QDateEdit, QTextEdit, QTableWidget, QTableWidgetItem, QMessageBox, QSplitter
from PySide6.QtCore import Qt, QDate
from conc import*   # Import kết nối đến cơ sở dữ liệu

class ThuePhongWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Đặt Phòng")
        self.resize(800, 600)



        # Tạo layout chính
        main_layout = QHBoxLayout()

        # Tạo splitter để chia layout thành hai phần
        splitter = QSplitter(Qt.Horizontal)
        

        # Phần nhập thông tin
        input_widget = QWidget()
        input_layout = QVBoxLayout(input_widget)
        
        home_button = QPushButton("Home", self)
        home_button.clicked.connect(self.go_to_main_window)
        input_layout.addWidget(home_button)

        label = QLabel("Điền thông tin đặt phòng", self)
        label.setAlignment(Qt.AlignCenter)
        input_layout.addWidget(label)

        label_ma_khach = QLabel("Mã khách hàng:", self)
        input_layout.addWidget(label_ma_khach)
        self.ma_khach_edit = QLineEdit(self)
        self.ma_khach_edit.setPlaceholderText("Nhập mã khách hàng")
        input_layout.addWidget(self.ma_khach_edit)

        label_ma_phong = QLabel("Mã phòng:", self)
        input_layout.addWidget(label_ma_phong)
        self.ma_phong_edit = QLineEdit(self)
        self.ma_phong_edit.setPlaceholderText("Nhập mã phòng")
        input_layout.addWidget(self.ma_phong_edit)

        label_ngay_vao = QLabel("Ngày vào:", self)
        input_layout.addWidget(label_ngay_vao)
        self.ngay_vao_edit = QDateEdit(self)
        self.ngay_vao_edit.setDisplayFormat("yyyy-MM-dd")
        self.ngay_vao_edit.setDate(QDate.currentDate())
        input_layout.addWidget(self.ngay_vao_edit)

        label_ngay_ra = QLabel("Ngày ra:", self)
        input_layout.addWidget(label_ngay_ra)
        self.ngay_ra_edit = QDateEdit(self)
        self.ngay_ra_edit.setDisplayFormat("yyyy-MM-dd")
        self.ngay_ra_edit.setDate(QDate.currentDate())
        input_layout.addWidget(self.ngay_ra_edit)

        label_dat_coc = QLabel("Đặt cọc:", self)
        input_layout.addWidget(label_dat_coc)
        self.dat_coc_edit = QLineEdit(self)
        self.dat_coc_edit.setPlaceholderText("Nhập số tiền đặt cọc")
        input_layout.addWidget(self.dat_coc_edit)


        thue_button = QPushButton("Đặt Phòng", self)
        thue_button.clicked.connect(self.thue_phong)
        input_layout.addWidget(thue_button)

        splitter.addWidget(input_widget)

        # Phần hiển thị cơ sở dữ liệu dưới dạng bảng
        db_display_widget = QWidget()
        db_display_layout = QVBoxLayout(db_display_widget)

        db_label = QLabel("Dữ liệu bảng Thuê Phòng", self)
        db_label.setAlignment(Qt.AlignCenter)
        db_display_layout.addWidget(db_label)

        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(6)  # Số lượng cột
        self.table_widget.setHorizontalHeaderLabels(["Mã Thuê", "Mã Khách", "Mã Phòng", "Ngày Vào", "Ngày Ra", "Đặt Cọc"])
        db_display_layout.addWidget(self.table_widget)

        splitter.addWidget(db_display_widget)

        # Thêm splitter vào layout chính
        main_layout.addWidget(splitter)

        # Thiết lập layout chính cho cửa sổ
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Hiển thị dữ liệu ban đầu
        self.display_database()

    def display_database(self):
        try:
            conn = connect_to_database()
            cursor = conn.cursor()

            # Lấy dữ liệu từ cơ sở dữ liệu
            cursor.execute("SELECT * FROM ThuePhong")
            records = cursor.fetchall()
            self.table_widget.setRowCount(0)  # Xóa dữ liệu cũ
            for row_number, row_data in enumerate(records):
                self.table_widget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.table_widget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

            cursor.close()
            conn.close()
        except Exception as e:
            print("Error:", e)

    def thue_phong(self):
        # Lấy thông tin từ các ô nhập liệu
        ma_khach = self.ma_khach_edit.text()
        ma_phong = self.ma_phong_edit.text()
        ngay_vao = self.ngay_vao_edit.date().toString(Qt.ISODate)
        ngay_ra = self.ngay_ra_edit.date().toString(Qt.ISODate)
        dat_coc = self.dat_coc_edit.text()

        # Kiểm tra xem có trường nào trống không
        if not (ma_khach and ma_phong and ngay_vao and ngay_ra and dat_coc):
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin.")
            return

        try:
            conn = connect_to_database()
            cursor = conn.cursor()

            # Gọi thủ tục DatPhong
            cursor.callproc("DatPhong", (ma_khach, ma_phong, ngay_vao, ngay_ra, dat_coc))
            conn.commit()

            QMessageBox.information(self, "Thông báo", "Đặt phòng thành công.")
            self.clear_fields()

            cursor.close()
            conn.close()

            # Sau khi đặt phòng thành công, hiển thị lại
            self.display_database()
        except Exception as e:
            QMessageBox.warning(self, "Lỗi", f"Lỗi khi đặt phòng: {e}")

    def clear_fields(self):
        self.ma_khach_edit.clear()
        self.ma_phong_edit.clear()
        self.dat_coc_edit.clear()
        
    def go_to_main_window(self):
        # Điều hướng đến giao diện chính (main.py)
        from main import MainWindow
        self.main_window = MainWindow()
        self.setCentralWidget(MainWindow())

        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ThuePhongWindow()
    window.show()
    sys.exit(app.exec())
