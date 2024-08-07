import machine
from mfrc522 import MFRC522
import time

# Set up the SPI interface for the MFRC522 RFID reader
sck = machine.Pin(2)
mosi = machine.Pin(3)
miso = machine.Pin(4)
rst = machine.Pin(5)
cs = machine.Pin(6)
spi = machine.SPI(0, baudrate=100000, polarity=0, phase=0, sck=sck, mosi=mosi, miso=miso)

# Initialize the MFRC522 RFID reader
reader = MFRC522(spi_id=0, sck=2, miso=4, mosi=3, cs=1, rst=0)

# Set up the LED and buzzer for feedback
red_led = machine.Pin(7, machine.Pin.OUT)
buzzer = machine.Pin(8, machine.Pin.OUT)
green_led = machine.Pin(9, machine.Pin.OUT)

# Set up the database of RFID tags and corresponding student names
database = {
    '0x333c2c0f': 'Om Kadam',
    '0x138cd59d': 'Manav Ghadi'
}

# Set up the attendance log as an empty list
attendance_log = []

# Main loop
while True:
    # Scan for an RFID tag
    (stat, tag_type) = reader.request(reader.REQIDL)

    if stat == reader.OK:
        # A tag was found, so get the UID
        (stat, uid) = reader.SelectTagSN()

        if stat == reader.OK:
            # Convert the UID to a string
            uid_str = "0x{:02x}{:02x}{:02x}{:02x}".format(uid[0], uid[1], uid[2], uid[3])
            print("UID:", uid_str)  # Print UID for debugging purposes

            # Check if the tag is in the database
            if uid_str in database:
                # Get the student name from the database
                student_name = database[uid_str]

                # Check if the student is already in the attendance log
                if student_name in attendance_log:
                    # Student is already in attendance log, so remove them
                    attendance_log.remove(student_name)

                # Add the student to the attendance log
                attendance_log.append(student_name)

                # Provide feedback with the LED and buzzer
                green_led.on()
                buzzer.on()
                time.sleep(1)
                green_led.off()
                buzzer.off()

                # Print the updated attendance log
                print("Valid card detected.")
                print("Attendance log:")
                for student in attendance_log:
                    print(student)
            else:
                # The tag is not in the database, so provide feedback with the LED and buzzer
                red_led.on()
                buzzer.on()
                time.sleep(1)
                red_led.off()
                buzzer.off()

                print("Invalid card detected.")

