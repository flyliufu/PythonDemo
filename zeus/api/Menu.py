import requests
import json

from zeus.api.Token import get_token
from constants import URL


class Menu(object):

    def create_menu(self):
        json_str = requests.post(
            URL.BASE_URL % "menu/create?access_token=" + get_token(),
            data=json.dumps({
                "button": [
                    {
                        "type": "click",
                        "name": "MY歌曲",
                        "key": "V1001_TODAY_MUSIC"
                    },
                    {
                        "name": "菜单",
                        "sub_button": [
                            {
                                "type": "view",
                                "name": "搜索",
                                "url": "http://www.soso.com/"
                            },
                            {
                                "type": "click",
                                "name": "赞一下我们",
                                "key": "V1001_GOOD"
                            }
                        ]
                    }
                ]
            }, ensure_ascii=False).encode("utf-8")
        ).content.decode("utf-8")
        return json_str
