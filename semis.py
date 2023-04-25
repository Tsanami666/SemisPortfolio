import mysql.connector
from mysql.connector import errorcode
import os

def connect():
    try:
        con = mysql.connector.connect(user = "root", password = "root", host = "localhost", database = "SemisDB")
        print("connection successful")
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
            char_ID = input("Enter Character ID: ")
            code = input("Enter Agent Name: ")
            name = input("Enter Character Real Name: ")
            role = input("Enter Character Role: ")
            country = input("Enter Character Country of Origin: ")

            cursor = con.cursor()
            sql = "INSERT INTO Characters (char_id, code_name, real_name, agent_type, country_orig) VALUES (%s, %s, %s, %s, %s)"
            data = (char_ID, code, name, role, country)

            cursor.execute(sql, data)
            con.commit()

            print('Record saved')
            x = input("Do you want to add another Agent [y/n]? ")
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


def retrieve(con):
    print("[1] Search for an Agent")
    print("[2] Display All Agents")
    choice = input("Enter choice: ")
    if choice == "1":
        os.system('cls')
        try:
            while True:
                code = input("Enter Agent Name: ")

                cursor = con.cursor()
                query = "SELECT * FROM Characters WHERE code_name = %s"
                data = (code,)

                cursor.execute(query, data)
                row = cursor.fetchone()
                if row is not None:
                    print('Character ID', row[0])
                    print('Agent Name', row[1])
                    print('Character Name', row[2])
                    print('Agent Role', row[3])
                    print('Character Origin', row[4])
                else:
                    print("Record Not Found")
                
                x = input("Do You Want To Search Another Agent [y/n]? ")
                if x == 'y':
                    os.system('cls')
                    continue
                else:
                    os.system('cls')
                    break
        except mysql.connector.Error as err:
            print(err)
            con.rollback()
        else:
            cursor.close()
            con.close()
    elif choice == '2':
        try:
            cursor = con.cursor()
            query = "SELECT * FROM Characters"

            cursor.execute(query)
            for row in cursor:
                print('Character ID', row[0])
                print('Agent Name', row[1])
                print('Character Name', row[2])
                print('Agent Role', row[3])
                print('Character Origin', row[4], "\n")
        except mysql.connector.Error as err:
            print(err)
            con.rollback()
        else:
            cursor.close()
            con.close()
    else:
        print("Choice Should Be [1] and [2] only")
        os.system('cls')
        c = connect()
        retrieve(c)


def update(con):
    try:
        while True:
            code = input("Enter Agent Name: ")
            cursor = con.cursor()
            sql = "SELECT * FROM Characters WHERE code_name = '%s'" % code
            cursor.execute(sql)
            results = cursor.fetchall()

            if not results:
                print("No record found for Agent Name:", code)
                break

            for row in results:
                print("ID:", row[0])
                print("Code Name:", row[1])
                print("Real Name:", row[2])
                print("Role:", row[3])
                print("Country of Origin:", row[4])

            char_ID = input("Enter Character ID to update: ")
            print("[code_name] [real_name] [agent_type] [country_orig]")
            print("[all] to update entire record")
            field = input("Enter Field to update : ")

            if field == 'all':
                code = input("Enter new Agent Code Name: ")
                name = input("Enter new Character Real Name: ")
                role = input("Enter new Character Role: ")
                country = input("Enter new Character Country of Origin: ")
                sql = "UPDATE Characters SET code_name = '%s', real_name = '%s', agent_type = '%s', country_orig = '%s' WHERE char_id = '%s'" % (code, name, role, country, char_ID)
            elif not field:
                break
            else:
                new_value = input(f"Enter new value for {field}: ")
                sql = f"UPDATE Characters SET {field} = '{new_value}' WHERE char_id = '{char_ID}'"

            cursor.execute(sql)
            con.commit()

            print(cursor.rowcount, "record(s) affected")
            x = input("Do You Want To Update Another Record [y/n]? ")
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


def delete(con):
    try:
        while True:
            cursor = con.cursor()
            query = "SELECT code_name FROM Characters"

            cursor.execute(query)
            print("Available code names:")
            for row in cursor:
                print(row[0])

            code = input("Enter Agent Name (press enter to exit): ")

            if not code:
                break

            cursor = con.cursor()
            sql = "DELETE FROM Characters WHERE code_name = '%s'" % code
            
            cursor.execute(sql,)
            con.commit()

            print("Agent deleted")
            x = input("Do you want to delete another agent information [y/n]? ")
            if x == 'y':
                os.system('cls')
                continue
            else:
                os.system('cls')
                break
    except mysql.connector.Error as err:
        print(err)
        con.rollback()
    else:
        cursor.close()
        con.close()
    

def main():
   while True:
       print("[1] Add An Agent")
       print("[2] Search Record")
       print("[3] Update Record")
       print("[4] Delete a Record")
       choice = input("Enter your choice : ")

       if choice == "1":
           os.system('cls')
           c = connect()
           add(c)
       elif choice == "2":
           os.system('cls')
           c = connect()
           retrieve(c)
       elif choice == "3":
           os.system('cls')
           c = connect()
           update(c)
       elif choice == "4":
           os.system('cls')
           c = connect()
           delete(c)

       x = input("Return to main menu [y/n]? ")
       if x == 'y':
           os.system('cls')
           continue
       else:
           os.system('cls')
           break

       exit(0)


main()


