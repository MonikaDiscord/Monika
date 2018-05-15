# Monika
![DBL Servers](https://discordbots.org/api/widget/servers/399315651338043392.svg) ![Travis CI](https://travis-ci.org/MonikaDiscord/Monika.svg?branch=master) ![DBL Upvotes](https://discordbots.org/api/widget/upvotes/399315651338043392.svg)

An entertaining Discord bot made to sharpen your server!

We've decided to make Monika open-source so you guys can help us make Monika even greater!
If you are able to contribute, we encourage doing so!
## Invite Monika
To invite Monika, use this [link](https://discordapp.com/oauth2/authorize?client_id=399315651338043392&permissions=8&scope=bot "Invite Link")!
## Prerequisites
* Python 3.6
* discord.py rewrite
* Lavalink's latest build (put it in `cogs/scripts/lavalink`).
* lavalink.py
* A sentry.io account and the module `raven`.
* A PostgreSQL server (scroll down to the last section!).
* All the API keys below.
## API keys needed
We won't be helping you with obtaining these.
* obviously Discord token
* weeb.sh (also needs waifu insult scope and generate love ship scope)
* discordbots.org
* NOT NEEDED YET: Google Perspective API (coming soon!)
## Setup
1. Install all the prerequisites.
2. Edit cogs/scripts/settings.py appropriately.
3. Edit cogs/scripts/lavalink/application.yml to set the password and the Sentry DSN.
4. Run cogs/scripts/lavalink/Lavalink.jar with `java -jar`.
5. Run monika.py with `python3`.
## Customizing a PostgreSQL server to Monika's needs
First, create a database named `monika`.
Go into the database.
Create a table with this command:

```CREATE TABLE users (id bigint primary key, name text, discrim varchar (4), money text, patron int, staff int, upvoter boolean);```

Make sure it went through successfully before moving on.
Now, create another table with this command:

```CREATE TABLE guilds (id bigint primary key, name text, prefix text, filteredwords text[]);```

You should be done!
