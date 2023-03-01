from flask import jsonify, request
from src.common.constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from src.modules.problem_module.models import ProblemModel
from . import problem_bp
from ...database.database_instance import db
from flask_jwt_extended import jwt_required

@problem_bp.get('/')
def getUsers():
    return {"msg": "hello problem module"}


@problem_bp.post("/create")
def handle_create_problems():
    # payload = request.get_json().get('payload', '')
    body = request.get_json()
    try:
        new_problem = ProblemModel(
            desc=body['desc'],
            lat=body['lat'],
            lng=body['lng']
        )
        db.session.add(new_problem)
        db.session.commit()
        return jsonify({'message': 'Create Problem was successfully'}), HTTP_200_OK
    except KeyError as e:
        key_error = ['desc', 'lat', 'lng']
        if str(e)[1:-1] in key_error:
            print(f"{str(e)} key error")
        else:
            print("other key error")
        return jsonify({'message': f'create problem was failed that {str(e)[1:-1]} key error'}), HTTP_400_BAD_REQUEST
    except BaseException as e:
        print("other exception occurred")
        return jsonify({'message': 'create problem was failed'}), HTTP_400_BAD_REQUEST


@problem_bp.get("/get")
def handle_get_problems():
    problems = ProblemModel.query.all()
    data: list = []
    for problem in problems:
        data.append({
            'id': problem.id,
            'desc': problem.desc,
            'lat': problem.lat,
            'lng': problem.lng,
        })

    return jsonify({
        "msg": "get problem was successfully",
        "paylolad": data
    }), HTTP_200_OK


@problem_bp.get("/get/<int:problem_id>")
def handle_get_one_problem(problem_id: str):
    problem = ProblemModel.query.filter_by(id=problem_id).first()
    data: list = {
            'id': problem.id,
            'desc': problem.desc,
            'lat': problem.lat,
            'lng': problem.lng,
        }

    return jsonify({
        "msg": "get problem was successfully",
        "paylolad": data
    }), HTTP_200_OK




@problem_bp.route("/update/<int:building_id>", methods=['PUT', 'PATCH'])
@jwt_required()
def handle_update_building(building_id):
    problem = ProblemModel.query.filter_by(id=building_id).first()
    if not problem:
        return jsonify({'message': 'problem not found'}), HTTP_404_NOT_FOUND

    body = request.get_json()

    # Update building fields
    try:
        if request.method == 'PUT':
            problem.desc = body['desc']
            problem.lat = body['lat']
            problem.lng = body['lng']
        elif request.method == 'PATCH':
            if 'desc' in body:
                problem.desc = body['desc']
            if 'lat' in body:
                problem.lat = body['lat']
            if 'lng' in body:
                problem.lng = body['lng']
        db.session.commit()
    except KeyError as e:
        key_error = ['desc', 'lat', 'lng']
        if str(e)[1:-1] in key_error:
            return jsonify({'message': f'update problem failed - {str(e)[1:-1]} key error'}), HTTP_400_BAD_REQUEST
        else:
            return jsonify({'message': 'update problem failed - other key error'}), HTTP_400_BAD_REQUEST
    except BaseException as e:
        return jsonify({'message': 'update problem failed'}), HTTP_400_BAD_REQUEST

    return jsonify({'message': 'problem updated successfully'}), HTTP_200_OK

@problem_bp.delete("/delete/<int:problem_id>")
@jwt_required()
def handle_delete_building(problem_id):
    problem = ProblemModel.query.filter_by(id=problem_id).first()
    if not problem:
        return jsonify({'message': 'Problem not found'}), HTTP_404_NOT_FOUND
    
    try:
        db.session.delete(problem)
        db.session.commit()
    except BaseException as e:
        return jsonify({'message': 'delete problem was failed'}), HTTP_400_BAD_REQUEST

    return jsonify({'message': 'problem deleted was successfully'}), HTTP_200_OK
