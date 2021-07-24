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
from time import sleep

def reportItem():
    app.hide()
    windowReport.show()
    
def submitItem():
    app.hide()
    window.show()
    
def retrieveItem():
    app.hide()
    window1.show()
    
def assignChute():
    locker_availability = "SELECT * FROM locker WHERE LOCKER_STATUS = 'A' " \
                                  "AND LOCKER_SIZE = %s ORDER BY LOCKER_ID ASC LIMIT 0, 1 "
    values = ("C",)
    
    getData.execute(locker_availability, values)
    locker_record = getData.fetchone()
    
    locker_id = locker_record[0]
    led = locker_record[4]
    button = locker_record[3]
    
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def confirm():
    check_uid = uid.value
    if check_uid =="":
        info("", "Please enter ID")
        
    else:      
        number_of_row = "SELECT * FROM item_information WHERE Locker_Assigned IS NULL AND item_deposit_id = %s "
        
        idsql = (check_uid,)
        getData.execute(number_of_row, idsql)
        record = getData.fetchall()
        
        if record == []:
            info("","Invalid ID")
        else:
            for row in record:
                id = row[0]
                locker_size_assigned = row[5]
                
                    
            if locker_size_assigned == "C":
                assignChute()
                
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
                            assignChute()
                            
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
                    
            uid.clear()
            update_locker = "UPDATE locker SET Locker_Status = %s WHERE Locker_id = %s "
            locker_updated = ("NA", locker_id)
            updateData.execute(update_locker, locker_updated)
            mydb.commit()

            
            update_locker = "UPDATE item_information SET Locker_Assigned = %s WHERE item_deposit_id = %s "
            locker_updated = (locker_id, check_uid)
            
            updateData.execute(update_locker, locker_updated)
            mydb.commit()
            
            if button == 0 and led == 0:
                info("","Test")
            else:
                button_gpio = Button(button)
                lock_gpio = LED(led)
                lock_gpio.on()
                info("","Please deposit item into Locker")
                button_gpio.wait_for_press()
                lock_gpio.off()

            
            info("","Thank You for Depositing Lost Item")
            
            now = datetime.datetime.now()
            
            
            update_locker = "UPDATE item_information SET Status = %s WHERE item_deposit_id = %s"
            locker_updated = ('DP',check_uid)
            updateData.execute(update_locker, locker_updated)
            mydb.commit()
            
            
            update_locker = "UPDATE item_information SET Time_Deposited = %s WHERE item_deposit_id = %s"
            locker_updated = (now,check_uid)
            updateData.execute(update_locker, locker_updated)
            mydb.commit()
            
            while True:
                rdmid2 = id_generator(6, "QWERTYUIOPASDFGHJKLZXCVBNM123456789")
            
                rIdChecker = "SELECT * FROM item_information WHERE Item_Retrieve_Id = %s "
                rValues = (rdmid2,)
                getData.execute(rIdChecker, rValues)
                rLocker_record = getData.fetchall()
                rChecker = getData.rowcount
                
                if rChecker == 1:
                    continue
                else:
                    itemInfo2 = "UPDATE item_information SET Item_Retrieve_ID = %s WHERE id = %s"
                    addItem2 = (rdmid2,id)                 
                    addData.execute(itemInfo2, addItem2)
                    mydb.commit()
                    False
                    break
            
            
            
            
def retrieve():
    check_uid = uid1.value
    if check_uid =="":
        info("", "Please enter ID")
        
    
        
    else:
        IdCheckSQL = "SELECT * FROM item_information WHERE Status = %s AND Item_Retrieve_Id = %s"
        IdCheckSQLVar = ('DP', check_uid)
        getData.execute(IdCheckSQL, IdCheckSQLVar)
        IdCheckSQLResult = getData.fetchone()
        IdChecker = getData.rowcount

        if IdChecker == 1:
            
            getData.execute(IdCheckSQL, IdCheckSQLVar)
            IdCheckSQLResult = getData.fetchone()
            
            
            
            locker_assigned = IdCheckSQLResult[10]
                
            
            
            lockerinfo = "SELECT * FROM locker WHERE locker_id = %s"
            lockerinfovar = (locker_assigned,)
            getData.execute(lockerinfo, lockerinfovar)
            locker_record = getData.fetchone()
            
            led = locker_record[4]
            button = locker_record[3]
            button_gpio = Button(button) 
            lock_gpio = LED(led)
            lock_gpio.on()
            info("","Please retrieve item from Locker " + str(locker_assigned))
            button_gpio.wait_for_press()
            lock_gpio.off()
            
            
            
            update_locker = "UPDATE item_information SET Status = %s WHERE item_retrieve_id = %s "
            locker_updated = ('RT', check_uid)
            updateData.execute(update_locker, locker_updated)
            mydb.commit()

            
            now = datetime.datetime.now()
            update_locker = "UPDATE item_information SET Time_Retrieved = %s WHERE item_retrieve_id = %s "
            locker_updated = (now, check_uid)
            updateData.execute(update_locker, locker_updated)
            mydb.commit()

            
            update_locker = "UPDATE locker SET Locker_Status = %s WHERE Locker_id = %s "
            locker_updated = ('A', locker_assigned)
            updateData.execute(update_locker, locker_updated)
            mydb.commit()
            
            info("","Thank You for Depositing Lost Item")
            
                        
                        
                

        else:
            info("","ID is Wrong, Please Try Again ")
            
                        



def Check():
    getFinder = "SELECT * FROM finder_information WHERE finder_name = %s AND finder_email = %s "
    Find = (name.value, email.value)
    getData.execute(getFinder, Find)

    
        
