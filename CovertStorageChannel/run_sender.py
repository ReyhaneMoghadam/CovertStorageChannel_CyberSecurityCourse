from covert_channel import sender, PING_OFFSET

def run_sender():
    proc = sender(PING_OFFSET)
    message = input("Message: ")

    for c in message:
        proc.send_message(c)
    proc.send_message('\0') # to signify end of message
run_sender()