from json.decoder import JSONDecodeError
import requests
import json
from discord_webhook import DiscordWebhook, DiscordEmbed
import time
import os


def getGroupDevs():
    getUsers = requests.get(
        f'https://groups.roblox.com/v1/groups/GROUPIDHERE/roles/ROLEIDHERE/users?sortOrder=Asc&limit=100').json()
    getuserids = getUsers['data'][0:]
    for i in getuserids:
        DevUserID = i['userId']
        DevUsername = i['username']
        CurrentPresence = requests.get(
            f'https://api.roblox.com/users/{DevUserID}/onlinestatus/').json()
        DevOnlineStatus = CurrentPresence['IsOnline']
        DevLastLocation = CurrentPresence['LastLocation']
        devdata = {DevUsername: DevLastLocation}
        with open("DEV_DATA.json", "r+") as file:
            try:
                data = json.load(file)
                if data[DevUsername] != DevLastLocation:
                    print("OLD STATUS:" + data[DevUsername] +
                          "- NEW STATUS:" + DevLastLocation)
                    webhook = DiscordWebhook(
                        url='WEBHOOKHERE')
                    embed = DiscordEmbed(
                        title='Grand Piece Online', description=f'Developer Status has been changed!')
                    embed.add_embed_field(
                        name=f"{DevUsername}", value=f"Old Status: {data[DevUsername]} - New Status: {DevLastLocation}")
                    webhook.add_embed(embed)
                    response = webhook.execute()
                    data.update(devdata)
                    file.seek(0)
                    json.dump(data, file)
                    file.truncate()
                elif data[DevUsername] == DevLastLocation:
                    pass
            except KeyError:
                print('updating')
                data.update(devdata)
                file.seek(0)
                json.dump(data, file)


while True:
    print('looped')
    getGroupDevs()
    time.sleep(30)
