from flask import Flask,render_template,redirect,url_for,request
from flask_bootstrap import Bootstrap
from forms import sign_up,login
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from flask_mail import Mail,Message
from flask_login import LoginManager,login_user,UserMixin,login_required
import requests
import random


app=Flask(__name__)
app.config['SECRET_KEY']='1234567890987654321'
Bootstrap(app)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///quiz.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False



app.config['MAIL_SERVER']='smtp.mail.yahoo.com'
app.config['MAIL_USERNAME']='mohamedalisaifudeen1@yahoo.com'
app.config['MAIL_PASSWORD']='opionphuapgtbfyj'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
app.config['MAIL_PORT']=465
mail=Mail(app)

login_manager=LoginManager()
login_manager.init_app(app)




database=SQLAlchemy(app)

class User(database.Model,UserMixin):
    id=database.Column(database.Integer,primary_key=True,unique=True)
    email=database.Column(database.String(250))
    name=database.Column(database.String(200))
    password=database.Column(database.String(250))
database.create_all()

class Questions(database.Model):
    id=database.Column(database.Integer,primary_key=True,unique=True)
    category=database.Column(database.String(200))
    question=database.Column(database.String(200))
    correct_ans=database.Column(database.String(200))
    incorrect=database.Column(database.String(200))
database.create_all()

#for item in range(9,28):
#    parameters = {'amount': 50,
#                  'category':item,
#                  'type':'multiple'}
#    api = requests.get(url='https://opentdb.com/api.php', params=parameters)
#    questions=api.json()
#    for item in questions['results']:
#        que=Questions(category=str(item['category']),question=str(item['question']),correct_ans=str(item['correct_answer']),incorrect=str(item['incorrect_answers']))
#        database.session.add(que)
#        database.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route("/")
def home_page():

    return render_template("index.html")


@app.route("/SignUp",methods=['Post','Get'])
def signup_page():
    form=sign_up()
    if(form.validate_on_submit()):
        user=User(email=form.username.data,name=form.name.data,password=generate_password_hash(form.password.data,method='pbkdf2:sha256',salt_length=8))
        database.session.add(user)
        database.session.commit()
        msg = Message( sender='mohamedalisaifudeen1@yahoo.com', recipients=[form.username.data])
        msg.html="<img src='static/vecteezy_.jpg'> <br><hr><h2>Thank you for choosing our website and signing up for it </h2>"
        mail.send(msg)
        return redirect(url_for('login_page'))

    return render_template("signup.html",form1=form)

@app.route("/Login",methods=['POST','GET'])
def login_page():
    form4=login()
    current_user=User.query.filter_by(email=form4.email.data).first()
    if(current_user):
        if(check_password_hash(current_user.password,form4.password.data)):
            login_user(current_user)
            return redirect(url_for("home_page"))
    return render_template("login.html",form2=form4)

@app.route("/Quizzes")
def quiz_page():
    cate={'General Knowledge':'Do you think that you have a good general knowledge try this quiz',
          'Entertainment: Books':'Do you think that you have a good  knowledge in books try this quiz',
          'Entertainment: Film':'Do you think that you have a good  knowledge in films try this quiz',
          'Entertainment: Music':'Do you think that you have a good  knowledge in music try this quiz',
          'Entertainment: Television':'Do you think that you have a good  knowledge tv try this quiz',
          'Entertainment: Video Games':'Do you think that you have a good knowledge in games try this quiz',
          'Entertainment: Board Games':'Do you think that you have a good  knowledge in board games try this quiz',
          'Science & Nature':'Do you think that you have a good knowledge in nature try this quiz',
          'Science: Computers':'Do you think that you have a good knowledge in computers try this quiz',
          'Sports':'Do you think that you have a good knowledge in sports try this quiz',
          'Geography':'Do you think that you have a good knowledge in geography try this quiz',
          'History':'Do you think that you have a good knowledge in history try this quiz',
          'Animals':'Do you think that you have a good knowledge in animals try this quiz'}
    return render_template('quiz.html',cateo=cate)

cato=''
correct=[]
wrong=[]

@app.route('/Questions/<catogery>',methods=['POST','GET'])
@login_required
def questions_page(catogery):
    correct.clear()
    specific_ques=Questions.query.filter_by(category=catogery).all()
    q_and_a=[]

    for item in specific_ques:
        q_and_a.append([item.incorrect.split(',')[0].strip("''[]'"),item.incorrect.split(',')[1].strip("[]'"),item.incorrect.split(',')[2].strip("[]'"),item.correct_ans])
        correct.append(item.correct_ans)
        wrong.append([item.incorrect.split(',')[0].strip("''[']'"),item.incorrect.split(',')[1].strip("[']'"),item.incorrect.split(',')[2].strip("[']'")])

    for j in q_and_a:
        random.shuffle(j)






    return render_template('questions.html',catt=specific_ques,q_a=q_and_a)

@app.route('/Score',methods=['GET','POST'])
def score_page():

    if request.method=='POST':
       score = 0
       for item in range(len(correct)):
           if(request.form.get(str(item))==correct[item]):
               score+=1


       return render_template('Score.html',score=score)

    return render_template('Score.html')


if(__name__=="__main__"):
    app.run(debug=True)