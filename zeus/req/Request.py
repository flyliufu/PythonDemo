import requests
from django.core.cache import caches
from zeus.util.reader import LocalProperties
import json

BASE_URL = "https://api.weixin.qq.com/cgi-bin/%s"

pro = LocalProperties()


def get_token():
    var = caches['default']
    token = var.get("access_token")
    if token is None:
        json_str = requests.get(BASE_URL % "token", {
            "grant_type": "client_credential",
            "appid": pro.get_app_id(),
            "secret": pro.get_app_secret(),
        }).content.decode("utf-8")
        token = json.loads(json_str)
        var.set("access_token", token, timeout=token["expires_in"])

    return token["access_token"]
