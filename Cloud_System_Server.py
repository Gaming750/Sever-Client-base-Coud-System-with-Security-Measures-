import socket,os,string,re
UDP_PORT = 5001
def discover_server():
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp.bind(("", UDP_PORT))
    print("Listening for server broadcast...")
    while True:
        msg, addr = udp.recvfrom(1024)
        text = msg.decode()
        match = re.search(r"SERVER_IP:(.*)", text)
        if match:
            ip = match.group(1)
            print("FOUND SERVER:", ip)
            return ip
def connect_tcp(ip):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, 1000))
    print("Connected to server!")
    print(client.recv(1024).decode())
server_ip = discover_server()
def recv_until_endmenu(sock):
    data = ""
    while True:
        chunk = sock.recv(1024).decode()
        data += chunk
        if "ENDMENU" in data:
            break
    return data.replace("ENDMENU", "")
def find_file_os(filename):
    drives = [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]
    results = []
    for drive in drives:
        for root, dirs, files in os.walk(drive):
            if filename in files:
                full_path = os.path.join(root, filename)
                results.append(full_path)
    return results
tries=0
server_ipa=server_ip
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((server_ipa,1000))
print("Connected to Server")
locked_gmails=[]
while True:
    data=recv_until_endmenu(client)
    print('\n'+data)
    choice=input("Enter your Choice:")
    client.sendall(choice.encode())
    if choice=='1':
        client.sendall(input("Enter your Gmail:").encode())
        data=client.recv(1024).decode()
        if data=='0':
            print("Invalid Gmail Format")
            continue
        password=input("Enter your Password:")
        client.sendall(password.encode())
        data=client.recv(1024).decode()
        if data=='0':
            print("Password is too Short in Length")
            continue
        password_0=input("Confirm Password:")
        client.sendall(password_0.encode())
        if password!=password_0:
            print("Password Do not match retry:")
            continue
        data=client.recv(1024).decode()
        client.sendall(input(data).encode())
        data=client.recv(1024).decode()
        client.sendall(input(data).encode())
        happen=client.recv(1024).decode()
        if happen=='0':
            print("Something Went Wrong on the Server Side:")
        elif happen=='1':
            print("Registration Success!")
    elif choice=='2':
        Gmail=input("Enter Gmail:")
        client.sendall(Gmail.encode())
        data=client.recv(1024).decode()
        if data=='s':
            print("Account is Locked Due to suspicious Activity:")
            continue
        elif data=='o':
            pass
        data=client.recv(1024).decode()
        if data=='0':
            print("Gmail not found please Register First:")
            continue
        if tries<3:
            client.sendall(input(data).encode())
            data=client.recv(1024).decode()
            print(data)
            if data=='1':
                print("Logged In Successfully:")
                continue
            elif data=='0':
                print('Invalid Password:')
                continue
            tries+=1
        elif tries>=3:
            prompt=client.recv(1024).decode()
            print(prompt)
            tries=0
            continue
    elif choice=='3':
        login_status=client.recv(1024).decode()
        if login_status=='1':
            while True:
                data=client.recv(1024).decode()
                choice_c=input(data)
                client.sendall(choice_c.encode())
                if choice_c=='1':
                    while True:
                        file_name=input("Enter the File Name with extension only Our System will automatically Find it:")
                        client.sendall(file_name.encode())
                        if file_name=='q':
                            break
                        data=client.recv(1024).decode()
                        print(data)
                        print("Searching For file...")
                        file_path_p=find_file_os(file_name)
                        if len(file_path_p)==0:
                            print("file not found:")
                            client.sendall('0'.encode())
                            continue
                        file_path=file_path_p[0]
                        file_size=os.path.getsize(file_path)
                        client.sendall(str(file_size).encode())
                        with open(file_path,'rb') as f:
                            client.sendfile(f)
                        data=client.recv(1024).decode()
                        if data=='1':
                            print("Transfer Was a Success:")
                elif choice_c=='2':
                    while True:
                        dir_str=client.recv(1024).decode()
                        dir_list=dir_str.split('\n')
                        better_show_it=''
                        no=1
                        for i in dir_list:
                            if i:
                                better_show_it+=f'{no}:{i}\n'
                                no+=1
                        print("\nYour Directory has\n"+better_show_it)
                        file_name_choice=input("Enter File number To transfer:")
                        client.sendall(file_name_choice.encode())
                        if file_name_choice=='q':
                            print("Going Back:")
                            break
                        file_name=dir_list[int(file_name_choice)-1]
                        client.sendall(file_name.encode())
                        file_size=int(client.recv(1024).decode())
                        print(f'file size is {file_size}')
                        received = 0
                        save_path = os.path.join(
                            os.path.dirname(os.path.abspath(__file__)),
                            "Received_" + file_name
                        )
                        with open(save_path, "wb") as f:
                            while received < file_size:
                                chunk = client.recv(4096)
                                if not chunk:
                                    break
                                f.write(chunk)
                                received += len(chunk)
                        client.sendall(b'1')
                        print("File is Saved in your this Directory")  
                elif choice_c=='3':
                    print("Request Server to Go Back")
                    break
        else:
            data=client.recv(1024).decode()
            print("Not logged IN")
    else:
        data=client.recv(1024).decode()
        print(data)
        continue
