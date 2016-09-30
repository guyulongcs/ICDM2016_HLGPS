import ConfigParser

class ConfigTool():
    @classmethod
    def read_conf(cls, folder, file):
        conf = ConfigParser.ConfigParser()
        conf.read(folder+file)
        return conf

    @classmethod
    def read_conf_file(cls, file):
        conf = ConfigParser.ConfigParser()
        conf.read(file)
        return conf
