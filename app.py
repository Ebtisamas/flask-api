from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:1086211925@localhost/mydb'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# postgresql+psycopg2
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name
        }

@app.route("/", methods=['GET','POST'])
def add_user_form():
    if request.method == 'POST':
        name=request.form.get('name')
        try:
            user=User(name=name)
            db.session.add(user)
            db.session.commit()
            return "User added. user id={}".format(user.id)
        except Exception as e:
            return(str(e))
    return render_template("index.html")

@app.route("/users/all", methods=['GET'])
def get_all():
    try:
        users=User.query.all()
        return  jsonify([e.serialize() for e in users])
    except Exception as e:
	    return(str(e))

@app.route("/users/<id>", methods=['GET'])
def get_by_id(id):
    try:
        user=User.query.filter_by(id=id).first()
        return jsonify(user.serialize())
    except Exception as e:
	    return(str(e))
    
@app.route("/users/<id>", methods=['PUT'])
def update_user(id):
    print('Hi')

    user_name = request.json['name']
    User.query.filter_by(id=id).update({'name': user_name})
    db.session.commit()
    return 'updated', 200


# **
@app.route("/users/<id>", methods=['DELETE'])
def delete_user(id):
    User.query.filter_by(id=id).delete()
    db.session.commit()
    return 'deleted', 200

if __name__ == '__main__':
    app.run(port=8080)