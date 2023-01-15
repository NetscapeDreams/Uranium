def buildSendCommand(msg, username, avatar, detectThread, sendToThread, redirect, embeds=None, attachments=None):
    baseCommand = "wh.send(msg, username={0}".format("name")

    if avatar == "*":
        pass
    else:
        baseCommand = baseCommand + ", avatar_url={0}".format("avtr")

    if attachments == None:
        pass
    else:
        baseCommand = baseCommand + ", files={0}".format("fileAttachments")

    if embeds == None:
        pass
    else:
        baseCommand = baseCommand + ", embeds={0}".format("embedList")

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