# mercurial-discord
Mercurial hook that posts to Discord

Copy it to the `.hg` directory of your repository on the server, change its `.hg/hgrc` like this:

```cfg
[hooks]
incoming = python:.hg/hooks.py:incoming
```

and put a `secrets.txt` file right next to it:

```json
{
    "hgwebUrl": "https://project.local/hg/reponame/",
    "webhookUrl": "https://discord.com/api/webhooks/gibberish123456789oijhzgtfrdsa"
}
```
