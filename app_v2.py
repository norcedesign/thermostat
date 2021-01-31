import threading
import time
import socket
from sense_emu import SenseHat

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.1.107',1234))

sense = SenseHat()
sense.clear()

sem = threading.Semaphore()

room_temperature: float = 0
desired_temperature: float = 0

min_temperature: float = 5
max_temperature: float = 30


def get_humidity() -> str:
    global sense

    humidity = 'HU' + "{:.2f}".format(sense.get_humidity())
    #print(f"{colors.CYAN}HUMIDITY: {humidity}{colors.END}")

    return humidity

def get_pressure() -> str:
    global sense

    pressure = 'PR' + "{:.0f}".format(sense.get_pressure())
    #print(f"{colors.CYAN}PRESSURE: {pressure}{colors.END}")
    return pressure

def get_room_temperature() -> str:
    global sense
 
    temperature = 'TP' + "{:.2f}".format(sense.get_temperature())
    #print(f"{colors.CYAN}ROOM TEMPERATURE: {temperature}{colors.END}")

    return temperature
'''
def get_desired_temperature() -> str:
    global desired_temperature

    temperature = 'TD' + "{:.2f}".format(desired_temperature)
    #print(f"{colors.CYAN}DESIRED TEMPERATURE: {temperature}{colors.END}")

    return temperature
'''

def get_fictive_power() -> str:
    global desired_temperature, room_temperature
    power: float = 0

    if desired_temperature >= room_temperature:
        power = ((desired_temperature - room_temperature) / 6) * 100

    fictive_power = 'PW' + "{:.2f}".format(power)
    #print(f"{colors.CYAN}FICTIVE POWER: {fictive_power}{colors.END}")

    return fictive_power

def adjust_desired_temperature(threshold: float) -> None:
    global desired_temperature, min_temperature, max_temperature

    temperature = desired_temperature + threshold

    if min_temperature <= temperature <= max_temperature:
        desired_temperature = temperature


#def send_message(message: str) -> None:
def display_message() -> None:
    tp = get_room_temperature()
    hu = get_humidity()
    pr = get_pressure()
    message = f'{tp}\n{hu}\n{pr}\n'
    
    s.send(message.encode())
    print(message)

#Threads
def calculate_power_task():
    global sense, desired_temperature, room_temperature
    
    desired_temperature = room_temperature = sense.get_temperature()
    #if desired_temperature == None:
    #    desired_temperature = room_temperature
        
    while True:
        event = sense.stick.wait_for_event()
        sem.acquire()                    
        if event.action == "pressed":
            if event.direction =="up":
                desired_temperature += 0.5
            elif event.direction == "down":
                desired_temperature -= 0.5                 
            
        td = 'TD' + "{:.2f}".format(desired_temperature)    
        print('Calculating power for : ' + td)
        pw = get_fictive_power()       
        
        message = f'{td}\n{pw}\n'    
        s.send(message.encode())
        print(message)
        sem.release()
        #time.sleep(0.1)

def main_task():     
    
    while True:
        sem.acquire()
        display_message()
        sem.release()
        time.sleep(1)

if __name__=="__main__":
    #main_task()
    t1 = threading.Thread(target=calculate_power_task)
    t2 = threading.Thread(target=main_task) 
    t1.start()
    t2.start()
       
