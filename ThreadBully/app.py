from pod import Pod
from time import sleep

def main():
    print("starting")
    pod0 = None
    pod1 = Pod(1, False, pod0)
    pod2 = Pod(2, False, pod1)
    pod3 = Pod(3, False, pod1)
    pod4 = Pod(4, False, pod1)

    pod1.connect(pod2)
    pod1.connect(pod3)
    pod1.connect(pod4)

    pod2.connect(pod3)
    pod2.connect(pod4)

    pod3.connect(pod4)


    pod1.send(pod2, "Hej")

    sleep(2)
    print("STARTING THREADS")
    pod1.start()
    pod2.start()
    pod3.start()
    pod4.start()

    #pod2.send(pod0, "Hej")
    sleep(1)
    print("Sending hej to 0")
    pod1.send(pod0, "Hej")

    print("Hi")




if __name__ == "__main__":
    main()

