from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisKeyIsASectretThatCantBeSharedWithAnyoneExceptTheAuthorizedReader'

# connect the project to a database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///garden.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


if __name__ == "__main__":
    from views.beds import beds_blueprint
    from views.current_plants import current_plants
    from views.plants import plants
    app.register_blueprint(beds_blueprint)
    app.register_blueprint(current_plants)
    app.register_blueprint(plants)
    app.run(host='0.0.0.0', port=5000, debug=True)
