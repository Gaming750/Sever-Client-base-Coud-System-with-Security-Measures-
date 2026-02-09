A Python + MySQL based secure cloud platform with user authentication, hashed passwords, brute-force protection, and file upload/download.

 Overview

This project is a secure cloud storage system built using:

Python (Client/Server)

MySQL Database

bcrypt password hashing

Socket programming (TCP & UDP)

File upload/download over the network

Automatic LAN server discovery (UDP broadcast)

It enables users to:

Register securely

Log in with brute-force protection

Upload files to their personal cloud

Download their stored files

Store passwords safely using bcrypt

Prevent hacking or automated login attacks

 Features
 1. Secure User Authentication

Passwords hashed using bcrypt

Email validation

Phone number & name stored safely

Duplicate email protection

 2. Brute Force Protection

Maximum 3 failed login attempts

Account temporarily locked for the session

Prevents automated password-guessing attacks

 3. File Storage System

Each user gets a unique folder:

/Data_base_work/<user_id>/


Secure file upload using sendfile()

Accurate file-size tracking

Server acknowledges successful uploads

 4. Server Auto-Discovery

Uses UDP broadcast packets

Clients automatically detect server IP on LAN

No manual IP entry required

 5. Client/Server Architecture

Server manages database + cloud storage

Client provides interactive CLI interface

 Database Structure

Database Name: security

Table: user_data
Column	Type	Description
id	INT (PK)	Auto increment user ID
name	VARCHAR(50)	User’s full name
email	VARCHAR(50)	Unique email
phone_number	VARCHAR(20)	Contact number
password	VARCHAR(255)	Bcrypt hashed password

Create Table SQL

CREATE TABLE user_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(50) UNIQUE,
    phone_number VARCHAR(20),
    password VARCHAR(255)
);

 Security Mechanisms
 Password Hashing

Passwords are stored like:

hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
cursor.execute("INSERT INTO user_data (name,email,phone_number,password) VALUES (%s,%s,%s,%s)",
               (name, Gmail, phone_no, hashed))

 Brute Force Blocking

3 failed login attempts → temp lock

User must return to main menu before retrying

Protects against hacking tools

 User File Isolation

Each user has a dedicated directory

No user can access directory of another user

 How It Works
 Client Tasks

Sends registration & login data

Uploads local files

Downloads cloud files

Auto-discovers server IP

 Server Tasks

Validates requests

Handles database operations

Stores files in respective user directory

Sends file lists & file data to client

 Folder Structure
/project-root
│
├── server.py
├── client.py
├── README.md
└── /Data_base_work/
     └── <user_id>/
          └── user_files_here

 How to Run
1. Start MySQL

Create database:

CREATE DATABASE security;


Run the table creation SQL (see above).

2. Run Server
python server.py


Server will start:

Broadcasting itself over LAN

Listening on TCP port 1000

3. Run Client
python client.py


Client will:

Automatically detect server IP

Show menu options

 Features Demo (Quick Preview)
Register
Enter Gmail:
Enter Password:
Confirm Password:
Enter Phone:
Enter Name:
Registration Successful!

Login
Enter Gmail:
Gmail Found
Enter Password:
Login Successful!

Upload File
1: Upload File
Enter file name:
Uploading...
DONE

Download File
Available files:
file1.txt
image.png

Enter file name:
Downloading...
SUCCESS

 Why This System Is Secure

✔ bcrypt hashing
✔ No plain-text passwords
✔ Account lockout
✔ Isolated user storage
✔ Data integrity checks
✔ No direct database access from client

👤 Author

Your Name
Secure Cloud Storage – Python/MySQL Project

📜 License

This project is open source under the MIT License.
