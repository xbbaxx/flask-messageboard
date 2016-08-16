#coding:utf-8

from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Required
import os 
from datetime import datetime




basedir = os.path.abspath(os.path.dirname(__file__))

#实例化一个应用
msgapp = Flask(__name__)

#应用相关配置
msgapp.config['SECRET_KEY'] = 'hello word'
msgapp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'msgapp.sqlite')
msgapp.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(msgapp)
manager = Manager(msgapp)


#定义应用模型
class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(64))
    text = db.Column(db.Text)
    create_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Message %r>' % self.text


#定义应用表单
class MessageForm(Form):
    name = StringField(u'姓名', validators=[Required()])
    text = TextAreaField(u'内容', validators=[Required()])
    submit = SubmitField(u'提交')
    



@msgapp.route('/msgapp', methods=['GET', 'POST'])
def Index():
    form = MessageForm()
    messages = Message.query.order_by(Message.create_time.desc())[:5]
    if form.validate_on_submit():
        message = Message(author=form.name.data,text=form.text.data)
        db.session.add(message)
        return redirect(url_for('Index'))
    return render_template('index.html', form=form, messages=messages)


if __name__ == '__main__':
    manager.run()

