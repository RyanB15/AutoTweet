import discord
import asyncio
import tweepy
import time
import requests
import datetime

#'Tweepy' Twitter API authentication data
consumer_key = 'otXd4O6dMglxjVBcYYNXuf1Hn'
consumer_secret = 'p6TFg2g9fqZZSvdWTmisuEknB9DlZTdv8A4QLCQ1mJPN9yU3bM'
access_key = '947878329708941313-kvHprQA9TsHGGTgMeKUDQdfIC2WYf5e'
access_secret = 'b53m9a8gx58k3RSziF8SShHZu0lx7bFNRThjAoRNya7wa'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)
baseurl = 'https://api.spacexdata.com/v2/'
def nextLaunchInfo():
    nextLaunch = getNextLaunch()
    message = getPayloadName(nextLaunch) + ' launch date ' + launchTimeDate(nextLaunch)
    message = 'SpaceX\'s next launch is'+ getPayloadName(nextLaunch) + ' on the ' + getRocketType(nextLaunch) + ' rocket at ' + launchTimeDate(nextLaunch)[:8] +' on'+ launchTimeDate(nextLaunch)[8:] + ' from ' + getLaunchPad(nextLaunch)
    return str(message)
def getPayloadName(launch):
    payloads = launch['rocket']['second_stage']['payloads']
    names = str()
    for i in range(len(payloads)):
        names += ' ' + str(payloads[i]['payload_id'])
    return names
def getRocketType(launch):
    rocket = launch['rocket']['rocket_name']
    return rocket
def getLaunchPad(launch):
    launchPad = launch['launch_site']['site_name_long']
    return launchPad
def getNextLaunch():
    nextLaunch = requests.get(baseurl + 'launches/upcoming').json()
    smallest = 20000
    for i in range(len(nextLaunch)):
        if nextLaunch[i]['flight_number'] < smallest:
            smallest = nextLaunch[i]['flight_number']
    for i in range(len(nextLaunch)):
        if nextLaunch[i]['flight_number'] == smallest:
            return nextLaunch[i]
def launchTimeDate(launch):
    Time = datetime.datetime.fromtimestamp(launch['launch_date_unix']).strftime('%H:%M:%S %Y-%m-%d')
    return Time
def tweetException(tweets):
    if tweets != '':
        return tweets
    else:
        return 'No new tweets'
def userTweets(screen_name):  
    '''
    Requires: screen_name is a valid twitter handle, count is an int > 0, < 200
    Modifies: Nothing
    Effects: fetches urls of last 'count' tweets from input user
    '''
    urls = str()
    alltweets = []
    alltweets = api.user_timeline(screen_name = screen_name,count = 3)
    outtweets = [tweet.id_str for tweet in alltweets]
    outtweets.reverse()
    with open('storedTweets.txt', 'r+') as myFile:
        openTweets = str(myFile.read())
        for i in range(len(outtweets)):
            tempvar = str(outtweets[i])
            if tempvar not in openTweets:
                myFile.seek(0, 2)
                myFile.write(str(outtweets[i]) + ' ')
                urls += '\n' + 'https://twitter.com/' + screen_name +'/status/' + outtweets[i]
    return urls
client = discord.Client()
def getChannel(channelName):
    for server in client.servers:
        for channel in server.channels:
            if channel.name == channelName:
                return channel

@client.event
async def autoTweet(destination, screen_name):
    message = userTweets(screen_name)
    if message != '':
        await client.send_message(destination, content = message)

@client.event
async def autoSetup():
    screen_name = input('user?')
    channelID = getChannel(input('channel?'))
    while(True):
        await autoTweet(channelID, screen_name)
        time.sleep(2)
        
@client.event
async def on_ready():
    print('Summoned as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    #await autoSetup()
@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')
    elif message.content.startswith('!tweet'):
        await client.send_message(message.channel, tweetException(userTweets('SpaceX')))
    elif message.content.startswith('!nextlaunch'):
        await client.send_message(message.channel, nextLaunchInfo())
client.run('NDAwODk2NjkxMjE1MTM4ODE2.DTiTuA.kd_6ZwSW5c1pgyIs1MfA3cd94EE')
