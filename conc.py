#import mysql.connector

# Replace 'username', 'password', 'host', and 'database' with your MySQL credentials
#cnx = mysql.connector.connect(user='freedb_qtdl123', password='$NFCygvs#bpwT3R',
#                              host='sql.freedb.tech',
#                              database='freedb_quantridulieu')

# Perform database operations here

  # Close the connection when done

#mycursor = cnx.cursor()

import mysql.connector

def connect_to_database():
    # Kết nối đến cơ sở dữ liệu
    conn = mysql.connector.connect(
        host="sql.freedb.tech",
        user="freedb_qtdl123",
        password="$NFCygvs#bpwT3R",
        database="freedb_quantridulieu"
    )
    return conn

