from flask_login import LoginManager
from vtu.models import Users
from vtu import app



# initialize LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# load user from user id
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))



# runnin' the app 
if __name__ == '__main__':
    app.run(debug=True, port=6000)