def confirmReport():
    
    chk_name = name.value
    chk_email = email.value
    chk_descrip = description.value
    chk_location = location.value
    if chk_name=="" or chk_email=="" or chk_descrip == "" or chk_location =="":
        info("", "Please enter your name, email, item description, and location found")
        
    else:
        if choice.value == "Small":
            size = "S"
        elif choice.value == "Medium":
            size = "M"
        elif choice.value == "Large":
            size = "L"
        else:
            size = "C"
        
        while True:
            rdmid = id_generator(6, "QWERTYUIOPASDFGHJKLZXCVBNM123456789")
            
            rIdChecker = "SELECT * FROM item_information WHERE item_deposit_id = %s "
            rValues = (rdmid,)
            getData.execute(rIdChecker, rValues)
            rLocker_record = getData.fetchall()
            rChecker = getData.rowcount
            
            if rChecker == 1:
                continue
            else:
                
                Check()
                fInfo = getData.fetchall()
                fInfoCheck = getData.rowcount
                
                if fInfoCheck == 1:
                    for row in fInfo:
                        sql_id =row[0]
                    itemInfo = "INSERT INTO item_information (item_deposit_id, item_description,item_Last_Found,Locker_Size_Assigned,status, reported_user ) VALUES (%s,%s,%s,%s,%s,%s)"
                    addItem = (rdmid, chk_descrip, chk_location, size, "RP", sql_id)                 
                    addData.execute(itemInfo, addItem)
                    mydb.commit()
                       
                else:
                    addFind = "INSERT INTO finder_information (finder_name, finder_email) VALUES (%s, %s)"
                    valFind = (chk_name, chk_email)
                    addData.execute(addFind, valFind)
                    mydb.commit()
                    Check()
                    getId = addData.fetchall()
                    for row in getId:
                        sql_id =row[0]
                    itemInfo = "INSERT INTO item_information (item_deposit_id, item_description,item_Last_Found,Locker_Size_Assigned,status, reported_user ) VALUES (%s,%s,%s,%s,%s,%s)"
                    addItem = (rdmid, chk_descrip, chk_location, size, "RP", sql_id)                 
                    addData.execute(itemInfo, addItem)
                    mydb.commit()
            break
        name.clear()
        email.clear()
        location.clear()
        description.clear()
        info("","Please Desposit Item into Locker or Bin")
        
    
def Close():
    app.show()
    window.hide()
    window1.hide()
    uid.clear()
    uid1.clear()
    windowReport.hide()
    name.clear()
    email.clear()
    location.clear()
    description.clear()
    
    
    
# GUI
app = App("Lost and Found",height = 450,width = 800)
picture = Picture(app,image="rplogo.png")
Text(app, text = "Welcome to Lost and Found", size= 24,font = "Arial")
Text(app)
#Buttons to report, submit, and retrieve button
reportItem = PushButton(app,text = "Report lost item",height=1,width=20,command=reportItem)
reportItem.text_size = 16
submitItem = PushButton(app,text = "Submit lost item",height=1,width=20,command=submitItem)
submitItem.text_size = 16
retrieveItem =PushButton(app,text = "Retrieve item",height=1,width=20,command=retrieveItem)
retrieveItem.text_size = 16
app.display




#Form for Submit lost item
window = Window(app, title= " ",height = 600,width = 800)
window.hide()
picture = Picture(window,image="rplogo.png")
Text(window, text="Submit Lost Item",size=18)
Text(window)
Text(window, text = "Please enter ID",size = 14)
uid = TextBox(window,width =20)
uid.text_size=14
Text(window)
#Layout for buttons
formBox = Box(window,layout="grid")
PushButton(formBox,text = "Confirm",command=confirm, grid=[0,0]).text_size=14
PushButton(formBox,text = "Close",command=Close, grid=[1,0]).text_size=14

window1 = Window(app, title= " ",height = 600,width = 800)
window1.hide()
picture = Picture(window1,image="rplogo.png")
Text(window1,text="Retrieve Lost Item", size=18)
Text(window1)
Text(window1, text = "Please enter ID",size = 14)
uid1 = TextBox(window1,width =20)
uid1.text_size=14
Text(window1)
#Layout for buttons
formBoxRpt = Box(window1,layout="grid")
PushButton(formBoxRpt,text = "Confirm",command=retrieve, grid=[0,0]).text_size=14
PushButton(formBoxRpt,text = "Close",command=Close, grid=[1,0]).text_size=14

#Form for reporting lost item
windowReport = Window(app, title= " ",height = 600,width = 800)
windowReport.hide()
picture = Picture(windowReport,image="rplogo.png")
message1 = Text(windowReport, text="Please enter item details",font="Arial",size=20)
Text(windowReport)
#Layout for user to enter item details
formBox1 = Box(windowReport,layout="grid")
Text(formBox1, grid=[0,0],text="Name*",size =14)
name = TextBox(formBox1, grid=[1,0],width=20)
name.text_size=14
Text(formBox1, grid=[0,1], text="Email*",size =14)
email = TextBox(formBox1, grid=[1,1],width=20)
email.text_size=14

Text(formBox1, grid=[0,2],text="Locker Size",size =14)
choice = ButtonGroup(formBox1,
            options=["Small", "Medium", "Large","Chute"],
            selected="Small",grid=[1,2],align="left" )
choice.text_size=14

Text(formBox1, grid=[0,3],text="Item Description",size =14)
description = TextBox(formBox1, grid=[1,3],width=20)
description.text_size=14
Text(formBox1, grid=[0,4],text="Location Found",size =14)
location = TextBox(formBox1, grid=[1,4],width=20)
location.text_size=14
Text(windowReport)
#Layout for buttons
formBox2 = Box(windowReport,layout="grid")
PushButton(formBox2,text = "Confirm",command=confirmReport, grid=[0,0])
PushButton(formBox2,text = "Close",command=Close, grid=[1,0])




