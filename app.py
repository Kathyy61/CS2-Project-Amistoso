from flask import Flask, render_template_string, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "secret"


data_list = []  
current_user = {"type": None, "index": None}  


style = '''
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
:root { --primary: #6366f1; --secondary: #a855f7; --bg: #0f172a; --card-bg: rgba(255, 255, 255, 0.05); }
body { font-family: 'Plus Jakarta Sans', sans-serif; background-color: var(--bg); background-image: radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.15) 0px, transparent 50%), radial-gradient(at 100% 100%, rgba(168, 85, 247, 0.15) 0px, transparent 50%); margin: 0; min-height: 100vh; color: #f8fafc; display: flex; align-items: center; justify-content: center; }
.container { width: 100%; max-width: 850px; padding: 40px; margin: 20px; background: var(--card-bg); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 40px; }
.header { text-align: center; margin-bottom: 30px; }
.header h1 { font-size: 2.2rem; font-weight: 800; background: linear-gradient(to right, #818cf8, #c084fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin:0; }
.input-group { margin-bottom: 15px; }
label { display: block; margin-bottom: 5px; font-size: 0.75rem; font-weight: 700; color: #818cf8; text-transform: uppercase; }
input, textarea { width: 100%; padding: 14px; border-radius: 12px; background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1); color: white; box-sizing: border-box; }
.btn-main { background: linear-gradient(135deg, var(--primary), var(--secondary)); color: white; border: none; padding: 16px; width: 100%; border-radius: 14px; font-weight: 700; cursor: pointer; text-decoration:none; display:block; text-align:center; }
.grid-container { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 20px; }
.profile-card { background: rgba(255, 255, 255, 0.03); padding: 25px; border-radius: 24px; border: 1px solid rgba(255, 255, 255, 0.05); }
.info-label { font-size: 0.65rem; color: #64748b; font-weight: 800; text-transform: uppercase; margin-top: 10px; }
.pass-tag { color: #f43f5e; font-weight: bold; background: rgba(244, 63, 94, 0.1); padding: 2px 6px; border-radius: 5px; }
.error-msg { color: #f43f5e; text-align: center; margin-bottom: 15px; font-weight: 600; }
</style>
'''


index_html = style + '''
<div class="container" style="max-width: 400px; text-align: center;">
    <div class="header"><h1>Job Portal</h1></div>
    <a href="/login" class="btn-main" style="margin-bottom:15px;">Login</a>
    <a href="/register" class="btn-main" style="background:transparent; border:1px solid var(--primary);">Register</a>
</div>
'''

register_html = style + '''
<div class="container" style="max-width: 400px;">
    <div class="header"><h1>Register</h1></div>
    {% with m = get_flashed_messages() %}{% if m %}<div class="error-msg">{{ m[0] }}</div>{% endif %}{% endwith %}
    <form method="POST">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
            <div class="input-group"><label>Username</label><input type="text" name="u" required></div>
            <div class="input-group"><label>Password</label><input type="password" name="p" required></div>
        </div>
        <div class="input-group"><label>Full Name</label><input type="text" name="n" required></div>
        <div style="display: grid; grid-template-columns: 100px 1fr; gap: 15px;">
            <div class="input-group"><label>Age</label><input type="number" name="a" required></div>
            <div class="input-group"><label>Address</label><input type="text" name="addr" required></div>
        </div>
        <div class="input-group"><label>Qualifications</label><textarea name="q" rows="2" required></textarea></div>
        <button class="btn-main">Submit</button>
    </form>
    <center><a href="/" style="color:#64748b; display:block; margin-top:15px; text-decoration:none;">← Back</a></center>
</div>
'''

login_html = style + '''
<div class="container" style="max-width: 400px;">
    <div class="header"><h1>Login</h1></div>
    {% with m = get_flashed_messages() %}{% if m %}<div class="error-msg">{{ m[0] }}</div>{% endif %}{% endwith %}
    <form method="POST">
        <div class="input-group"><label>Username</label><input type="text" name="user" required></div>
        <div class="input-group"><label>Password</label><input type="password" name="pass" required></div>
        <button class="btn-main">Login</button>
    </form>
    <center><a href="/" style="color:#64748b; display:block; margin-top:15px; text-decoration:none;">← Back</a></center>
</div>
'''

applicant_view_html = style + '''
<div class="container" style="max-width: 500px; text-align: center;">
    <div class="header"><h1>Welcome, {{user.name}}!</h1></div>
    <div class="profile-card" style="text-align: left;">
        <div class="info-label">Username</div><div style="color:var(--primary);">@{{user.username}}</div>
        <div class="info-label">Password</div><div class="pass-tag">{{user.password}}</div>
        <div class="info-label">Full Name</div><div>{{user.name}}</div>
        <div class="info-label">Age</div><div>{{user.age}}</div>
        <div class="info-label">Address</div><div>{{user.address}}</div>
        <div class="info-label">Qualifications</div><div style="font-style:italic; margin-top:5px;">"{{user.quals}}"</div>
    </div>

    <a href="/edit/{{user_index}}" class="btn-main" style="margin-top:10px;">Edit Profile</a>
    <a href="/logout" class="btn-main" style="margin-top:20px; background:rgba(255,255,255,0.1);">Logout</a>
</div>
'''

