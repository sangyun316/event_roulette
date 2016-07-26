from system.core.controller import *

class Events(Controller):
    def __init__(self, action):
        super(Events, self).__init__(action)
        self.load_model('Event')
        self.db = self._app.db

    def index(self):
        return self.load_view('index.html')

    def register(self):
        user_info = {
            'name': request.form['name'],
            'email': request.form['email'],
            'password': request.form['password'],
            'confirm_pw': request.form['confirm_pw']
        }
        register_status = self.models['Registration'].register_user(user_info)
        if register_status['status'] == False:
            for message in register_status['errors']:
                flash(message)
            return redirect('/')
        else:
            session['name'] = request.form['name']
            return redirect('/success')

    def login(self):
        user_info = {
            'email': request.form['email'],
            'password': request.form['password']
        }
        user = self.models['Registration'].login_validation(user_info)
        if user:
            session['name'] = user[0]['name']
            return redirect('/success')
        else:
            flash('Email or password is incorrect. Please log-in again!')
            return redirect('/')

    def success(self):
        return self.load_view('register.html')

    def logout(self):
        session.clear()
        return redirect('/')

