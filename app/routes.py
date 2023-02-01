from app import app
from user import User
from flask import request, redirect, url_for, render_template, Flask, g, session, make_response, flash
import requests
import mercadopago
import json

sdk = mercadopago.SDK("APP_USR-4934646089222264-122923-bf1294b3a3453e088f504b453e64031a-1273205957")
#main

@app.route('/', methods=['GET','POST'])
def index():
    global userclass
    userclass = User()
    if session.get('USER'):
        return render_template("index.html", user = session['USER'])
    else:
        return render_template("index.html", user = None)

#login

@app.route('/login', methods=['GET','POST'])
def login():
    return render_template("login.html")

@app.route('/generateUser', methods=['POST'])
def generateUser():
    user, email, password, ip = request.form['text'], request.form['email'], request.form['password'], request.form['ip']
    status = userclass.registerUser(user, email, password, ip)
    if len(user) > 0 or len(password) > 0 or len(email) > 0:
        if status:
           session['USER'] = user
           session['IP'] = ip
           return redirect(url_for('index'))
        else:
           return redirect(url_for('login'), code = 304)
    else:
       return redirect(url_for('login'), code = 304)

@app.route('/loginUser', methods=['POST'])
def loginUser():
    user, password = request.form['text'], request.form['password']
    if len(user) > 0 or len(password) > 0:
       status = userclass.loginUser(user, password)
       if status:
          session['USER'] = user
          return redirect(url_for('index'))
       else:
            return redirect(url_for('login'), code = 304)
    else:
      return redirect(url_for('login'), code = 304)

#Payment

@app.route('/shop', methods=['GET','POST'])
def shop():
    if session.get('USER'):
        return render_template("shop.html", user = session['USER'])
    else:
        return render_template("shop.html", user = None)

@app.route('/payment/<name>', methods=['GET','POST'])
def payment(name):
    if session.get('USER'):
            license = userclass.getTokenInfo(session.get('USER'), name)
            if not license:
                if name == "FiveM":
                    preference_data = {
                    # o "purpose": "wallet_purchase", permite apenas pagamentos logados
                    # para permitir pagamentos como guest, você pode omitir essa propriedade
                        "items": [
                            {
                                "title": "FiveM",
                                "quantity": 1,
                                "unit_price": 35
                            }
                        ],
                        "back_urls": {
                            "success": "https://web-admin.tech/approved/FiveM",
                            "failure": "https://web-admin.tech",
                            "pending": "https://web-admin.tech"
                            },
                        "auto_return": "approved"
                    }

                    preference_response = sdk.preference().create(preference_data)
                    preference = preference_response["response"]
                    return redirect(preference_response["response"]["init_point"])
                elif name == "MTA":
                    preference_data = {
                    # o "purpose": "wallet_purchase", permite apenas pagamentos logados
                    # para permitir pagamentos como guest, você pode omitir essa propriedade
                        "items": [
                            {
                                "title": "MTA",
                                "quantity": 1,
                                "unit_price": 1
                            }
                        ],
                        "back_urls": {
                            "success": "http://localhost:5000/approved/MTA",
                            "failure": "http://www.failure.com",
                            "pending": "http://www.pending.com"
                            },
                        "auto_return": "approved"
                    }

                    preference_response = sdk.preference().create(preference_data)
                    preference = preference_response["response"]
                    return redirect(preference_response["response"]["init_point"])
            else:
                return redirect(url_for('index'))
    else:
        return redirect(url_for('login'), code = 302)

@app.route('/approved/<name>', methods=['GET','POST'])
def approved(name):
    if name == "FiveM":
        userclass.savePayment(session["USER"], request.args.get('payment_id'), request.args.get('payment_type'),request.args.get('status'))
        userclass.createLicense(session["USER"], name)
        return redirect(url_for('index'))

#clientarea

