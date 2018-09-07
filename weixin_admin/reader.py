import configparser


class LocalProperties:
    parser = configparser.ConfigParser()
    parser.read("local.properties")

    def get_app_id(self):
        return self.parser["WX_INFO"]["AppID"]

    def get_app_secret(self):
        return self.parser["WX_INFO"]["AppSecret"]

    def get_mysql_host(self):
        return self.parser["MYSQL"]["HOST"]

    def get_mysql_db_name(self):
        return self.parser["MYSQL"]["DB_NAME"]

    def get_mysql_user(self):
        return self.parser["MYSQL"]["USER"]

    def get_mysql_port(self):
        return self.parser["MYSQL"]["PORT"]

    def get_mysql_passwd(self):
        return self.parser["MYSQL"]["PASSWD"]
