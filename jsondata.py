import json
import os
from datetime import date

def loadData(authorid):
    with open("./user-data/{0}.json".format(authorid)) as user_file:
        file_contents = user_file.read()
    datafile = json.loads(file_contents)
    return datafile

def saveData(ctx, data):
    data = json.dumps(data)
    updateDatabase = open("./user-data/{0}.json".format(ctx.message.author.id), "w")
    updateDatabase.write(data)
    updateDatabase.close()

def registerProxy(ctx, brackets, name, proxyAvatar):
    if os.path.exists("./user-data/{0}.json".format(ctx.message.author.id)) == True:
        datafile = loadData(ctx.message.author.id)
        for key, value in datafile["isotopes"].items():
            if key == brackets:
                conflictions = "brackets"
                break
            if name in datafile["isotopes"][key]["name"]:
                conflictions = "name"
                break
        else:
            conflictions = None
    else:
        createDatabase = open("./user-data/{0}.json".format(ctx.message.author.id), "a")
        todaysDate = str(date.today())
        proxyDict = {
            "isotopes": {
                brackets: {
                    "name": name,
                    "avatar": proxyAvatar,
                    "group": "N/A",
                    "birthday": "N/A",
                    "desc": "",
                    "nick": "N/A",
                    "tag": "N/A",
                    "messages": 0,
                    "creationdate": todaysDate,
                    "sortingID": 0
                }
            }
        }
        proxyJson = json.dumps(proxyDict)
        createDatabase.write(proxyJson)
        createDatabase.close()
        return ctx.send("Wonderful! `{0}` has been created under your user data using the brackets `{1}`.\nTo send a message via this isotope, you can just use the brackets. `{1}I'm a proxy!`".format(name, brackets))
    if conflictions == None:
        todaysDate = str(date.today())
        sortingID = 0
        for key, value in datafile["isotopes"].items():
            if datafile["isotopes"][key]["sortingID"] > sortingID:
                sortingID = datafile["isotopes"][key]["sortingID"]
        datafile["isotopes"].update({
            brackets: {
                "name": name,
                "avatar": proxyAvatar,
                "group": "N/A",
                "birthday": "N/A",
                "desc": "",
                "nick": "N/A",
                "tag": "N/A",
                "messages": 0,
                "creationdate": todaysDate,
                "sortingID": sortingID + 1
            }
        })
        saveData(ctx, datafile)
        return ctx.send("Wonderful! `{0}` has been created under your user data using the brackets `{1}`.\nTo send a message via this isotope, you can just use the brackets. `{1}I'm a proxy!`".format(name, brackets))
    elif conflictions == "name":
        return ctx.send(":x: There already is an isotope with this name in your user data.")
    elif conflictions == "brackets":
        return ctx.send(":x: There already is an isotope with these brackets in your user data.")

def removeProxy(ctx, name):
    datafile = loadData(ctx.message.author.id)
    for key, value in datafile["isotopes"].items():
        if name in datafile["isotopes"][key]["name"]:
            datafile["isotopes"].pop(key)
            saveData(ctx, datafile)
            return ctx.send(":white_check_mark: `{0}` has been removed from your isotope list.".format(name))
    else:
        return ctx.send(":x: Isotope not found.")

def parseProxy(ctx, brackets, userid=None):
    if userid == None:
        userid = ctx.message.author.id
    datafile = loadData(userid)
    return datafile["isotopes"][brackets]["name"], datafile["isotopes"][brackets]["avatar"]

def proxyAvatar(ctx, name, avatar=None):
    datafile = loadData(ctx.message.author.id)
    for key, value in datafile["isotopes"].items():
        if name in datafile["isotopes"][key]["name"]:
            if avatar == None:
                if datafile["isotopes"][key]["avatar"] == "N/A":
                    return ctx.send(":x: This proxy doesn't have an avatar.")
                else:
                    return ctx.send(datafile["isotopes"][key]["avatar"])
            else:
                datafile["isotopes"][key]["avatar"] = avatar.url
                saveData(ctx, datafile)
                return ctx.send(":white_check_mark: *Avatar successfully saved.*\nPlease note, if the image you specified gets deleted, then your proxy's avatar will no longer work.\n(This will be changed in the future so that Uranium will save avatars!)")
    else:
        return ctx.send(":x: Isotope not found.")

