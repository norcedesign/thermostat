import sys
import time
import socket

from threading import Semaphore, Thread
from sense_emu import SenseHat
from screen import connect
from colors import colors

semaphore: Semaphore
sense: SenseHat
screen: socket

host: str = 'localhost'  # update to the desired ip address
port: int = 1234  # update to the desired port

fictive_power: float = 0
room_temperature: float = 0
desired_temperature: float = 0

min_temperature: float = 5
max_temperature: float = 30


def get_pressure() -> str:
    global sense
    return 'PR' + '{:.2f}'.format(sense.get_pressure())


def get_humidity() -> str:
    global sense
    return 'HU' + '{:.2f}'.format(sense.get_humidity())


def get_room_temperature() -> str:
    global room_temperature
    return 'TP' + '{:.2f}'.format(room_temperature)


def get_desired_temperature() -> str:
    global desired_temperature
    return 'TD' + '{:.2f}'.format(desired_temperature)


def get_fictive_power() -> str:
    global desired_temperature, room_temperature, fictive_power

    if desired_temperature >= room_temperature:
        fictive_power = ((desired_temperature - room_temperature) / 6) * 100

    return 'PW' + '{:.2f}'.format(fictive_power)


def adjust_desired_temperature(threshold: float) -> None:
    global desired_temperature, min_temperature, max_temperature

    temperature = desired_temperature + threshold

    if min_temperature <= temperature <= max_temperature:
        desired_temperature = temperature


def send_message(message: str) -> None:
    global screen

    screen.send(message.encode())
    print(f'{colors.CYAN}{message}{colors.END}')


def process() -> None:
    global screen, sense, semaphore

    try:
        while True:
            event = sense.stick.wait_for_event()
            semaphore.acquire()

            if event.action == 'pressed' and event.direction == 'up':
                adjust_desired_temperature(0.5)
            elif event.action == 'pressed' and event.direction == 'down':
                adjust_desired_temperature(-0.5)

            send_message(f'{get_desired_temperature()}\n{get_fictive_power()}\n')
            semaphore.release()
    except:
        print(f'{colors.RED}\nExit Application\n{colors.END}')
        print('Error: {}'.format(sys.exc_info()))

        screen.close()


def display() -> None:
    global semaphore

    while True:
        semaphore.acquire()

        tp = get_room_temperature()
        td = get_desired_temperature()

        hu = get_humidity()
        pr = get_pressure()

        pw = get_fictive_power()
        send_message(f'{tp}\n{td}\n{hu}\n{pr}\n{pw}\n')

        semaphore.release()
        time.sleep(1)


def main() -> None:
    global desired_temperature, room_temperature, screen, sense, semaphore

    sensor_thread: Thread
    events_thread: Thread

    try:
        print(f'{colors.GREEN}Initializing the thermostat using sense hat{colors.END}')
        sense = SenseHat()
        sense.clear()

        desired_temperature = room_temperature = sense.get_temperature()

        print(f'{colors.GREEN}Connecting to screen via socket{colors.END}')
        screen = connect(host, port)

        print(f'{colors.GREEN}Initializing application threads{colors.END}')
        semaphore = Semaphore()

        sensor_thread = Thread(target=display)
        events_thread = Thread(target=process)
    except:
        print(f'{colors.RED}Failed to initialize the thermostat{colors.END}')
        print('Error: {}'.format(sys.exc_info()))
        sys.exit(1)

    print(f'{colors.GREEN}Initialization complete!{colors.END}')

    sensor_thread.start()
    events_thread.start()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f'{colors.GREEN}\nExiting application\n{colors.END}')
        sys.exit(0)
