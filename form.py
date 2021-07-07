from guizero import App,Text,TextBox,PushButton,info,Picture
app = App("Lost and Found",height = 300,width = 450)


picture = Picture(app,image="rplogo.png")
message = Text(app, text = "Welcome to Lost and Found", size= 20,font = "Arial", color="Green")
uid = TextBox(app,width =20)

def check():
    info("Test", "Testing")

check_avail = PushButton(app,text = "Submit",command=check)

app.display()
