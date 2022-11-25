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
    filesaver[editedLine] = "{0}\t{1}\t{2}\n".format(proxy[0], proxy[1], avatar.url)
    f.close()

    x = open("./user-data/{0}.tsv".format(ctx.message.author.id), 'w')
    x.writelines(filesaver)
    x.close()

    return ctx.send(":white_check_mark: *Avatar successfully saved.*\nPlease note, if the image you specified gets deleted, then your proxy's avatar will no longer work.")

def parseProxy(ctx, brackets):
    with open("./user-data/{0}.tsv".format(ctx.message.author.id)) as f:
        for line in f:
            proxy = line.split("\t")
            if proxy[0] == brackets:
                return proxy[1], proxy[2].strip()