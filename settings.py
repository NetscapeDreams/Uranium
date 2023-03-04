# YOU MUST SET THESE OPTIONS IF YOU ARE MODIFYING THIS CODE AND HOSTING IT!!!!
# As according to the GNU Affero General Public License version 3, network use of this application counts as DISTRIBUTION.
# If distribution occurs, you MUST disclose the source code in a PUBLIC repository where your changes to the code are STATED, and must follow and include the same license as the GNU AGPL v3.
modified = False
respositoryLink = "https://github.com/NetscapeDreams/Uranium"

# the settings below in this file are not considered "modifications" and do not need the modified variable changed

# please keep this in an array
prefixes = ["u.", "U."]

# mainly for the about section
botName = "Uranium"

# message id backup
# this variable is in charge of u.edit and the reaction system (delete, and show proxy info).
# every time a message gets sent, the:
# - message id
# - user id of who sent the proxy
# - proxy brackets
# get stored into a message.log file for later use, and the log file is only checked when the methods above are used.
# should Uranium keep a persistent log file for every single time it used a webhook, or do you want it cleared every time Uranium starts?
# persistance is recommended, but if you have a small storage space/large discord server, it's probably better to use perSession.

messageLogging = "persistent" # persistent or perSession

# settings below do nothing, they're just placeholders for now

# Allow Proxy Redirections
proxyRedirections = True

# Allow Dice Rolls
diceRolls = True
