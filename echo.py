import RPi.GPIO as GPIO
import time
i = 0
while i<3:
    GPIO.setmode(GPIO.BCM)

    TRIG=20
    ECHO=16

    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)
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
    distance = elasped * 17150
    distance = distance/2
    print("Distance : %2.f cm"%distance)
    if distance<3 or distance>5:
        i=i+1
print("Thank You")