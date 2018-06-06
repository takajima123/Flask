from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))


@app.route('/')
def hello_world():
    return 'this is my Crud sql to json output\n' \
           'Requirements:\n' \
           ' * Postman \n \n' \
           'To run my commands \n\n' \
           'Read all in Database\n' \
           '127.0.0.1/user \n ' \
           '(use GET in Postman)\n \n' \
           'Read specific user\n' \
           '127.0.0.0/user/<public_id> \n' \
           '(use GET in Postman) \n' \
           '(copy the public id in the json file)\n \n' \
           'Create user\n' \
           '127.0.0.0/user \n' \
           '(use POST in Postman)' \
           '    *   Click body \n' \
           '    *   Click raw (radiobutton) \n' \
           '    *   Change Text to Json(application/json) \n' \
           '    *   Copy my code bellow concatenate each word with apostrophe \n' \
           '    *   {name:name_of_new_user, password:new_user_password}; \n\n' \
           'Update user\n' \
           '127.0.0.0/user \n' \
           '1.(use READ specific user)\n' \
           '2.(use POST in Postman)' \
           '    *   Click body \n' \
           '    *   Click raw (radiobutton) \n' \
           '    *   Change Text to Json(application/json) \n' \
           '    *   Copy my code bellow concatenate each word with apostrophe \n' \
           '    *   {name:Update_user, password:Update_password}; \n\n' \
           'Delete user \n' \
           '1.(use Read specific user)\n' \
           '2.(change function to DELETE and send)\n' \
           'Thank you!'


@app.route('/user', methods=['POST'])
def create():
    data = request.get_json()
    new_user = User(name=data['name'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'Message': ' New User Created'})


@app.route('/user', methods=['GET'])
def getAll():
    users = User.query.all()
    output = []

    for user in users:
        user_data = {}
        user_data['id'] = user.id
        user_data['name'] = user.name
        user_data['password'] = user.password
        output.append(user_data)

    return jsonify({'users': output})


@app.route('/user/<id>', methods=['GET'])
def getbyId(id):
    user = User.query.filter_by(id=id).first()

    if not user:
        return jsonify({'Message': 'No user found!'})

    user_data = {}
    user_data['name'] = user.name
    user_data['password'] = user.password
    return jsonify({'user': user_data})


@app.route('/user/<id>', methods=['PUT'])
def update(id):
    user = User.query.filter_by(id=id).first()

    if not user:
        return jsonify({'Message': 'No user found!'})

    data = request.get_json()

    user.name = data['name']
    user.password = data['password']
    db.session.commit()

    return jsonify({'Message': 'User updated'})


@app.route('/user/<id>', methods=['DELETE'])
def delete(id):
    user = User.query.filter_by(id=id).first()

    if not user:
        return jsonify({'Message': 'No user found'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'Data Deleted'})


if __name__ == '__main__':
    app.run(debug=True)
