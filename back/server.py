import json
import secrets
from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from server_helper.api_manager import Manager

key = secrets.token_urlsafe(16)

app = Flask(__name__)
app.config['SECRET_KEY'] = key
socket = SocketIO(app)
manager = Manager()


@app.route('/login', methods=['POST'])
def login():
    response = {'data': 'Error'}

    try:
        data = request.get_json()

        username = data['user']
        password = data['password']
        is_student = data['is_student']

        if manager.check_user(username, password, is_student):
            response['data'] = key
            status_code = 200

        else:
            status_code = 401

    except json.JSONDecodeError:
        status_code = 415

    except KeyError:
        status_code = 400

    except TypeError:
        status_code = 400

    return jsonify(response), status_code


@app.route('/avaliadores', methods=['POST'])
def register_valuer():
    response = {'data': 'Error'}

    try:
        data = request.get_json()

        username = data['user']
        password = data['password']

        if manager.add_valuer(username, password):
            response['data'] = key
            status_code = 200

        else:
            status_code = 401

    except json.JSONDecodeError:
        status_code = 415

    except KeyError:
        status_code = 400

    except TypeError:
        status_code = 400

    return jsonify(response), status_code


@app.route('/avaliadores/avaliar', methods=['POST'])
def rate_team():
    response = {'data': 'Error'}

    try:
        data = request.get_json()

        if not check_key(data['key']):
            status_code = 403

        else:
            valuer_name = data['valuer']
            team_name = data['team_name']
            software = data['software']
            pitch = data['pitch']
            innovation = data['innovation']
            team = data['team']

            if manager.rate_team(valuer_name, team_name, software, pitch, innovation, team):
                response['data'] = 'Team rated'
                status_code = 200

            else:
                status_code = 401

    except json.JSONDecodeError:
        status_code = 415

    except KeyError:
        status_code = 400

    except TypeError:
        status_code = 400

    return jsonify(response), status_code


@app.route('/equipes', methods=['GET'])
def get_teams():
    response = {'data': 'Error'}

    try:
        data = request.get_json()

        if not check_key(data['key']):
            status_code = 403

        else:
            response['data'] = manager.get_teams()
            status_code = 200

    except json.JSONDecodeError:
        status_code = 415

    except KeyError:
        status_code = 400

    except TypeError:
        status_code = 400

    return jsonify(response), status_code


@app.route('/equipes/<team_name>', methods=['GET'])
def get_team(team_name):
    response = {'data': 'Error'}

    try:
        data = request.get_json()

        if not check_key(data['key']):
            status_code = 403

        else:
            team = manager.get_team(team_name)
            if team is None:
                status_code = 404
            else:
                response['data'] = team
                status_code = 200

    except json.JSONDecodeError:
        status_code = 415

    except KeyError:
        status_code = 400

    except TypeError:
        status_code = 400

    return jsonify(response), status_code


@app.route('/equipes/equipe', methods=['POST'])
def create_team():
    response = {'data': 'Error'}

    try:
        data = request.get_json()

        if not check_key(data['key']):
            status_code = 403

        else:
            team_name = data['team_name']
            admin_name = data['username']

            if manager.add_team(team_name, admin_name):
                response['data'] = 'Team created'
                status_code = 200
                socket.emit('teams_update', manager.get_teams(), broadcast=True)

            else:
                status_code = 401

    except json.JSONDecodeError:
        status_code = 415

    except KeyError:
        status_code = 400

    except TypeError:
        status_code = 400

    return jsonify(response), status_code


@app.route('/equipes/equipe', methods=['DELETE'])
def delete_team():
    response = {'data': 'Error'}

    try:
        data = request.get_json()

        if not check_key(data['key']):
            status_code = 403

        else:
            team_name = data['team_name']
            admin_name = data['username']

            if manager.delete_team(team_name, admin_name):
                response['data'] = 'Team deleted'
                status_code = 200
                socket.emit('teams_update', manager.get_teams(), broadcast=True)

            else:
                status_code = 401

    except json.JSONDecodeError:
        status_code = 415

    except KeyError:
        status_code = 400

    except TypeError:
        status_code = 400

    return jsonify(response), status_code


@app.route('/equipes/equipe/team', methods=['PUT'])
def edit_team_add_members():
    response = {'data': 'Error'}

    try:
        data = request.get_json()

        if not check_key(data['key']):
            status_code = 403

        else:
            team_name = data['team_name']
            admin = data['username']
            members = data['members']

            if manager.add_members(team_name, admin, members):
                response['data'] = 'Members added'
                status_code = 200
                socket.emit('teams_update', manager.get_teams(), broadcast=True)

            else:
                status_code = 401

    except json.JSONDecodeError:
        status_code = 415

    except KeyError:
        status_code = 400

    except TypeError:
        status_code = 400

    return jsonify(response), status_code


