from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message
import ipdb

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    
    if request.method == 'GET':
        # ipdb.set_trace()
        all_message = Message.query.order_by(Message.create_at).all()
        all_message_dict = [m.to_dict() for m in all_message]
        response = make_response(all_message_dict, 200)

        return response

    elif request.method == 'POST':
        new_message = Message(
            body = request.get_json()['body'],
            username = request.get_json()['username']
        )

        db.session.add(new_message)
        db.session.commit()

        response = make_response(new_message.to_dict(), 201)
    
        return response

@app.route('/messages/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):

    selected_entry = Message.query.filter_by(id = id).one()

    if request.method == 'GET':
        return make_response(selected_entry.to_dict(), 200)

    elif request.method == 'PATCH':
        data = request.get_json()
        for attr in data:
            setattr(selected_entry, attr, data[attr])

        db.session.add(selected_entry)
        db.session.commit()

        response = make_response(selected_entry.to_dict(), 201)

        return response

    # elif request.method == 'DELTE':


    # return 'Good Morning'

if __name__ == '__main__':
    app.run(port=5555)
