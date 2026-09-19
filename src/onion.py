import sys, ast
from encrypt import getEncrypted
from decrypt import decapsule
from prints import help,printError,sendNext,stillMe,printInfo
from config import MYNODE, MQTT_USER, MQTT_PASSWD, MQTT_PORT, MQTT_IP
import paho.mqtt.client as mqtt

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

def publishMessage(nextHop: str, msg: bytes):
    mqttc.publish(topic=nextHop,payload=msg)


def stillForMe(hop, msg):
    while True:
        hop, msg = decapsule(msg)
        if hop != MYNODE:
            return hop, msg
        stillMe()


def on_message(client, userdata, message):
    try:
        hop, msg = stillForMe(MYNODE, message.payload)
        if hop is not None:
            sendNext(hop)
            publishMessage(hop, msg)
    except Exception as e:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        printError(f"Something went wrong: {ex_value}\n")


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"Failed to connect: {reason_code}.")
    else:
        client.subscribe(MYNODE)


def conn():
    mqttc.username_pw_set(MQTT_USER, MQTT_PASSWD)
    mqttc.connect(MQTT_IP, MQTT_PORT)
    mqttc.on_connect= on_connect
    mqttc.on_message= on_message


def getAllValues():
    source = getSource().encode('ascii')
    route = getRoute()
    msg = getMessage().encode('ascii')
    return source, route, msg


def encrypt():
    source, route, msg = getAllValues()
    hop, send = getEncrypted(source,route,msg)
    print(f'Send message to {hop}')
    print()
    print(send)


def decrypt():
    printInfo("Format: b'<nextNode><cipherKey><cipherText>'")
    hop, capsule = decapsule(ast.literal_eval(getMessage()))
    if capsule != None:
        print(capsule)


def send():
    conn()
    source, route, msg = getAllValues()
    hop, send = getEncrypted(source,route,msg)
    publishMessage(hop, send)


def checkOptions():
    size = len(sys.argv)
    if size == 2:
        command = sys.argv[1]
        if command in ["-a","--activate"]:
            conn()
            mqttc.loop_forever()
        if command in ["-e","--encrypt"]:
            encrypt()
        elif command in ["-d","--decrypt"]:
            decrypt()
        elif command in ["-s","--send"]:
            send()
        else:  
            help()
    else:
        help()


def checkValidNode(node):
    if len(node)< 1 or len(node) > 5:
        return False
    return True      


def getSource():
    source = input('Input a valid id or press Enter to send Anonymously\n')
    print()
    return source if checkValidNode(source) else "none"


def getRoute():
    while True:
        correct = True
        r = input('Enter the route separating the nodes with \',\'\n')
        print()

        route = r.split(',')

        if route == ['']:
            printError("Enter at least 1 node to send the message\n\n")
            continue
        
        for node in route:
            if not checkValidNode(node):
                printError(f'Node \'{node}\' is invalid\n')
                correct = False
                break
        
        if correct == False:
            continue
        
        return route
        

def getMessage():
    text = ''
    while True:
        text = input('Enter the message\n')
        print()
        if text != '':
            break
        printError("Message cannot be empty\n\n")    
    return text


if __name__ == '__main__':
    checkOptions()
