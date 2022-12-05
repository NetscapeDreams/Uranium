import discord
import os
import re
from random import randint
from discord.ext import commands
from discord import Webhook

# import tsv editing commands
from tsv import removeProxy, getProxyAvatar, parseProxy, setProxyAvatar, editProxyName, editProxyBrackets

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

intents = discord.Intents.default()
intents.message_content = True

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
    
    game = discord.Game("with proxies! | {0}help".format(settings.prefixes[0]))
    await uranium.change_presence(status=discord.Status.online, activity=game)

# await uranium.process_commands(message)

@uranium.command()
async def about(ctx):
    embedVar = discord.Embed(
    title="About {0}".format(settings.botName), description="{0} is a Discord bot that is used for roleplay and for use in systems/plurality.".format(settings.botName), color=0xff5e00
            )
    if settings.modified == True:
        embedVar.add_field(name="Warning:", value="*The owner of this bot has enabled the modified variable, which means this bot's code has been modified and put up for public use. A valid respository link for this code will be provided at the bottom.*", inline=False)
    embedVar.set_footer(text="Created by BurningInfern0. // Plutonium Release")
    embedVar.set_image(url="https://user-images.githubusercontent.com/74492478/203663460-6863d8e6-66d8-4379-8fe9-aba48de15262.png")
    embedVar.add_field(name="Did you know the bot is open source?", value="That means **anyone** can view the source code, or how the bot works. You can change/add/remove what you want, and self host your own {0} instance. But remember, if you distribute your personal code, you **must** follow the terms and conditions of the GNU Affero General Public Licence v3.".format(settings.botName), inline=False)
    embedVar.add_field(name="GNU Affero General Public License v3", value="https://www.gnu.org/licenses/agpl-3.0.html", inline=False)
    embedVar.add_field(name="Repository Link", value=settings.respositoryLink, inline=False)
    await ctx.send(embed=embedVar)

@uranium.group(invoke_without_command=True)
async def reinit(ctx):
    databasePath = "./user-data/{0}.tsv".format(ctx.message.author.id)
    databaseExists = os.path.exists(databasePath)
    if databaseExists == True:
        await ctx.send(":grey_exclamation: *A database under your user ID has been found.*\nIf you would like to re-initalize it, this will **delete all of your current proxies and settings**.\n*Please note that you can export your user data via `{0}export` if you would like to.*\nIf you are sure you want to do this, please do `{0}reinit confirm`.".format(settings.prefixes[0]))
    else:
        await ctx.send(":x: *There is nothing to re-initialize.*")

@reinit.command()
async def confirm(ctx):
    databasePath = "./user-data/{0}.tsv".format(ctx.message.author.id)
    os.remove(databasePath)
    databaseCreation = open(databasePath, "w")
    databaseCreation.close()
    await ctx.send(":white_check_mark: *Your database has been reinitalized. All former proxies and settings have been deleted.*")
    

@uranium.group(invoke_without_command=True, aliases=["p"])
async def proxy(ctx):
    await ctx.send(":x: *Please provide a subcommand.*\nWhat do you want me to do with proxies? See `{0}help proxy` for more information.".format(settings.prefixes[0]))

@proxy.command(description="register proxy")
async def register(ctx, name:str, brackets:str):
    if len(name) > 80:
        await ctx.send(":x: *Your proxy's name is too long, please keep it equal to or under 80 characters.*")
        return

    try:
        avatar = ctx.message.attachments[0]
        proxyAvatar = avatar.url
    except:
        proxyAvatar = "*"

    appendProxy = open("./user-data/{0}.tsv".format(ctx.message.author.id), "a")
    appendProxy.write("{0}\t{1}\t{2}\n".format(brackets, name, proxyAvatar))
    appendProxy.close()
    await ctx.send("Wonderful! `{0}` has been created under your user data using the brackets `{1}`.\nTo send a message via this proxy, send `{2}proxy send {1} I'm a proxy!`".format(name, brackets, settings.prefixes[0]))

@proxy.command(description="delete a proxy")
async def remove(ctx, name:str):
    await removeProxy(ctx, name)

