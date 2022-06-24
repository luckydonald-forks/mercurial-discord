EXTENSIONS = [
    "bat", "cginc", "compute", "cpp", "cs", "groovy", "h", "hgignore", "js", "lua", "py",
    "shader"
]

import json, os, re, urllib.error, urllib.request

try:
    secretsPath = os.path.dirname(os.path.abspath(__file__)) + "/secrets.json"
    secrets = json.load(open(secretsPath))
except (IOError, ValueError) as ex:
    from mercurial import ui

    ui.write(("Discord incoming hook could not load secrets because " + str(ex) + "\n").encode("utf-8"))
    exit(1)


def EscapeMarkdown(str):
    return str  # TODO


def incoming(ui, repo, node, **kwargs):
    ctx = repo[node]

    pattern = r"\.(?:" + "|".join(EXTENSIONS) + ")$"
    if not any(re.search(pattern, i.decode("utf-8")) != None for i in ctx.files()):
        return
    # end if

    shortId = ctx.hex()[:12].decode("utf-8")

    description = ctx.description().strip()
    lineBreak = description.find(b"\n")
    if lineBreak >= 0:
        title = description[:lineBreak].strip()
        description = description[lineBreak:].strip()
    else:
        title = description
        description = None
    # end if

    branch = ctx.branch().decode("utf-8")
    author = ctx.user().decode("utf-8")

    post_discord(ui, title, description, branch, author, shortId)
# end def


def post_discord(ui, title, description, branch, author, shortId):
    embed = {
        "url": secrets["hg"]["commitUrl"].format(short_id=shortId),
        "fields": [
            {"name": "Branch", "value": branch, "inline": True},
            {"name": "Author", "value": author, "inline": True},
            {"name": "Node", "value": shortId, "inline": True}
        ]
    }
    if title:
        embed["title"] = title.decode("utf-8")
    # end if
    if description:
        embed["description"] = description.decode("utf-8")
    # end if

    request = urllib.request.Request(
        secrets["webhookUrl"],
        json.dumps({"embeds": [embed]}).encode("utf-8"),
        {"Content-Type": "application/json", "User-Agent": "Mercurial/5.8"}
    )

    try:
        urllib.request.urlopen(request)
    except urllib.error.URLError as ex:
        ui.write(("Discord incoming hook web request failed because " + str(ex) + "\n").encode("utf-8"))
        return
    # end try
# end def


def post_issue_numbers_to_hacknplan(ui, title, description, branch, author, shortId):
    project_id = 0
    url_to_post = secrets["hg"]["commitUrl"].format(short_id=shortId)
    "<a href={}"
    payload = {
        "projectId": project_id,
        # "workItemId": 0,
        # "commentId": 0,
        "text": "",
        "user": {
            "id": secrets['hacknplan']['user']['id'],
            "username": "",
            "email": "string",
            "name": "string",
            "creationDate": "2022-06-19T17:42:07.576Z"
        },
        "workLog": {
            "projectId": 0,
            "workItemId": 0,
            "workLogId": 0,
            "user": {
                "id": 0,
                "username": "string",
                "email": "string",
                "name": "string",
                "creationDate": "2022-06-19T17:42:07.576Z"
            },
            "value": 0,
            "comment": "string",
            "creationDate": "2022-06-19T17:42:07.576Z"
        },
        "creationDate": "2022-06-19T17:42:07.576Z",
        "updateDate": "2022-06-19T17:42:07.576Z"
    }
    if title:
        embed["title"] = title.decode("utf-8")
    # end if
    if description:
        embed["description"] = description.decode("utf-8")
    # end if

    request = urllib.request.Request(
        secrets["webhookUrl"],
        json.dumps({"embeds": [embed]}).encode("utf-8"),
        {"Content-Type": "application/json", "User-Agent": "Mercurial/5.8"}
    )

    try:
        urllib.request.urlopen(request)
    except urllib.error.URLError as ex:
        ui.write(("Discord incoming hook web request failed because " + str(ex) + "\n").encode("utf-8"))
        return
    # end try
# end def
