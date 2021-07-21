import mysql.connector
import string
import random
import datetime

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password ="password", 
    database="c300"
    
)

getData = mydb.cursor()
updateData = mydb.cursor()
addData = mydb.cursor()

from guizero import App,Text,TextBox,PushButton,info,Picture,Window,ButtonGroup,Box
from gpiozero import LED
from gpiozero import Button

def reportItem():
    app.hide()
    window1.show()
    
def submitItem():
    app.hide()
    message.append("Submit Lost Item")
    window.show()
    
def retrieveItem():
    app.hide()
    message.append("Retrieve Lost Item")
    window.show()
    

def confirm():
    check_uid = uid.value
    if check_uid =="":
        info("", "Please enter ID")
    else:      
        number_of_row = "SELECT * FROM item_information WHERE Locker_Assigned IS NULL AND item_id = %s "
        
        idsql = (check_uid,)
        getData.execute(number_of_row, idsql)
        record = getData.fetchall()
        
        if record == []:
            info("","Invalid ID")
        else:
            for row in record:
                locker_size_assigned = row[4]
                
                locker_assigned = row[9]
                
                
            if locker_size_assigned == "C":
                locker_availability = "SELECT * FROM locker WHERE LOCKER_STATUS = 'A' " \
                                  "AND LOCKER_SIZE = %s ORDER BY LOCKER_ID ASC LIMIT 0, 1 "
                values = ("C",)
                
                getData.execute(locker_availability, values)
                locker_record = getData.fetchone()
                
                locker_id = locker_record[0]
                led = locker_record[4]
                button = locker_record[3]
            
            else:
                j = True
                while j:
                    
                    
                    locker_availability = "SELECT * FROM locker WHERE LOCKER_STATUS = 'A' " \
                                          "AND LOCKER_SIZE = %s ORDER BY LOCKER_ID ASC LIMIT 0, 1 "
                    values = (locker_size_assigned,)
                    
                    getData.execute(locker_availability, values)
                    locker_record = getData.fetchone()
                    alchecker = getData.rowcount
                    
                    if alchecker == -1:
                        if locker_size_assigned == "S":
                            locker_size_assigned = "M"
                            continue
                            
                        elif locker_size_assigned == "M":
                            locker_size_assigned = "L"
                            continue
                            
                            
                        else:
                            locker_availability = "SELECT * FROM locker WHERE LOCKER_STATUS = 'A' " \
                                  "AND LOCKER_SIZE = %s ORDER BY LOCKER_ID ASC LIMIT 0, 1 "
                            values = ("C",)
                            
                            getData.execute(locker_availability, values)
                            locker_record = getData.fetchone()
                            
                            locker_id = locker_record[0]
                            led = locker_record[4]
                            button = locker_record[3]
                            
                            j = False
                            break
                            
                        
                        
                    else:
                        
                        getData.execute(locker_availability, values)
                        
                        locker_record = getData.fetchone()
                        locker_id = locker_record[0]
                        led = locker_record[4]
                        button = locker_record[3]
                        
                        j = False
                        break
                            

            
            update_locker = "UPDATE locker SET Locker_Status = %s WHERE Locker_id = %s "
            locker_updated = ("NA", locker_id)
            updateData.execute(update_locker, locker_updated)
            mydb.commit()

            
            update_locker = "UPDATE item_information SET Locker_Assigned = %s WHERE item_id = %s "
            locker_updated = (locker_id, check_uid)
            
            updateData.execute(update_locker, locker_updated)
            mydb.commit()
            
    
            window2.show()
            
            
            button_gpio = Button(button)
            lock_gpio = LED(led)
            lock_gpio.on()
            button_gpio.wait_for_press()
            lock_gpio.off()
            window2.hide()
            info("","Thank You for Depositing Lost Item")
            
            now = datetime.datetime.now()
            
            mystatuscursor = mydb.cursor()
            update_locker = "UPDATE item_information SET Status = %s WHERE item_id = %s"
            locker_updated = ('DP',check_uid)
            mystatuscursor.execute(update_locker, locker_updated)
            mydb.commit()
            
            mystatuscursor = mydb.cursor()
            update_locker = "UPDATE item_information SET Time_Deposited = %s WHERE item_id = %s"
            locker_updated = (now,check_uid)
            mystatuscursor.execute(update_locker, locker_updated)
            mydb.commit()
            
            
            
                        

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def Check():
    getFinder = "SELECT * FROM finder_information WHERE finder_name = %s AND finder_email = %s "
    Find = (name.value, email.value)
    getData.execute(getFinder, Find)
    
        