@app.route('/clientarea/selectLicense', methods=['GET','POST'])
def selectLicense():
    if session["USER"]:
        licensemta = userclass.getTokenInfo(session.get('USER'), "MTA")
        licensefivem = userclass.getTokenInfo(session.get('USER'), "FiveM")
        if not licensemta:
            mtastatus = None
            mtatoken = None
            mtadate = None
            mtaendtime = None
        else:
            mtastatus = True
            mtatoken = licensemta[1]
            mtadate = licensemta[2]
            mtaendtime = licensemta[3]
        
        if not licensefivem:
            fivemstatus = None
            fivemtoken = None
            fivemdate = None
            fivemendtime = None
            fivemIP = None
        else:
            fivemstatus = True
            fivemtoken = licensefivem[1]
            fivemdate = licensefivem[2]
            fivemendtime = licensefivem[3]
            fivemIP = licensefivem[5]
            session["TOKEN"] = licensefivem[1]
            session["IP"] = licensefivem[5]

        return render_template('licenseselect.html', fivem=fivemstatus, fivemtoken=fivemtoken, fivemdate=fivemdate, fivemendtime=fivemendtime, fivemIP=fivemIP, mta=mtastatus, mtatoken=mtatoken, mtadate=mtadate, mtaendtime=mtaendtime)

@app.route('/clientarea/<name>', methods=['GET','POST'])
def clientarea(name):
    if name == "FiveM":
        infos = requests.get('http://'+session["IP"]+'/web_admin/players/'+session["TOKEN"])
        print(infos)
        infos = infos.text
        infos = json.loads(infos)[0]
        print(infos)
        maxids = requests.get('http://'+session["IP"]+'/web_admin/players/maxids/'+session["TOKEN"])
        maxids = maxids.text
        maxids = json.loads(maxids)[0]
        print(maxids)
        info = requests.get('http://'+session["IP"]+'/web_admin/players/getInfos/'+session["TOKEN"])
        info = info.text
        info = json.loads(info)
        money = "{:,}".format(info[0])
        vip = info[1]

        vehicles = requests.get('http://'+session["IP"]+'/web_admin/players/returnVehicles/'+session["TOKEN"])
        vehicles = vehicles.text
        vehicles = json.loads(vehicles)

        items = requests.get('http://'+session["IP"]+'/web_admin/players/returnItems/'+session["TOKEN"])
        items = items.text
        items = json.loads(items)

        groups = requests.get('http://'+session["IP"]+'/web_admin/players/returnGroups/'+session["TOKEN"])
        groups = groups.text
        groups = json.loads(groups)
        return render_template('clientarea.html', user=session["USER"], infos = infos, players = len(infos), maxids = maxids, economy = money, vips = vip, cars = vehicles[0], items = items[0], groups = groups[0])

@app.route('/ungroup/<id>/<group>', methods=['GET','POST'])
def ungroup(id, group):
    return requests.get("http://"+session["IP"]+"/web_admin/players/ungroup/"+id+"/"+group+"/"+session["TOKEN"])

@app.route('/ban/<id>', methods=['GET','POST'])
def ban(id):
    requests.get("http://"+session["IP"]+"/web_admin/players/ban/"+id+"/"+session["TOKEN"])
    return redirect(url_for("clientarea", name="FiveM"))

@app.route('/kick/<id>', methods=['GET','POST'])
def kick(id):
    requests.get("http://"+session["IP"]+"/web_admin/players/kick/"+id+"/"+session["TOKEN"])
    return redirect(url_for("clientarea", name="FiveM"))

@app.route('/setMoney/<id>/<value>', methods=['GET','POST'])
def setMoney(id, value):
    requests.get("http://"+session["IP"]+"/web_admin/players/setMoney/"+id+"/"+value+"/"+session["TOKEN"])
    return redirect(url_for("clientarea", name="FiveM"))

@app.route('/setGroup/<id>/<group>', methods=['GET','POST'])
def setGroup(id, group):
    requests.get("http://"+session["IP"]+"/web_admin/players/setGroup/"+id+"/"+group+"/"+session["TOKEN"])
    return redirect(url_for("clientarea", name="FiveM"))

@app.route('/setVehicle/<id>/<veh>', methods=['GET','POST'])
def setVehicle(id, veh):
    requests.get("http://"+session["IP"]+"/web_admin/players/setVehicle/"+id+"/"+veh+"/"+session["TOKEN"])
    return redirect(url_for("clientarea", name="FiveM"))

@app.route('/setItem/<id>/<item>', methods=['GET','POST'])
def setItem(id, item):
    requests.get("http://"+session["IP"]+"/web_admin/players/setItem/"+id+"/"+item+"/"+session["TOKEN"])
    return redirect(url_for("clientarea", name="FiveM"))
