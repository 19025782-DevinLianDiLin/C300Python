import mysql.connector
import string
import random
import datetime
import smtplib
from Email import Emailer

#Connect to SQL 
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password ="password", 
    database="c300"
    
)

getData = mydb.cursor()
updateData = mydb.cursor()
addData = mydb.cursor()



from guizero import App,Text,TextBox,PushButton,info,error,warn,Picture,Window,ButtonGroup,Box
from gpiozero import LED
from gpiozero import Button
import RPi.GPIO as GPIO
import time


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# Code to Activate the Chute 
def chute():
    i = 0
    info("","Please deposit item into chute")
    try:
        GPIO.setmode(GPIO.BCM)
        TRIG=23
        ECHO=24
        b= False
        GPIO.setup(TRIG,GPIO.OUT)
        GPIO.setup(ECHO,GPIO.IN)
        e = 0
        while b == False:
            GPIO.output(TRIG,False)
            time.sleep(1.2)
            GPIO.output(TRIG,True)
            time.sleep(0.00001)
            GPIO.output(TRIG,False)
            
            start =time.time()
            while GPIO.input(ECHO)== 0:
                start = time.time()
            
            while GPIO.input(ECHO)== 1:
                stop = time.time()

            elasped = stop-start
            distance = elasped * 34300
            distance = distance/2
            print("Distance : %2.2f cm"%distance)
            if distance<26 or distance>27:
                i=i+1
                if i>3:
                    b=True
                    info("","Thank You for Depositing Lost Item")
                    
            e=e+1
            if e >20:
                b=True
                error("","Error, please head to counter for help")
                

                
    finally:
        GPIO.cleanup()
        
        
        
def confirm():
    check_uid = uid.value
    if check_uid =="":
        warn("", "Please enter ID")
    # To check if Id exist     
    else:      
        number_of_row = "SELECT * FROM item_information WHERE Status = %s AND item_deposit_id = %s "
        
        idsql = ('RP', check_uid)
        getData.execute(number_of_row, idsql)
        
        record = getData.fetchall()
        
        if record == []:
            warn("","Invalid ID")
        else:
            for row in record:
                id = row[0]
                user = row[11]
                locker_size_assigned = row[5]
                
        # Assign to Chute if Size_Assigned = Chute             
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
                    
                    # Assign locker based on locker available
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
                    
            uid.clear()
            # Update SQL Fields 
            update_locker = "UPDATE item_information SET Locker_Assigned = %s WHERE item_deposit_id = %s "
            locker_updated = (locker_id, check_uid)

            updateData.execute(update_locker, locker_updated)
            mydb.commit()
            
            # Part Where Locker Open/Closes , Chute to be used 
            if button == 0 and led == 0:
                chute()
            else:
                button_gpio = Button(button)
                lock_gpio = LED(led)
                lock_gpio.on()
                info("","Please deposit item into Locker")
                button_gpio.wait_for_press()
                lock_gpio.off()
                info("","Thank You for Depositing Lost Item")           
            
            now = datetime.datetime.now()
            
            # Update SQL Fields
            
            update_locker = "UPDATE item_information SET Status = %s WHERE item_deposit_id = %s"
            locker_updated = ('DP',check_uid)
            updateData.execute(update_locker, locker_updated)
            mydb.commit()
            
            
            update_locker = "UPDATE item_information SET Time_Deposited = %s WHERE item_deposit_id = %s"
            locker_updated = (now,check_uid)
            updateData.execute(update_locker, locker_updated)
            mydb.commit()
            
            # Chute should be Available / Locker Should not be available
            if locker_size_assigned != "C":
                
                update_locker = "UPDATE locker SET Locker_Status = %s WHERE Locker_id = %s "
                locker_updated = ("NA", locker_id)
                updateData.execute(update_locker, locker_updated)
                mydb.commit()
                
            
            # ID generator for Retrieve ID 
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
                    
                    
                    #Send email to inform user they sucessfully deposit the lost item
                    getUser = "SELECT * FROM finder_information WHERE finder_id = %s "
                    u_Info = (user, )
                    getData.execute(getUser, u_Info)
                    finder_info = getData.fetchone()
                    
                    email2 = str(finder_info[2])
                        
                    
                    sender = Emailer()
                    
                    emailSubject = "RP-DO-NOT-REPLY"
                    emailContent = "Thank you for deposit the lost item at " + str(now) + " "
                    sender.sendmail(email2, emailSubject, emailContent)
                    
                    
                    break
                
                    
                
                
            
                
                
            
            
            