def confirmReport():
    sql_id = 1
    chk_name = name.value
    chk_email = email.value
    chk_descrip = description.value
    chk_location = location.value
    if chk_name=="" or chk_email=="" or chk_descrip == "" or chk_location =="":
        info("", "Please enter your name, email, item description, and location found")
        print(choice.value)
    else:
        
        while True:
            rdmid = id_generator(6, "QWERTYUIOPASDFGHJKLZXCVBNM123456789")
            
            rIdChecker = "SELECT * FROM item_information WHERE item_id = %s "
            rValues = (rdmid,)
            getData.execute(rIdChecker, rValues)
            rLocker_record = getData.fetchall()
            rChecker = getData.rowcount
        
            if rChecker == 1:
                continue
            else:
                now = datetime.datetime.now()
                Check()
                fInfo = getData.fetchall()
                fInfoCheck = getData.rowcount
                
                if fInfoCheck == 1:
                    for row in fInfo:
                        sql_id = row[0]
                        break
                else:
                    addFind = "INSERT INTO finder_information (finder_name, finder_email) VALUES (%s, %s)"
                    valFind = (chk_name, chk_email)
                    addData.execute(addFind, valFind)
                    mydb.commit()
                    
                    getId = addData.fetchall()
                    for row in getId:
                        sql_id =row[0]
                        
                
            break
        if choice.value == "Card":
            size = "S"
        elif choice.value == "Wallet":
            size = "M"
        elif choice.value == "Phone":
            size = "L"
        else:
            size = "C"
        
        itemInfo = "INSERT INTO item_information (item_id, item_description, item_Last_Found, Locker_Size_Assigned,status, time_reported, reported_user ) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        addItem = (rdmid, chk_descrip, chk_location, size, "RP", now, sql_id)
        addData.execute(itemInfo, addItem)
        mydb.commit()
        print(rdmid)
        print(description.value)
        print(location.value)
        print(size)
        print(now)
        print(sql_id)
        
            
        
        


        
        
        info("","Submitted")
    
    
    
def Close():
    app.show()
    window.hide()
    uid.clear()
    message.clear()
    window1.hide()
    name.clear()
    email.clear()
    description.clear()
    
    
    
# GUI
app = App("Lost and Found",height = 300,width = 450)
picture = Picture(app,image="rplogo.png")
Text(app, text = "Welcome to Lost and Found", size= 20,font = "Arial")
#Buttons to report, submit, and retrieve button
reportItem = PushButton(app,text = "Report lost item",command=reportItem)
submitItem = PushButton(app,text = "Submit lost item",command=submitItem)
retrieveItem =PushButton(app,text = "  Retrieve item   ",command=retrieveItem)
app.display

#Form for Submit/Retrieve lost item
window = Window(app, title= " ",height = 300,width = 450)
window.hide()
picture = Picture(window,image="rplogo.png")
message = Text(window, size=14)
Text(window)
Text(window, text = "Please enter ID")
uid = TextBox(window,width =20)
#Layout for buttons
formBox = Box(window,layout="grid")
PushButton(formBox,text = "Confirm",command=confirm, grid=[0,0])
PushButton(formBox,text = "Close",command=Close, grid=[1,0])


#Form for reporting lost item
window1 = Window(app, title= " ",height = 450,width = 450)
window1.hide()
picture = Picture(window1,image="rplogo.png")
message1 = Text(window1, text="Please enter item details",font="Arial")
Text(window1)
#Layout for user to enter item details
formBox1 = Box(window1,layout="grid")
Text(formBox1, grid=[0,0],text="Name*")
name = TextBox(formBox1, grid=[1,0],width=20)
Text(formBox1, grid=[0,1], text="Email*")
email = TextBox(formBox1, grid=[1,1],width=20)

Text(formBox1, grid=[0,2],text="Item Type")
choice = ButtonGroup(formBox1,
            options=["Card", "Wallet", "Phone","Others"],
            selected="Card",grid=[1,2],align="left" )





Text(formBox1, grid=[0,3],text="Item Description")
description = TextBox(formBox1, grid=[1,3],width=20)
Text(formBox1, grid=[0,4],text="Location Found")
location = TextBox(formBox1, grid=[1,4],width=20)
Text(window1)
#Layout for buttons
formBox2 = Box(window1,layout="grid")
PushButton(formBox2,text = "Confirm",command=confirmReport, grid=[0,0])
PushButton(formBox2,text = "Close",command=Close, grid=[1,0])

window2 = Window(app, title= " ",height = 200,width = 600)
Text(window2, text="Please Deposit Item into Locker")
window2.hide()


