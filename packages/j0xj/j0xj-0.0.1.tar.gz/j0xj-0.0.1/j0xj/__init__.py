class c:
    blue = "\033[1;34m"
    white = "\033[1;37m"
    red = "\033[1;31m"
    green = "\033[1;32m"
    yellow = "\033[1;33m"

def sprint(text, time=0.001):
    from time import sleep
    for letter in text:
        print(letter, end="", flush=True)
        sleep(time)