import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="c3000"
)
# Loop to check if ID matches
while True:
    idnChecker = input("Please Enter the ID provided:- ")

    mycursor = mydb.cursor()
    number_of_row = "SELECT * FROM item_details"
    mycursor.execute(number_of_row)
    record = mycursor.fetchall()

    item_id = ""
    lockersize = ""

    for row in record:
        if idnChecker == row[0]:
            item_id = row[0]
            lockersize = row[1]

    print(item_id)
    print(lockersize)
