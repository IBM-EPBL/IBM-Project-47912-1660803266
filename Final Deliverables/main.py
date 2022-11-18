from flask import Flask, render_template, flash, request,session

import mysql.connector
from werkzeug.utils import secure_filename

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from requests import get
from bs4 import BeautifulSoup
import os
from flask import Flask, render_template, request, jsonify
import datetime
import re

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

bot = ChatBot('ChatBot')

trainer = ListTrainer(bot)

for file in os.listdir('C:/Users/ELCOT/Desktop/project/OnlineShoppingChat/OnlineShoppingChat/data/'):
    chats = open('C:/Users/ELCOT/Desktop/project/OnlineShoppingChat/OnlineShoppingChat/data/' + file, 'r').readlines()

    trainer.train(chats)


@app.route("/")
def homepage():

    return render_template('index.html')


@app.route("/AdminLogin")
def AdminLogin():

    return render_template('AdminLogin.html')

@app.route("/NewUser")
def NewUser():

    return render_template('NewUser.html')
@app.route("/UserLogin")
def UserLogin():

    return render_template('UserLogin.html')



@app.route("/hello")
def hello():
    ss=jsonify({'status': 'OK', 'answer': "Hai"})

    return render_template('chat.html', data=ss)





@app.route("/ask", methods=['GET', 'POST'])
def ask():
    message = str(request.form['messageText'])
    bott=''
    bott1 = ''
    sresult1=''

    bot_response = bot.get_response(message)

    print(bot_response)

    if( message != 'hi'):
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1pynewshop')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * from protb where ProductType like '%" + message + "%' or  ProductTitle like '%" + message + "%'")
        data = cursor.fetchone()

        if data is None:

            # data1 = 'Username or Password is wrong'
            print("no data")
            # return render_template('goback.html', data=data1)
            # bot_response="No Data"

            # return jsonify({'status': 'OK', 'answer': bot_response})



        else:

            conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='1pynewshop')
            #search Result

            cur1 = conn1.cursor()
            cur1.execute(
                "SELECT *  from protb where ProductType like '%" + message + "%' or  ProductTitle like '%" + message + "%'  LIMIT 10")
            data = cur1.fetchall()

            for item in data:
                sresult = ' <p class="price">  Your Search Result </p> <br>'


                ss = '<a href="http://127.0.0.1:5000/fullInfo?pid='
                ss1 = item[0] + '">ViewProduct</a> <br>'

                # iimage1 = '<img src='+ item[9] +'width="100" height="100"><br>'
                # str
                iimage1 = '<img src="' + item[9] + '" width="150" height="200"><br>'
                number = item[0]

                pricelist =str( int(str(number)[:3]))

                price = '<p class="price">Price ' + pricelist + '</p> <br>'

                bot_response = ss + ss1 + iimage1 + price

                if (bott == ""):
                    bott = bot_response
                else:
                    bott = bott + bot_response

                print(bott)

                #search Result


            conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='1pynewshop')
            # search Result

            cur1 = conn1.cursor()
            cur1.execute(
                "SELECT *  from reviewtb where ProductType like '%" + message + "%' and Result='postive' ")
            data1 = cur1.fetchall()

            for item1 in data1:
                sresult1 = ' <p class="price">  	Recommend Products Details </p> <br>'

                ss1 = '<a href="http://127.0.0.1:5000/fullInfo?pid='
                ss11 = item1[1] + '">ViewProduct</a> <br>'

                # iimage1 = '<img src='+ item[9] +'width="100" height="100"><br>'
                # str
                iimage11 = '<img src="' + item1[5] + '" width="150" height="200"><br>'
                number1 = item1[1]

                pricelist1 = str(int(str(number1)[:3]))

                price1 = '<p class="price">Price ' + pricelist1 + '</p> <br>'

                bot_response1 = ss1 + ss11 + iimage11 + price1

                if (bott1 == ""):
                    bott1 = bot_response1
                else:
                    bott1 = bott1 + bot_response1

                print(bott1)

                # search Result








            return jsonify({'status': 'OK', 'answer':sresult+bott + sresult1+bott1 })

    elif (message =='hi' or message =='hai' ):

        conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='1pynewshop')

        cur1 = conn1.cursor()
        cur1.execute(
            "SELECT  distinct  ProductType  from protb")
        data = cur1.fetchall()

        for item in data:

            ss1 = ' <p class="price">  Hello </p> <br>'

            ss = ' <p class="price">  Please Enter Your Product to this list </p> <br>'

           # ss2 = '<a href="http://127.0.0.1:5000/ask?messageText='
            #ss12 = item[0] + '">Search Product</a> <br>'
            #cc = +ss2+ss12


            ptype = '<p class="price">' + item[0] + '</p> <br>'

            bot_response = ptype

            if (bott == ""):
                bott = bot_response
            else:
                bott = bott + bot_response

            print(bott)





        return jsonify({'status': 'OK', 'answer':ss1+ ss+bott})










    while True:




        if bot_response.confidence > 0.1:

            bot_response = str(bot_response)
            print(bot_response)
            return jsonify({'status': 'OK', 'answer': bot_response})

        elif message == ("bye") or message == ("exit"):

            bot_response = 'Hope to see you soon' + '<a href="http://127.0.0.1:5000/UserHome">Exit</a>'

            print(bot_response)
            return jsonify({'status': 'OK', 'answer': bot_response})

            break



        else:

            try:
                url = "https://en.wikipedia.org/wiki/" + message
                page = get(url).text
                soup = BeautifulSoup(page, "html.parser")
                p = soup.find_all("p")
                return jsonify({'status': 'OK', 'answer': p[1].text})



            except IndexError as error:

                bot_response = 'Sorry i have no idea about that.'

                print(bot_response)
                return jsonify({'status': 'OK', 'answer': bot_response})

    # return render_template("index.html")

