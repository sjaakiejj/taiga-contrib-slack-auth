Taiga contrib slack auth
=========================

The Taiga plugin for slack authentication, based on Taiga.io's Github plugin.

Installation
------------

### Taiga Back

In your Taiga back python virtualenv install the pip package `taiga-contrib-slack-auth` with:

```bash
  pip install taiga-contrib-slack-auth
```

Modify your settings/local.py and include the line:

```python
  INSTALLED_APPS += ["taiga_contrib_slack_auth"]

  # Get these from https://slack.com/settings/developers
  SLACK_API_CLIENT_ID = "YOUR-SLACK-CLIENT-ID"
  SLACK_API_CLIENT_SECRET = "YOUR-SLACK-CLIENT-SECRET"
```

### Taiga Front

Download in your `dist/plugins/` directory of Taiga front the `taiga-contrib-slack-auth` compiled code (you need subversion in your system):

```bash
  cd dist/
  mkdir -p plugins
  cd plugins
  svn export "https://slack.com/sjaakiejj/taiga-contrib-slack-auth/tags/$(pip show taiga-contrib-slack-auth | awk '/^Version: /{print $2}')/front/dist"  "slack-auth"
```

Include in your dist/conf.json in the contribPlugins list the value `"/plugins/slack-auth/slack-auth.json"`:

```json
...
    "slackClientId": "YOUR-slack-CLIENT-ID",
    "contribPlugins": [
        (...)
        "/plugins/slack-auth/slack-auth.json"
    ]
...
```

Running tests
-------------

We only have backend tests, you have to add your taiga-back directory to the
PYTHONPATH environment variable, and run py.test, for example:

```bash
  cd back
  add2virtualenv /home/taiga/taiga-back/
  py.test
```
