import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password ="password",
    database="c300"
    
)


from guizero import App,Text,TextBox,PushButton,info
from gpiozero import LED
from gpiozero import Button

button = Button(22)
avail = LED(17)
lock = LED(27)

avail.on()
lock.on()

app = App("Lost and Found",height = 300,width = 450)
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password ="password", 
    database="c300"
    
)


from guizero import App,Text,TextBox,PushButton,info,Picture
from gpiozero import LED
from gpiozero import Button

button = Button(22)
avail = LED(17)
lock = LED(27)

avail.on()
lock.on()

app = App("Lost and Found",height = 300,width = 450)
picture = Picture(app,image="rplogo.png")
message = Text(app, text = "Welcome to Lost and Found", size= 20,font = "Arial", color="Green",align ="top")

message = Text(app, text = "Please enter ID",align ="top")
uid = TextBox(app,width =20, align ="top")

def check():
    check_uid = uid.value
    if check_uid =="":
        info("", "Please enter ID")
    else:
        item_id = ""
        locker_size = ""
        in_use = 0
        check = mydb.cursor()
        no_of_row = "SELECT * FROM item_details"
        check.execute(no_of_row)
        record = check.fetchall()
        
        for row in record:
            if check_uid == row[0]:
                item_id = row[0]
                locker_size = row[1]
                in_use = row[3]
    
    if item_id == "":
        info("","Please enter valid ID")
    elif in_use > 0:
        info("", "Lost item has already been deposited")
    elif locker_size == "C":
        info("", "Please deposit item into General Chute.")
    else:
        lock.off()
        info("", "Please deposit item into locker.")
        button.wait_for_press()
        avail.off()
        lock.on()
        update = mydb.cursor()
        update_detail = """UPDATE item_details SET in_use = 1 WHERE id = %s"""
        update.execute(update_detail,(item_id,))
        mydb.commit()
        info("", "Thank you for the lost item deposit")
        


check_avail = PushButton(app,text = "Submit",command=check)
app.display
