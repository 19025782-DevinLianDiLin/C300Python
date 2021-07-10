import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password ="password", 
    database="c300"
    
)


from guizero import App,Text,TextBox,PushButton,info,Picture,Window,ButtonGroup,Box
from gpiozero import LED
from gpiozero import Button
# GUI
app = App("Lost and Found",height = 300,width = 450)
picture = Picture(app,image="rplogo.png")
Text(app, text = "Welcome to Lost and Found", size= 20,font = "Arial")

#Form for Submit/Retrieve lost item
window = Window(app, title= " ",height = 400,width = 450)
window.hide()
picture = Picture(window,image="rplogo.png")
message = Text(window, size=14)
Text(window)
Text(window, text = "Please enter ID")
uid = TextBox(window,width =20)

#Form for reporting lost item
window1 = Window(app, title= " ",height = 400,width = 450)
window1.hide()
picture = Picture(window1,image="rplogo.png")
message1 = Text(window1, text="Please enter details",font="Arial")
Text(window1)   
formBox1 = Box(window1,layout="grid")
Text(formBox1, grid=[0,0],text="Name")
name = TextBox(formBox1, grid=[1,0])
Text(formBox1, grid=[0,1], text="Email")
email = TextBox(formBox1, grid=[1,1])
Text(formBox1, grid=[0,2],text="Item")
choice = ButtonGroup(formBox1,
            options=["Card", "Wallet", "Phone","Others"],
            selected="Card",grid=[1,2] )


def submitItem():
    app.hide()
    message.append("Submit Lost Item")
    window.show()
    
def retrieveItem():
    app.hide()
    message.append("Retrieve Lost Item")
    window.show()

def confirm():
    info("","Submitted")

def Close():
    app.show()
    window.hide()
    message.clear()
    window1.hide()
    
def reportItem():
    app.hide()
    window1.show()

reportItem = PushButton(app,text = "Report lost item",command=reportItem)
submitItem = PushButton(app,text = "Submit lost item",command=submitItem)
retrieveItem =PushButton(app,text = "  Retrieve item  ",command=retrieveItem)
app.display

#Form for Submit/Retrieve lost item(cont)    
formBox = Box(window,layout="grid")
PushButton(formBox,text = "Confirm",command=confirm, grid=[0,0])
PushButton(formBox,text = "Close",command=Close, grid=[1,0])


#Form for reporting lost item(cont)
formBox2 = Box(window1,layout="grid")
PushButton(formBox2,text = "Confirm",command=confirm, grid=[0,0])
PushButton(formBox2,text = "Close",command=Close, grid=[1,0])

