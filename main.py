import discord
import os
import re
import asyncio
from random import randint
from discord.ext import commands
from discord import Webhook

# import editing commands
from tsv import * # tsv is still used for message logs
from jsondata import *
import json

# import webhook send command builder
from webhook import buildSendCommand

# initialization
import settings

try:
    f = open("token", "r")
    tokenTest = f.read()
except:
    print("[URANIUM|Error] Token file could not be found or could not be read successfully, please create a bot via discordapi.com and copy the bot token into a file called 'token'.")
    exit()
print("[URANIUM] Token file exists.")

userDataExists = os.path.exists("./user-data/")
if userDataExists == False:
    os.mkdir("user-data")
print("[URANIUM] User data directory exists.")

webhookDataExists = os.path.exists("./webhook-data/")
if webhookDataExists == False:
    os.mkdir("webhook-data")
print("[URANIUM] Webhook data directory exists.")

messageLogsExists = os.path.exists("./message-logs/")
if messageLogsExists == False:
    os.mkdir("message-logs")
print("[URANIUM] Message log directory exists.")
if settings.messageLogging == "perSession":
    print("[LOGGING] Deleting all previous message ID logging...")
    for f in os.listdir("./message-logs/"):
        os.remove(os.path.join("./message-logs/", f))
else:
    print("[LOGGING] Persistent messaging logging on.")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

async def obtainWebhookData(ctx, channelID):
    # check if channel webhook exists in local database
    direc = os.listdir("./webhook-data/")
    for file in direc:
        if str(channelID) in file:
            webhookRead = open("./webhook-data/{0}".format(str(channelID), "r"))
            webhookID = webhookRead.read()
            webhookRead.close()
            return webhookID
    # if not, create and store it
    else:
        channel = uranium.get_channel(int(channelID))
        webhookID = await channel.create_webhook(name="Uranium Proxy Webhook")
        webhookPath = "./webhook-data/{0}".format(str(channelID))
        webhookStore = open(webhookPath, "w")
        webhookStore.write(str(webhookID))
        webhookStore.close()
        return webhookID

uranium = commands.Bot(command_prefix=settings.prefixes, intents=intents)

@uranium.event
async def on_ready():
    print(f'[URANIUM] I have logged in as {uranium.user}!')
    
    game = discord.Game("with isotopes! | {0}help".format(settings.prefixes[0]))
    await uranium.change_presence(status=discord.Status.online, activity=game)

@uranium.event
async def on_reaction_add(reaction, user):
    ctx = await uranium.get_context(reaction.message)
    if (ctx.author.bot):
        if reaction.emoji == "❌":
            await ctx.invoke(uranium.get_command("delete"), user=user)
        if reaction.emoji == "❓":
            await ctx.invoke(uranium.get_command("showmsg"), user=user)

@uranium.event
async def on_message(message):
    # this event will handle autoproxy and multiproxies

    ctx = await uranium.get_context(message)

    if os.path.exists("./user-data/{0}.json".format(ctx.message.author.id)):
        datafile = loadData(ctx.message.author.id)
        proxyStart = False
        
        # check if multiproxy is being invoked
        for key, value in datafile["isotopes"].items():
            if message.content.startswith(key):
                proxyStart = True

        if proxyStart == True:
            multiproxyList = []
            # search for other proxies being used
            for key, value in datafile["isotopes"].items():
                if key in message.content:
                    multiproxyList.append(key)

            # detect attachments
            try:
                getAttachments = ctx.message.attachments[0]
            except:
                fileAttachments = None
            else:
                fileAttachments = []
                for x in ctx.message.attachments:
                    x = await discord.Attachment.to_file(x)
                    fileAttachments.append(x)

            # detect a reply
            try:
                getReply = ctx.message.reference
                replyInformation = await ctx.fetch_message(getReply.message_id)
            except:
                replyInformation = None

            rawLines = message.content.split("\n")
            lineCount = message.content.count("\n") + 1
            finishedLine = ""
            currentBrackets = ""
            firstMessage = True
            firstMessage2 = True # for images and reply information
            for x in range(lineCount):
                for proxy in multiproxyList:
                    if proxy in rawLines[x]:
                        if firstMessage == False:
                            if firstMessage2 == True:
                                await ctx.invoke(uranium.get_command("send"), brackets=currentBrackets, msg=finishedLine, multiProxy=True, replyInformation=replyInformation, fileAttachments=fileAttachments)
                                firstMessage2 = False
                            else:
                                await ctx.invoke(uranium.get_command("send"), brackets=currentBrackets, msg=finishedLine, multiProxy=True)
                        finishedLine = rawLines[x][(len(proxy)):]
                        currentBrackets = proxy
                        firstMessage = False
                        break
                else:
                    finishedLine += "\n{0}".format(rawLines[x])
            else:
                await ctx.invoke(uranium.get_command("send"), brackets=currentBrackets, msg=finishedLine, replyInformation=replyInformation, fileAttachments=fileAttachments)

    await uranium.process_commands(message)

