import time
from networktables import NetworkTables

if __name__ == "__main__":
    NetworkTables.initialize(server="192.168.255.5")
    while NetworkTables.isConnected() != True:
        time.sleep(1)
    print("we in")