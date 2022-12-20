import time
from multiprocessing import Value, Array, Process, Manager
from ctypes import c_char_p


def hub(count, string):
    while count.value<10:
        if count.value==3:
            string.value = "0001"
            print("sent: " + string.value)


def child1(count, string):
    while count.value<10:
        if string.value == "0001":
            print("received: " + string.value)
            string.value = "0001,hello"


def clock(count, string):
    for i in range(11):
        time.sleep(0.001)
        count.value += 1
        print("time: "+str(count.value))
        print("string: "+str(string.value))


if __name__ == '__main__':
    count = Value('i', 0)
    array = Array('i', 15)

    manager = Manager()
    string = manager.Value(c_char_p, "")

    print("count:" + str(type(count)))
    print("array:" + str(type(array)))
    print(array[:])

    hub = Process(target=hub, args=[count, string])
    child1 = Process(target=child1, args=[count, string])
    clock = Process(target=clock, args=[count, string])

    hub.start()
    child1.start()
    clock.start()

    hub.join()
    child1.join()
    clock.join()

    print(array[:])
    print("process ended")