@uranium.command()
async def about(ctx):
    embedVar = discord.Embed(
    title="About {0}".format(settings.botName), description="{0} is a Discord bot that is used for roleplay and for use in systems/plurality.".format(settings.botName), color=0xffff66
            )
    if settings.modified == True:
        embedVar.add_field(name="Warning:", value="*The owner of this bot has enabled the modified variable, which means this bot's code has been modified and put up for public use. A valid respository link for this code will be provided at the bottom.*", inline=False)
    embedVar.set_footer(text="Created by NetscapeDreams. // Curium Release [v0.4.0]")
    embedVar.set_image(url="https://user-images.githubusercontent.com/121664679/213885228-339ba626-c546-4745-acad-6c7c13415a70.png")
    embedVar.add_field(name="Did you know the bot is open source?", value="That means **anyone** can view the source code, or how the bot works. You can change/add/remove what you want, and self host your own {0} instance. But remember, if you distribute your personal code, you **must** follow the terms and conditions of the GNU Affero General Public Licence v3.".format(settings.botName), inline=False)
    embedVar.add_field(name="GNU Affero General Public License v3", value="https://www.gnu.org/licenses/agpl-3.0.html", inline=False)
    embedVar.add_field(name="Repository Link", value=settings.respositoryLink, inline=False)
    await ctx.send(embed=embedVar)

@uranium.group(invoke_without_command=True)
async def reinit(ctx):
    databasePath = "./user-data/{0}.json".format(ctx.message.author.id)
    databaseExists = os.path.exists(databasePath)
    if databaseExists == True:
        await ctx.send(":grey_exclamation: *A database under your user ID has been found.*\nIf you would like to delete it, this will **remove all of your current isotopes and settings**.\n*Please note that you can export your user data via `{0}export` if you would like to.*\nIf you are sure you want to do this, please do `{0}reinit confirm`.".format(settings.prefixes[0]))
    else:
        await ctx.send(":x: *There is nothing to delete.*")

@reinit.command()
async def confirm(ctx):
    databasePath = "./user-data/{0}.json".format(ctx.message.author.id)
    databaseExists = os.path.exists(databasePath)
    if databaseExists == True:
        os.remove(databasePath)
        await ctx.send(":white_check_mark: *Your database has been deleted. All former isotopes and settings have been removed from my user data folder.*")
    else:
        await ctx.send(":x: *There is nothing to delete.*")

@uranium.command(description="register isotope")
async def register(ctx, name:str, brackets:str):
    if len(name) > 80:
        await ctx.send(":x: *Your isotope's name is too long, please keep it equal to or under 80 characters.*")
        return

    if "text" in brackets:
        await ctx.send(":speech_balloon: *I have detected the \"text\" parameter in your isotope's brackets, commonly used by Tupperbox and PluralKit.*\n\nPlease note, Uranium does not support the \"text\" parameter, and you can change your isotope's brackets via the `{0}brackets` command.\n**Registration will continue.**".format(settings.prefixes[0]))

    try:
        avatar = ctx.message.attachments[0]
        proxyAvatar = avatar.url
    except:
        proxyAvatar = "N/A"

    await registerProxy(ctx, brackets, name, proxyAvatar)

