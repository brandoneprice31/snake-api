import os

class Config:

    def __init__(self):
        self.env = 'development' if self.isDev(self.getEnvVar('ENV')) else self.getEnvVar('ENV')
        self.dbURI = 'mongodb://localhost:27017/' if self.isDev(self.env) else self.getEnvVar('DB_URI')
        self.dbName = 'snake'

    def getEnvVar(self, key):
        if key in os.environ:
            return os.environ[key]
        return None

    def isDev(self, var):
        return var != 'testing' and var != 'production'

    def isTesting(self):
        return self.env == 'testing'

    def isProd(self):
        return self.env == 'production'
