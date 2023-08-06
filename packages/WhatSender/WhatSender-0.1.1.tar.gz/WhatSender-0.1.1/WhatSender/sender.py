from pyautogui import click, locateCenterOnScreen, size, moveTo
import time
import webbrowser
from urllib.parse import quote
from datetime import datetime
import termcolor
import os
from sys import platform



class SendMessage():
    '''Send Whatsapp messages with one line of code!\n
    The class takes this params: reciver, message, send_time -> all of them required.\n
    You can call the class like a function, you don't need to make an object out of it becaues its
    executing on the __init__ function.\n
    \n
    Make sure you have all the dependecise before running!\n
    The App has been created by Ido Barel, and it's free to use.'''
    def __init__(self, reciver, message, send_time) -> None:
        send_png_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00"\x00\x00\x00-\x08\x06\x00\x00\x00\xcb\x11\xb9\x17\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00\tpHYs\x00\x00\x0e\xc3\x00\x00\x0e\xc3\x01\xc7o\xa8d\x00\x00\x01 IDATXG\xed\x97\xcd\r\x82@\x10FW{`\xb9y\xf2`"\x16\x81\x14\xa1\xb1@\xa3E E\x08E\x00E(\x83K\xa2\x13\xdc\xdfA9\xccK6.\\|3\xdf\x0e\x81\xc5j\xbdy\x88\x19\xb0T\xbf\x7f\x87E0,\x82a\x11\x0c\x8b`X\x04\xc3"\x18\xa3\xc8.\xd9\xaa\xdd\xb4\x18_\x03N\xc7\x83\xda\tq\xbe\\\xd5\x8e\x1e\xa7h@\nV\x1cKu\x87\x0e\xaf3\x92\xa5i/D\x19\x9bS4:Bc#\x9b\x9a\xd0\xd8\xc8\xc7\xd776\xb2ht\xd8\xc4f\xf5\x16\x0f\xed\x96Q\xd4U\x99\xa8;~\xe4E!\xea\xbaQW\x9f\x90|N@\x0cRJ\x11w\xcb\x86{Yv\xabRW/\x82\xcf\x08t\xabi\xdb~_7\xe3\xd5b@\x1a\xe3\x14\x8dK\xd5\x18\x90,\xab\xca?\x9a\xd0\xc3j\x12\x18 \x1f\xdf\x01\x10\x80i\xc9o\xdf\x0f\xe8;\xa4\x1d\xb1\xad~\x0c\x92\x8e\x80\x00\x8c\xa6m\xf5c\x04\x89\xb8\xb6_\x87s4!\xed\xd7a\xdd\x11\x8a\xf6\xeb0v$\xdb\xa7\xfd\x9fO\x8d\xd5\x03\xed\x17L\xf6\x1cq\x85E0,\x82a\x11\x0c\x8b`f""\xc4\x13Z\x90\x84Bf-Gk\x00\x00\x00\x00IEND\xaeB`\x82'
        close_png_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00!\x00\x00\x00\x1c\x08\x06\x00\x00\x00\xef\x00\xd6\x1c\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00\tpHYs\x00\x00\x0e\xc3\x00\x00\x0e\xc3\x01\xc7o\xa8d\x00\x00\x00\xc8IDATHKc\xe4\xe1\x11\xff\xcf0\xc0\x80\tJ\x0f(\x18u\x04\x0c\x8c:\x02\x06F\x1d\x01\x03D;\xe2\xf3\xe7\x17\x0c\xd1\xd1\xe1P\x1e&\x00\xc9\x81\xd4\x90\x03\x88vDFF>\xc3\x8c\x19\x13\xb1:\x04$\x06\x92\x03\xa9!\x070\xb3\xb1\xf14@\xd9x\xc1\xe5\xcbW\x19\x1e=z\x0c\xb6\x0cD\x83\xf8 \x80\xec\x80\xa5KW\x82\xc5H\x05D;\x02\x04\xd0\x1d\xa2\xa7\xa7C\xb1\x03@\x80\xac\xba\x03\xe6{\x10\xa0\xd4\x01 04\xb3(r\x1a\x00a\x10\x1b[b%\x05\x90\x94&\xd0\x13!\xae\xc4J* \xda\x11\xb8r\x015\x1cBt\xc2\x04\x15D\xf8\x12!\xcc\x91\xbc\xbc\x12P\x11\xe2\xc1h\xcb\n\x06F\x1d\x01\x03\xa3\x8e\x80\x81QG\xc0\xc0\xa8# \x80\x81\x01\x00\x05wsO$\x07\x07\x1f\x00\x00\x00\x00IEND\xaeB`\x82'
        self._download_Image(send_png_bytes, "send.png")
        self._download_Image(close_png_bytes, "close.png")
        self._help()
        self.reciver = reciver
        self.message = message
        self.send_time = send_time
        self.sent = False
        self.WIDTH, self.HEIGHT = size()
        while True:
            if self._compareTime():
                self.send_message()

    def _web(self, receiver: str, message: str) -> None:
        """Opens WhatsApp Web based on the Receiver"""
        webbrowser.open(
            "https://web.whatsapp.com/send?phone="
            + receiver
            + "&text="
            + quote(message)
        )

    def send_message(self):
        self._web(receiver=self.reciver, message=self.message)
        time.sleep(2)
        send_icon = self._waitCheckOnScreen("send.png")
        time.sleep(1)
        click(send_icon)
        print(termcolor.colored("All done!","green"))
        self.sent = True
        time.sleep(3)
        self._close(0)

    def _waitCheckOnScreen(self, filename):
        printed = False
        while locateCenterOnScreen(filename) == None:
            if not printed:
                print("Scan code if needed.")
                printed = True
        return locateCenterOnScreen(filename)

    def _compareTime(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        return self.send_time == current_time

    def _close(self, code:int):
        close_btn = self._waitCheckOnScreen("close.png")
        click(close_btn)
        print("Closed.")
        moveTo(self.WIDTH // 2, self.HEIGHT // 2, 0.2)
        exit(code)

    def __str__(self) -> str:
        if self.sent:
            return f"Sent {self.message} TO {self.reciver}"
        else:
            return f"Hasent sent yet."

    def _download_Image(self, bytes, filename):
        path = f"C:\Users\Administrator\AppData\Local\Programs\Python\Python39\Lib\site-packages\WhatSender\{filename}"
        open(path, "wb").write(bytes)
    
    def _clear(self):
        if platform == "win32":
            os.system("cls")
        else:
            os.system("clear")

    def _help(self):
        print(termcolor.colored("Make sure you are not closing the app!".upper(), "red"))
        print(termcolor.colored("IT WILL SHUTDOWN AUTOMATICLY AFTER SENDING THE MESSAGE!", "blue"))
        print(termcolor.colored("MAKE SURE YOURE PHONE IS CHARGED AND HAVE A WIFI CONNECTION!", "green"))
        print(termcolor.colored("TO CLOSE CTRL + C", 'red'))


if __name__ == "__main__":
    try:
        SendMessage("+972544985275", "TEST", "12:05")
    except KeyboardInterrupt:
        print("Closed..")
        exit(0)

