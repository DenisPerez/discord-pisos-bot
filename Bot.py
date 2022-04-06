import re
from unicodedata import name
import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix='-')

formatMessage = "This User: {userID} send a message to a bot-music channel. What a Shame {userID}!! THE MESSAGE: {message}"
image_types = ["png", "jpeg", "gif", "jpg", "bmp"]

botMusicID = 943200279065661470
botMusicPrivID = 943200511010697217

outStandard = 490941149821796383
outPriv = 619365686493577232

@client.event
async def on_ready():
    print("Bot online.")

@client.command(name = 'clear')
async def clear(ctx):
    print("entre")
    await ctx.channel.purge()

@client.event
async def on_message(message):
    outCh = client.get_channel(490941149821796383)
    chMessageID = message.channel.id
    botFlag = message.author.bot

    messageContent = message.content

    not_allow_true = (re.search("^!",messageContent) or 
                      re.search("^-",messageContent))

    currentFilesList = []

    if((chMessageID == botMusicID or chMessageID == botMusicPrivID) and
        (not botFlag) and
        (not not_allow_true)):
            print("Deleting {m} from {f}".format(m = message.content, f = message.author.name))
            await message.delete()

            outFormatMessage = formatMessage.format(userID = message.author.name, message = message.content)

            if(chMessageID == botMusicID):
                outCh = client.get_channel(outStandard)
            else:
                outCh = client.get_channel(outPriv)

            for attachment in message.attachments:
                if any(attachment.filename.lower().endswith(image) for image in image_types):

                    print(attachment.filename)
                    await attachment.save(attachment.filename)
                    currentFilesList.append(attachment.filename)

            if not currentFilesList:
                await outCh.send(outFormatMessage)

            for file in currentFilesList:
                
                await outCh.send(outFormatMessage, file = discord.File(file))
                os.remove(file)
            
    await client.process_commands(message)

client.run('OTYwNzIyMjQzOTI1NzMzNDI2.YkukUA.B2PBNDDMxFAAnIVajBGjKuGqfA4')