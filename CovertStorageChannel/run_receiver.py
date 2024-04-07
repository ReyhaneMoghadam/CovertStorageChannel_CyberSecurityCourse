from covert_channel import receiver, PING_OFFSET
import time

def run_receiver():
    proc = receiver(PING_OFFSET, 35)
    channel_active = True

    while(channel_active):
        if(proc.watch()):
            if(len(proc.get_hidden_message()) > 0):
                if(proc.get_hidden_message()[-1] == '\0'):
                    channel_active = False
    hidden_message = proc.get_hidden_message()
    i = 0
    while(hidden_message[i] != '\0'):
        print(hidden_message[i], end='')
        i += 1

run_receiver()
