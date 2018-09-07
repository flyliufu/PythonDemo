import configparser


class LocalProperties:
    parser = configparser.ConfigParser()
    parser.read("local.properties")

    def get_app_id(self):
        return self.parser["WX_INFO"]["AppID"]

    def get_app_secret(self):
        return self.parser["WX_INFO"]["AppSecret"]
