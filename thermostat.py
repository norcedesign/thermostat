import sys
import socket

from sense_emu import SenseHat
from screen import connect
from colors import colors

sense: SenseHat
screen: socket

room_temperature: float = 0
desired_temperature: float = 0

min_temperature: float = 5
max_temperature: float = 30


def get_pressure() -> str:
    global sense

    pressure = 'PR' + "{:.2f}".format(sense.get_pressure())
    print(f"{colors.CYAN}PRESSURE: {pressure}{colors.END}")

    return pressure


def get_humidity() -> str:
    global sense

    humidity = 'HU' + "{:.2f}".format(sense.get_humidity())
    print(f"{colors.CYAN}HUMIDITY: {humidity}{colors.END}")

    return humidity


def get_room_temperature() -> str:
    global room_temperature

    temperature = 'TP' + "{:.2f}".format(room_temperature)
    print(f"{colors.CYAN}ROOM TEMPERATURE: {temperature}{colors.END}")

    return temperature


def get_desired_temperature() -> str:
    global desired_temperature

    temperature = 'TD' + "{:.2f}".format(desired_temperature)
    print(f"{colors.CYAN}DESIRED TEMPERATURE: {temperature}{colors.END}")

    return temperature


def get_fictive_power() -> str:
    global desired_temperature, room_temperature
    power: float = 0

    if desired_temperature >= room_temperature:
        power = ((desired_temperature - room_temperature) / 6) * 100

    fictive_power = 'PW' + "{:.2f}".format(power)
    print(f"{colors.CYAN}FICTIVE POWER: {fictive_power}{colors.END}")

    return fictive_power


def adjust_desired_temperature(threshold: float) -> None:
    global desired_temperature, min_temperature, max_temperature

    temperature = desired_temperature + threshold

    if min_temperature <= temperature <= max_temperature:
        desired_temperature = temperature


def send_message(message: str) -> None:
    global screen, sense

    print(f"{colors.WARNING}SENDING MESSAGE: {message}{colors.END}")

    sense.show_message(message)
    screen.send(message.encode())


def process() -> None:
    global screen, sense

    # todo - introduce threads + manage priorities

    try:
        while True:
            for event in sense.stick.get_events():
                if event.action == 'pressed' and event.direction == 'up':
                    adjust_desired_temperature(0.5)
                elif event.action == 'pressed' and event.direction == 'down':
                    adjust_desired_temperature(-0.5)

                send_message(get_desired_temperature())
                send_message(get_fictive_power())
    except:
        print(f"{colors.FAIL}\nExit Application\n{colors.END}")
        print('Error: {}'.format(sys.exc_info()))

        sense.show_message("\nExit Application\n")
        screen.close()


def init() -> None:
    send_message(get_desired_temperature())
    send_message(get_room_temperature())

    send_message(get_pressure())
    send_message(get_humidity())

    send_message(get_fictive_power())


def main() -> None:
    global desired_temperature, room_temperature, screen, sense

    try:
        print(f"{colors.GREEN}Initializing the thermostat using sense hat{colors.END}")

        sense = SenseHat()
        sense.clear()

        room_temperature = sense.get_temperature()
        desired_temperature = room_temperature

        print(f"{colors.GREEN}Connecting to screen via socket{colors.END}")
        screen = connect()

        print(f"{colors.GREEN}Sending initial values to screen via socket{colors.END}")
        init()
    except:
        print(f"{colors.FAIL}Failed to initialize the thermostat{colors.END}")
        print('Error: {}'.format(sys.exc_info()))
        sys.exit(1)

    print(f"{colors.GREEN}Initialization complete!{colors.END}")
    process()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"{colors.GREEN}\nExiting application\n{colors.END}")
        sys.exit(0)
