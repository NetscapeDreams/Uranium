def buildSendCommand(msg, username, avatar, detectThread, sendToThread, redirect, embeds=None, attachments=None):
    baseCommand = "wh.send(msg, username=name"

    if avatar == "*":
        pass
    else:
        baseCommand = baseCommand + ", avatar_url=avtr"

    if attachments == None:
        pass
    else:
        baseCommand = baseCommand + ", files=fileAttachments"

    if embeds == None:
        pass
    else:
        baseCommand = baseCommand + ", embeds=embedList"

    if detectThread == True and redirect == False:
        baseCommand = baseCommand + ", thread=ctx.channel"
    elif redirect == True:
        if sendToThread == True:
            baseCommand = baseCommand + ", thread=channel"
        else:
            pass
    else:
        pass

    baseCommand = baseCommand + ", wait=True)"
    return baseCommand