@proxy.command(description="set a proxy's avatar")
async def avatar(ctx, name:str):
    try:
        avatar = ctx.message.attachments[0]
    except:
        await getProxyAvatar(ctx, name)
    
    await setProxyAvatar(ctx, name, avatar)

@proxy.command(description="mainly for debugging", aliases=["whs"])
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

@proxy.command()
async def rename(ctx, oldname, newname):
    await editProxyName(ctx, oldname, newname)

@proxy.command()
async def brackets(ctx, name, newbrackets):
    await editProxyBrackets(ctx, name, newbrackets)

@proxy.command(aliases=["s"])
async def send(ctx, brackets:str, *, msg):

    # attempt to detect if sending channel is a thread
    try:
        # thread channels have a parent_id attribute
        detectThread = ctx.channel.parent_id
    except:
        detectThread = False
    else:
        detectThread = True

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

            try:
                name, avtr = parseProxy(ctx, brackets)
            except:
                return
            await ctx.message.delete()

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

                embedVar = discord.Embed(
                title=res[0], description="{1} + {2} → **{3}**".format(res[0], result, numberz[2], sum(result, numberz[2])), color=0x20FD00
                        )

                if avtr == "*":
                    if detectThread == True and redirect == False:
                        await wh.send(msg, username=name, embed=embedVar, thread=ctx.channel)
                    elif redirect == True:
                        if sendToThread == True:
                            await wh.send(msg, username=name, embed=embedVar, thread=channel)
                        else:
                            await wh.send(msg, username=name, embed=embedVar)
                    else:
                        await wh.send(msg, username=name, embed=embedVar)
                else:
                    if detectThread == True and redirect == False:
                        await wh.send(msg, username=name, avatar_url=avtr, embed=embedVar, thread=ctx.channel)
                    elif redirect == True:
                        if sendToThread == True:
                            await wh.send(msg, username=name, avatar_url=avtr, thread=channel, embed=embedVar)
                        else:
                            await wh.send(msg, username=name, avatar_url=avtr, embed=embedVar)
                    else:
                        await wh.send(msg, username=name, avatar_url=avtr, embed=embedVar)
                return

            if avtr == "*":
                if detectThread == True and redirect == False:
                    await wh.send(msg, username=name, thread=ctx.channel)
                elif redirect == True:
                    if sendToThread == True:
                        await wh.send(msg, username=name, thread=channel)
                    else:
                        await wh.send(msg, username=name)
                else:
                    await wh.send(msg, username=name)
            else:
                if detectThread == True and redirect == False:
                    await wh.send(msg, username=name, avatar_url=avtr, thread=ctx.channel)
                elif redirect == True:
                    if sendToThread == True:
                        await wh.send(msg, username=name, avatar_url=avtr, thread=channel)
                    else:
                        await wh.send(msg, username=name, avatar_url=avtr)
                else:
                    await wh.send(msg, username=name, avatar_url=avtr)
            
            return
    await ctx.send(":x: **Something went wrong!**\nThe webhook ID in my local database could not be found in this channel's webhook list. *Did the webhook get deleted?*")

@uranium.command()
@commands.is_owner()
async def execute(ctx, *, com):
    exec(com)

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
    title="{0} and your data.".format(botName), description="What does {0} exactly do with data it obtains?".format(botName), color=0x00fff4
            )
    embedVar.set_footer(text="Last updated November 30th, 2022.")
    embedVar.add_field(name="User data", value="This bot stores your user ID (this is to help identify which file belongs to who) and the proxies you create via the information you provide.\nThis information is exportable via the bot's export command.", inline=False)
    embedVar.add_field(name="Webhook data", value="This bot stores webhook ID data under a channel ID filename, to help keep a local value for comparison to send proxies via webhooks.", inline=False)
    embedVar.add_field(name="Channel data", value="This bot stores channel IDs as filenames for help in identifying the webhook ID for the channel you are sending the proxy to.", inline=False)
    embedVar.add_field(name="Who can see this data?", value="It depends. All information can only be read by the bot host(s), with the exception of user data, which can be viewed at the user's request.", inline=False)
    await ctx.send(embed=embedVar)

f = open("token", "r")
token = f.read()
uranium.run(token)