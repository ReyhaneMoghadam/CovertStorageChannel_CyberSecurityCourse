import os
import platform    # For getting the operating system name
import subprocess  # For executing a shell command
import time
PING_OFFSET = 280

class sender:
    offset = 280
    no_confirmation_size = 0

    def __init__(self, n_offset):
        self.offset = n_offset
        self.no_confirmation_size = self.__check_confirmation()
        self.reset()
    
    def __ping(self, host):
    # Option for the number of packets as a function of
        param = '-n' if platform.system().lower()=='windows' else '-c'

        # Building the command. Ex: "ping -c 1 google.com"
        command = ['ping', param, '1', host]

        f = open("./ping/log.txt", "w")
        subprocess.call(command, stdout=f)
        f.close()
    def __update_log(self, n):
        self.__ping("8.8.8.8")
        size = os.path.getsize('./ping/log.txt')
        left = n - size
        if(left < 0):
            left = 0
        f = open("./ping/log.txt", "a")
        for i in range(left):
            f.write(" ")
    
    def reset(self):
        f = open("./ping/log.txt", "w")
        f.write("No history of outgoing connections.")
    
    def __check_confirmation(self):
        return os.path.getsize('./arp/arp.txt')

    def send_message(self, val):
        print("sending: {} with ord value of {}".format(val, ord(val)))
        self.no_confirmation_size = self.__check_confirmation() # get preliminary file size
        self.__update_log(ord(val) + self.offset) #updates file so its byte size reprsents ascii data

        while(self.no_confirmation_size == self.__check_confirmation()):
            pass
        self.no_confirmation_size = self.__check_confirmation() # get changing file size
        self.reset() # change file back to no message

        # wait for sender to reset receive confirmation to avoid skips
        confirm_received = False
        while(not confirm_received):
            time.sleep(1)
            if(self.no_confirmation_size == self.__check_confirmation()):
                confirm_received = True
            self.no_confirmation_size = self.__check_confirmation() # get changing file size

class receiver:
    offset = 280
    no_message_size = 35
    file_size = 0
    switch = False
    expecting = False
    message = []
    def __init__(self, n_offset, n_no_message_size):
        self.offset = n_offset
        self.no_message_size = n_no_message_size
        self.switch = False
        self.expecting = False
        self.message = []
        self.file_size = os.path.getsize('./ping/log.txt')
    
    def __arp(self):
        f = open("./arp/arp.txt", "w")
        subprocess.call("arp", stdout=f)

    def __receive_confirmation(self):
        if(self.switch):
            self.__arp()
            self.switch = False
        else:
            f = open("./arp/arp.txt", "w")
            f.write("No Address Resolution Protocol Recorded.")
            self.switch = True
    
    # returns true if character was recorded returns false otherwise
    def watch(self):
        self.file_size = os.path.getsize('./ping/log.txt')
        # if file size has changed to relay message -> get info
        if (self.file_size >= self.offset):
            verify_change = False
            while(not verify_change): # wait for file size change to stop
                time.sleep(1) # wait a second to allow full changing of file
                if(self.file_size == os.path.getsize('./ping/log.txt')):
                    verify_change = True
                self.file_size = os.path.getsize('./ping/log.txt')
                
            self.message.append(chr(self.file_size - self.offset))
            print("file size: {}, To add: {}".format(self.file_size, chr(self.file_size - self.offset)))
            self.__receive_confirmation() # confirm with sender message was received
            
            while(os.path.getsize('./ping/log.txt') > self.offset): # wait for confirmation to process with sender
                pass
            return True # message received
        return False # no message received

    def get_hidden_message(self):
        return self.message
    

def main():
    pass

if __name__ == "__main__":
    main()