import discord
import os
import re
import asyncio
from random import randint
from discord.ext import commands
from discord import Webhook

# import tsv editing commands
from tsv import *

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
    print("[LOGGING] Persistant messaging logging on.")

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
    if reaction.emoji == "❌":
        ctx = await uranium.get_context(reaction.message)
        await ctx.invoke(uranium.get_command("delete"), user=user)

@uranium.event
async def on_message(message):
    # this event will handle autoproxy and multiproxies

    ctx = await uranium.get_context(message)

    settingsPath = "./user-data/{0}.tsv".format(message.author.id)
    if os.path.exists(settingsPath):
        with open(settingsPath) as f:
            multiproxyList = []
            proxyStart = False
            for line in f:
                proxy = line.split("\t")
                proxyDetect = "\n{0}".format(proxy[0])
                if message.content.startswith(proxy[0]):
                    multiproxyList.append(proxy[0])
                    proxyStart = True
                if proxyDetect in message.content and proxyStart == True:
                    multiproxyList.append(proxy[0])
    
            if len(multiproxyList) > 0:

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
    title="About {0}".format(settings.botName), description="{0} is a Discord bot that is used for roleplay and for use in systems/plurality.".format(settings.botName), color=0xC71203
            )
    if settings.modified == True:
        embedVar.add_field(name="Warning:", value="*The owner of this bot has enabled the modified variable, which means this bot's code has been modified and put up for public use. A valid respository link for this code will be provided at the bottom.*", inline=False)
    embedVar.set_footer(text="Created by NetscapeDreams. // Americium Release [v0.3.0]")
    embedVar.set_image(url="https://user-images.githubusercontent.com/121664679/213885228-339ba626-c546-4745-acad-6c7c13415a70.png")
    embedVar.add_field(name="Did you know the bot is open source?", value="That means **anyone** can view the source code, or how the bot works. You can change/add/remove what you want, and self host your own {0} instance. But remember, if you distribute your personal code, you **must** follow the terms and conditions of the GNU Affero General Public Licence v3.".format(settings.botName), inline=False)
    embedVar.add_field(name="GNU Affero General Public License v3", value="https://www.gnu.org/licenses/agpl-3.0.html", inline=False)
    embedVar.add_field(name="Repository Link", value=settings.respositoryLink, inline=False)
    await ctx.send(embed=embedVar)

@uranium.group(invoke_without_command=True)
async def reinit(ctx):
    databasePath = "./user-data/{0}.tsv".format(ctx.message.author.id)
    databaseExists = os.path.exists(databasePath)
    if databaseExists == True:
        await ctx.send(":grey_exclamation: *A database under your user ID has been found.*\nIf you would like to re-initalize it, this will **delete all of your current isotopes and settings**.\n*Please note that you can export your user data via `{0}export` if you would like to.*\nIf you are sure you want to do this, please do `{0}reinit confirm`.".format(settings.prefixes[0]))
    else:
        await ctx.send(":x: *There is nothing to re-initialize.*")

@reinit.command()
async def confirm(ctx):
    databasePath = "./user-data/{0}.tsv".format(ctx.message.author.id)
    os.remove(databasePath)
    databaseCreation = open(databasePath, "w")
    databaseCreation.close()
    await ctx.send(":white_check_mark: *Your database has been reinitalized. All former isotopes and settings have been deleted.*")

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
        proxyAvatar = "*"

    if os.path.exists("./user-data/{0}.tsv".format(ctx.message.author.id)) == True:
        conflictions = checkForConflicts(ctx, name, brackets)
    else:
        conflictions = None
    if conflictions == None:
        appendProxy = open("./user-data/{0}.tsv".format(ctx.message.author.id), "a")
        appendProxy.write("{0}\t{1}\t{2}\n".format(brackets, name, proxyAvatar))
        appendProxy.close()
        await ctx.send("Wonderful! `{0}` has been created under your user data using the brackets `{1}`.\nTo send a message via this isotope, you can just use the brackets. `{1}I'm a proxy!`".format(name, brackets))
    elif conflictions == "name":
        await ctx.send(":x: There already is an isotope with this name in your user data.")
    elif conflictions == "brackets":
        await ctx.send(":x: There already is an isotope with these brackets in your user data.")

@uranium.command(description="delete an isotope")
async def remove(ctx, name:str):
    await removeProxy(ctx, name)