@uranium.command(description="delete an isotope")
async def unregister(ctx, name:str):
    await removeProxy(ctx, name)

@uranium.command(description="set an isotope's avatar")
async def avatar(ctx, name:str):
    try:
        avatar = ctx.message.attachments[0]
        await proxyAvatar(ctx, name, avatar)
    except:
        await proxyAvatar(ctx, name)

@uranium.command()
async def rename(ctx, oldname, newname):
    await editProxyName(ctx, oldname, newname)

@uranium.command()
async def brackets(ctx, name, newbrackets=None):
    await editProxyBrackets(ctx, name, newbrackets)

@uranium.command()
async def list(ctx, member: discord.Member=None):
    if member == None:
        member = ctx.message.author
    proxies, proxyCount = parseAll(ctx, member)
    if proxies == None:
        await ctx.send(":x: This user does not have any isotopes.")
        return
    embedVar = discord.Embed(
    title="{0}'s Isotopes".format(member.name), description="{0} has a total of {1} isotopes. Page 1/{2}.".format(member.name, proxyCount, len(proxies))
            )
    embedVar.set_footer(text="You have 1 minute to respond to this message in-between reactions.")
    for key, value in proxies[1].items():
        embedVar.add_field(name=proxies[1][key]["name"], value="brackets: {0}\navatar url: {1}".format(key, proxies[1][key]["avatar"]), inline=False)
    msg = await ctx.send(embed=embedVar)
    await msg.add_reaction("🛑")
    if 2 in proxies:
        await msg.add_reaction("⬅️")
        await msg.add_reaction("➡️")

    def check(reaction, user):
        if int(user.id) == int(ctx.author.id):
            return True
        else:
            return False

    pageCount = 1
    while True:
        try:
            reaction, user = await uranium.wait_for("reaction_add", timeout=60.0, check=check)
        except asyncio.TimeoutError:
            embedVar.set_footer(text="Message timeout. You can no longer interact with this message.")
            await msg.edit(embed=embedVar)
            break
        else:
            userCheck = check("nothing", user)
            if userCheck == True:
                if reaction.emoji == '🛑':
                    try:
                        await msg.delete()
                    except discord.errors.NotFound:
                        pass
                    break
                elif reaction.emoji == '⬅️' or reaction.emoji == '➡️':
                    if reaction.emoji == '➡️':
                        if pageCount + 1 > len(proxies):
                            pass
                        else:
                            pageCount += 1
                    elif reaction.emoji == '⬅️':
                        if pageCount - 1 == 0:
                            pass
                        else:
                            pageCount -= 1
                    embedVar = discord.Embed(
                    title="{0}'s Isotopes".format(member.name), description="{0} has a total of {1} isotopes. Page {2}/{3}.".format(member.name, proxyCount, pageCount, len(proxies))
                            )
                    embedVar.set_footer(text="You have 1 minute to respond to this message in-between reactions.")
                    for key, value in proxies[pageCount].items():
                        embedVar.add_field(name=proxies[pageCount][key]["name"], value="brackets: {0}\navatar url: {1}".format(key, proxies[pageCount][key]["avatar"]), inline=False)
                    await msg.edit(embed=embedVar)

