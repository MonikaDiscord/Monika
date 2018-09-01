# Monika
An entertaining Discord bot made to sharpen your server!

We've decided to make Monika open-source so you guys can help us make Monika even greater!
If you are able to contribute, we encourage doing so!
## Invite Monika
To invite Monika, use this [link](https://discordapp.com/oauth2/authorize?client_id=399315651338043392&permissions=8&scope=bot "Invite Link")!
# Self-hosting Monika
## Prerequisites
* Python 3.6
* A customized `config.json` file. (see "Configuration")
* A Lavalink server.
* A sentry.io account.
* pybooru.py
* A PostgreSQL server (with a database named `monika`).
* All the API keys below.
## API keys needed
We won't be helping you with obtaining these.
* obviously Discord token
* weeb.sh (also needs waifu insult scope and generate love ship scope)
* discordbots.org
* danbooru.donmai.us
* NOT NEEDED YET: Google Perspective API (coming soon!)
## Configuration
Here's a template for `config.json`:
```
{
  "token": "discord token",
  "dbuser": "psql user",
  "dbpass": "psql password",
  "dblkey": "discordbots.org token",
  "pwkey": "bots.discord.pw token",
  "kbkey": "bots.disgd.pw token",
  "weebkey": "weeb.sh token",
  "perspectivekey": "google perspective api token",
  "danboorukey": "danbooru api key",
  "lavapass": "lavalink password",
  "sentry_dsn": "sentry dsn",
  "datadog_api_key": "datadog api key",
  "datadog_app_key": "datadog app key"
}
```
Just put the file in Monika's main directory.
