from MySQLdb import IntegrityError
from flask import jsonify, request
from src.common.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR
from src.common.utils.password_hasher import password_hasher, verify_password
from src.modules.user_module.models import UserModel
from . import user_bp
from ...database.database_instance import db
from flask_jwt_extended import jwt_required, create_refresh_token, create_access_token

@user_bp.get('/')
def getUsers():
	return {"msg": "hello user module"}


@user_bp.route('/create', methods=['POST'])
@jwt_required()
def handle_create_user():
	try:
		data = request.get_json()
		hashing = password_hasher(data['password'])
		new_user = UserModel(username=data['username'], password=hashing)
		db.session.add(new_user)
		db.session.commit()
	except KeyError as e:
		return jsonify({'message': f'create user failed due to missing {e} key'}), HTTP_400_BAD_REQUEST
	except IntegrityError:
		return jsonify({'message': f'create user failed due to duplicate email or username'}), HTTP_400_BAD_REQUEST
	except Exception:
		return jsonify({'message': 'create user failed'}), HTTP_500_INTERNAL_SERVER_ERROR

	return jsonify({'message': 'User created successfully'}), HTTP_201_CREATED


@user_bp.post('/login')
def login():
	username: str = request.json.get('username', '')
	password: str = request.json.get('password', '')
	user: UserModel = UserModel.query.filter_by(username=username).first()
	print(user)
	if user:
		is_pass_correct = verify_password(user.password, password)
		if is_pass_correct:
			refresh_token: str = create_refresh_token(
				identity=user.id, 
				)
			access_token: str = create_access_token(identity=user.id)

			return jsonify({
				'user': {
					'refresh_token': refresh_token,
					'access_token': access_token,
					'username': user.username,
				}
			}), HTTP_200_OK
	return jsonify({
		'error': 'Wrrong credential'
	}), HTTP_401_UNAUTHORIZED

