# Uranium

Uranium is a bot designed for roleplaying and for plurality or system creation, created under Python via the pycord library under the GNU Affero General Public License version 3.

Or to put it bluntly, Uranium is designed to be an open source version of Tupperbox.

## What is currently possible as of now?
* Registering and removing proxies
    * `u.proxy register`
    * `u.proxy remove`
* Listing proxies owned by you or others
    * `u.proxy list`
* Changing proxy information
    * `u.proxy avatar`
    * `u.proxy rename`
    * `u.proxy brackets`
* Sending proxy messages
    * `u.proxy send`
    * `logan:hello!`
* Purging all data
    * `u.reinit`
* Proxy Dice Rolls
    * `u.proxy send Logan I cast fireball for {{2d6+5}} damage!`
* Redirecting proxy messages to different channels
    * `u.proxy send Logan {{#channel}} hey, i'm being sent into a different channel!`
* Exporting user data
    * `u.export`
* Proxies in Threads or Forums

## What is not possible/planned to be added?
* High importance:
    * Proxy groups
    * Listing your current proxies in groups
    * Listing specific proxy information
    * Finding proxies
    * User settings file
        * Who can see your proxies
    * Multiproxies
    * Editing proxy messages
    * Reactions on messages
        * X for deletion
        * Pencil for editing
        * Question mark for proxy information
    * Sending images or files under a proxy
    * Replying using proxies
* Medium importance:
    * Importing user data
    * Autoproxy (requires user settings file)
    * Server specific settings
        * Specific prefixes per server
        * Logging
        * Channel-specific permissions
    * Showing information about a proxy message
* Low importance:
    * Proxy birthdays
    * Proxy descriptions
    * Proxy nicknames
    * Proxy tags
    * Including proxy brackets in messages (requires user settings file)
    * Slash commands

## Permissions

Uranium should only ever have the `Manage Messages` and `Manage Webhooks` permissions. Administrator is a little overkill.