def editProxyName(ctx, oldname, newname):
    if len(newname) > 80:
        return ctx.send(":x: Your isotope's new name is too long, please keep it equal to or under 80 characters.")
    
    datafile = loadData(ctx.message.author.id)
    for key, value in datafile["isotopes"].items():
        if oldname in datafile["isotopes"][key]["name"]:
            datafile["isotopes"][key]["name"] = newname
            saveData(ctx, datafile)
            return ctx.send(":white_check_mark: Name successfully saved.")
    else:
        return ctx.send(":x: Isotope not found.")

def editProxyBrackets(ctx, name, newbrackets):
    datafile = loadData(ctx.message.author.id)
    for key, value in datafile["isotopes"].items():
        if name in datafile["isotopes"][key]["name"]:
            if newbrackets == None:
                return ctx.send("The brackets for {0} are `{1}`.".format(name, key))
            else:
                datafile["isotopes"][newbrackets] = datafile["isotopes"][key]
                del datafile["isotopes"][key]
                saveData(ctx, datafile)
                return ctx.send(":white_check_mark: Brackets successfully saved.")
    else:
        return ctx.send(":x: Isotope not found.")

def parseAll(ctx, user, search=None, globalSearch=False):
    if globalSearch == False:
        try:
            datafile = loadData(user.id)
        except FileNotFoundError:
            return None, None
    
    if globalSearch == False:
        totalIsotopes = len(datafile["isotopes"])
    isotopeCounter = 0
    searchIsotopeCounter = 0
    currentSortingID = 0
    pageCounter = 0
    pageProxyCounter = 0
    pageDict = {}
    totalDict = {}

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
                userFile = "./user-data/{0}.json".format(str(member.id))
                if os.path.exists(userFile) == True:
                    validMemberIDs.append(member.id)
        for memberID in validMemberIDs:
            datafile = loadData(memberID)
            totalIsotopes = len(datafile["isotopes"])
            currentSortingID = 0
            isotopeCounter = 0
            while True:
                for key, value in datafile["isotopes"].items():
                    if datafile["isotopes"][key]["sortingID"] == currentSortingID:
                        if pageProxyCounter == 5:
                            pageProxyCounter = 0
                            pageCounter += 1
                            totalDict[pageCounter] = pageDict
                            pageDict = {}
                        if search.lower() in datafile["isotopes"][key]["name"].lower():
                            searchIsotopeCounter += 1
                            pageProxyCounter += 1
                            datafile["isotopes"][key]["owner"] = memberID
                            pageDict[key] = datafile["isotopes"][key]
                        isotopeCounter += 1
                if isotopeCounter == totalIsotopes:
                    break
                currentSortingID += 1
        if bool(pageDict) == True:
            pageCounter += 1
            totalDict[pageCounter] = pageDict

        return totalDict, searchIsotopeCounter

    while True:
        for key, value in datafile["isotopes"].items():
            if datafile["isotopes"][key]["sortingID"] == currentSortingID:
                if pageProxyCounter == 5:
                    pageProxyCounter = 0
                    pageCounter += 1
                    totalDict[pageCounter] = pageDict
                    pageDict = {}
                if search != None:
                    if search.lower() in datafile["isotopes"][key]["name"].lower():
                        searchIsotopeCounter += 1
                        pageProxyCounter += 1
                        pageDict[key] = datafile["isotopes"][key]
                else:
                    pageProxyCounter += 1
                    pageDict[key] = datafile["isotopes"][key]
                isotopeCounter += 1
        if isotopeCounter == totalIsotopes:
            if bool(pageDict) == True:
                pageCounter += 1
                totalDict[pageCounter] = pageDict
            break
        currentSortingID += 1
    
    if search == None:
        return totalDict, isotopeCounter
    else:
        return totalDict, searchIsotopeCounter