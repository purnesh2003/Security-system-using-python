import pywhatkit
from datetime import datetime
import csv



now = datetime.now()


# Extract hour and minute as integers
current_hour = now.hour
current_minute = now.minute + 1



# Extract hour and minute as integers
reader ="hi ninu shanda"

print(current_hour)
print(current_minute)
pywhatkit.sendwhatmsg('+919916149904',reader,current_hour,current_minute)