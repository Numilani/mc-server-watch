#mc-server-watch
A simple tool that uses the mcsrvstat.us API to generate emails based on a watchlist.

## Usage

I threw this tool together basically overnight, so there is no UI; Everything is done via SQL commands.

* **Add a User.** 
    * Users have an ID and 2 required fields (email and username).
        * Email is for emailing the user.
        * Username is the user's Minecraft username, so the app doesn't remind you that players are online while you're online to see that for yoruself. 
        * Phone number was for a planned Twilio integration, it can be left as null. 
        * LastSeen is handled internally.
* **Add a Watch.**
    * Watches have an ID and 2 required fields (UserID and Username).  
        * UserID associates the watch with a user so it knows to who to email.
        * Username is the Minecraft player name to watch for and send reminders to the user about.
        * LastNotify is handled internally.
* **Configure the settings.**
    * Most of it's self-explanatory. 
        * The system requires a Gmail account to send emails from (like I said, I threw this together overnight, so email support is basic).
        * The URL field needs the server IP plugged into the end.
        * checkInterval is how often to check the mcsrvstat.us API. Don't bother setting it lower than 10 (the default), because that's how long the data stays cached on their end.
        * bufferIntervalPerPerson is the wait time in between emails (in minutes), so people don't get flooded with emails every 10 minutes. Defaults to 60, which is probably too often.
* **Let it run.**
    * Seriously, that's it. Told you it was simple :)

## Default Config

Just in case you need it.

```
[TECHNICAL]
dbFile = .\watchtables.db
checkInternal = 10
bufferIntervalPerPerson = 60

[SERVER]
url = https://api.mcsrvstat.us/2/<server-ip-goes-here>

[EMAIL]
port = 465
sender_email = your-email@example.com
password = passwd1234
```