@uranium.command(description="set an isotope's avatar")
async def avatar(ctx, name:str):
    try:
        avatar = ctx.message.attachments[0]
    except:
        await getProxyAvatar(ctx, name)
    
    await setProxyAvatar(ctx, name, avatar)

@uranium.command(description="mainly for debugging", aliases=["whs"])
async def webhookstatus(ctx):
    direc = os.listdir("./webhook-data/")
    for file in direc:
        if str(ctx.channel.id) in file:
            webhookRead = open("./webhook-data/{0}".format(str(ctx.channel.id), "r"))
            webhookID = webhookRead.read()
            webhookRead.close()
            await ctx.send(":white_check_mark: Webhook ID of `{0}` for this channel is present in my local database.".format(str(webhookID)))
            break
    else:
        await ctx.send(":x: I do not have a local webhook database entry for this channel.")

    webhookList = await ctx.message.channel.webhooks()
    try:
        for wh in webhookList:
           if str(webhookID) == str(wh):
               await ctx.send(":white_check_mark: My local webhook database entry for this channel was found in this channel's webhook list.")
               return
    except:
        await ctx.send(":x: My local webhook database did not find a match in this channel's webhook list.")

@uranium.command()
async def rename(ctx, oldname, newname):
    await editProxyName(ctx, oldname, newname)

@uranium.command()
async def brackets(ctx, name, newbrackets=None):
    if newbrackets == None:
        with open("./user-data/{0}.tsv".format(ctx.message.author.id)) as f:
            for line in f:
                proxy = line.split("\t")
                if proxy[1] == name:
                    await ctx.send("The brackets for {0} are `{1}`.".format(name, proxy[0]))
    else:
        await editProxyBrackets(ctx, name, newbrackets)

@uranium.command()
async def list(ctx, member: discord.Member=None):
    if member == None:
        member = ctx.message.author
    pageCount = 0
    proxies, proxyCount = parseAll(ctx, member)
    embedVar = discord.Embed(
    title="{0}'s Isotopes".format(member.name), description="{0} has a total of {1} isotopes. Page 1/{2}.".format(member.name, proxyCount, len(proxies))
            )
    for x in proxies[0]:
        embedVar.add_field(name=x[1], value="brackets: {0}\navatar url: {1}".format(x[0], x[2]), inline=False)
    msg = await ctx.send(embed=embedVar)
    await msg.add_reaction("🛑")
    await msg.add_reaction("⬅️")
    await msg.add_reaction("➡️")

    def check(reaction, user):
        if int(user.id) == int(ctx.author.id):
            return True
        else:
            return False

    while True:
        try:
            reaction, user = await uranium.wait_for("reaction_add", timeout=60.0, check=check)
        except asyncio.TimeoutError:
            break
        else:
            userCheck = check("nothing", user)
            if userCheck == True:
                if reaction.emoji == '🛑':
                    await msg.delete()
                elif reaction.emoji == '⬅️' or reaction.emoji == '➡️':
                    if reaction.emoji == '➡️':
                        literalPageCount = pageCount + 1
                        if literalPageCount == len(proxies):
                            pageCount = 0
                        else:
                            pageCount += 1
                    else:
                        if pageCount == 0:
                            pageCount = len(proxies) - 1
                        else:
                            pageCount -= 1
                    embedVar = discord.Embed(
                    title="{0}'s Isotopes".format(member.name), description="{0} has a total of {1} isotopes. Page {2}/{3}.".format(member.name, proxyCount, pageCount + 1, len(proxies))
                            )
                    for x in proxies[pageCount]:
                        embedVar.add_field(name=x[1], value="brackets: {0}\navatar url: {1}".format(x[0], x[2]), inline=False)
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
    try:
        if os.stat('./user-data/{0}.tsv'.format(ctx.author.id)).st_size == 0:
            await ctx.send(":x: *Why would I send a blank user data file?*")
        else:
            dmChannel = await ctx.author.create_dm()
            try:
                await dmChannel.send("**Hi, {0}!** :wave:\nHere is your user data file you requested.\nOh, and please note: user data importing is not supported at the moment, so all you can really do is view your data. Sorry :(".format(ctx.author.name), file=discord.File(r'./user-data/{0}.tsv'.format(ctx.author.id)))
                await ctx.message.add_reaction("✅")
            except discord.errors.Forbidden:
                await ctx.send(":x: *I was not able to message you, please allow server DMs so that I can send your user data file privately.*")
    except FileNotFoundError:
        await ctx.send(":x: *I could not find a user data file with your user ID. I think you should create your file first before exporting it.*")

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
async def find(ctx, *, search):
    getMember = ctx.message.author
    proxies, proxyCount = parseAll(ctx, getMember, search) 
    pageCount = 0
    embedVar = discord.Embed(
    description="A total of {0} isotope(s) matches your search. Page 1/{1}.".format(proxyCount, len(proxies))
            )
    for x in proxies[0]:
        embedVar.add_field(name=x[1], value="brackets: {0}\navatar url: {1}".format(x[0], x[2]), inline=False)
    msg = await ctx.send(embed=embedVar)
    await msg.add_reaction("🛑")
    await msg.add_reaction("⬅️")
    await msg.add_reaction("➡️")

    def check(reaction, user):
        if int(user.id) == int(ctx.author.id):
            return True
        else:
            return False

    while True:
        try:
            reaction, user = await uranium.wait_for("reaction_add", timeout=60.0, check=check)
        except asyncio.TimeoutError:
            break
        else:
            userCheck = check("nothing", user)
            if userCheck == True:
                if reaction.emoji == '🛑':
                    await msg.delete()
                elif reaction.emoji == '⬅️' or reaction.emoji == '➡️':
                    if reaction.emoji == '➡️':
                        literalPageCount = pageCount + 1
                        if literalPageCount == len(proxies):
                            pageCount = 0
                        else:
                            pageCount += 1
                    else:
                        if pageCount == 0:
                            pageCount = len(proxies) - 1
                        else:
                            pageCount -= 1
                    embedVar = discord.Embed(
                    description="A total of {0} isotope(s) matches your search. Page {1}/{2}.".format(proxyCount, pageCount + 1, len(proxies))
                            )
                    for x in proxies[pageCount]:
                        embedVar.add_field(name=x[1], value="brackets: {0}\navatar url: {1}".format(x[0], x[2]), inline=False)
                    await msg.edit(embed=embedVar)

