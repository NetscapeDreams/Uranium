import discord
import os
import re
from random import randint
from discord.ext import commands
from discord import Webhook

# import tsv editing commands
from tsv import removeProxy, getProxyAvatar, parseProxy, setProxyAvatar

# YOU MUST SET THESE OPTIONS IF YOU ARE MODIFYING THIS CODE AND HOSTING IT!!!!
# As according to the GNU Affero General Public License version 3, network use of this application counts as DISTRIBUTION.
# If distribution occurs, you MUST disclose the source code in a PUBLIC repository where your changes to the code are STATED, and must follow and include the same license as the GNU AGPL v3.
modified = False
respositoryLink = "https://github.com/BurningInfern0/Uranium"

# initialization
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

prefixes = "np.", "Np."

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
        webhookID = await channel.create_webhook(name="Neptunium Proxy Webhook")
        webhookPath = "./webhook-data/{0}".format(str(channelID))
        webhookStore = open(webhookPath, "w")
        webhookStore.write(str(webhookID))
        webhookStore.close()
        return webhookID

uranium = commands.Bot(command_prefix=prefixes, intents=intents)

@uranium.event
async def on_ready():
    print(f'[URANIUM] I have logged in as {uranium.user}!')
    
    game = discord.Game("with proxies! | u.help")
    await uranium.change_presence(status=discord.Status.online, activity=game)

# await uranium.process_commands(message)

@uranium.command()
async def about(ctx):
    embedVar = discord.Embed(
    title="About Neptunium", description="Neptunium is a Discord bot that is used for roleplay and for use in systems/plurality.", color=0x00fff4
            )
    if modified == True:
        embedVar.add_field(name="Warning:", value="*The owner of this bot has enabled the modified variable, which means this bot's code has been modified and put up for public use. A valid respository link for this code will be provided at the bottom.*", inline=False)
    embedVar.set_footer(text="Created by BurningInfern0.")
    embedVar.set_image(url="https://user-images.githubusercontent.com/74492478/204309975-8b937ad8-99c1-40f1-a373-ce692873fada.png")
    embedVar.add_field(name="Did you know the bot is open source?", value="That means **anyone** can view the source code, or how the bot works. You can change/add/remove what you want, and self host your own Neptunium instance. But remember, if you distribute your personal code, you **must** follow the terms and conditions of the GNU Affero General Public Licence v3.", inline=False)
    embedVar.add_field(name="GNU Affero General Public License v3", value="https://www.gnu.org/licenses/agpl-3.0.html", inline=False)
    embedVar.add_field(name="Repository Link", value=respositoryLink, inline=False)
    await ctx.send(embed=embedVar)

# all this does is create an empty CSV file for storing user proxy information.
@uranium.group(invoke_without_command=True)
async def init(ctx):
    databasePath = "./user-data/{0}.tsv".format(ctx.message.author.id)
    databaseExists = os.path.exists(databasePath)
    if databaseExists == True:
        await ctx.send(":x: *Your database is already initialized, and exists.*\nIf you would like to initialize it again, **deleting all of your proxies and settings**, please do `u.init confirm`.")
    else:
        databaseCreation = open(databasePath, "w")
        databaseCreation.close()
        await ctx.send(":white_check_mark: *Your database has been created and initialized. You can now create proxies.*")

@init.command()
async def confirm(ctx):
    databasePath = "./user-data/{0}.tsv".format(ctx.message.author.id)
    os.remove(databasePath)
    databaseCreation = open(databasePath, "w")
    databaseCreation.close()
    await ctx.send(":white_check_mark: *Your database has been reinitalized. All former proxies and settings have been deleted.*")
    

@uranium.group(invoke_without_command=True, aliases=["p"])
async def proxy(ctx):
    await ctx.send(":x: *Please provide a subcommand.*\nWhat do you want me to do with proxies? See `u.help proxy` for more information.")

@proxy.command(description="register proxy")
async def register(ctx, name:str, brackets:str):
    if len(name) > 80:
        await ctx.send(":x: *Your proxy's name is too long, please keep it equal to or under 80 characters.*")
        return
    appendProxy = open("./user-data/{0}.tsv".format(ctx.message.author.id), "a")
    appendProxy.write("{0}\t{1}\t*\n".format(brackets, name))
    appendProxy.close()
    await ctx.send("Wonderful! `{0}` has been created under your user data using the brackets `{1}`.\nTo send a message via this proxy, send `u.proxy send {1} I'm a proxy!`".format(name, brackets))

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

@proxy.command(aliases=["s"])
async def send(ctx, brackets:str, *, msg):
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
            webhookID = await obtainWebhookData(ctx, channelID)
            msg = msg.replace(originalres, "")
            redirect = True
        else:
            webhookID = await obtainWebhookData(ctx, ctx.channel.id)
    else:
        webhookID = await obtainWebhookData(ctx, ctx.channel.id)

    if redirect == True:
        channel = uranium.get_channel(int(channelID))
        webhookList = await channel.webhooks()
    else:
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
                    await wh.send(msg, username=name, embed=embedVar)
                else:
                    await wh.send(msg, username=name, avatar_url=avtr, embed=embedVar)
                return

            if avtr == "*":
                await wh.send(msg, username=name)
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
        await ctx.send(file=discord.File(r'./user-data/{0}.tsv'.format(ctx.author.id)))
    except:
        await ctx.send(":x: *I'm sorry, an error occurred, please try again later.*")

f = open("token", "r")
token = f.read()
uranium.run(token)