@uranium.command(aliases=["s"])
async def send(ctx, brackets:str, *, msg, multiProxy=None, replyInformation=None, fileAttachments=None):

    # attempt to detect if sending channel is a thread
    try:
        # thread channels have a parent_id attribute
        detectThread = ctx.channel.parent_id
    except:
        detectThread = False
    else:
        detectThread = True

    sendToThread = False
    redirect = False
    detectRedirect = re.compile("\{\{.*\}\}")
    if detectRedirect.search(msg):
        res = re.findall(r"\{\{.*?\}\}", msg)
        originalres = res[0]
        res[0] = res[0].replace('{{', '')
        res[0] = res[0].replace('}}', '')

        if res[0].startswith("<#"):
            urghID = re.sub("\D", " ", res[0]);
            channelID = re.sub("\s", "", urghID);
            channel = uranium.get_channel(int(channelID))

            try:
                sendToThread = channel.parent_id
            except:
                sendToThread = False
                webhookID = await obtainWebhookData(ctx, channel.id)
                webhookList = await channel.webhooks()
            else:
                sendToThread = True
                webhookID = await obtainWebhookData(ctx, channel.parent_id)
                parentChannel = uranium.get_channel(int(channel.parent_id))
                webhookList = await parentChannel.webhooks()

            msg = msg.replace(originalres, "")
            redirect = True
    
    if detectThread == True and redirect == False:
        webhookID = await obtainWebhookData(ctx, ctx.channel.parent_id)
        channel = uranium.get_channel(int(ctx.channel.parent_id))
        webhookList = await channel.webhooks()
    elif detectThread == False and redirect == False:
        webhookID = await obtainWebhookData(ctx, ctx.channel.id)
        webhookList = await ctx.message.channel.webhooks()

    for wh in webhookList:
        if str(webhookID) == str(wh):

            embedList = []

            try:
                name, avtr = parseProxy(ctx, brackets)
            except:
                return

            detectCommand = re.compile("\{\{.*\}\}")
            if detectCommand.search(msg):
                res = re.findall(r"\{\{.*?\}\}", msg)
                originalres = res[0]
                res[0] = res[0].replace('{{', '')
                res[0] = res[0].replace('}}', '')

                separateDie = res[0].split('d')
                if not separateDie[0]:
                    separateDie[0] = 1
                separateExtra = separateDie[1].split('+')
                separateExtra.append(0)
                numberz = [int(separateDie[0]), int(separateExtra[0]), int(separateExtra[1])]
                result = []
                for die in range(numberz[0]):
                    die = randint(1, numberz[1])
                    result.append(die)

                msg = msg.replace(originalres, "`🎲{0}`".format(sum(result, numberz[2])))

                dieEmbed = discord.Embed(
                title=res[0], description="{1} + {2} → **{3}**".format(res[0], result, numberz[2], sum(result, numberz[2])), color=0x20FD00
                        )
                embedList.append(dieEmbed)
            else:
                dieEmbed = None

            if replyInformation == None:
                pass
            else:
                replyEmbed = discord.Embed(
                description=replyInformation.content, color=0x20FD00
                        )
                try:
                    replyAvatar = replyInformation.author.avatar.url
                except:
                    replyEmbed.set_author(name=replyInformation.author.name)
                else:
                    replyEmbed.set_author(name=replyInformation.author.name, icon_url=replyInformation.author.avatar.url)
                embedList.append(replyEmbed)

            if replyInformation == None and dieEmbed == None:
                embedList = None

            sendCommand = buildSendCommand(msg=msg, username=name, avatar=avtr, attachments=fileAttachments, detectThread=detectThread, sendToThread=sendToThread, redirect=redirect, embeds=embedList)
            webhookMessage = await eval(sendCommand)

            appendMessage = open("./message-logs/{0}.tsv".format(ctx.guild.id), "a")
            appendMessage.write("{0}\t{1}\t{2}\n".format(webhookMessage.id, ctx.author.id, brackets))
            appendMessage.close()

            if multiProxy == None:
                await ctx.message.delete()

            return
    await ctx.send(":x: **Something went wrong!**\nThe webhook ID in my local database could not be found in this channel's webhook list. *Did the webhook get deleted?*")

