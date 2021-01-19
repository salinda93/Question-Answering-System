from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
from flask_wtf import Form, RecaptchaField
from wtforms import TextField, HiddenField, ValidationError, RadioField, BooleanField, SubmitField
from wtforms.validators import Required
import re
import gevent.monkey
from gevent.pywsgi import WSGIServer
gevent.monkey.patch_all()

from give_answer import answer_question
import unicodedata
import wolframalpha
import wikipedia

class ExampleForm(Form):
    question = TextField('', description='', validators=[Required()])
    submit_button = SubmitField('Go')


def create_app(configfile=None):
    app = Flask(__name__)
    AppConfig(app, configfile)
    Bootstrap(app)


    app.config['SECRET_KEY']= 'ffedg0890489574'


    @app.route('/', methods=('GET', 'POST'))
    def index():
        if request.method == 'POST':
            try:
                question = request.form['question']
            except e:
                print("key error")
                print ("I got a KeyError - reason %s") % str(e)
            except:
                print ("I got another exception, but I should re-raise")
                raise


            print(question)
            answer = answer_question(question)
            print ("answer: "),answer
            answer=re.sub('([(].*?[)])',"",answer)

            return render_template('answer.html', answer=answer, question=question)

        form = ExampleForm()
        return render_template('index.html', form=form)



    return app

# create main callable
app = create_app()

if __name__ == '__main__':
    http_server = WSGIServer(('127.0.0.1', 9191), app)
    print("starting server on port 9191")
    http_server.serve_forever()
    
