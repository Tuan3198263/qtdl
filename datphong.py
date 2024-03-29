from connection import conn
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QDateEdit, QTableWidget, QTableWidgetItem, QSplitter, QMessageBox, QFormLayout
from PyQt5.QtCore import Qt, QDate

class ThuePhongWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Đặt Phòng")
        self.resize(1080, 720)

        # Tạo layout chính
        main_layout = QHBoxLayout()

        # Tạo splitter để chia layout thành hai phần
        splitter = QSplitter(Qt.Horizontal)


       # Phần nhập thông tin
        input_widget = QWidget()
        input_layout = QFormLayout(input_widget)
        input_layout.setVerticalSpacing(20) 
        
        home_button = QPushButton("Home", self)
        home_button.setFixedHeight(40)
        home_button.setFixedWidth(60)
        home_button.setCursor(Qt.PointingHandCursor)  
        
        #home_button.clicked.connect(self.go_to_main_window)
        input_layout.addWidget(home_button)

        label = QLabel("Điền thông tin đặt phòng", self)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 24px; color: #333;")
        input_layout.addWidget(label)

        labels = ["Mã khách hàng", "Mã phòng", "Ngày vào", "Ngày ra", "Đặt cọc"]
        self.inputs = []

        for label_text in labels:
            label = QLabel(label_text, self)
            label.setStyleSheet("font-size: 18px; color: #666;")
            input_layout.addWidget(label)
            if label_text in ["Ngày vào", "Ngày ra"]:
                date_edit = QDateEdit(self)
                date_edit.setCalendarPopup(True)  
                date_edit.setDate(QDate.currentDate())  # Đặt ngày mặc định là ngày hiện tại
                input_layout.addWidget(date_edit)
                self.inputs.append(date_edit)
                date_edit.setFixedHeight(35)
            else:
                line_edit = QLineEdit(self)
                line_edit.setPlaceholderText(f"Nhập {label_text.lower()}")
                line_edit.setFixedHeight(35)  # Đặt kích thước tối thiểu của ô nhập dữ liệu
                input_layout.addWidget(line_edit)
                self.inputs.append(line_edit)



        thue_button = QPushButton("Xác nhận", self)
        thue_button.setStyleSheet("font-size: 16px; padding: 7px 10px; background-color: #4CAF50; color: white; border: none; border-radius: 5px; max-width:200px")
        thue_button.setCursor(Qt.PointingHandCursor)  
        thue_button.setMinimumWidth(thue_button.sizeHint().width())
        thue_button.clicked.connect(self.thue_phong)
        input_layout.addWidget(thue_button)
        splitter.addWidget(input_widget)

        # Phần hiển thị cơ sở dữ liệu dưới dạng bảng
        db_display_widget = QWidget()
        db_display_layout = QVBoxLayout(db_display_widget)

        db_label = QLabel("Dữ liệu Thuê Phòng", self)
        db_label.setAlignment(Qt.AlignCenter)
        db_label.setStyleSheet("font-size: 18px; color: #333;")
        db_display_layout.addWidget(db_label)

        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(6)  # Số lượng cột
        self.table_widget.setHorizontalHeaderLabels(["Mã Thuê", "Mã Khách", "Mã Phòng", "Ngày Vào", "Ngày Ra", "Đặt Cọc"])
        db_display_layout.addWidget(self.table_widget)

        splitter.addWidget(db_display_widget)

        # Thiết lập tỷ lệ kích thước cho splitter
        splitter_ratio = 0.4  # Tỉ lệ của phần nhập thông tin
        splitter_width = self.width()  # Chiều rộng của cửa sổ
        input_width = int(splitter_width * splitter_ratio)
        db_width = splitter_width - input_width
        splitter.setSizes([input_width, db_width])

        # Thêm splitter vào layout chính
        main_layout.addWidget(splitter)



        # Thiết lập layout chính cho cửa sổ
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Hiển thị dữ liệu ban đầu
        self.display_database()

#-----------------------------------------------------------------------------------------------------------
#
    def display_database(self):
        try:
            #conn = connect_to_database()
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
            #conn.close()
        except Exception as e:
            print("Error:", e)

    def thue_phong(self):
        # Lấy thông tin từ các ô nhập liệu và QDateEdit
        ma_khach = self.inputs[0].text()
        ma_phong = self.inputs[1].text()
        ngay_vao = self.inputs[2].date().toString("yyyy-MM-dd")  # Lấy ngày từ QDateEdit và chuyển đổi thành chuỗi
        ngay_ra = self.inputs[3].date().toString("yyyy-MM-dd")   # Lấy ngày từ QDateEdit và chuyển đổi thành chuỗi
        dat_coc = self.inputs[4].text()

        if not (ma_khach and ma_phong and ngay_vao and ngay_ra and dat_coc):
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin.")
            return

        try:
            #conn = connect_to_database()
            cursor = conn.cursor()

            # Gọi thủ tục DatPhong
            cursor.callproc("DatPhong", (ma_khach, ma_phong, ngay_vao, ngay_ra, dat_coc))
            conn.commit()

            QMessageBox.information(self, "Thông báo", "Đặt phòng thành công.")
            self.clear_fields()

            cursor.close()
            #conn.close()

            # Sau khi đặt phòng thành công, hiển thị lại
            self.display_database()
        except Exception as e:
            QMessageBox.warning(self, "Lỗi", f"Lỗi khi đặt phòng: {e}")
        
    def clear_fields(self):
        for widget in self.inputs:
            if isinstance(widget, QLineEdit):
                widget.clear()
            elif isinstance(widget, QDateEdit):
                widget.setDate(QDate.currentDate())

        """""
    def go_to_main_window(self):
        # Điều hướng đến giao diện chính (main.py)
        from main import MainWindow
        self.main_window = MainWindow()
        self.setCentralWidget(MainWindow())
        """

        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ThuePhongWindow()
    window.show()
    sys.exit(app.exec())