@uranium.command()
async def edit(ctx, *, msg):
    getReply = ctx.message.reference
    replyInformation = await ctx.fetch_message(getReply.message_id)
    checkPermission = checkForPermission(ctx, replyInformation.id, ctx.author.id)
    if checkPermission == True:

        try:
            detectThread = ctx.channel.parent_id
        except:
            detectThread = False
        else:
            detectThread = True

        if detectThread == True:
            webhookID = await obtainWebhookData(ctx, ctx.channel.parent_id)
            channel = uranium.get_channel(int(ctx.channel.parent_id))
            webhookList = await channel.webhooks()
        elif detectThread == False:
            webhookID = await obtainWebhookData(ctx, ctx.channel.id)
            webhookList = await ctx.message.channel.webhooks()

        for wh in webhookList:
            if str(webhookID) == str(wh):
                if detectThread == False:
                    await wh.edit_message(replyInformation.id, content=msg)
                else:
                    await wh.edit_message(replyInformation.id, content=msg, thread=ctx.channel)
                await ctx.message.delete()

@uranium.command()
async def delete(ctx, user=None):
    if user == None:
        getReply = ctx.message.reference
        reply = await ctx.fetch_message(getReply.message_id)
        checkPermission = checkForPermission(ctx, reply.id, ctx.author.id)
        if checkPermission == True:
            await reply.delete()
            await ctx.message.delete()
    else:
        checkPermission = checkForPermission(ctx, ctx.message.id, user.id)
        if checkPermission == True:
            await ctx.message.delete()
    

@uranium.command()
async def export(ctx):
    databasePath = "./user-data/{0}.json".format(ctx.message.author.id)
    databaseExists = os.path.exists(databasePath)
    if databaseExists == True:
        dmChannel = await ctx.author.create_dm()
        try:
            await dmChannel.send("**Hi, {0}!** :wave:\nHere is your user data file you requested.\nOh, and please note: user data importing is not supported at the moment, so all you can really do is view your data. Sorry :(".format(ctx.author.name), file=discord.File(r'./user-data/{0}.json'.format(ctx.author.id)))
            await ctx.message.add_reaction("✅")
        except discord.errors.Forbidden:
            await ctx.send(":x: *I was not able to message you, please allow server DMs so that I can send your user data file privately.*")
    else:
        await ctx.send(":x: *There is nothing to export.*")

@uranium.command()
async def data(ctx):
    embedVar = discord.Embed(
    title="{0} and your data.".format(settings.botName), description="What does {0} exactly do with data it obtains?".format(settings.botName), color=0x20FD00
            )
    embedVar.set_footer(text="Last updated January 21st, 2023.")
    embedVar.add_field(name="User data", value="This bot stores your user ID (this is to help identify which file belongs to who) and the proxies you create via the information you provide, and your user ID used in message logging for helping determine if you own a proxy message.\nThis information is exportable via the bot's **export** command.", inline=False)
    embedVar.add_field(name="Webhook data", value="This bot stores webhook ID data under a channel ID filename, to help keep a local value for comparison to send proxies via webhooks.", inline=False)
    embedVar.add_field(name="Channel data", value="This bot stores channel IDs as filenames for help in identifying the webhook ID for the channel you are sending the proxy to.", inline=False)
    embedVar.add_field(name="Guild and message data", value="This bot stores guild (server) IDs as filenames and message IDs for help in message logging, and to determine if the proxy message you sent is in the logs.", inline=False)
    embedVar.add_field(name="Who can see this data?", value="It depends. All information can only be read by the bot host(s), with the exception of user data, which can be viewed at the user's request.", inline=False)
    await ctx.send(embed=embedVar)

