from connection import*   # Import kết nối đến cơ sở dữ liệu
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QDateEdit, QTableWidget, QTableWidgetItem, QSplitter, QMessageBox, QFormLayout,QComboBox
from PyQt5.QtCore import Qt, QDate

class ThuePhongWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sử Dụng Dịch Vụ")
        self.resize(1080, 720)

        # Tạo layout chính
        main_layout = QHBoxLayout()

        # Tạo splitter để chia layout thành hai phần
        splitter = QSplitter(Qt.Horizontal)

        # Phần nhập thông tin
        input_widget = QWidget()
        input_layout = QFormLayout(input_widget)
        input_layout.setVerticalSpacing(20)

        label = QLabel("Điền thông tin yêu cầu dịch vụ", self)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 24px; color: #333;")
        input_layout.addWidget(label)

        labels = ["Mã Thuê", "Dịch Vụ", "Ngày Sử Dụng", "Đơn Giá"]
        self.inputs = []

        for label_text in labels:
            label = QLabel(label_text, self)
            label.setStyleSheet("font-size: 18px; color: #666;")
            input_layout.addWidget(label)
            if label_text == "Ngày Sử Dụng":
                date_edit = QDateEdit(self)
                date_edit.setCalendarPopup(True)
                date_edit.setDate(QDate.currentDate())  # Đặt ngày mặc định là ngày hiện tại
                input_layout.addWidget(date_edit)
                self.inputs.append(date_edit)
                date_edit.setFixedHeight(35)
                
            elif label_text == "Dịch Vụ":
                combo_box = QComboBox(self)
                # Lấy dữ liệu từ cơ sở dữ liệu cho ComboBox
                self.fill_combo_box(combo_box)
                combo_box.setFixedHeight(35)
                input_layout.addWidget(combo_box)
                self.inputs.append(combo_box)
            else:
                line_edit = QLineEdit(self)
                line_edit.setPlaceholderText(f"Nhập {label_text.lower()}")
                line_edit.setFixedHeight(35)  # Đặt kích thước tối thiểu của ô nhập dữ liệu
                input_layout.addWidget(line_edit)
                self.inputs.append(line_edit)

        thue_button = QPushButton("Yêu Cầu", self)
        thue_button.setStyleSheet("font-size: 16px; padding: 7px 10px; background-color: #4CAF50; color: white; border: none; border-radius: 5px; max-width:200px")
        thue_button.setCursor(Qt.PointingHandCursor)
        thue_button.setMinimumWidth(thue_button.sizeHint().width())
        thue_button.clicked.connect(self.su_dung_dich_vu)
        input_layout.addWidget(thue_button)
        splitter.addWidget(input_widget)
        
        huy_button = QPushButton("Hủy Yêu Cầu", self)
        huy_button.setStyleSheet("font-size: 16px; padding: 7px 10px; background-color: #FF0000; color: white; border: none; border-radius: 5px; max-width:200px")
        huy_button.setCursor(Qt.PointingHandCursor)
        huy_button.setMinimumWidth(thue_button.sizeHint().width())
        huy_button.clicked.connect(self.huy_dich_vu)
        input_layout.addWidget(huy_button)
        splitter.addWidget(input_widget)

        # Phần hiển thị cơ sở dữ liệu dưới dạng bảng
        db_display_widget = QWidget()
        db_display_layout = QVBoxLayout(db_display_widget)

        db_label = QLabel("Thông Tin Sử Dụng Dịch Vụ", self)
        db_label.setAlignment(Qt.AlignCenter)
        db_label.setStyleSheet("font-size: 18px; color: #333;")
        db_display_layout.addWidget(db_label)

        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(6)  # Số lượng cột
        self.table_widget.setHorizontalHeaderLabels(["Mã Sử Dụng","Mã Thuê", "Mã Dịch Vụ", "Tên Dịch Vụ", "Ngày Sử Dụng", "Đơn Giá"])
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


    def display_database(self):
        try:
            conn = connect_to_database()
            cursor = conn.cursor()

            # Lấy dữ liệu từ cơ sở dữ liệu
            cursor.execute("SELECT sd.masd, sd.mathue, sd.madichvu, dv.tendichvu, sd.ngaysudung, sd.dongia FROM SuDungDichVu sd JOIN DichVu dv ON sd.madichvu = dv.madichvu;")
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
    


    
    def fill_combo_box(self, combo_box):
          try:
              conn = connect_to_database()
              cursor = conn.cursor()

              # Lấy dữ liệu từ cơ sở dữ liệu
              cursor.execute("SELECT MaDichVu, TenDichVu FROM DichVu")
              records = cursor.fetchall()
              for record in records:
                  ma_dich_vu, ten_dich_vu = record
                  combo_box.addItem(f"{ma_dich_vu} - {ten_dich_vu}")

              cursor.close()
              conn.close()
          except Exception as e:
              print("Error:", e)

    # Hàm xử lý khi nhấn nút Xác Nhận
    def su_dung_dich_vu(self):
        # Lấy thông tin từ các ô nhập liệu
        ma_thue = self.inputs[0].text()
        ma_dich_vu = self.inputs[1].currentText().split(" - ")[0]  # Lấy mã dịch vụ từ ComboBox
        ngay_su_dung = self.inputs[2].date().toString("yyyy-MM-dd")
        don_gia = self.inputs[3].text()

        # Kiểm tra thông tin đã nhập đủ chưa
        if not (ma_thue and ma_dich_vu  and ngay_su_dung and don_gia):
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin.")
            return

        try:
            conn = connect_to_database()
            cursor = conn.cursor()
            # Gọi thủ tục DatPhong
            cursor.callproc("YeuCauDichVu", ( ma_thue, ma_dich_vu, ngay_su_dung, don_gia))
            conn.commit()
      

            QMessageBox.information(self, "Thông báo", "Đặt Dịch Vụ thành công.")
            self.clear_fields()

            cursor.close()
            conn.close()

            # Sau khi đặt phòng thành công, hiển thị lại
            self.display_database()
        except Exception as e:
            QMessageBox.warning(self, "Lỗi", f"Lỗi khi đặt phòng: {e}")



                
    
    # Hủy dịch vụ
    def huy_dich_vu(self):
        ma_thue = self.inputs[0].text()
        ma_dich_vu = self.inputs[1].currentText().split(" - ")[0]  # Lấy mã dịch vụ từ ComboBox
        try:
            conn = connect_to_database()
            cursor = conn.cursor()

            # Gọi thủ tục HuyDichVu với tham số maSD
            cursor.callproc("HuyDichVu", (ma_thue,ma_dich_vu))

            # Commit các thay đổi
            conn.commit()

            QMessageBox.information(self,"Thông Báo", "Hủy Dịch Vụ Thành Công")
            self.clear_fields()

            cursor.close()
            conn.close()

            # Sau khi đặt phòng thành công, hiển thị lại
            self.display_database()
        except Exception as e:
            print("Lỗi:", e)


      # Phương thức để xóa nội dung của các ô nhập liệu sau khi xác nhận
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
