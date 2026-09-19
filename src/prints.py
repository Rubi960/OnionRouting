from colors import Colors as c
from config import MYNODE

def help():
    help = f"""
        This code consists in a direct implementation of nested encryption and onion 
        routing. It is able to encrypt, send, recieve and decrypt arbitrary messages
        using a MQTT message broker as intermediate.

        usage: {c.GREEN}onion.py [options]{c.END}
            options:
                {c.BLUE}-a, --activate{c.END}          Starts the MQTT to recieve messages
                {c.BLUE}-e, --encrypt text{c.END}      Encrypts a given text and returns the result
                {c.BLUE}-d, --decrypt text{c.END}      Decrypts a given ciphertext and returns the result
                {c.BLUE}-s, --send message{c.END}      Encrypts and sends a message

        Made by {c.URL}{c.BOLD}{c.GREEN}Rubén Diz Martínez{c.END}
        """
    print(help)

def dangerIcon():
    return f'{c.RED}{c.BOLD}[!]{c.END}'

def infoIcon():
    return f'{c.YELLOW}{c.BOLD}[*]{c.END}'

def printInfo(info: str):
    print(f'\n\t{infoIcon()}{c.YELLOW} {info}{c.END}\n')

def printError(error: str):
    print('\t' + dangerIcon() + f' {c.RED}' + error + f'{c.END}')

def finalMessage(source, msg):
    s = f"""
        {infoIcon()} {c.YELLOW}Final message recieved:{c.END}

            > {msg}

        {f'{c.GREEN}Sent by {c.BOLD}{source}{c.END}' 
         if source.lower() != "none"
         else f'{c.GREEN}{c.BOLD}Unknown{c.END} {c.GREEN}sender{c.END}'}
    """
    print(s)

def sendNext(nextHop):
    s = f"""
        {infoIcon()} {c.YELLOW}Sending message to the nextHop:{c.END}
                {f'{c.GREEN}{c.BOLD}{MYNODE}{c.END} {c.BLUE}> > >{c.END} {c.URL}{c.GREEN2}{nextHop}{c.END}'}
    """
    print(s)

def stillMe():
    s = f"""
        {infoIcon()} {c.YELLOW}Decrypting next package...{c.END}
    """
    print(s)