# Uranium

Uranium is a bot designed for roleplaying and for plurality or system creation, created under Python via the pycord library under the GNU Affero General Public License version 3.

Or to put it bluntly, Uranium is designed to be an open source version of Tupperbox.

## What is currently possible as of now?
* Registering and removing proxies
    * `u.proxy register`
    * `u.proxy remove`
* Setting and viewing proxy avatars
    * `u.proxy avatar`
* Sending proxy messages
    * `u.proxy send`
* Purging all data
    * `u.reinit`
* Proxy Dice Rolls
    * `u.proxy send Logan I cast fireball for {{2d6+5}} damage!`
* Redirecting proxy messages to different channels
    * `u.proxy send Logan {{#channel}} hey, i'm being sent into a different channel!`
* Exporting user data
    * `u.export`

## What is not possible as of now?
* Changing proxy names or brackets
* Proxy birthdays
* Proxy descriptions
* Proxy nicknames
* Proxy tags
* Including proxy brackets in messages
* Listing your current proxies (with or without groups) and listing specific proxy information
* Finding proxies
* Proxy groups
* Importing user data
* Autoproxy
* Privacy settings
* Multiproxies
* Slash commands
* Server specific settings
* Editing proxy messages
* Showing information about a proxy message
* Reactions on messages
    * X for deletion
    * Pencil for editing
    * Questiom mark for proxy information
* Sending images or files under a proxy
* Proxies in Threads or Forums
* Replying using proxies

## Permissions

Uranium should only ever have the `Manage Messages` and `Manage Webhooks` permissions. Administrator is a little overkill.