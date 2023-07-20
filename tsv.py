import os

from error import noProxyFound, noDatabaseFound

# this file is just meant for removing/searching/editing tsv user data in one file.

global editedLine

def removeProxy(ctx, name):
    editedLine = 0
    try:
        with open("./user-data/{0}.tsv".format(ctx.message.author.id)) as f:
            for line in f:
                proxy = line.split("\t")
                if proxy[1] == name:
                    break
                editedLine = editedLine + 1
            else:
                return noProxyFound(ctx)
    except IOError:
            return noDatabaseFound(ctx)

    f = open("./user-data/{0}.tsv".format(ctx.message.author.id), 'r')
    filesaver = f.readlines()
    filesaver[editedLine] = ""
    f.close()

    x = open("./user-data/{0}.tsv".format(ctx.message.author.id), 'w')
    x.writelines(filesaver)
    x.close()

    if os.stat('./user-data/{0}.tsv'.format(ctx.message.author.id)).st_size == 0:
        os.remove('./user-data/{0}.tsv'.format(ctx.message.author.id))
        return ctx.send(":white_check_mark: {0} has been removed from your proxy list, and since you no longer have any more isotopes, your user data file has been deleted.".format(name))
    else:
        return ctx.send(":white_check_mark: {0} has been removed from your proxy list.".format(name))

def getProxyAvatar(ctx, name):
    try:
        with open("./user-data/{0}.tsv".format(ctx.message.author.id)) as f:
            for line in f:
                proxy = line.split("\t")
                if proxy[1] == name:
                    if proxy[2].strip() == "*":
                        return ctx.send(":x: *This proxy doesn't have an avatar.*")
                    else:
                        return ctx.send(proxy[2])
            else:
                return noProxyFound(ctx)
    except IOError:
        return noDatabaseFound(ctx)

def setProxyAvatar(ctx, name, avatar):
    editedLine = 0

    try:
        with open("./user-data/{0}.tsv".format(ctx.message.author.id)) as f:
            for line in f:
                proxy = line.split("\t")
                if proxy[1] == name:
                    break
                editedLine = editedLine + 1
            else:
                return noProxyFound(ctx)
    except IOError:
            return noDatabaseFound(ctx)

    f = open("./user-data/{0}.tsv".format(ctx.message.author.id), 'r')
    filesaver = f.readlines()
    filesaver[editedLine] = "{0}\t{1}\t{2}".format(proxy[0], proxy[1], avatar.url)
    f.close()

    x = open("./user-data/{0}.tsv".format(ctx.message.author.id), 'w')
    x.writelines(filesaver)
    x.close()

    return ctx.send(":white_check_mark: *Avatar successfully saved.*\nPlease note, if the image you specified gets deleted, then your proxy's avatar will no longer work.")

def parseProxy(ctx, brackets, userid=None):
    if userid == None:
        userid = ctx.message.author.id
    with open("./user-data/{0}.tsv".format(userid)) as f:
        for line in f:
            proxy = line.split("\t")
            if proxy[0] == brackets:
                return proxy[1], proxy[2].strip()
            
def parseProxyByName(ctx, name):
    with open("./user-data/{0}.tsv".format(ctx.message.author.id)) as f:
        for line in f:
            proxy = line.split("\t")
            if proxy[1] == name:
                return proxy

def editProxyName(ctx, oldname, newname):
    editedLine = 0

    try:
        with open("./user-data/{0}.tsv".format(ctx.message.author.id)) as f:
            for line in f:
                proxy = line.split("\t")
                if proxy[1] == oldname:
                    break
                editedLine = editedLine + 1
            else:
                return noProxyFound(ctx)
    except IOError:
            return noDatabaseFound(ctx)

    f = open("./user-data/{0}.tsv".format(ctx.message.author.id), 'r')
    filesaver = f.readlines()
    filesaver[editedLine] = "{0}\t{1}\t{2}".format(proxy[0], newname, proxy[2])
    f.close()

    x = open("./user-data/{0}.tsv".format(ctx.message.author.id), 'w')
    x.writelines(filesaver)
    x.close()

    return ctx.send(":white_check_mark: *Name successfully saved.*")

