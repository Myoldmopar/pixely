from RPi import GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

times_pressed = 0
while True:
    if GPIO.input(10) == GPIO.HIGH:
         times_pressed += 1
         print('Button was pushed (%i)' % times_pressed)

