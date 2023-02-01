import mysql.connector as mysql
from uuid import uuid4
from flask import request, redirect, url_for, render_template, Flask, g, session, make_response, flash
import datetime
from dateutil import parser

class dbGenerate:

    def __init__(self):
        self.db = mysql.connect(
            host="127.0.0.1",
            user="debian-sys-maint",
            password="CSRfD16MAIHCMtS8",
            database="webadmin"
        )
        self.cursor = self.db.cursor()

    def registerUser(self, user, email, password, ip):
            self.cursor.execute("SELECT * FROM users WHERE Login = %s", (user,))
            check = self.cursor.fetchone()
            if check == None:
                self.cursor.execute("INSERT INTO users (Login,Password,Email,IP) VALUES (%s,%s,%s,%s)", (user, password, email, ip))
                self.db.commit()
                self.user = user
                self.password = password
                self.email = email
                self.ip = ip
                return True
            else:
                return False

    def loginUser(self, user, password):
        self.cursor.execute("SELECT * FROM users WHERE Login = %s AND Password = %s", (user, password))
        check = self.cursor.fetchone()
        if check[0] == user and check[1] == password:
            self.user = user
            self.password = password
            self.email = check[2]
            self.ip = check[3]
            print(check[3])
            return True
        else:
            return False

    def getLicenseInfos(self, user, game):
        self.cursor.execute("SELECT * FROM license WHERE login = %s AND game = %s", (user, game))
        usersInfos = self.cursor.fetchone()
        if not usersInfos:
            return False
        else:
            return usersInfos

    def generateLicense(self, user, game):
        license = self.getLicenseInfos(user, game)
        print(license)
        if not license:
            token = uuid4()
            current_time = datetime.datetime.now()
            end_data = current_time + datetime.timedelta(days=30)
            self.cursor.execute("INSERT INTO license (login,token,date,enddate,game,ip) VALUES (%s,%s,%s,%s,%s,%s)", (user, str(token), str(current_time), str(end_data), game, session['IP']))
            self.db.commit()
        else:
            return False

    def isLicenseValid(self, user, game):
        license = self.getLicenseInfos(user, game)
        if parser.parse(license[3]) > datetime.datetime.now():
            return True
        else:
            return False

    def registerPayment(self, user, pid, pmethod,status):
        self.cursor.execute("INSERT INTO payment (Login,payment_id,payment_method,status,date) VALUES (%s,%s,%s,%s,%s)", (user, str(pid), str(pmethod), str(status), datetime.datetime.now()))