@uranium.command()
async def find(ctx, *, search=None):
    if search == None:
        await ctx.send(":x: Please provide a search term to use.")
        return
    getMember = ctx.message.author
    proxies, proxyCount = parseAll(ctx, getMember, search) 
    if proxies == None:
        await ctx.send(":x: You do not have any isotopes to search through.")
        return
    embedVar = discord.Embed(
    description="A total of {0} isotope(s) matches your search. Page 1/{1}.".format(proxyCount, len(proxies))
            )
    embedVar.set_footer(text="You have 1 minute to respond to this message in-between reactions.")
    for key, value in proxies[1].items():
        embedVar.add_field(name=proxies[1][key]["name"], value="brackets: {0}\navatar url: {1}".format(key, proxies[1][key]["avatar"]), inline=False)
    msg = await ctx.send(embed=embedVar)
    await msg.add_reaction("🛑")
    if 2 in proxies:
        await msg.add_reaction("⬅️")
        await msg.add_reaction("➡️")

    def check(reaction, user):
        if int(user.id) == int(ctx.author.id):
            return True
        else:
            return False

    pageCount = 1
    while True:
        try:
            reaction, user = await uranium.wait_for("reaction_add", timeout=60.0, check=check)
        except asyncio.TimeoutError:
            embedVar.set_footer(text="Message timeout. You can no longer interact with this message.")
            await msg.edit(embed=embedVar)
            break
        else:
            userCheck = check("nothing", user)
            if userCheck == True:
                if reaction.emoji == '🛑':
                    try:
                        await msg.delete()
                    except discord.errors.NotFound:
                        pass
                    break
                elif reaction.emoji == '⬅️' or reaction.emoji == '➡️':
                    if reaction.emoji == '➡️':
                        if pageCount + 1 > len(proxies):
                            pass
                        else:
                            pageCount += 1
                    elif reaction.emoji == '⬅️':
                        if pageCount - 1 == 0:
                            pass
                        else:
                            pageCount -= 1
                    embedVar = discord.Embed(
                    description="A total of {0} isotope(s) matches your search. Page {1}/{2}.".format(proxyCount, pageCount, len(proxies))
                            )
                    embedVar.set_footer(text="You have 1 minute to respond to this message in-between reactions.")
                    for key, value in proxies[pageCount].items():
                        embedVar.add_field(name=proxies[pageCount][key]["name"], value="brackets: {0}\navatar url: {1}".format(key, proxies[pageCount][key]["avatar"]), inline=False)
                    await msg.edit(embed=embedVar)

@uranium.command()
async def gfind(ctx, *, search=None):
    if search == None:
        await ctx.send(":x: Please provide a search term to use.")
        return
    proxies, proxyCount = parseAll(ctx, None, search, True) 
    embedVar = discord.Embed(
    description="A total of {0} isotope(s) matches your search. Page 1/{1}.".format(proxyCount, len(proxies))
            )
    embedVar.set_footer(text="You have 1 minute to respond to this message in-between reactions.")
    for key, value in proxies[1].items():
        proxyMember = ctx.guild.get_member(proxies[1][key]["owner"])
        embedVar.add_field(name=proxies[1][key]["name"], value="owned by: {0}\nbrackets: {1}\navatar url: {2}".format(proxyMember.name, key, proxies[1][key]["avatar"]), inline=False)
    msg = await ctx.send(embed=embedVar)
    await msg.add_reaction("🛑")
    if 2 in proxies:
        await msg.add_reaction("⬅️")
        await msg.add_reaction("➡️")

    def check(reaction, user):
        if int(user.id) == int(ctx.author.id):
            return True
        else:
            return False

    pageCount = 1
    while True:
        try:
            reaction, user = await uranium.wait_for("reaction_add", timeout=60.0, check=check)
        except asyncio.TimeoutError:
            embedVar.set_footer(text="Message timeout. You can no longer interact with this message.")
            await msg.edit(embed=embedVar)
            break
        else:
            userCheck = check("nothing", user)
            if userCheck == True:
                if reaction.emoji == '🛑':
                    try:
                        await msg.delete()
                    except discord.errors.NotFound:
                        pass
                    break
                elif reaction.emoji == '⬅️' or reaction.emoji == '➡️':
                    if reaction.emoji == '➡️':
                        if pageCount + 1 > len(proxies):
                            pass
                        else:
                            pageCount += 1
                    elif reaction.emoji == '⬅️':
                        if pageCount - 1 == 0:
                            pass
                        else:
                            pageCount -= 1
                    embedVar = discord.Embed(
                    description="A total of {0} isotope(s) matches your search. Page {1}/{2}.".format(proxyCount, pageCount, len(proxies))
                            )
                    embedVar.set_footer(text="You have 1 minute to respond to this message in-between reactions.")
                    for key, value in proxies[pageCount].items():
                        proxyMember = ctx.guild.get_member(proxies[pageCount][key]["owner"])
                        embedVar.add_field(name=proxies[pageCount][key]["name"], value="owned by: {0}\nbrackets: {1}\navatar url: {2}".format(proxyMember.name, key, proxies[pageCount][key]["avatar"]), inline=False)
                    await msg.edit(embed=embedVar)