@app.route("/viewproduct")
def viewproduct():
    searc = request.args.get('searc')

    conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='1pynewshop')

    cur1 = conn1.cursor()
    cur1.execute(
        "SELECT * from protb where ProductType like '%" + searc + "%' or  ProductName like '%" + searc + "%'")
    data = cur1.fetchall()
    data1=''
    return render_template('ViewProduct.html', data=data,data1=data1)





@app.route("/AdminHome")
def AdminHome():
    conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='1pynewshop')

    cur1 = conn1.cursor()
    cur1.execute("SELECT * FROM regtb ")
    data = cur1.fetchall()
    # return 'file register successfully'
    # return render_template('order.html', data=data)

    return render_template('AdminHome.html', data=data)


@app.route("/NewProduct")
def NewProduct():
    conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='1pynewshop')

    cur1 = conn1.cursor()
    cur1.execute("SELECT DISTINCT ProductType FROM protb ")
    data = cur1.fetchall()


    return render_template('NewProduct.html',data=data)

@app.route("/ProductInfo")
def ProductInfo():
    conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='1pynewshop')

    cur1 = conn1.cursor()
    cur1.execute("SELECT * FROM protb ")
    data = cur1.fetchall()

    return render_template('ProductInfo.html',data=data)

@app.route("/SalesInfo")
def SalesInfo():

    return render_template('SalesInfo.html')


@app.route("/FeedBackInfo")
def FeedBackInfo():

    return render_template('FeedBackInfo.html')






@app.route("/RNewUser", methods=['GET', 'POST'])
def RNewUser():
    if request.method == 'POST':

        name1 = request.form['name']
        gender1 = request.form['gender']
        Age = request.form['age']
        email = request.form['email']
        address = request.form['address']
        pnumber = request.form['phone']
        uname = request.form['uname']
        password = request.form['psw']


        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1pynewshop')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO regtb VALUES ('" + name1 + "','" + gender1 + "','" + Age + "','" + email + "','" + pnumber + "','" + address + "','" + uname + "','" + password + "')")
        conn.commit()
        conn.close()
        # return 'file register successfully'


    return render_template('userlogin.html')

@app.route("/RNewProduct", methods=['GET', 'POST'])
def RNewProduct():
    if request.method == 'POST':


        file = request.files['fileupload']
        file.save("static/upload/" + file.filename)


        ProductId =request.form['pid']
        Gender =request.form['gender']
        Category =request.form['cat']
        SubCategory=request.form['subcat']
        ProductType=request.form['ptype']
        Colour=request.form['color']
        Usage=request.form['usage']
        ProductTitle=request.form['ptitle']

        Image= file.filename
        ImageURL="static/upload/" + file.filename



        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1pynewshop')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO protb VALUES ('"+ ProductId +"','" + Gender + "','" + Category + "','" + SubCategory + "','" + ProductType + "','" + Colour + "','"+
            Usage +"','"+ProductTitle+"','"+ Image +"','"+ ImageURL +"')")
        conn.commit()
        conn.close()
        # return 'file register successfully'


    return render_template('NewProduct.html')