def retrieve():
    check_uid = uid1.value
    if check_uid =="":
        warn("", "Please enter ID")
        
    
    # To check if ID exist     
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
                
            # pull the information to what locker it was assigned to 
            lockerinfo = "SELECT * FROM locker WHERE locker_id = %s"
            lockerinfovar = (locker_assigned,)
            getData.execute(lockerinfo, lockerinfovar)
            locker_record = getData.fetchone()
            
            led = locker_record[4]
            button = locker_record[3]
            
            # Part Where Locker Open/Closes , Inform user to head to counter if item was deposited via the chute
            if led == 0 or button == 0:
                info("","Please head to counter to retrieve lost item")
            else:
                button_gpio = Button(button) 
                lock_gpio = LED(led)
                lock_gpio.on()
                info("","Please retrieve item from Locker")
                button_gpio.wait_for_press()
                lock_gpio.off()
                
                #Update SQL fields 
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
                
                info("","Thank you for retrieving your lost item.")
                
            
            
            
            uid1.clear()
                        
                        
                

        else:
            warn("","ID is Wrong, Please Try Again ")
            
                        



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
        warn("", "Please enter your name, email, item description, and location found")
        
    #Assign Locker Size     
    else:
        if choice.value == "Small":
            size = "S"
        elif choice.value == "Medium":
            size = "M"
        elif choice.value == "Large":
            size = "L"
        else:
            size = "C"
            
        # Generate Deposit ID 
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
                # Check if user Exist 
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
        info("","Report Successful. Please check your email for a 6 digit code.")
        
        
        #Send email to inform user about their UID
        sender = Emailer()
        emailSubject = "RP-DO-NOT-REPLY"
        emailContent = "Thank you for reporting lost item: "+ chk_descrip + ", your 6 digit ID is " + rdmid + "."
        sender.sendmail(chk_email, emailSubject, emailContent)
        
        
def Close():
    app.show()
    window.hide()
    retrieveWindow.hide()
    uid.clear()
    uid1.clear()
    windowReport.hide()
    name.clear()
    email.clear()
    location.clear()
    description.clear()
    
def reportItem():
    windowReport.show()
    retrieveWindow.hide()
    window.hide()
    app.hide()
    
def submitItem():
    window.show()
    retrieveWindow.hide()
    windowReport.hide()
    app.hide()

def retrieveItem():
    retrieveWindow.show()
    window.hide()
    windowReport.hide()
    app.hide()    
    
# GUI
app = App("Lost and Found",height = 450,width = 800)
picture = Picture(app,image="rplogo.png")
Text(app, text = "Welcome to Lost and Found", size= 28,font = "Arial")
Text(app)
Text(app,text="Please select the service", size = 20)
Text(app)
#Buttons to report, submit, and retrieve button
reportItem = PushButton(app,text = "Report lost item",height=1,width=20,command=reportItem)
reportItem.text_size = 16
submitItem = PushButton(app,text = "Submit lost item",height=1,width=20,command=submitItem)
submitItem.text_size = 16
retrieveItem =PushButton(app,text = "Retrieve item",height=1,width=20,command=retrieveItem)
retrieveItem.text_size = 16
#Display in full screen
app.display
app.full_screen = True



#Form for Submit lost item
window = Window(app, title= " ",height = 500,width = 900)
window.hide()
picture = Picture(window,image="rplogo.png")
Text(window, text="Submit Lost Item",size=24)
Text(window)
Text(window, text = "Please enter ID",size = 16)
uid = TextBox(window,width =20)
uid.text_size=14
window.full_screen = True

#Layout for buttons
formBox = Box(window,layout="grid")
PushButton(formBox,text = "Confirm",command=confirm, grid=[0,0]).text_size=14
PushButton(formBox,text = "Close",command=Close, grid=[1,0]).text_size=14

#Spacing
Text(window)

#Instructions for on how to use locker
formBoxInstruc = Box(window,layout="grid")
Text(formBoxInstruc, grid=[0,0], text="How to use the locker:",size =14,align="left")
Text(formBoxInstruc, grid=[0,1], text="1. Enter the 6 digit ID sent",size =12,align="left")
Text(formBoxInstruc, grid=[0,2], text="2. Click Confirm to submit ID",size =12,align="left")
Text(formBoxInstruc, grid=[0,3], text="3. If successful, look for a locker with a powered LED",size =12,align="left")
Text(formBoxInstruc, grid=[0,4], text="4. Click 'Ok' on the pop-up window before depositing item    ",size =12,align="left")
Text(formBoxInstruc, grid=[0,5], text="5. Close the locker once item has been deposited",size =12,align="left")

