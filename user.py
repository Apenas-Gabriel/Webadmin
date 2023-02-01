from dbconsult import dbGenerate
import hashlib

class User:

    def __init__(self):
	    self.db = dbGenerate()

    def registerUser(self, user, email, password, ip):
        if user and email and password:
            status = self.db.registerUser(user, email, hashlib.md5(password.encode()).hexdigest(), ip)
            if status == True:
                self.user = user
                self.password = hashlib.md5(password.encode()).hexdigest()
            return status

    def loginUser(self, user, password):
        if user and password:
            status = self.db.loginUser(user, hashlib.md5(password.encode()).hexdigest())
            if status == True:
                self.user = user
                self.password = hashlib.md5(password.encode()).hexdigest()
            return status

    def getTokenInfo(self, user, game):
        token = self.db.getLicenseInfos(user, game)
        return token

    def createLicense(self, user, game):
        db.generateLicense(user, game)
    
    def checkLicenseStatus(self):
        return self.db.isLicenseValid()

    def returnUserLogin(self):
        if self.user:
            return self.user
        else:
            return False

    def savePayment(self, user, pid, pmethod,status):
        self.db.registerPayment(user, pid, pmethod,status)