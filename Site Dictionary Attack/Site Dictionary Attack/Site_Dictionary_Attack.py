
from english_words import get_english_words_set
from requests import Session, post
from os import system
from asyncio import get_event_loop, run, create_task, gather
from aiohttp import ClientSession
from time import sleep

webhook = input("Discord webhook link: ")
prefix = input("Site folder link (example: https://zedpuzzle.neocities.org/start/): ")
processes = int(input("Word batch size (the higher = the faster. if the program crashes, try a lower batch size!): "))
sleepTime = int(input("Wait amount after each batch: (the lower = the faster. if the program crashes, try waiting more!): "))

range_processes = range(processes)

words = list(get_english_words_set(['web2'], lower=True))
file = open("other_words.txt", "r")
data = file.read()
other_words = data.split(" ")

words = words + other_words
while len(words) % processes != 0:
    words.append("no spaces allowed")

count = 0

get = Session().get

def check(responses, links):
    global webhook
    
    for i in range(len(responses)):
        if responses[i] == 200:
            data = {
                "content": links[i],
                "username": "Site Dictionary Attactk"
            }

            post(webhook, json = data)

async def fetch_response(shead, link):
    async with shead(link) as r:
        return r.status

async def get_responses(shead, links):
    tasks = []

    for i in range_processes:
            
        task = create_task(fetch_response(shead, links[i]))
        tasks.append(task)
                           
    responses = await gather(*tasks)    

    return responses                 

async def trylinks(shead, links):
    responses = await get_responses(shead, links)
    check(responses, links)

def get_links(count):
    global prefix
    global words
    
    links = []
    for i in range_processes:
        links.append(prefix+words[count + i])

    return links    

wordcount = len(words)
async def main():
    global count
    
    while count <= len(words):
        links = get_links(count)
        count += processes
    
        async with ClientSession() as session:
            await trylinks(session.head, links)

        print(str(count / wordcount*100)+"%")
        
        sleep(sleepTime)        

if __name__ == '__main__':
    run(main())
