# Uranium

<p align="center">
<img src="https://user-images.githubusercontent.com/121664679/213885228-339ba626-c546-4745-acad-6c7c13415a70.png" />
</p>

Uranium is a bot whose purpose is for roleplaying and for plurality or system creation, created under Python via the pycord library and under the GNU Affero General Public License version 3.

Uranium is designed to be a base engine for proxy use, and can be tweaked in any way you desire. Uranium is to be self-hosted, where you're in control.

Why not try Uranium today? 

If it's just not your cup of tea yet, that's okay! Maybe you should come back later when there are more features and quality of life improvements.

## What is currently possible as of now?
* Registering and removing proxies
    * `u.register`
    * `u.unregister`
* Listing proxies owned by you or others
    * `u.list`
* Changing proxy information
    * `u.avatar`
    * `u.rename`
    * `u.brackets`
* Sending proxy messages via brackets
    * `logan:hello!`
* Purging all data
    * `u.reinit`
* Proxy Dice Rolls
    * `logan:I cast fireball for {{2d6+5}} damage!`
* Redirecting proxy messages to different channels
    * `logan:{{#channel}} hey, i'm being sent into a different channel!`
* Exporting user data
    * `u.export`
* Proxies in Threads or Forums
* Sending images or files under a proxy
* Replying using proxies
* Editing/deleting proxy messages
    * `u.edit`
    * `u.delete`
* Reactions on messages
    * :x: for deletion
    * :question: for message information
* Multiproxies
* Finding proxies
    * `u.find`
    * `u.gfind`
* Listing specific proxy information
    * `u.isotope`
* Showing information about a proxy message
    * `u.showmsg`

## What is not possible/planned to be added?
* High importance:
    * Proxy groups
    * Listing your current proxies in groups
    * User settings file
        * Who can see your proxies
    
* Medium importance:
    * Importing user data
    * Autoproxy (requires user settings file)
    * Server specific settings
        * Specific prefixes per server
        * Logging
        * Channel-specific permissions

* Low importance:
    * Proxy birthdays
    * Proxy descriptions
    * Proxy nicknames
    * Proxy tags
    * Including proxy brackets in messages (requires user settings file)
    * Slash commands

## Permissions

Uranium should only ever have the `Manage Messages` and `Manage Webhooks` permissions. Administrator is a little overkill.