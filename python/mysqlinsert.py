import mysql.connector

def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="itc123",
        database="challenge1"
    )

def insert_data(cursor):
    name = input("Enter name: ")
    age = int(input("Enter value: "))

    insert_query = "INSERT INTO testing (name, value) VALUES (%s, %s)"
    cursor.execute(insert_query, (name, age))

    print("Record inserted successfully into testing table")

def select_data(cursor):
    cursor.execute("SELECT * FROM testing")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def main():
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        while True:
            print("\n1. Insert Data\n2. Select Data\n3. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                insert_data(cursor)
                connection.commit()
            elif choice == '2':
                select_data(cursor)
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please enter a valid option.")

    except mysql.connector.Error as error:
        print("Error while connecting to MySQL", error)

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()

if __name__ == "__main__":
    main()
