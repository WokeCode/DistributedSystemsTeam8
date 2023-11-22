import threading
from Logger import Logger
from time import sleep
from array import array
import logging


class Pod(threading.Thread):
   
    def __init__(self, pod_ID, electionStatus, leader):
        threading.Thread.__init__(self)
        self.logger = Logger(pod_ID)            # Logging function that will write to a different file
        self.pod_ID = pod_ID                    # Unique ID for each pod (Highest will determine leader)
        self.electionStatus = electionStatus    # Boolean to determine wether or not an election is taking place
        self.leader = leader                    # Leader Pod
        self.connected_pods = set()             # set of connected pods

        self.ok = False                         # Boolean to determine wether or not an 'ok' message has been recieved during election 
        self.electioneers = dict()              # Dictionary containg the pods that should take place in election
        self.recievedelection = False           # Boolean to determine wether or not the pod recieved the election (contra to calling for an election)

    # Function that keeps the pod running
    def run(self):
        while True:
            if not self.electionStatus and not self.ok:
                self.logger.Log(f"Running, Leader {self.leader}")           # Log the leader
                sleep(4)
           
            sleep(1)

    # Connect a pod to another
    def connect(self, other_pod):
        self.logger.Log(f"{self.pod_ID} connected to {other_pod.pod_ID}")
        self.connected_pods.add(other_pod)                                  # Add the pod to the set of connected pods 
        other_pod.connected_pods.add(self)                                  # Connect oneself to the different pods set

    # Disconnect one-self from every pod
    def disconnect(self):
        for pods in self.connected_pods:        # Remove one-self from other pods
            pods.connected_pods.remove(self)
        
        self.connected_pods = set()             # Empty connected pods
    
    # Send a message
    def send(self, other_pod, msg):
        if other_pod in self.connected_pods:
            self.logger.Log(f"sending {msg} to {other_pod.pod_ID}")
            other_pod.recieve(self, msg)                # Call the reciever function in the other pod
        
        elif other_pod == self.leader:                  # If the pods is trying to reach the leader but is disconnected
            self.logger.Log("No response from leader")
            self.election()                             # Start election
        else:
            self.logger.Log(f"FAILED:  {self.pod_ID} tried sending to {other_pod.pod_ID}")

    # Recieve a message
    def recieve(self, sender, msg):
        self.logger.Log(f"Recieved message from {sender.pod_ID}:")
        self.logger.Log(msg)

    # Set leader variable 
    def set_leader(self, leader):
        self.logger.Log(f"Setting leader to {leader.pod_ID}")
        self.leader = leader

    # Will try to remove elements from a dictionary that can be manipulated elsewhere
    def thread_safe_del(self, pod):
        max_retries = 3
        retry_count = 0
        success = False
        
        while retry_count < max_retries and not success:    # Tries 3 time an accepts exceptions
                try:
                    del self.electioneers[pod.pod_ID]       # Remove pod  
                    success = True
                except Exception as e:
                    self.logger.Log(f"Exception: {Exception}")
                    retry_count += 1

    # Recieve an OK from other pod  
    def OK(self):
        self.logger.Log(f"Recieved OK")
        self.ok = True
        self.electionStatus = False
   
    # Recieve new leader 
    def coordinator(self, sender):
        self.logger.Log(f"Recieved new leader {sender.pod_ID}")
        self.set_leader(sender)
        self.electionStatus = False
        self.ok = False
        self.recievedelection = False
    
    # Send coordinator to the different different pods
    def sendCoordinator(self):
        for pod in self.connected_pods:
            self.logger.Log(f"Sending coordinator to {pod.pod_ID}")
            pod.coordinator(self)
        self.electionStatus = False
        self.recievedelection = False
        self.set_leader(self)
        self.ok = False

    def recieve_election(self, sender, electioneers):
        if (sender.pod_ID == self.pod_ID):
            return
        self.logger.Log(f"Recieved election from {sender.pod_ID}")
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
                    self.logger.Log(f"Sending election to {pod.pod_ID}")
                    pod.recieve_election(self, self.electioneers)   # send one self and the electioneers
            
            if not self.ok:
                sleep(5)
                # Find the smallest pod id in dict and check ok:
                min_pod = min(self.electioneers.keys())
                if min_pod != self.pod_ID and not self.ok and self.electionStatus:
                    self.logger.Log(f"Min pod is {min_pod}")
                    pod = self.electioneers[min_pod]
                    sleep(5)
                    self.logger.Log(f"Sending OK to {min_pod}")
                    pod.OK()
                    self.logger.Log(f"Removing {min_pod} from election")
                    self.thread_safe_del(self.electioneers[min_pod])
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

