from .ev3mailbox import mailbox
import time
import sys
import bluetooth
from threading import Thread
import time
import re

class EV3Searcher:
    def __init__(self, status_messages=True) -> None:
        self.__status_messages = status_messages
        pass

    def search_all(self, duration=10):
        if self.__status_messages:
            print("{}: Searching for all Bluetooth Devices in your Area".format(time.asctime()), file=sys.stderr)
        devices = bluetooth.discover_devices(duration=duration, lookup_names=True)
        if self.__status_messages:
            for x, y in devices:
                print("-----------------")
                print(f"Device Name: {y}")
                print(f"Mac Address: {x}")
        return devices

    def search_by_name(self, name):
        if self.__status_messages:
            print("{}: Searching for an EV3 Called {}".format(time.asctime(), name), file=sys.stderr)
        devices = bluetooth.discover_devices(lookup_names=True)
        for x, y in devices:
            if y == name:
                print("{}: Found your EV3 with the address {}".format(time.asctime(), x), file=sys.stderr)
                return x
        print("{}: Couldn't find your EV3 {}".format(time.asctime(), name), file=sys.stderr)
        return None

class Message:
    def __init__(self, name, value, d_type=None, payload=None):
        self.title  = name
        self.value = value
        self.d_type = d_type

class EV3:
    """
    Representation of the EV3 mailbox
    """
    def __init__(self, address, status_messages=True):
        """
        Connect to the EV3
        """
        if not re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", address.lower()):
            name = address
            address = EV3Searcher(status_messages=status_messages).search_by_name(address)
            if address == None:
                raise Exception("No EV3 with name {} found".format(name))
        if status_messages:
            print("{}: Connection attempt to {}".format(time.asctime(), address), file=sys.stderr)
        bt_socket = bluetooth.BluetoothSocket()
        try:
            bt_socket.connect((address, 1))
            bt_socket.settimeout(5)
            self.bt_socket = bt_socket
            if status_messages:
                print("{}: BT Connected".format(time.asctime()), file=sys.stderr)
        except Exception as e:
            if status_messages:
                print("{}: BT failed to connect - {}".format(time.asctime(),e), file=sys.stderr)
            raise Exception("Failed to connect to EV3") from None

        self.__received_messages = []
        self.__status_messages = status_messages
        Thread(target=self.__recv_thread, daemon=True).start()

    def __recv_thread(self):
        """
        Receive messages from the EV3
        """
        while self.bt_socket:
            try:
                payload = self.bt_socket.recv(1024)
                content = mailbox.decode(payload)
                name = content.name
                value = content.value
                typ = content.d_type
                self.__received_messages.append({"title": name, "content": value, "type": typ})
                if self.__status_messages:
                    print("{}: Received message with title: {}".format(time.asctime(), name), file=sys.stderr)
            except Exception as e:
                continue

    def send_message(self, title, value, d_type=None):
        """
        Send a message to the EV3
        """
        ev3mailbox = mailbox.encode(title, value, d_type)
        self.bt_socket.send(ev3mailbox.payload)
        if self.__status_messages:
            print("{}: Sent Message".format(time.asctime()), file=sys.stderr)

    def disconnect(self):
        """
        Disconnect from the EV3
        """
        try:
            self.bt_socket.close()
            self.bt_socket = None
            self.__received_messages = []
        except:
            pass
        if self.__status_messages:
            print("{}: BT Disconnected".format(time.asctime()), file=sys.stderr)

    def get_message(self, name=None, timeout=5):
        """
        Wait for a Message with a specific title
        Default Timeout = 5 Seconds
        """
        n = 0.0
        print("{}: Waiting for Message".format(time.asctime()), file=sys.stderr)
        while True:
            for x in self.__received_messages:
                if x["title"] == name:
                    msg = x["content"]
                    d_type = x["type"]
                    return Message(name, msg, d_type)
            if n >= timeout:
                return None
            time.sleep(0.1)
            n += 0.1
        