import mysql.connector
from mysql.connector import errorcode
import os

def connect():
    try:
        con = mysql.connector.connect(user='root', password='root', host='localhost', database='EnrollmentDB')
        print('Connection successful')
        return con
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
            con.rollback()

def add(con):
    try:
        while True:
            code = input("Enter Subject Code: ")
            name = input("Enter Subject Name: ")
            units = float(input("Enter Subject Units: "))
            
            cursor = con.cursor()
            sql = "INSERT INTO Subjects (SubjectCode, SubjectName, Units) VALUES (%s, %s, %s)"
            data = (code, name, units)
            
            cursor.execute(sql, data)
            con.commit()

            print('Record saved')
            x = input("Do you want to add another record [y/n]? ")
            if x == 'y':
                os.system('cls')
                continue
            else:
                break

    except mysql.connector.Error as err:
        print(err)
        con.rollback()
    else:
        cursor.close()
        con.close()

def search(con):
    try:
        while True:
            code = input("Enter Subject Code: ")
            
            cursor = con.cursor()
            query = "SELECT * FROM Subjects WHERE SubjectCode = %s"
            data = (code)
            
            cursor.execute(query, data)
            row = cursor.fetchone()
            if row is not None:
                print('Subject Name:', row[1])
                print('Subject Units:', row[2])
            else:
                print("Record not found")

            x = input("Do you want to search another record [y/n]? ")
            if x == 'y':
                os.system('cls')
                continue
            else:
                break

    except mysql.connector.Error as err:
        print(err)
        con.rollback()
    else:
        cursor.close()
        con.close()

def searchAll(con):
    try:
        cursor = con.cursor()
        query = "SELECT * FROM Subjects"
        cursor.execute(query)
        for row in cursor:
            print("Subject Code:", row[0])
            print("Subject Name:", row[1])
            print("Subject Units:", row[2], "\n")

    except mysql.connector.Error as err:
        print(err)
        con.rollback()
    else:
        cursor.close()
        con.close()
        
def main():
    while True:
        print("[1] Add New Record")
        print("[2] Search Record")
        print("[3] Display All Record")
        choice = input("Enter your choice: ")

        if choice == "1":
            os.system('cls')
            c = connect()
            add(c)
        elif choice == "2":
            os.system('cls')
            c = connect()
            search(c)
        elif choice == "3":
            os.system('cls')
            c = connect()
            searchAll(c)

        x = input("Return to main menu [y/n]? ")
        if x == 'y':
            os.system('cls')
            continue
        else:
            break

    exit(0)


main()