@app.route('/equipes/equipe/team', methods=['DELETE'])
def edit_team_remove_members():
    response = {'data': 'Error'}

    try:
        data = request.get_json()

        if not check_key(data['key']):
            status_code = 403

        else:
            team_name = data['team_name']
            admin = data['username']
            members = data['members']

            if manager.delete_members(team_name, admin, members):
                response['data'] = 'Members removed'
                status_code = 200
                socket.emit('teams_update', manager.get_teams(), broadcast=True)

            else:
                status_code = 401

    except json.JSONDecodeError:
        status_code = 415

    except KeyError:
        status_code = 400

    except TypeError:
        status_code = 400

    return jsonify(response), status_code


@app.route('/equipes/equipe/me', methods=['PUT'])
def enter_team():
    response = {'data': 'Error'}

    try:
        data = request.get_json()

        if not check_key(data['key']):
            status_code = 403

        else:
            team_name = data['team_name']
            username = data['username']

            if manager.add_member(team_name, username):
                response['data'] = 'User added'
                status_code = 200
                socket.emit('teams_update', manager.get_teams(), broadcast=True)

            else:
                status_code = 401

    except json.JSONDecodeError:
        status_code = 415

    except KeyError:
        status_code = 400

    except TypeError:
        status_code = 400

    return jsonify(response), status_code


@app.route('/equipes/equipe/me', methods=['DELETE'])
def leave_team():
    response = {'data': 'Error'}

    try:
        data = request.get_json()

        if not check_key(data['key']):
            status_code = 403

        else:
            team_name = data['team_name']
            username = data['username']

            if manager.delete_member(team_name, username):
                response['data'] = 'User removed'
                status_code = 200
                socket.emit('teams_update', manager.get_teams(), broadcast=True)

            else:
                status_code = 401

    except json.JSONDecodeError:
        status_code = 415

    except KeyError:
        status_code = 400

    except TypeError:
        status_code = 400

    return jsonify(response), status_code


@app.route('/equipes/rank', methods=['GET'])
def teams_rank():
    response = {'data': 'Error'}

    try:
        data = request.get_json()

        if not check_key(data['key']):
            status_code = 403

        else:
            response['data'] = manager.get_teams_rank()
            status_code = 200

    except json.JSONDecodeError:
        status_code = 415

    except KeyError:
        status_code = 400

    except TypeError:
        status_code = 400

    return jsonify(response), status_code


@app.route('/certificates', methods=['GET'])
def get_certificates():
    response = {'data': 'Error'}

    try:
        data = request.get_json()

        if not check_key(data['key']):
            status_code = 403

        else:
            valuer_name = data['valuer']

            certificates = manager.get_certificates(valuer_name)

            if not certificates:
                status_code = 404

            else:
                response['data'] = certificates
                status_code = 200

    except json.JSONDecodeError:
        status_code = 415

    except KeyError:
        status_code = 400

    except TypeError:
        status_code = 400

    return jsonify(response), status_code


@app.route('/certificates/<student_name>', methods=['GET'])
def get_certificate(student_name):
    response = {'data': 'Error'}

    try:
        data = request.get_json()

        if not check_key(data['key']):
            status_code = 403

        else:
            valuer_name = data['valuer']

            certificate = manager.get_certificate(valuer_name, student_name)

            if certificate is None:
                status_code = 404

            else:
                response['data'] = certificate
                status_code = 200

    except json.JSONDecodeError:
        status_code = 415

    except KeyError:
        status_code = 400

    except TypeError:
        status_code = 400

    return jsonify(response), status_code


@app.route('/certificates/<student_name>', methods=['POST'])
def generate_certificate(student_name):
    response = {'data': 'Error'}

    try:
        data = request.get_json()

        if not check_key(data['key']):
            status_code = 403

        else:
            valuer_name = data['valuer']

            if not manager.generate_certificate(valuer_name, student_name):
                status_code = 401

            else:
                response['data'] = 'Certificate created'
                status_code = 200

    except json.JSONDecodeError:
        status_code = 415

    except KeyError:
        status_code = 400

    except TypeError:
        status_code = 400

    return jsonify(response), status_code


def check_key(external_key):
    if len(external_key) != len(key):
        return False

    for external_letter, internal_letter in zip(external_key, key):
        if external_letter != internal_letter:
            return False

    return True


if __name__ == '__main__':
    socket.run(app, host='127.0.0.1', port='8080')
