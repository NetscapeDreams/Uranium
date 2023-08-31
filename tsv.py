import os

# this file is only exists for the message-logs.

def checkForPermission(ctx, msgid, userid):
    with open("./message-logs/{0}.tsv".format(ctx.guild.id)) as f:
        for line in f:
            message = line.split("\t")
            if message[0] == str(msgid):
                if message[1] == str(userid):
                    return True
        else:
            return False

def showProxyMessage(ctx, msgid):
    with open("./message-logs/{0}.tsv".format(ctx.guild.id)) as f:
        for line in f:
            message = line.split("\t")
            if message[0] == str(msgid):
                return message[1], message[2]
        else:
            return False