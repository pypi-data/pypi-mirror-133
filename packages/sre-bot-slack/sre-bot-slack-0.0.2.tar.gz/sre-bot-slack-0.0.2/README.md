# sre-bot-slack

Sends notifications to slack.


# Configuration

```bash
/etc/sre/slack.conf


# a default token (necessary)
{
  "token": "<token>",
}

# different channels:
{
  "token": "<token>",
  "channels": {
    "channel1": <"token_channel>",
    "channel2": <"token_channel>"
  },
}

``

# How to upload new version
  * increase version in setup.py
  * one time: pipenv install twine --dev
  * pipenv shell
  * python3 setup.py upload

# install directly

pip3 install git+https://github.com/marcwimmer/sre-bot`