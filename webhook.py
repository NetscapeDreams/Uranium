def buildSendCommand(msg, username, avatar, detectThread, sendToThread, redirect, embed=None, attachments=None):
    baseCommand = "wh.send(msg, username={0}".format("name")

    if avatar == "*":
        pass
    else:
        baseCommand = baseCommand + ", avatar_url={0}".format("avtr")

    if attachments == None:
        pass
    else:
        baseCommand = baseCommand + ", files={0}".format("fileAttachments")

    if embed == None:
        pass
    else:
        baseCommand = baseCommand + ", embed={0}".format("embedVar")

    if detectThread == True and redirect == False:
        baseCommand = baseCommand + ", thread={0}".format("ctx.channel")
    elif redirect == True:
        if sendToThread == True:
            baseCommand = baseCommand + ", thread={0}".format("channel")
        else:
            pass
    else:
        pass

    baseCommand = baseCommand + ")"
    return baseCommand