def noProxyFound(ctx):
    return ctx.send(":x: *I could not find a proxy with that name in your user database file. Has it been registered yet?*")

def noDatabaseFound(ctx):
    return ctx.send(":x: *I could not find your user database file. Has it been initialized?*")