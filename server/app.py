# server/app.py
from flask import Flask, session, jsonify
from flask_migrate import Migrate
from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200 Successfully cleared session data'}, 200

@app.route('/articles/<int:id>')
def show_article(id):
    # Initialize page_views if it doesn't exist
    session['page_views'] = session.get('page_views', 0)
    
    # Increment the page view count
    session['page_views'] += 1
    
    # Check if the user has exceeded the view limit
    if session['page_views'] > 3:
        return {'message': 'Maximum pageview limit reached'}, 401
    
    # If within limit, return the article data
    article = Article.query.get_or_404(id)
    return jsonify(article.to_dict())

if __name__ == '__main__':
    app.run(port=5555)