edit_html = style + '''
<div class="container">
    <div class="header"><h1>Edit Profile</h1></div>
    {% with m = get_flashed_messages() %}{% if m %}<div class="error-msg">{{ m[0] }}</div>{% endif %}{% endwith %}
    <form method="POST">
        <div class="input-group"><label>Username</label><input type="text" name="u" value="{{user.username}}" required></div>
        <div class="input-group"><label>Password</label><input type="text" name="p" value="{{user.password}}" required></div>
        <div class="input-group"><label>Full Name</label><input type="text" name="n" value="{{user.name}}" required></div>
        <div class="input-group"><label>Age</label><input type="number" name="a" value="{{user.age}}" required></div>
        <div class="input-group"><label>Address</label><input type="text" name="addr" value="{{user.address}}" required></div>
        <div class="input-group"><label>Qualifications</label><textarea name="q" required>{{user.quals}}</textarea></div>
        <button class="btn-main">Update</button>
    </form>
</div>
'''


admin_html = style + '''
<div class="container">
    <div class="header" style="display:flex; justify-content:space-between; align-items:center;">
        <h1 style="margin:0;">Admin Dashboard</h1>
        <a href="/logout" style="color:#f43f5e; text-decoration:none; font-weight:bold;">Logout</a>
    </div>
    <div class="grid-container" style="margin-top: 20px;">
        {% for x in records %}
        <div class="profile-card">
            <div style="color:var(--primary); font-size:0.8rem; font-weight:bold;">@{{x.username}}</div>
            <h3 style="margin:5px 0;">{{x.name}}</h3>
            <div class="info-label">Password</div><div class="pass-tag">{{x.password}}</div>
            <div class="info-label">Age & Address</div><div>{{x.age}} | {{x.address}}</div>
            <div class="info-label">Qualifications</div><div style="font-size:0.85rem;">{{x.quals}}</div>

            <!-- Admin Edit/Delete Buttons -->
            <a href="/admin-edit/{{loop.index0}}" class="btn-main" style="margin-top:5px; background:rgba(99,102,241,0.2);">Edit</a>
            <a href="/admin-delete/{{loop.index0}}" 
               class="btn-main" 
               style="margin-top:5px; background:rgba(244,63,94,0.2);" 
               onclick="return confirm('Are you sure you want to delete this user?');">
               Delete
            </a>
        </div>
        {% endfor %}
    </div>
</div>
'''


@app.route('/')
def index():
    return render_template_string(index_html)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('u')
        if any(u['username'] == username for u in data_list):
            flash("Username already exists")
            return render_template_string(register_html)
        data_list.append({
            "username": username,
            "password": request.form.get('p'),
            "name": request.form.get('n'),
            "age": request.form.get('a'),
            "address": request.form.get('addr'),
            "quals": request.form.get('q')
        })
        flash("Account created successfully!")
        return redirect(url_for('login'))
    return render_template_string(register_html)

@app.route('/login', methods=['GET','POST'])
def login():
    global current_user
    if request.method == 'POST':
        u = request.form.get('user')
        p = request.form.get('pass')

        
        if u == "admin" and p == "admin123":
            current_user["type"] = "admin"
            current_user["index"] = None
            return redirect(url_for('admin_page'))

        
        for index, user in enumerate(data_list):
            if user['username'] == u and user['password'] == p:
                current_user["type"] = "user"
                current_user["index"] = index
                return redirect(url_for('applicant_profile', user_index=index))
        flash("Invalid Username or Password")
    return render_template_string(login_html)

@app.route('/profile/<int:user_index>')
def applicant_profile(user_index):
    if current_user["type"] != "user" or current_user["index"] != user_index:
        flash("Access denied")
        return redirect(url_for('login'))
    user = data_list[user_index]
    return render_template_string(applicant_view_html, user=user, user_index=user_index)

@app.route('/edit/<int:user_index>', methods=['GET','POST'])
def edit(user_index):
    if current_user["type"] != "user" or current_user["index"] != user_index:
        flash("Access denied")
        return redirect(url_for('login'))
    user = data_list[user_index]
    if request.method == 'POST':
        new_username = request.form.get('u')
        if any(u['username'] == new_username and u != user for u in data_list):
            flash("Username already exists")
            return render_template_string(edit_html, user=user)
        user.update({
            "username": new_username,
            "password": request.form.get('p'),
            "name": request.form.get('n'),
            "age": request.form.get('a'),
            "address": request.form.get('addr'),
            "quals": request.form.get('q')
        })
        flash("Profile updated successfully!")
        
        return render_template_string(applicant_view_html, user=user, user_index=user_index)
    return render_template_string(edit_html, user=user)


@app.route('/admin-dashboard')
def admin_page():
    if current_user["type"] != "admin":
        flash("Access denied")
        return redirect(url_for('login'))
    return render_template_string(admin_html, records=data_list)

@app.route('/admin-edit/<int:user_index>', methods=['GET','POST'])
def admin_edit(user_index):
    if current_user["type"] != "admin":
        flash("Access denied")
        return redirect(url_for('login'))
    user = data_list[user_index]
    if request.method == 'POST':
        new_username = request.form.get('u')
        if any(u['username'] == new_username and u != user for u in data_list):
            flash("Username already exists")
            return render_template_string(edit_html, user=user)
        user.update({
            "username": new_username,
            "password": request.form.get('p'),
            "name": request.form.get('n'),
            "age": request.form.get('a'),
            "address": request.form.get('addr'),
            "quals": request.form.get('q')
        })
        flash("Profile updated successfully!")
        return redirect(url_for('admin_page'))
    return render_template_string(edit_html, user=user)

@app.route('/admin-delete/<int:user_index>')
def admin_delete(user_index):
    if current_user["type"] != "admin":
        flash("Access denied")
        return redirect(url_for('login'))
    data_list.pop(user_index)
    flash("User deleted successfully!")
    return redirect(url_for('admin_page'))


@app.route('/logout')
def logout():
    current_user["type"] = None
    current_user["index"] = None
    return redirect(url_for('login'))

if (__name__) == "_main_":
    app.run(debug=True)