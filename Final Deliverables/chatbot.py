from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from requests import get
from bs4 import BeautifulSoup
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.config['DEBUG']
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

bot= ChatBot('ChatBot')

trainer = ListTrainer(bot)

for file in os.listdir('C:/Users/Fantasy-PC/PycharmProjects/chatbotpyflask/data/'):

    chats = open('C:/Users/Fantasy-PC/PycharmProjects/chatbotpyflask/data/' + file, 'r').readlines()

    trainer.train(chats)


@app.route("/")
def hello():
    return render_template('chat.html')

@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/ask",  methods=['GET', 'POST'])
def ask():

    message = str(request.form['messageText'])

    bot_response = bot.get_response(message)

    print(bot_response)

    while True:

        if bot_response.confidence > 0.1:

            bot_response = str(bot_response)      
            print(bot_response)
            return jsonify({'status':'OK','answer':bot_response})
 
        elif message == ("bye") or  message == ("exit"):

            bot_response='Hope to see you soon' + '<a href="http://127.0.0.1:5000/UserHome">Exit</a>'


            print(bot_response)
            return jsonify({'status':'OK','answer':bot_response})

            break



        elif message.lower() == ("tv"):

            bot_response='<a href="http://127.0.0.1:5000/index?ptype=tv">ViewProduct</a>'


            print(bot_response)
            return jsonify({'status':'OK','answer':bot_response})

            break


        else:
        
            try:
                url  = "https://en.wikipedia.org/wiki/"+ message
                page = get(url).text
                soup = BeautifulSoup(page,"html.parser")
                p    = soup.find_all("p")
                return jsonify({'status':'OK','answer':p[1].text})



            except IndexError as error:

                bot_response = 'Sorry i have no idea about that.'
            
                print(bot_response)
                return jsonify({'status':'OK','answer':bot_response})




    #return render_template("index.html")

def exxxx():
    return render_template("index.html")
    #pass

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)