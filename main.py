import discord
import os
import csv
from discord.ext import commands
from discord import Webhook

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

uranium = commands.Bot(command_prefix="u.", intents=intents)

@uranium.event
async def on_ready():
    print(f'[URANIUM] I have logged in as {uranium.user}!')
    
    game = discord.Game("with proxies! | u.help")
    await uranium.change_presence(status=discord.Status.online, activity=game)

@uranium.command()
async def about(ctx):
    embedVar = discord.Embed(
    title="About Uranium", description="Uranium is a Discord bot that is used for roleplay and for use in systems/plurality.", color=0x20FD00
            )
    if modified == True:
        embedVar.add_field(name="Warning:", value="*The owner of this bot has enabled the modified variable, which means this bot's code has been modified and put up for public use. A valid respository link for this code will be provided at the bottom.*", inline=False)
    embedVar.set_footer(text="Created by BurningInfern0.")
    embedVar.set_image(url="https://user-images.githubusercontent.com/74492478/203663460-6863d8e6-66d8-4379-8fe9-aba48de15262.png")
    embedVar.add_field(name="Did you know the bot is open source?", value="That means **anyone** can view the source code, or how the bot works. You can change/add/remove what you want, and self host your own Uranium instance. But remember, if you distribute your personal code, you **must** follow the terms and conditions of the GNU Affero General Public Licence v3.", inline=False)
    embedVar.add_field(name="GNU Affero General Public License v3", value="https://www.gnu.org/licenses/agpl-3.0.html", inline=False)
    embedVar.add_field(name="Repository Link", value=respositoryLink, inline=False)
    await ctx.send(embed=embedVar)

# all this does is create an empty CSV file for storing user proxy information.
@uranium.group(invoke_without_command=True)
async def init(ctx):
    databasePath = "./user-data/{0}.csv".format(ctx.message.author.id)
    databaseExists = os.path.exists(databasePath)
    if databaseExists == True:
        await ctx.send(":x: *Your database is already initialized, and exists.*\nIf you would like to initialize it again, **deleting all of your proxies and settings**, please do `u.init confirm`.")
    else:
        databaseCreation = open(databasePath, "w")
        databaseCreation.close()
        await ctx.send(":white_check_mark: *Your database has been created and initialized. You can now create proxies.*")

@init.command()
async def confirm(ctx):
    databasePath = "./user-data/{0}.csv".format(ctx.message.author.id)
    os.remove(databasePath)
    databaseCreation = open(databasePath, "w")
    databaseCreation.close()
    await ctx.send(":white_check_mark: *Your database has been reinitalized. All former proxies and settings have been deleted.*")
    

@uranium.group(invoke_without_command=True, aliases=["p"])
async def proxy(ctx):
    await ctx.send(":x: *Please provide a subcommand.*\nWhat do you want me to do with proxies? See `u.help proxy` for more information.")

@proxy.command(description="register proxy")
async def register(ctx, name:str, brackets:str):
    appendProxy = open("./user-data/{0}.csv".format(ctx.message.author.id), "a")
    appendProxy.write("{0},{1},*\n".format(brackets, name))
    appendProxy.close()
    await ctx.send("Wonderful! `{0}` has been created under your user data using the brackets `{1}`.\nTo send a message via this proxy, send `u.proxy send {1} I'm a proxy!`".format(name, brackets))

@proxy.command(description="delete a proxy")
async def remove(ctx, name:str):
    global editedLine
    editedLine = 0
    try:
        with open("./user-data/{0}.csv".format(ctx.message.author.id)) as f:
            csv_reader = csv.reader(f, delimiter=',')
            for line in csv_reader:
                if line[1] == name:
                    break
                editedLine = editedLine + 1
            else:
                raise EOFError()
    except IOError:
            await ctx.send(":x: *I could not find your user database file. Has it been initialized?*")
            return
    except EOFError:
            await ctx.send(":x: *I could not find a proxy with that name in your user database file. Has it been registered yet?*")
            return

    f = open("./user-data/{0}.csv".format(ctx.message.author.id), 'r')
    filesaver = f.readlines()
    filesaver[editedLine] = ""
    f.close()

    x = open("./user-data/{0}.csv".format(ctx.message.author.id), 'w')
    x.writelines(filesaver)
    x.close()

    await ctx.send(":white_check_mark: {0} has been removed from your proxy list.".format(name))


@proxy.command(description="set a proxy's avatar")
async def avatar(ctx, name:str):
    global line
    line = ""
    try:
        avatar = ctx.message.attachments[0]
    except:
        try:
            with open("./user-data/{0}.csv".format(ctx.message.author.id)) as f:
                csv_reader = csv.reader(f, delimiter=',')
                for line in csv_reader:
                    if line[1] == name:
                        if line[1] == "*":
                            await ctx.send(":x: *This proxy doesn't have an avatar.*")
                        else:
                            await ctx.send(line[2])
                        return
                else:
                    raise EOFError()
        except IOError:
            await ctx.send(":x: *I could not find your user database file. Has it been initialized?*")
            return
        except EOFError:
            await ctx.send(":x: *I could not find a proxy with that name in your user database file. Has it been registered yet?*")
            return
    
    global editedLine
    editedLine = 0

    try:
        with open("./user-data/{0}.csv".format(ctx.message.author.id)) as f:
            csv_reader = csv.reader(f, delimiter=',')
            for line in csv_reader:
                if line[1] == name:
                    break
                editedLine = editedLine + 1
            else:
                raise EOFError()
        f = open("./user-data/{0}.csv".format(ctx.message.author.id), 'r')
        filesaver = f.readlines()
        filesaver[editedLine] = "{0},{1},{2}\n".format(line[0], line[1], avatar.url)
        f.close()

        x = open("./user-data/{0}.csv".format(ctx.message.author.id), 'w')
        x.writelines(filesaver)
        x.close()

        await ctx.send(":white_check_mark: *Avatar successfully saved.*\nPlease note, if the image you specified gets deleted, then your proxy's avatar will no longer work.")
    except IOError:
        await ctx.send(":x: *I could not find your user database file. Has it been initialized?*")
    except EOFError:
        await ctx.send(":x: *I could not find a proxy with that name in your user database file. Has it been registered yet?*")

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
    # check if channel webhook exists in local database
    direc = os.listdir("./webhook-data/")
    for file in direc:
        if str(ctx.channel.id) in file:
            webhookRead = open("./webhook-data/{0}".format(str(ctx.channel.id), "r"))
            webhookID = webhookRead.read()
            webhookRead.close()
            break
    # if not, create and store it
    else:
        webhookID = await ctx.channel.create_webhook(name="Uranium Proxy Webhook")
        webhookPath = "./webhook-data/{0}".format(str(ctx.channel.id))
        webhookStore = open(webhookPath, "w")
        webhookStore.write(str(webhookID))
        webhookStore.close()

    webhookList = await ctx.message.channel.webhooks()
    for wh in webhookList:
        if str(webhookID) == str(wh):
            with open("./user-data/{0}.csv".format(ctx.message.author.id)) as f:
                csv_reader = csv.reader(f, delimiter=',')
                for line in csv_reader:
                    if line[0] == brackets:
                        name = line[1]
                        avtr = line[2]
            await ctx.message.delete()
            if avtr == "*":
                await wh.send(msg, username=name)
            else:
                await wh.send(msg, username=name, avatar_url=avtr)
            
            return
    await ctx.send(":x: **Something went wrong!**\nThe webhook ID in my local database could not be found in this channel's webhook list. *Did the webhook get deleted?*")

f = open("token", "r")
token = f.read()
uranium.run(token)