#Instructions for on how to use chute
Text(formBoxInstruc, grid=[1,0], text="How to use the Chute:",size =14,align="left")
Text(formBoxInstruc, grid=[1,1], text="1. Enter the 6 digit ID sent",size =12,align="left")
Text(formBoxInstruc, grid=[1,2], text="2. Click Confirm to submit ID",size =12,align="left")
Text(formBoxInstruc, grid=[1,3], text="3. If successful, open the chute",size =12,align="left")
Text(formBoxInstruc, grid=[1,4], text="4. Click 'Ok' on the pop-up window before depositing item",size =12,align="left")
Text(formBoxInstruc, grid=[1,5], text="5. Close the chute once item has been deposited",size =12,align="left")

#Form for retrieve lost item
retrieveWindow = Window(app, title= " ",height = 500,width = 900)
retrieveWindow.hide()
picture = Picture(retrieveWindow,image="rplogo.png")
Text(retrieveWindow,text="Retrieve Lost Item", size=24)
Text(retrieveWindow)
Text(retrieveWindow, text = "Please enter ID",size = 16)
uid1 = TextBox(retrieveWindow,width =20)
uid1.text_size=14
retrieveWindow.full_screen=True

#Layout for buttons
formboxRtv = Box(retrieveWindow,layout="grid")
PushButton(formboxRtv,text = "Confirm",command=retrieve, grid=[0,0]).text_size=14
PushButton(formboxRtv,text = "Close",command=Close, grid=[1,0]).text_size=14

#Spacing
Text(retrieveWindow)

#Instructions for on how to use locker
formBoxInstruc = Box(retrieveWindow,layout="grid")
Text(formBoxInstruc, grid=[0,0], text="How to retrieve item from locker:",size =14,align="left")
Text(formBoxInstruc, grid=[0,1], text="1. Enter the 6 digit ID sent",size =12,align="left")
Text(formBoxInstruc, grid=[0,2], text="2. Click Confirm to submit ID",size =12,align="left")
Text(formBoxInstruc, grid=[0,3], text="3. If successful, look for a locker with a powered LED",size =12,align="left")
Text(formBoxInstruc, grid=[0,4], text="4. Click 'Ok' on the pop-up window before retrieving item    ",size =12,align="left")
Text(formBoxInstruc, grid=[0,5], text="5. Close the locker once item has been retrieved",size =12,align="left")

#Instructions for on how to use chute
Text(formBoxInstruc, grid=[1,0], text="How to item from Chute:",size =14,align="left")
Text(formBoxInstruc, grid=[1,1], text="1. Enter the 6 digit ID sent",size =12,align="left")
Text(formBoxInstruc, grid=[1,2], text="2. Click Confirm to submit ID",size =12,align="left")
Text(formBoxInstruc, grid=[1,3], text="3. If successful, follow instructions on the ",size =12,align="left")
Text(formBoxInstruc, grid=[1,4], text="    pop-up window to retrieve item",size =12,align="left")


#Form for reporting lost item
windowReport = Window(app, title= " ",height = 600,width = 800)
windowReport.hide()
picture = Picture(windowReport,image="rplogo.png")
message1 = Text(windowReport, text="Please enter item details",font="Arial",size=20)
Text(windowReport)

#Layout for user to enter item details to report lost item
formboxDetails = Box(windowReport,layout="grid")
Text(formboxDetails, grid=[0,0],text="Name*",size =14)
name = TextBox(formboxDetails, grid=[1,0],width=20)
name.text_size=14
Text(formboxDetails, grid=[0,1], text="Email*",size =14)
email = TextBox(formboxDetails, grid=[1,1],width=20)
email.text_size=14

Text(formboxDetails, grid=[0,2],text="Locker Size",size =14)
choice = ButtonGroup(formboxDetails,
            options=["Small", "Medium", "Large","Chute"],
            selected="Small",grid=[1,2],align="left" )
choice.text_size=12

Text(formboxDetails, grid=[0,3],text="Item Description*",size =14)
description = TextBox(formboxDetails, grid=[1,3],width=20)
description.text_size=14
Text(formboxDetails, grid=[0,4],text="Location Found*",size =14)
location = TextBox(formboxDetails, grid=[1,4],width=20)
location.text_size=14
Text(windowReport)
windowReport.full_screen=True

#Layout for buttons
formboxRpt = Box(windowReport,layout="grid")
PushButton(formboxRpt,text = "Confirm",command=confirmReport, grid=[0,0])
PushButton(formboxRpt,text = "Close",command=Close, grid=[1,0])

#Spacing
Text(windowReport)

#Text to tell user to provide accurate information
Text(windowReport,text="Please provide accurate details for item description and location found", size =14)