@uranium.command()
async def showmsg(ctx, user=None):
    if user == None:
        getReply = ctx.message.reference
        reply = await ctx.fetch_message(getReply.message_id)
        try:
            userID, brackets = showProxyMessage(ctx, reply.id)
        except:
            return
        if userID != False:
            proxyName, proxyAvatar = parseProxy(ctx, brackets.strip(), userID)
            embedVar = discord.Embed(
            title="Show Message", color=0x20FD00
                    )
            if proxyAvatar != "N/A":
                embedVar.set_thumbnail(url=proxyAvatar)
            embedVar.add_field(name="Isotope Information", value="Name: {0}\nBrackets: {1}\nAvatar: {2}".format(proxyName, brackets.strip(), proxyAvatar), inline=False)
            embedVar.add_field(name="User Information", value="This proxy was sent by:\nID: {0}\nUser: <@{0}>".format(userID), inline=False)
            embedVar.set_footer(text="Message ID: {0}".format(reply.id))
            await ctx.send(embed=embedVar)
    else:
        try:
            userID, brackets = showProxyMessage(ctx, ctx.message.id)
        except:
            return
        await ctx.message.remove_reaction("❓", user)
        if userID != False:
            proxyName, proxyAvatar = parseProxy(ctx, brackets.strip(), userID)
            dmChannel = await user.create_dm()
            embedVar = discord.Embed(
            title="Show Message", color=0x20FD00
                    )
            if proxyAvatar != "N/A":
                embedVar.set_thumbnail(url=proxyAvatar)
            embedVar.add_field(name="Isotope Information", value="Name: {0}\nBrackets: {1}\nAvatar: {2}".format(proxyName, brackets.strip(), proxyAvatar), inline=False)
            embedVar.add_field(name="User Information", value="This proxy was sent by:\nID: {0}\nUser: <@{0}>".format(userID), inline=False)
            embedVar.add_field(name="Message Content", value=ctx.message.content, inline=False)
            embedVar.set_footer(text="Message ID: {0}".format(ctx.message.id))
            await dmChannel.send("Here's that information you wanted.", embed=embedVar)

@uranium.command()
async def isotope(ctx, name):
    datafile = loadData(ctx)
    for key, value in datafile["isotopes"].items():
        if name in datafile["isotopes"][key]["name"]:
            if "variants" in datafile["isotopes"][key]:
                variantsDetected = True
            else:
                variantsDetected = False
            isotope = value
            break
    else:
        await ctx.send(":x: Isotope not found.")
        return
    embedVar = discord.Embed(
    title=isotope["name"], color=0x20FD00, description=isotope["desc"]
            )
    embedVar.add_field(name="Brackets", value=key, inline=True)
    if isotope["avatar"] != "N/A":
        embedVar.set_thumbnail(url=isotope["avatar"])
        embedVar.add_field(name="Avatar", value="[Link]({0})".format(isotope["avatar"]), inline=True)
    else:
        embedVar.add_field(name="Avatar", value="N/A", inline=True)
    embedVar.add_field(name="Post count", value=isotope["messages"], inline=True)
    embedVar.add_field(name="Birthday", value=isotope["birthday"], inline=True)
    embedVar.add_field(name="Tag", value=isotope["tag"], inline=True)
    embedVar.add_field(name="Group", value=isotope["group"], inline=True)
    embedVar.add_field(name="Registered", value=isotope["creationdate"], inline=True)
    if variantsDetected == True:
        embedVar.add_field(name="This Isotope has **variants**!", value="Use `{0}variants \"{1}\"` to show them.".format(settings.prefixes[0], isotope["name"]), inline=False)
    await ctx.send(embed=embedVar)

f = open("token", "r")
token = f.read()
uranium.run(token)
