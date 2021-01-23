#from sense_hat import SenseHat
from sense_emu import SenseHat
from time import sleep

sense = SenseHat()
sense.clear()

tp = sense.get_temperature()
hu = sense.get_humidity()
pr = sense.get_pressure()
td = tp

#Afficher message sur SenseHat
sleep(1)
sense.show_message("TP" + str(round(tp,1))+"*C")
sleep(1)
sense.show_message("HU" + str(round(hu,2)))
sleep(1)
sense.show_message("PR" + str(round(pr,2)))

print("Sélectionner la température désirée à l'aide du joystick.. (5-30)" )
min_value = 5
max_value = 30

# Lecture Joystick
try:
    while True:
        for event in sense.stick.get_events():
            if event.action == "pressed":
                if event.direction =="up":
                    td = td + 0.5
                elif event.direction == "down":
                    td = td -0.5                    
                sleep(0.5)
                sense.show_message(str(round(td,1)))
                if td > tp:
                    pw = ((td -tp)/6) *100
                    print("puissance fictive: " + str(pw))

except KeyboardInterrupt:
    sense.show_message("Bye!")