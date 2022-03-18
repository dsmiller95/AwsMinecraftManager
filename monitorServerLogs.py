import time
import sys
import re
import boto3
import os
session = boto3.Session(region_name="us-west-2")
client = session.client('cloudwatch')

playerCountMatch = re.compile("\[(\d\d:\d\d:\d\d)\] \[Server thread\/INFO\] \[minecraft\/DedicatedServer\]: There are (\d+) of a max of (\d+) players online:", re.MULTILINE | re.DOTALL)
lagSpikeMatch = re.compile("\[(\d\d:\d\d:\d\d)\] \[Server thread\/WARN\] \[minecraft\/MinecraftServer\]: Can't keep up! Is the server overloaded\? Running (\d+)ms or (\d+) ticks behind", re.MULTILINE | re.DOTALL)


def follow(thefile):
    thefile.seek(0,2) # Go to the end of the file
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1) # Sleep briefly
            continue
        yield line


def logChanges(fileName):
    with open(fileName) as file:
        for line in follow(file):
            playCountMatch = playerCountMatch.search(line)
            if playCountMatch:
                playCount = int(playCountMatch.group(2))
                print("found player count " + str(playCount))
                client.put_metric_data(
                    Namespace='Minecraft',
                    MetricData=[{
                        'MetricName': 'MinecraftPlayerCount',
                        'Value': playCount,
                        'Unit': 'Count'
                    }]
                )
                continue
            lagSpike = lagSpikeMatch.search(line)
            if(lagSpike):
                spikeTime = int(lagSpike.group(2))
                lagMessage = "detected lag spike of " + str(spikeTime) + "ms or " + lagSpike.group(3) + " ticks";
                print(lagMessage)
                printToMinecraftServerChat(lagMessage)
                
                client.put_metric_data(
                    Namespace='Minecraft',
                    MetricData=[{
                        'MetricName': 'LagSpikeTime',
                        'Value': spikeTime,
                        'Unit': 'Milliseconds'
                    }]
                )
                continue

def printToMinecraftServerChat(message):
    command = """/usr/bin/screen -p 0 -S mc-server -X eval 'stuff "say """ + message + """ "\015'"""
    os.system(command)

logChanges(sys.argv[1])