@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    error = None
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['uname'] = request.form['uname']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1pynewshop')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where UserName='" + username + "' and password='" + password + "'")
        data = cursor.fetchone()

        if data is None:

            data1 = 'Username or Password is wrong'
            return render_template('goback.html', data=data1)



        else:
            conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='1pynewshop')

            cur1 = conn1.cursor()
            cur1.execute("SELECT * FROM regtb where username='"+ session['uname'] +"' ")
            data = cur1.fetchall()
            # return 'file register successfully'
            # return render_template('order.html', data=data)


            return render_template('UserHome.html',data=data)

@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    error = None
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['uname'] = request.form['uname']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1pynewshop')
        cursor = conn.cursor()
        cursor.execute("SELECT * from admintb where UserName='" + username + "' and password='" + password + "'")
        data = cursor.fetchone()

        if data is None:
            data1 = 'Username or Password is wrong'
            return render_template('goback.html', data=data1)

        else:

            conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='1pynewshop')

            cur1 = conn1.cursor()
            cur1.execute("SELECT * FROM regtb  ")
            data = cur1.fetchall()
            # return 'file register successfully'
            #return render_template('order.html', data=data)

            return render_template('AdminHome.html',data=data)



@app.route("/Remove", methods=['GET'])
def Remove():


    pid = request.args.get('id')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1pynewshop')
    cursor = conn.cursor()
    cursor.execute("Delete from protb  where id='"+ pid +"'")
    conn.commit()
    conn.close()
    conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='1pynewshop')
    # cursor = conn.cursor()
    cur1 = conn1.cursor()
    cur1.execute("SELECT * FROM protb ")
    data = cur1.fetchall()
    # return 'file register successfully'
    return render_template('ProductInfo.html',data=data)


@app.route("/fullInfo")
def fullInfo():
    pid = request.args.get('pid')
    session['pid'] = pid

    rat1 = ''
    rat2 = ''
    rat3 = ''
    rat4 = ''
    rat5 = ''

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1pynewshop')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT  ROUND(AVG(Rate), 1) as numRating FROM reviewtb WHERE ProductId  ='" + pid + "' ")
    data2 = cursor.fetchone()
    print(data2[0])
    if data2 is None:
        avgrat = 0
    else:
        if data2[0] == 'None':
            avgrat = 0
            if (int(avgrat) == 1):
                rat1 = 'checked'
            if (int(avgrat) == 2):
                rat2 = 'checked'
            if (int(avgrat) == 3):
                rat3 = 'checked'
            if (int(avgrat) == 4):
                rat4 = 'checked'
            if (int(avgrat) == 5):
                rat5 = 'checked'
        else:
            avgrat = data2[0]

            if (avgrat == 1):
                rat1 = 'checked'
            if (avgrat == 2):
                rat2 = 'checked'
            if (avgrat == 3):
                rat3 = 'checked'
            if (avgrat == 4):
                rat4 = 'checked'
            if (avgrat == 5):
                rat5 = 'checked'



    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1pynewshop')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT  count(Rate)  as numRating FROM reviewtb WHERE ProductId  ='" + pid + "' ")
    data3 = cursor.fetchone()
    if data3:
        avgrat = data3[0]

    else:
        return 'Incorrect username / password !'

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1pynewshop')
    cur = conn.cursor()
    cur.execute("SELECT UserName,Review FROM reviewtb where ProductId='" + pid + "' ")
    reviewdata = cur.fetchall()




    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1pynewshop')
    cur = conn.cursor()
    cur.execute("SELECT * FROM protb where ProductId='" + pid + "' ")
    data1 = cur.fetchall()

    number = pid

    pricelist = str(int(str(number)[:3]))


    return render_template('ProductFullInfo.html',data=data1,pricelist=pricelist ,avgrat=avgrat, rat1=rat1, rat2=rat2, rat3=rat3, rat4=rat4, rat5=rat5,reviewdata=reviewdata )

