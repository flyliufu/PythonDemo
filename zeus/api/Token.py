import requests
import logging
import json

from django.core.cache import caches
from weixin_admin.reader import LocalProperties
from constants import URL

logger = logging.getLogger("django.request")
pro = LocalProperties()


def get_token(force_clear=False):
    var = caches['default']
    token = var.get("access_token")
    if token is None or force_clear:
        json_str = requests.get(URL.BASE_URL % "token", {
            "grant_type": "client_credential",
            "appid": pro.get_app_id(),
            "secret": pro.get_app_secret(),
        }).content.decode("utf-8")
        token = json.loads(json_str)
        var.set("access_token", token, timeout=token["expires_in"])

    return token["access_token"]