def editProxyBrackets(ctx, name, newbrackets):
    editedLine = 0

    try:
        with open("./user-data/{0}.tsv".format(ctx.message.author.id)) as f:
            for line in f:
                proxy = line.split("\t")
                if proxy[1] == name:
                    break
                editedLine = editedLine + 1
            else:
                return noProxyFound(ctx)
    except IOError:
            return noDatabaseFound(ctx)

    f = open("./user-data/{0}.tsv".format(ctx.message.author.id), 'r')
    filesaver = f.readlines()
    filesaver[editedLine] = "{0}\t{1}\t{2}".format(newbrackets, proxy[1], proxy[2])
    f.close()

    x = open("./user-data/{0}.tsv".format(ctx.message.author.id), 'w')
    x.writelines(filesaver)
    x.close()

    return ctx.send(":white_check_mark: *Brackets successfully saved.*")

def parseAll(ctx, user, search=None, globalSearch=False):
    linesLength = 0
    lineCounter = 0
    searchLineCounter = 0
    proxyCounter = 0
    groupArray = []
    finalArray = []

    if globalSearch == True:
        validMemberIDs = []
        validMatches = []
        userFiles = []
        userDirectory = os.listdir("./user-data/")
        memberList = ctx.guild.members
        for member in memberList:
            if member.bot == True:
                pass
            else:
                for file in userDirectory:
                    if str(member.id) in file:
                        validMemberIDs.append(member.id)
        for memberID in validMemberIDs:
            with open("./user-data/{0}.tsv".format(memberID)) as g:
                # length check
                for lineCheck in g:
                    if lineCheck == "\n":
                        pass
                    else:
                        linesLength += 1
            with open("./user-data/{0}.tsv".format(memberID)) as f:
                for line in f:
                    proxy = line.split("\t")
                    if line == "\n":
                        pass
                    elif proxy[2].endswith("/n") or proxy[2].endswith("\n"):
                        proxy[2] = proxy[2][:-1]
                        if search.lower() in proxy[1].lower():
                            proxy.append(memberID)
                            validMatches.append(proxy)
                            searchLineCounter += 1
        pageCounter = 0
        for x in validMatches:
            groupArray.append(x)
            proxyCounter += 1
            pageCounter += 1
            if pageCounter == 5 or proxyCounter == len(validMatches):
                finalArray.append(groupArray)
                groupArray = []
                pageCounter = 0

        return finalArray, searchLineCounter


    try:
        with open("./user-data/{0}.tsv".format(user.id)) as g:
            # length check
            for lineCheck in g:
                if lineCheck == "\n":
                    pass
                else:
                    linesLength += 1
        with open("./user-data/{0}.tsv".format(user.id)) as f:
            for line in f:
                proxy = line.split("\t")
                if line == "\n":
                    pass
                else:
                    if proxy[2].endswith("/n") or proxy[2].endswith("\n"):
                        proxy[2] = proxy[2][:-1]
                    if search != None:
                        if search.lower() in proxy[1].lower():
                            groupArray.append(proxy)
                            searchLineCounter += 1
                            proxyCounter += 1
                    else:
                        groupArray.append(proxy)
                        proxyCounter += 1
                    lineCounter += 1

                if proxyCounter == 5 or lineCounter == linesLength:
                    finalArray.append(groupArray)
                    groupArray = []
                    proxyCounter = 0
                
    except IOError:
            return noDatabaseFound(ctx)
    
    if search == None:
        return finalArray, lineCounter
    else:
        return finalArray, searchLineCounter

def checkForPermission(ctx, msgid, userid):
    with open("./message-logs/{0}.tsv".format(ctx.guild.id)) as f:
        for line in f:
            message = line.split("\t")
            if message[0] == str(msgid):
                if message[1] == str(userid):
                    return True
        else:
            return False

def checkForConflicts(ctx, name, brackets):
    with open("./user-data/{0}.tsv".format(ctx.author.id)) as f:
        editedLine = 0
        for line in f:
            proxy = line.split("\t")
            try:
                if proxy[0] == brackets:
                    return "brackets"
                if proxy[1] == name:
                    return "name"
                editedLine = editedLine + 1
            except IndexError:
                f = open("./user-data/{0}.tsv".format(ctx.message.author.id), 'r')
                filesaver = f.readlines()
                filesaver[editedLine] = ""
                f.close()

                x = open("./user-data/{0}.tsv".format(ctx.message.author.id), 'w')
                x.writelines(filesaver)
                x.close()
        else:
            return None

def showProxyMessage(ctx, msgid):
    with open("./message-logs/{0}.tsv".format(ctx.guild.id)) as f:
        for line in f:
            message = line.split("\t")
            if message[0] == str(msgid):
                return message[1], message[2]
        else:
            return False