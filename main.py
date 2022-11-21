import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

uranium = commands.Bot(command_prefix="u.", intents=intents)

@uranium.event
async def on_ready():
    print(f'We have logged in as {uranium.user}')
    #uranium.status = "discord bot development totally isn't hard"

@uranium.event
async def on_message(message):
    if message.author == uranium.user:
        return

    await uranium.process_commands(message)

@uranium.command()
async def userid(ctx):
    await ctx.reply("you have a user id of {0} lmao that's lame what a weirdo".format(ctx.message.author.id), mention_author=False)

@uranium.command(description="erm... what the what?")
async def about(ctx):
    embedVar = discord.Embed(
    title="About Uranium", description="Uranium is a Discord bot that is used for roleplay and for use in systems/plurality.", color=0x20FD00
            )
    embedVar.add_field(name="Did you know the bot is open source?", value="That means **anyone** can view the source code, or how the bot works. You can change/add/remove what you want, and self host your own Uranium instance. But remember, if you distribute your personal code, you **must** follow the terms and conditions of the GNU General Public Licence v3.", inline=False)
    embedVar.add_field(name="GNU General Public License v3", value="https://www.gnu.org/licenses/gpl-3.0.en.html", inline=False)
    embedVar.add_field(name="Github", value="https://github.com/BurningInfern0/Uranium", inline=False)
    embedVar.set_footer(text="Created by BurningInfern0.")
    await ctx.send(embed=embedVar)

@uranium.command(description="have me say something!")
async def say(ctx, msg):
    await ctx.message.delete()
    await ctx.send(msg)

f = open("token", "r")
token = f.read()

uranium.run(token)