import socket, threading, time, os, mysql.connector, bcrypt
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except:
        return "127.0.0.1"
    finally:
        s.close()
def get_broadcast(ip):
    p = ip.split(".")
    return f"{p[0]}.{p[1]}.{p[2]}.255"
SERVER_IP = get_local_ip()
BROADCAST_IP = get_broadcast(SERVER_IP)
SERVER_PORT = 1000
def broadcast_ip():
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    while True:
        udp.sendto(f"SERVER_IP:{SERVER_IP}".encode(), (BROADCAST_IP, 5001))
        time.sleep(0.2)
def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='10by10is1',
        database='security'
    )
def send_menu(conn):
    menu = (
        "Welcome to our cloud Site please choose the options according to your needs\n"
        "1: Register user\n"
        "2: Login\n"
        "3: Access your Cloud\n"
        "ENDMENU\n"
    )
    conn.sendall(menu.encode())
def Gmail_checker(gmail):
    return gmail if '@gmail.com' in gmail else 0
def get_user_id(gmail):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT email,id FROM user_data')
    result = cursor.fetchall()
    for i in range(len(result)):
        if gmail == result[i][0]:
            return result[i][1]
def handle_client(conn, addr):
    print("Client connected:", addr[0])
    conn.sendall(b"Connected OK")  
    Logged_IN_STATUS = False
    tries = 0
    locked_accounts = []
    Gmail_good = ""  
    db = connect_db()
    cursor = db.cursor()
    while True:
        time.sleep(1.2)
        try:
            send_menu(conn)
            choice = conn.recv(1024).decode()
        except:
            print(f"Client {addr[0]} disconnected.")
            break
        print(f"User {addr[0]} chose {choice}")
        if choice == '1':
            conn.sendall('Enter your Gmail'.encode())
            Gmail = conn.recv(1024).decode()
            if Gmail_checker(Gmail) == 0:
                conn.sendall('0'.encode())
                continue
            print(f"User Gmail is {Gmail}")    
            conn.sendall('Enter Your password:'.encode())
            password = conn.recv(1024).decode()
            if len(password) < 8:
                conn.sendall('0'.encode())
                continue
            password_0 = conn.recv(1024).decode()
            if password != password_0:
                print("Password Do not Match Previous Password try again:")
                continue    
            conn.sendall('Enter Phone number'.encode())
            phone_no = conn.recv(1024).decode()
            conn.sendall('Enter your Name:'.encode())
            name = conn.recv(1024).decode()
            print(f"User Name is {name}")
            try:
                hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                cursor.execute(
                    "INSERT INTO user_data (name,email,phone_number,password) VALUES (%s,%s,%s,%s)",
                    (name, Gmail, phone_no, hashed)
                )
                db.commit()
                print("Successful Registration")
                conn.sendall('1'.encode())
                cursor.execute('SELECT email FROM user_data')
                result = cursor.fetchall()
                for i in range(len(result)):
                    if Gmail in result[i][0]:
                        id = i + 1
                os.makedirs(str(id), exist_ok=True)
            except mysql.connector.Error as er:
                print('Something went Wrong Error code', er)
                conn.sendall('0'.encode())
        elif choice == '2':
            gmail = conn.recv(1024).decode()
            if gmail in locked_accounts:
                conn.sendall('s'.encode())
                continue
            else:
                conn.sendall('o'.encode())     
            cursor.execute('SELECT email FROM user_data')
            result = cursor.fetchall()
            found = False
            for i in range(len(result)):
                if gmail == result[i][0]:
                    conn.sendall("Gmail Found:\nEnter Your Password to login:".encode())
                    id = i
                    found = True
            if not found:
                conn.sendall('0'.encode())
                continue      
            user_password = conn.recv(1024).decode()
            cursor.execute("SELECT id, password FROM user_data WHERE email=%s", (gmail,))
            row = cursor.fetchone()
            user_id, db_hash = row
            if tries < 3:
                if bcrypt.checkpw(user_password.encode(), db_hash.encode()):
                    print("Login success")
                    Logged_IN_STATUS = True
                    Gmail_good = gmail
                    conn.sendall('1'.encode())
                else:
                    print("Invalid password")
                    conn.sendall('0'.encode())
                tries += 1
            else:
                prompt = 'Account Locked'
                print(prompt)
                locked_accounts.append(gmail)
                conn.sendall(prompt.encode())
                tries = 0
                continue
        elif choice == '3':
            conn.sendall(('1' if Logged_IN_STATUS else '0').encode())
            if Logged_IN_STATUS:
                while True:
                    conn.sendall('Make your Choice:\n1:Upload File\n2:Download file from your Cloud\n3:Quit/Back'.encode())
                    user_id = get_user_id(Gmail_good)
                    choice_n = conn.recv(1024).decode()
                    if choice_n == '1':
                        while True:
                            file_name = conn.recv(1024).decode()
                            if file_name == 'q':
                                break
                            conn.sendall('Ready for Transfer:'.encode())
                            file_size_str = conn.recv(1024).decode()
                            if file_size_str == '0':
                                print("Client could not find the file retrying:")
                                continue
                            file_size = int(file_size_str)
                            path = f'D:/University/Programming/Data_base_work/{user_id}/{file_name}'
                            received = 0
                            with open(path, 'wb') as f:
                                while received < file_size:
                                    data = conn.recv(4096)
                                    if not data:
                                        break
                                    f.write(data)
                                    received += len(data)
                            print('DONE:')
                            conn.sendall('1'.encode())
                    elif choice_n == '2':
                        while True:
                            result = ''
                            id = get_user_id(Gmail_good)
                            for i in os.listdir(str(user_id)):
                                result += i + '\n'
                            conn.sendall(result.encode())
                            data = conn.recv(1024).decode()
                            if data == 'q':
                                break
                            file_name = conn.recv(1024).decode()
                            dir_list = os.listdir(str(user_id))
                            path = f'D:/University/Programming/Data_base_work/{user_id}/{file_name}'
                            size = os.path.getsize(path)
                            conn.sendall(str(size).encode())
                            with open(path, "rb") as f:
                                conn.sendfile(f)
                            ack = conn.recv(1024).decode()
                            if ack == '1':
                                print("Client Got the file Successfully")
                    elif choice_n == '3':
                        break
            else:
                conn.sendall('0'.encode())
        else:
            conn.sendall('Invalid Choice:'.encode())
            continue
threading.Thread(target=broadcast_ip, daemon=True).start()
def start_tcp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((SERVER_IP, SERVER_PORT))
    server.listen()
    print("TCP Server running on", SERVER_IP)
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
start_tcp_server()