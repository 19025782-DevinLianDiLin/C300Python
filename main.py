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

message = Text(app, text = "Welcome to Lost and Found", size= 20,font = "Arial", color="Green")

uid = TextBox(app,width =20)
in_use = 0
item_id = ""
locker_size = ""
def check():
    check_uid = uid.value
    if check_uid =="":
        info("", "Please enter ID")
    else:
        item_id = ""
        locker_size = ""
        in_use = 0
        mycursor = mydb.cursor()
        no_of_row = "SELECT * FROM item_details"
        mycursor.execute(no_of_row)
        record = mycursor.fetchall()
    
        for row in record:
            if check_uid == row[0]:
                item_id = row[0]
                locker_size = row[1]
                in_use = row[3]
    
    if item_id == "":
        info("","Please enter valid ID")
    elif in_use > 0:
        info("", "Lost item is already in locker")
    else:
        
        info("", "Please desposit item into locker.")
        #lock.off()
        #button.wait_for_press()
        #avail.off()
        #lock.on()
        my2ndcursor = mydb.cursor()
        update_detail = "UPDATE item_details SET in_use = %d WHERE id = %s"
        val = (1,item_id)
        my2ndcursor.execute(update_detail,val)
        mydb.commit()
        info("", "Thank you for the lost item deposit")
        


check_avail = PushButton(app,text = "Confirm Unique ID",command=check)
app.display


