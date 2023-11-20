import threading
from Logger import Logger
from time import sleep
from array import array
import logging


class Pod(threading.Thread):
   
    def __init__(self, pod_ID, electionStatus, leader):
        threading.Thread.__init__(self)
        self.logger = Logger(pod_ID)
        self.pod_ID = pod_ID
        self.electionStatus = electionStatus
        self.leader = leader
        self.connected_pods = set()
        self.ok = False
        self.electioneers = dict()
        self.recievedelection = False

    def run(self):
        while True:
            if not self.electionStatus and not self.ok:
                self.logger.Log(f"Running, Leader {self.leader}")
                sleep(4)
            sleep(1)


    def connect(self, other_pod):
        self.logger.Log(f"{self.pod_ID} connected to {other_pod.pod_ID}")
        self.connected_pods.add(other_pod)
        other_pod.connected_pods.add(self)

    def disconnect(self):
        for pods in self.connected_pods:
            pods.connected_pods.remove(self)
    
    def send(self, other_pod, msg):
        if other_pod in self.connected_pods:
            self.logger.Log(f"sending {msg} to {other_pod.pod_ID}")
            other_pod.recieve(self, msg)
        
        elif other_pod == self.leader: # If the pods is trying to reach the leader but is disconnected
            self.logger.Log("I AM DUMBD")
            self.election()            # Start election
        else:
            self.logger.Log(f"FAILED:  {self.pod_ID} tried sending to {other_pod.pod_ID}")


    def recieve(self, sender, msg):
        self.logger.Log(f"Message from {sender.pod_ID}:")
        self.logger.Log(msg)

    def set_leader(self, leader):
        self.logger.Log(f"Setting leader to {leader.pod_ID}")
        self.leader = leader

    def thread_safe_del(self, pod):
        max_retries = 3
        retry_count = 0
        success = False
        while retry_count < max_retries and not success:
            try:
                del self.electioneers[pod.pod_ID]
                success = True
            except Exception as e:
                self.logger.Log(f"Exception: {Exception}")
                retry_count += 1


    def OK(self):
        self.logger.Log(f"OK")
        self.ok = True
        self.electionStatus = False

        max_retries = 4
        retry_count = 0
        success = False
        while retry_count < max_retries and not success:
            try:
                for pod in self.electioneers.values():
                    try:
                        if self.pod_ID != pod.pod_ID:
                            pod.recieve_OK(self)
                    except Exception as e:
                        self.logger.Log(f"Exception in OK for: {e}")
                self.logger.Log("SUCCESS")
                success = True
            except Exception as e:
                self.logger.Log(f"{e}")
                retry_count += 1
        return
        

    def recieve_OK(self, pod):
        self.logger.Log(f"Ok from {pod.pod_ID}")
        self.logger.Log(f"will try to remove {pod.pod_ID} from {self.electioneers.keys()}")
        try:
            self.thread_safe_del(pod)
            self.logger.Log(f"Removed {pod.pod_ID}")
        except Exception as e:
            self.logger.Log(f"tried removing {pod.pod_ID}")

    def coordinator(self, sender):
        self.logger.Log(f"recieved new leader {sender.pod_ID}")
        self.set_leader(sender)
        self.electionStatus = False
        self.ok = False
        self.recievedelection = False

    def sendCoordinator(self):
        for pod in self.connected_pods:
            self.logger.Log(f"{self.pod_ID} sending coordinator to {pod.pod_ID}")
            pod.coordinator(self)
        self.electionStatus = False
        self.recievedelection = False
        self.leader = self
        self.ok = False

    def recieve_election(self, sender, electioneers):
        if (sender.pod_ID == self.pod_ID):
            return
        self.logger.Log(f"recieved election from {sender.pod_ID}")
        self.recievedelection = True
        electioneers[sender.pod_ID] = sender
        self.electioneers = electioneers        
        self.election()

    def election(self):
        self.logger.Log(f"Election")
        self.electionStatus = True

        if not self.recievedelection:                       #If the pod detected an election was needed
            self.electioneers = {pod.pod_ID: pod for pod in self.connected_pods if pod.pod_ID >= self.pod_ID}   # Then it should set the list of who should take part in it
            self.logger.Log(self.electioneers)

        while len(self.electioneers) > 1 and self.electionStatus and not self.ok:
            for pod in self.electioneers.values():
                if ((pod.pod_ID > self.pod_ID) and (not pod.electionStatus) and (not self.ok) and (not pod.ok)):
                    self.logger.Log(f"sending election to {pod.pod_ID}")
                    pod.recieve_election(self, self.electioneers)   # send one self and the electioneers
            
            if not self.ok:
                sleep(5)
                # Find the smallest pod id in dict and check ok:
                min_pod = min(self.electioneers.keys())
                if min_pod != self.pod_ID and not self.ok and self.electionStatus:
                    self.logger.Log(f"Min pod is {min_pod}")
                    pod = self.electioneers[min_pod]
                    sleep(5)
                    pod.OK()
                sleep(3)
                
                if len(self.electioneers) > 1:
                    self.logger.Log(self.electioneers)
                    self.logger.Log(f"Not finished")
                    try:
                        for pod in self.electioneers.values():
                            pod.recieve_election(self,self.electioneers)
                    except Exception as e:
                        self.logger.Log(f"{e}")
                elif self.electionStatus and not self.ok:
                    self.logger.Log(f"Finished, am leader")
                    self.sendCoordinator()
                    self.electionStatus = False
                    self.recievedelection = False
                    return
            else: return
        pass

# Set loggers logging function
#Logger.LogFunc = lambda x : print(x)

pod0 = Pod(0, False, None)
pod1 = Pod(1, False, pod0)
pod2 = Pod(2,False,pod0)
pod3 = Pod(3,False,pod0)
pod4 = Pod(4,False,pod0)


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

pod1.send(pod0, "Hej")
sleep(50)

pod3.send(pod4, "Hej")