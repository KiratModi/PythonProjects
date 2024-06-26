#pip install --upgrade setuptools wheel 
#pip install playsound

from playsound import playsound
import time

CLEAR = "\033[2J"
CLEAR_AND_RETURN = "\033[H"

def alarm(seconds):
    time_elapsed = 0

    print(CLEAR)
    while time_elapsed < seconds:
        time.sleep(1)
        time_elapsed += 1

        time_left = seconds - time_elapsed
        minutes_left = time_left // 60
        seconds_left = time_left % 60 # reminder after division

        print(f"{CLEAR_AND_RETURN}{minutes_left:02d}:{seconds_left:02d}") #02d formate to 2 digit

    playsound("alarm.mp3")

minutes = int(input("How many minutes to wait: "))
seconds = int(input("How many Seconds to wait: "))
total_seconds = minutes * 60 + seconds
alarm(total_seconds)



