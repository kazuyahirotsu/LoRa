class NetworkHelper:
    def __init__(self, time):
        self.time = time
        self.sending = False
        self.sending_dst = 0
        self.sending_message = ""

    def hello_world(self):
        print("hello world from networkHelper")

    def add_time(self):
        self.time += 1

    def send(self, dst, message):
        self.sending = True
        self.sending_dst = dst
        self.sending_message = message


class NetworkSimHub:
    def __init__(self, child_num, time, NetworkHelper):
        self.child_num = child_num
        self.time = time
        self.networkHelper = NetworkHelper


    def hello_world(self):
        print("hello world")
        self.networkHelper.hello_world()
    
    def send(self, dst , message):
        self.networkHelper.send(dst, message)
    
    def add_time(self):
        self.time += 1


class NetworkSimChild:
    
    def __init__(self, id, time, NetworkHelper):
        self.id = id
        self.sleeping = False
        self.time = time
        self.networkHelper = NetworkHelper

    def hello_world(self):
        print("hello world")
    
    def add_time(self):
        self.time += 1
        


nsHelper = NetworkHelper(0)
ns0 = NetworkSimHub(1,0,nsHelper)
ns1 = NetworkSimChild(1,0,nsHelper)
for i in range(10):
    nsHelper.add_time()
    ns0.add_time()
    ns1.add_time()
    print(nsHelper.time, ns0.time, ns1.time)