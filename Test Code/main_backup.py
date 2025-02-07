from picozero import LED, Speaker, Buzzer
import machine
from time import sleep
import network
import socket
import asyncio
from random import randint


onboard_led = machine.Pin("LED", machine.Pin.OUT)
onboard_led.off()

red = LED(16)
yellow = LED(17)
green = LED(18)
white = LED(19)
blue = LED(20)
buzzer = Buzzer(15)

"""
async def blink_led():
    while True:
        print("toggle")
        red.toggle()  # Toggle LED state
        await asyncio.sleep(1)
"""

def light_display():
    while True:
        number = randint(1,5)
        if number == 1:
            red.toggle()
        if number == 2:
            yellow.toggle()
        if number == 3:
            green.toggle()
        if number == 4:
            white.toggle()
        if number == 5:
            blue.toggle()
        sleep(0.2)
            
    print(number)

    

def traffic_lights():
    red.on()
    sleep(2)
    red.off()

    yellow.on()
    sleep(2)
    yellow.off()

    green.on()
    sleep(2)
    green.off()

def buzz_alarm():
    print("beeping")
    buzzer.beep()
    sleep(4)
    print("stopping")
    buzzer.off()

def onboard_cycle():
    onboard_led.off()
    sleep(0.1)
    onboard_led.on()
    sleep(0.1)
    onboard_led.off()
    sleep(0.1)
    onboard_led.on()
      

def web_page():
    #Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <form action="./traffic_light">
            <input type="submit" value="Traffic Light" />
            </form>
            <form action="./light_display">
            <input type="submit" value="Light Display" />
            </form>
            <form action="./alarm">
            <input type="submit" value="Alarm" />
            </form>
            </body>
            </html>
            """
    return str(html)

# if you do not see the network you may have to power cycle
# unplug your pico w for 10 seconds and plug it in again
def ap_mode(ssid, password):
    """
        Description: This is a function to activate AP mode

        Parameters:

        ssid[str]: The name of your internet connection
        password[str]: Password for your internet connection

        Returns: Nada
    """
    # Just making our internet connection
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password)
    ap.active(True)

    while ap.active() == False:
        pass
    print('AP Mode Is Active, You can Now Connect')
    print('IP Address To Connect to:: ' + ap.ifconfig()[0])
    
    #indicator light that access point is available
    onboard_led.on()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #creating socket object
    s.bind(('', 80))
    s.listen(5)

    while True:
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        str_request = str(request)
        print('Content = %s' % str_request)
        onboard_cycle()
        try:
            str_request = str_request.split()[1]
        except IndexError:
            pass
        if str_request == '/traffic_light?':
            traffic_lights()
        elif str_request =='/light_display?':
            light_display()
            
            #asyncio.create_task(blink_led())
        elif str_request == '/alarm?':
            buzz_alarm()
        else:
            pass
      
        response = web_page()
        onboard_cycle()
        conn.send(response)
        conn.close()

ap_mode('pi-pico',
        'password')


