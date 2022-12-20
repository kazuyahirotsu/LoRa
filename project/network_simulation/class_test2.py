class NetworkSimHub:
    def __init__(self, child_num, time):
        self.child_num = child_num
        self.time = time
        self.receivedMessage = ""

    def send(self, dst, message):
        dst.receivedMessage = message
        print("sent: "+ str(message))
    
    def add_time(self, time):
        self.time += time

    def check_message(self):
        print("received: "+ str(self.receivedMessage))

class NetworkSimChild:
    def __init__(self, id, time):
        self.id = id
        self.sleeping = False
        self.time = time
        self.receivedMessage = ""

    def send(self, dst, message):
        dst.receivedMessage = message
        print("sent: "+ str(message))

    def add_time(self, time):
        self.time += time

    def check_message(self):
        print("received: "+ str(self.receivedMessage))
    
    def respond_with_data(self, dst):
        if self.receivedMessage!="":
            self.send(dst, "hello from "+str(self.id))

        
ns0 = NetworkSimHub(1,0)
ns1 = NetworkSimChild(1,0)

for i in range(10):
    ns0.add_time(0.1)
    ns1.add_time(0.1)
    print(ns0.time, ns1.time)
    if i == 3:
        ns0.send(ns1,"hello")
        ns0.add_time(0.3)
        ns1.add_time(0.3)
    ns0.check_message()
    ns1.check_message()