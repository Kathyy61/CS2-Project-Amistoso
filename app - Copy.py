from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "secret"

data_list = [] 

@app.route('/')
def index():
    
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        new_entry = {
            "username": request.form.get('u'),
            "password": request.form.get('p'),
            "name": request.form.get('n'),
            "age": request.form.get('a'),
            "address": request.form.get('addr'),
            "quals": request.form.get('q')
        }
        data_list.append(new_entry)
        return redirect(url_for('login'))
    return render_template('register.html')

