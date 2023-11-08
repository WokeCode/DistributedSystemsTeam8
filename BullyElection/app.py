import asyncio
from aiohttp import web
import os
import socket
import random
import aiohttp
import requests

POD_IP = str(os.environ['POD_IP'])
WEB_PORT = int(os.environ['WEB_PORT'])
POD_ID = random.randint(0, 100)
LEADER = 0

async def setup_k8s():
    # If you need to do setup of Kubernetes, i.e. if using Kubernetes Python client
	print("K8S setup completed")

async def get_pod_id(session, pod_ip):
    endpoint = '/pod_id'
    url = f'http://{pod_ip}:{WEB_PORT}{endpoint}'
    async with session.get(url, timeout=5) as response:
        return pod_ip, await response.json()
 

async def election_check(other_pods, own_ID):
    print("election check")
    max_other_ID = max(other_pods.values())
    max_ID = max(max_other_ID, POD_ID)
    #CHANGE IN LEADER ELECTION CHECKING
    #if LEADER != max_ID:
    if POD_ID > max_other_ID:
        return True
    else:
        return False

# POST new leader
async def send_leader(other_pods, new_leader):
    for ip in other_pods:
        print(f"Attempting to send {new_leader} to {ip}")
        try:
            print(f"sending leader {new_leader} to {ip}")
            endpoint = '/receive_answer'
            url = f'http://{ip}:{WEB_PORT}{endpoint}'
            async with aiohttp.ClientSession() as session:
                data = {'leader': new_leader}
                async with session.post(url, json=data, timeout = 5) as response:
                    response_text = await response.text()
                    print("RESPONSE:")
                    print(response_text)
            await asyncio.sleep(5)

        except Exception as e:
            print("Exception in send_leader")
            print(e)
            await asyncio.sleep(2)


async def election(other_pods):
    try:
        print("election")
        max_ID = max(other_pods.values())
        if POD_ID > max_ID:
            new_leader = POD_ID
        else:
            new_leader = max_ID
        
        await send_leader(other_pods, new_leader)
        return new_leader
    except Exception as e:
            print("Exception in election")
            print(e)
            await asyncio.sleep(2)
            return 0

#POST /receive_answer leader
async def receive_answer(request):
    print("RECIEVED LEADER")
    data = await request.text()
    try:
        data = await request.json()  # Parse JSON data from the request
        int_value = data.get('leader')
        if int_value is not None:
            print(f"recieved data {int_value}")
        else:
            print("GOT")
            print(int_value)
            print("ERROR IN RECIEVING DATA")
        received_leader = int(int_value)
        print(f"Received leader: {received_leader}")
        global LEADER
        LEADER = received_leader
    except Exception as e:
            print("Invalid leader ID recieved")
            print(e)
            await asyncio.sleep(2)

async def run_bully():
    num_request = 0
    while True:
        try:
            print("Running bully")
            await asyncio.sleep(5) # wait for everything to be up
            
            # Get all pods doing bully
            ip_list = []
            print("Making a DNS lookup to service")
            response = socket.getaddrinfo("bully-service",0,0,0,0)
            print("Get response from DNS")
            for result in response:
                ip_list.append(result[-1][0])
            ip_list = list(set(ip_list))
            print(f"Got {len(ip_list)} pod ip's + my own")
            # Remove own POD ip from the list of pods
            ip_list.remove(POD_IP)
            print("Got %d other pod ip's" % (len(ip_list)))
            
            # Get ID's of other pods by sending a GET request to them
            await asyncio.sleep(random.randint(1, 5))
            other_pods = dict()
            print("Getting ID's of other pods")
            async with aiohttp.ClientSession() as session:
                print("Getting pod id")
                tasks = [get_pod_id(session, pod_ip) for pod_ip in ip_list]
                results = await asyncio.gather(*tasks)
                for pod_ip, pod_id in results:
                    other_pods[pod_ip] = pod_id

            # Other pods in network
            print(other_pods)

            # Number of requests done
            print(f"number of requests: {num_request}")
            num_request += 1

            election_time = await election_check(other_pods, POD_ID)
            if election_time:
                print("running election")
                new_leader = await election(other_pods)
                global LEADER 
                LEADER = new_leader
                print(f"leader is {new_leader}")
                print("election done")
            
            # Leader
            if POD_ID == LEADER:
                print("LEADER IS SELF")
            else:
                print(f"LEADER IS {LEADER}")

            # Sleep a bit, then repeat
            await asyncio.sleep(2)
        except Exception as e:
            print("Exception in run_bully")
            print(e)
            await asyncio.sleep(2)
    
#GET /pod_id
async def pod_id(request):
    print("returning pod id")
    return web.json_response(POD_ID)



#POST /receive_election
async def receive_election(request):
    pass

#POST /receive_coordinator
async def receive_coordinator(request):
    pass

async def background_tasks(app):
    task = asyncio.create_task(run_bully())
    yield
    task.cancel()
    await task

if __name__ == "__main__":
    print("version 3")
    app = web.Application()
    app.router.add_get('/pod_id', pod_id)
    app.router.add_post('/receive_answer', receive_answer)
    app.router.add_post('/send_leader', send_leader)
    app.router.add_post('/receive_election', receive_election)
    app.router.add_post('/receive_coordinator', receive_coordinator)
    app.cleanup_ctx.append(background_tasks)
    web.run_app(app, host='0.0.0.0', port=WEB_PORT)