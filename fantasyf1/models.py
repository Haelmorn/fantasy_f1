from datetime import datetime
from fantasyf1 import db, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """User class for db
    
    Builds an User class, can be used in any SQL-like database
    
    Extends:
        db.Model
        UserMixin
    
    Variables:
        __tablename__ {str} -- name of table, necessary for PostgeSQL
        id {int} -- ID
        username {string} -- Username for the user
        email {string} -- Email for the user
        image_file {string} -- Image file access route for the user
        password {string} -- Hashed password
        posts {string} -- Back reference to all posts by user
        team {string} -- Back refernece to user's team
    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    team = db.relationship('Team', backref='head', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}','{self.image_file}')"

    def get_reset_token(self, expires_sec=1800):
        """Creates reset token for current user
        
        [description]
        
        Keyword Arguments:
            expires_sec {number} -- Time in which the token will expire (default: {1800})
        
        Returns:
            string -- The token, decoded to utf-8
        """
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        
        return User.query.get(user_id)


    

class Post(db.Model):
    """[summary]
    Creates Post model for the database
    [description]
    
    Extends:
        db.Model
    
    Variables:
        __tablename__ {str} -- table name for PostgreSQL
        id int -- Post id
        title string -- Post title
        date_posted string -- When the post was added
        content string -- Post content
        user_id type -- Foreign key, refers to User model by id
    """
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Team(db.Model):
    """[summary]
    Creates Team model for the database
    [description]
    
    Extends:
        db.Model
    
    Variables:
        __tablename__ {str} -- table name for PostgreSQL
        id {int} -- Team id
        name {str} -- Team name
        primary_driver {str} -- Team's primary driver
        secondary_driver {str} -- Team's secondary driver
        team {str} -- Team's name
        points {str} -- Team's current points
        user_id {int} -- Foreign key, refers to User table id field
    """
    __tablename__ = 'team'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    primary_driver = db.Column(db.String(100), nullable=False)
    secondary_driver = db.Column(db.String(100), nullable=False)
    team = db.Column(db.String(100), nullable=False)
    points = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)

    def __repr__(self):
        return f"Team('{self.name}', '{self.primary_driver}', '{self.secondary_driver}', '{self.team}', '{self.points}')"
