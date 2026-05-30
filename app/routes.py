from flask import Blueprint, request, jsonify
from . import db
from .models import RobotData

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/data', methods=['POST'])
def collect_data():
    payload = request.get_json(force=True, silent=True)

    if not payload:
        return jsonify({'error': 'Corps de requête JSON invalide ou manquant'}), 400

    bot = payload.get('bot')
    persons = payload.get('persons')
    datetime_val = payload.get('datetime')

    if bot is None or persons is None or datetime_val is None:
        return jsonify({'error': 'Champs requis manquants: bot, persons, datetime'}), 400

    if not isinstance(bot, dict):
        return jsonify({'error': 'Le champ "bot" doit être un objet JSON'}), 400

    if not isinstance(persons, (list, dict)):
        return jsonify({'error': 'Le champ "persons" doit être un tableau ou objet JSON'}), 400

    entry = RobotData(bot=bot, persons=persons, datetime=str(datetime_val))
    db.session.add(entry)
    db.session.commit()

    return jsonify({'message': 'Données enregistrées avec succès', 'id': entry.id}), 201
