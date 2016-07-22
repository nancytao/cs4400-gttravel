from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('Login.html')

@app.route('/Register.html/', methods=["GET","POST"])
def register():
    try:
        form = RegistrationForm(request.form)

        if request.method == "POST" and form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            c, conn = connection()

            x = c.execute("SELECT * FROM USERS WHERE username = (%s)", (thwart(username)))
            y = c.execute("SELECT * FROM USERS WHERE email = (%s)", (thwart(email)))

            if int(x) > 0:
                flash("Username taken")
                return render_template('Register.html', form=form)
            elif int(y) > 0:
                flash("Email previously used")
                return render_template('Register.html', form=form)
            else:
                c.execute("INSERT INTO users (username, password, email, tracking) VALUES (%s, %s, %s, %s)",
                         (thwart(username), thwart(password), thwart(email), thwart("/introduction-to-python-programming/")))

                conn.commit()
                flash("Thanks for registering!")
                c.close()
                conn.close()
                gc.collect()

                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('dashboard'))
        return render_template("Register.html", form=form)

    except Exception as e:
        return(str(e))

if __name__ == '__main__':
    app.run()