@uranium.command()
async def gfind(ctx, *, search):
    proxies, proxyCount = parseAll(ctx, None, search, True) 
    pageCount = 0
    embedVar = discord.Embed(
    description="A total of {0} isotope(s) matches your search. Page 1/{1}.".format(proxyCount, len(proxies))
            )
    for x in proxies[0]:
        proxyMember = ctx.guild.get_member(x[3])
        embedVar.add_field(name=x[1], value="owned by: {0}\nbrackets: {1}\navatar url: {2}".format(proxyMember.name, x[0], x[2]), inline=False)
    msg = await ctx.send(embed=embedVar)
    await msg.add_reaction("🛑")
    await msg.add_reaction("⬅️")
    await msg.add_reaction("➡️")

    def check(reaction, user):
        if int(user.id) == int(ctx.author.id):
            return True
        else:
            return False

    while True:
        try:
            reaction, user = await uranium.wait_for("reaction_add", timeout=60.0, check=check)
        except asyncio.TimeoutError:
            break
        else:
            userCheck = check("nothing", user)
            if userCheck == True:
                if reaction.emoji == '🛑':
                    await msg.delete()
                elif reaction.emoji == '⬅️' or reaction.emoji == '➡️':
                    if reaction.emoji == '➡️':
                        literalPageCount = pageCount + 1
                        if literalPageCount == len(proxies):
                            pageCount = 0
                        else:
                            pageCount += 1
                    else:
                        if pageCount == 0:
                            pageCount = len(proxies) - 1
                        else:
                            pageCount -= 1
                    embedVar = discord.Embed(
                    description="A total of {0} isotope(s) matches your search. Page {1}/{2}.".format(proxyCount, pageCount + 1, len(proxies))
                            )
                    for x in proxies[pageCount]:
                        proxyMember = ctx.guild.get_member(x[3])
                        embedVar.add_field(name=x[1], value="owned by: {0}\nbrackets: {1}\navatar url: {2}".format(proxyMember.name, x[0], x[2]), inline=False)
                    await msg.edit(embed=embedVar)

f = open("token", "r")
token = f.read()
uranium.run(token)