@app.route("/Book", methods=['GET', 'POST'])
def Book():
    if request.method == 'POST':


        uname = session['uname']
        pid = session['pid']

        qty = request.form['qty']

        ctype = request.form['ctype']
        cardno = request.form['cardno']
        cvno = request.form['cvno']


        Bookingid = ''
        ProductName =''
        UserName= uname
        Mobile=''
        Email=''
        Qty = qty
        Amount=''


        CardType = ctype
        CardNo = cardno
        CvNo = cvno
        date = datetime.datetime.now().strftime('%d-%b-%Y')

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1pynewshop')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM protb where  ProductId='" + pid + "'")
        data = cursor.fetchone()

        if data:
            ProductName = data[7]
            price = str(int(str(data[0])[:3]))


            Amount= float(price) *  float(Qty)

            print(Amount)


        else:
            return 'Incorrect username / password !'

        string = ProductName
        new_string = re.sub(r"[^a-zA-Z0-9]", "", string)
        print(new_string)



        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1pynewshop')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM  regtb where  UserName='" + uname + "'")
        data = cursor.fetchone()

        if data:
            Mobile = data[4]
            Email= data[3]


        else:
            return 'Incorrect username / password !'

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1pynewshop')
        cursor = conn.cursor()
        cursor.execute("SELECT  count(*) as count  FROM  booktb  ")
        data = cursor.fetchone()

        if data:
            count = data[0]

            if count == 0:
                count =1;
            else:
                count+=1




        else:
            return 'Incorrect username / password !'
        print(count)

        Bookingid="BOOKID00" + str(count)



        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1pynewshop')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO booktb VALUES ('','" + Bookingid + "','"+ pid +"','" + new_string + "','" + uname + "','" + Mobile + "','" + Email + "','" + str(Qty) + "','" + str(Amount) + "','"+ str(CardType) +"','"+ str(CardNo) +"','"+ str(CvNo) +"','"+ str(date) +"')")
        conn.commit()
        conn.close()
        # return 'file register successfully'

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1pynewshop')
        cur = conn.cursor()
        cur.execute("SELECT * FROM booktb where  UserName= '" + uname + "' ")
        data = cur.fetchall()

    return render_template('UOrderInfo.html', data=data)



@app.route("/UOrderInfo")
def UOrderInfo():

    uname = session['uname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1pynewshop')
    cur = conn.cursor()
    cur.execute("SELECT * FROM booktb where  UserName= '" + uname + "' ")
    data = cur.fetchall()


    return render_template('UOrderInfo.html', data=data)


@app.route("/UserHome")
def UserHome():

    uname = session['uname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1pynewshop')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where  UserName= '" + uname + "' ")
    data = cur.fetchall()


    return render_template('UserHome.html', data=data)

@app.route("/Review")
def Review():
    pid = request.args.get('pid')
    session['rpid'] = pid

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1pynewshop')
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM  protb where  ProductId='" + pid + "'")
    data = cursor.fetchone()

    if data:
        pname = data[7]



    else:
        return 'Incorrect username / password !'

    return render_template('NewReview.html', pname=pname)


@app.route("/ureview",methods = ['GET', 'POST'])
def ureview():

    if request.method == 'POST':


        uname = session['uname']
        pid = session['rpid']

        pname = request.form['pname']

        feedback = request.form['feed']

        star = request.form['star']

        ProductId=''
        ProductType=''
        ProductName=''
        Price=''
        Image=''
        UserName=uname
        Rate=star
        Review=feedback
        Result=''

        if (int(star) > 2):
            Result = 'postive'
        else:
            Result = 'nagative'







        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1pynewshop')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM  protb where  ProductId='" + pid + "'")
        data = cursor.fetchone()
        if data:

            ProductId = data[0]
            ProductType=data[4]
            ProductName = data[7]
            Price = str(int(str(data[0])[:3]))
            Image= data[9]


        else:
            return 'Product Info Not Avalible..!'

        string = ProductName
        new_string = re.sub(r"[^a-zA-Z0-9]", "", string)
        print(new_string)


        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1pynewshop')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO  reviewtb VALUES ('','" + str(ProductId) + "','" + ProductType + "','" + str(
                new_string) + "','" + str(
                Price) + "','" + str(Image) + "','" + str(UserName) + "','" + str(Rate) + "','" + str(
                Review) + "','" + str(Result) + "')")
        conn.commit()
        conn.close()


        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1pynewshop')
        cur = conn.cursor()
        cur.execute("SELECT * FROM reviewtb where  UserName= '" + uname + "' ")
        data = cur.fetchall()

        return render_template('UReviewInfo.html', data=data)



@app.route("/UReviewInfo")
def UReviewInfo():

    uname = session['uname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1pynewshop')
    cur = conn.cursor()
    cur.execute("SELECT * FROM reviewtb where  UserName= '" + uname + "' ")
    data = cur.fetchall()


    return render_template('UReviewInfo.html', data=data)



@app.route("/AReviewInfo")
def AReviewInfo():



    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1pynewshop')
    cur = conn.cursor()
    cur.execute("SELECT * FROM reviewtb  ")
    data = cur.fetchall()


    return render_template('AReviewInfo.html', data=data)

@app.route("/ASalesInfo")
def ASalesInfo():



    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1pynewshop')
    cur = conn.cursor()
    cur.execute("SELECT * FROM booktb  ")
    data = cur.fetchall()


    return render_template('ASalesInfo.html', data=data)

def main():
    app.run(debug=True, use_reloader=True)

if __name__ == '__main__':
    main()