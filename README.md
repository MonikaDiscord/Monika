# Monika
Monika ~~is~~/was an entertainment bot for Discord servers.

I would like to make Monika available again, although we'll see how this goes.

If you are able to contribute, I encourage doing so.

**_Credits go to the original creator [kanielyaniel](https://github.com/kanielyaniel)._**

## Invite Monika
To invite Monika, use this *~~link~~*!

# Self-hosting Monika
You can host your own version of Monika! [Disclaimer](https://github.com/gpago/Monika/wiki/Self-hosting-Disclaimer)

## Prerequisites
- Obviously a way to host the python app and accompanying software
* **Python 3.6** (other python versions may work, but only the version here has been tested)
* **Python PIP** installed for the above version of Python
* **A PostgreSQL server** (with a database already created, preferably empty and with its own user)
* **A Lavalink server** ([Lavalink Repository](https://github.com/Frederikam/Lavalink))
* **A [Sentry IO](https://sentry.io/) account** (technically optional, but recommended)
* **A [DataDog](https://www.datadoghq.com/) account** (technically optional, but recommended)
* A customized `config.json` file (see [Configuration](https://github.com/gpago/Monika#configuration) below)
* ↓ All the API keys below ↓

## API keys needed
* Discord bot token
* weeb.sh (also needs waifu insult scope and generate love ship scope)
* Token from [DiscordBots.org](https://discordbots.org/)
* Token from [Bots.discord.pw](https://bots.discord.pw/) (may be removed soon)
* API key from [Danbooru.donmai.us](https://danbooru.donmai.us/)
* API key from [Sentry IO](https://sentry.io/)
* API and APP keys from [DataDog](https://www.datadoghq.com/)
* NOT NEEDED YET: Google Perspective API (coming soon!)

## Configuration
Here's a template for `config.json`:
```
{
  "token": "discord client bot token",
  "dbhost": "postgres host",
  "dbname": "postgres database",
  "dbuser": "postgres user",
  "dbpass": "postgres password",
  "lavahost": "lavalink host",
  "lavaport": "lavalink port",
  "lavapass": "lavalink password",
  "dblkey": "discordbots.org token",
  "weebkey": "weeb.sh token",
  "danbooruuser": "danbooru username",
  "danboorukey": "danbooru api key",
  "pwkey": "bots.discord.pw token",
  "kbkey": "bots.disgd.pw token",
  "sentry_dsn": "sentry.io dsn",
  "datadog_api_key": "datadog api key",
  "datadog_app_key": "datadog app key",
  "perspectivekey": "google perspective api token"
}
```
Just put the file in Monika's main directory **or** copy and rename the already included `config.json.example` file as `config.json`.
