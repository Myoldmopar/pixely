from rpi_ws281x import PixelStrip, Color
import time
import math

from RPi import GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)

LED_COUNT = 144        # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # This will be the forever max brightness - use color values to alter brightness later (0, 255)
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

def do_one_arm_charge():

    # reset back to zero
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    
    MAX_VAL = 20  # 255
    MIN_VAL = 0
    AMPLITUDE = (MAX_VAL - MIN_VAL) / 2
    DIVISIONS = 12
    c = 2 * math.pi / DIVISIONS
    offsets = [
        -0 * c, -1 * c, -2 * c, -3 * c, -4 * c, -5 * c,
        -6 * c, -7 * c, -8 * c, -9 * c, -10 * c, -11 * c,
    ] * 8
    
    time_step = 0.3
    for offset in offsets:
        for pixel in range(LED_COUNT):
            x = pixel / LED_COUNT
            radians = 2 * 3.141 * x + offset
            green_value = AMPLITUDE + AMPLITUDE * math.sin(radians)
            strip.setPixelColor(pixel, Color(0, int(green_value), 0))
        strip.show()
        time_step *= 0.9
        time_step = max(time_step, 0.02)
        time.sleep(time_step)
    
    for pixel in range(100):
        strip.setPixelColor(pixel, Color(0, int(pixel * 0.25), 0))
        strip.show()
        time.sleep(0.02)
    
    for i in [0, 1, 2, 3, 4, 5]:
        for brightness in range(0, 255, 25):
            for pixel in range(100, LED_COUNT):
                strip.setPixelColor(pixel, Color(0, int(brightness / 6), 0))
            strip.show()
            time.sleep(0.02)
        for brightness in range(255, -5, -25):
            for pixel in range(100, LED_COUNT):
                strip.setPixelColor(pixel, Color(0, int(brightness / 6), 0))
            strip.show()
            time.sleep(0.02)
    for brightness in range(0, 255, 25):
        for pixel in range(100, LED_COUNT):
            strip.setPixelColor(pixel, Color(0, int(brightness / 6), 0))
        strip.show()
        time.sleep(0.02)

def reset_arm(do_fade=False):
    if not do_fade:
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(0, 0, 0))
        return
    current_brightness = 40
    while True:
        current_brightness -= 1
        if current_brightness < 0:
            current_brightness = 0
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(0, current_brightness, 0))
        strip.show()
        if current_brightness <= 0:
            break

def set_leds_ready():
    GPIO.output(13, GPIO.LOW)
    GPIO.output(15, GPIO.HIGH)

def set_leds_running():
    GPIO.output(13, GPIO.HIGH)
    GPIO.output(15, GPIO.LOW)

def turn_on_stone():
    GPIO.output(7, GPIO.HIGH)
    time.sleep(0.25)

def turn_off_stone():
    GPIO.output(7, GPIO.LOW)
    time.sleep(0.25)

reset_arm()
turn_off_stone()
stone_active = False
set_leds_ready()
arm_on = False

try:    
    while True:
        if GPIO.input(10) == GPIO.HIGH:
            if not stone_active:
                print('Cannot engage time manipulation until stone is activated')
                time.sleep(0.1)
                continue
            set_leds_running()
            arm_on = True
            do_one_arm_charge()
            set_leds_ready()
        if GPIO.input(8) == GPIO.HIGH:
            if stone_active:
                reset_arm(arm_on)
                arm_on = False
                set_leds_running()
                turn_off_stone()
                set_leds_ready()
                stone_active = False
            else:
                set_leds_running()
                turn_on_stone()
                set_leds_ready()
                stone_active = True
except KeyboardInterrupt:
    turn_off_stone()
    reset_arm()
    GPIO.cleanup()

