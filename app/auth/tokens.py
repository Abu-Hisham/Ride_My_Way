from flask import jsonify, g
from app.main import bp_main
from app.auth.authorize import basic_auth


@bp_main.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = g.current_user.get_token()
    return jsonify({'token': token})