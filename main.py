from picozero import LED, Speaker, Buzzer
import machine
from time import sleep
import network
import socket
import uasyncio as asyncio
from random import randint
from machine import Pin
import uasyncio as asyncio

onboard = machine.Pin("LED", machine.Pin.OUT)

red = LED(16)
yellow = LED(17)
green = LED(18)
white = LED(19)
blue = LED(20)
buzzer = Buzzer(15)


display = False

html = f"""<!DOCTYPE html>
            <html>
            <form action="./traffic_light">
            <input type="submit" value="Traffic Light" />
            </form>
            <form action="./alarm">
            <input type="submit" value="Alarm" />
            </form>
            <form action="./light_display_on">
            <input type="submit" value="Light Display On" />
            </form>
            <form action="./light_display_off">
            <input type="submit" value="Light Display Off" />
            </form>
            </body>
            </html>
"""

wlan = network.WLAN(network.AP_IF)

def get_display():
    return display

async def light_display():
    display = get_display()
    while display == True:
        
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
        display = get_display()
        await asyncio.sleep(0.2)
    else:
        red.off()
        yellow.off()
        green.off()
        white.off()
        blue.off()
        return

    
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

def ap_mode(ssid, password):
    """
        Description: This is a function to activate AP mode

        Parameters:

        ssid[str]: The name of your internet connection
        password[str]: Password for your internet connection

        Returns: Nada
    """
    print("in AP mode")
    # Just making our access point 
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password)
    ap.active(True)

    while ap.active() == False:
        pass
    print('AP Mode Is Active, You can Now Connect')
    print('IP Address To Connect to:: ' + ap.ifconfig()[0])
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #creating socket object
    s.bind(('', 80))
    s.listen(5)
    """
    return ap.ifconfig()[0]

async def serve_client(reader, writer):
    global display
    
    
    print("Client connected")
    request_line = await reader.readline()
    print("Request:", request_line)
    # We are not interested in HTTP request headers, skip them
    while await reader.readline() != b"\r\n":
        pass
    
    str_request = str(request_line)
    print('Content = %s' % str_request)
    try:
        str_request = str_request.split()[1]
    except IndexError:
        pass
    if str_request == '/traffic_light?':
        traffic_lights()
    elif str_request == '/alarm?':
        buzz_alarm()
    elif str_request =='/light_display_on?':
        #light_display()        
        display = True
        asyncio.create_task(light_display())
    elif str_request =='/light_display_off?':
        display = False
        
    else:
        pass
  
    response = html
    writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    writer.write(response)

    await writer.drain()
    await writer.wait_closed()
    print("Client disconnected")


async def main():
    print('Setting up AP mode...')
    
    ip = ap_mode('pi-pico','password')

    print('Setting up webserver...')
    asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0", 80))

    
    while True:
        onboard.on()
        print("heartbeat")
        print(display)
        await asyncio.sleep(0.25)
        onboard.off()
        await asyncio.sleep(5)
        
try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()

