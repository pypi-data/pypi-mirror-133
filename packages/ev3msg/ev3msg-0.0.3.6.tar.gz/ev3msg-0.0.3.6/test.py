from ev3msg import EV3

ev3 = EV3("00:16:53:47:27:F4")
input("Press Enter to start Scanning!")
ev3.send_message("start", True)
fields = []
for x in range(25):
    fields.append(int(ev3.get_message("color").value))
    print("Scanned field {}".format(x))
print(fields)
exit()
