from ev3msg import EV3

ev3 = EV3('00:16:53:47:27:F4')

ev3.send_message('Command', 'test')
message_object = ev3.get_message('back', timeout=5)
content = message_object.value
type = message_object.d_type
title = message_object.title
ev3.disconnect()
