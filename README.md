# Monika
An entertaining Discord bot made to sharpen your server (again)!
## Invite Monika
To invite Monika, use this [link](https://discordapp.com/oauth2/authorize?client_id=399315651338043392&permissions=8&scope=bot "Invite Link")!
# Self-hosting Monika
## Prerequisites
* Python 3.6
* A customized `config.json` file. (see "Configuration")
* A Lavalink server.
* pybooru.py
* A PostgreSQL server (with a database named `monika`).
* All the API keys below.
## API keys needed
We won't be helping you with obtaining these.
* obviously Discord token
* weeb.sh (also needs waifu insult scope and generate love ship scope)
* danbooru.donmai.us
## Configuration
Here's a template for `config.json`:
```
{
  "token": "discord token",
  "dbuser": "psql user",
  "dbpass": "psql password",
  "weebkey": "weeb.sh token",
  "lavapass": "lavalink password",
  "danboorukey": "danbooru api key",
  "danbooruname": "danbooru username"
}
```
Just put the file in Monika's main directory.
