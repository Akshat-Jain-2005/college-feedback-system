from flask import Flask
from flask_cors import CORS
from models import db
from views import routes_bp

app = Flask(__name__)
app.config.from_object('config.Config')  
CORS(app)
db.init_app(app)
app.register_blueprint(routes_bp)

if __name__ == '__main__':
    with app.app_context():           
        db.create_all()              
    app.run(debug=True)
