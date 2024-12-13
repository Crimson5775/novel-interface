from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, User, UserPermission, Novel
from functools import wraps

admin = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if user.role != 'admin':
            return jsonify({'error': 'Admin privileges required'}), 403
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/translators', methods=['GET'])
@jwt_required()
@admin_required
def get_translators():
    translators = User.query.filter_by(role='translator').all()
    return jsonify({
        'translators': [{
            'id': t.id,
            'username': t.username,
            'email': t.email,
            'is_active': t.is_active,
            'created_at': t.created_at.isoformat()
        } for t in translators]
    }), 200

@admin.route('/translators', methods=['POST'])
@jwt_required()
@admin_required
def add_translator():
    data = request.get_json()

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400

    translator = User(
        username=data['username'],
        email=data['email'],
        role='translator'
    )
    translator.set_password(data['password'])

    permissions = UserPermission(
        user_id=translator.id,
        can_add_novels=True,
        can_edit_all_novels=data.get('can_edit_all_novels', False),
        can_delete_novels=data.get('can_delete_novels', False)
    )

    db.session.add(translator)
    db.session.add(permissions)
    db.session.commit()

    return jsonify({'message': 'Translator added successfully'}), 201

@admin.route('/translators/<int:translator_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_translator(translator_id):
    translator = User.query.get_or_404(translator_id)
    data = request.get_json()

    if 'is_active' in data:
        translator.is_active = data['is_active']

    permissions = UserPermission.query.filter_by(user_id=translator_id).first()
    if permissions:
        if 'can_edit_all_novels' in data:
            permissions.can_edit_all_novels = data['can_edit_all_novels']
        if 'can_delete_novels' in data:
            permissions.can_delete_novels = data['can_delete_novels']

    db.session.commit()
    return jsonify({'message': 'Translator updated successfully'}), 200

@admin.route('/translators/<int:translator_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_translator(translator_id):
    translator = User.query.get_or_404(translator_id)
    
    # Reassign or handle novels by this translator
    novels = Novel.query.filter_by(author_id=translator_id).all()
    for novel in novels:
        novel.status = 'dropped'
    
    db.session.delete(translator)
    db.session.commit()
    
    return jsonify({'message': 'Translator deleted successfully'}), 200

@admin.route('/users', methods=['GET'])
@jwt_required()
@admin_required
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    users = User.query.filter_by(role='reader').paginate(page=page, per_page=per_page)
    
    return jsonify({
        'users': [{
            'id': u.id,
            'username': u.username,
            'email': u.email,
            'is_active': u.is_active,
            'created_at': u.created_at.isoformat()
        } for u in users.items],
        'total': users.total,
        'pages': users.pages,
        'current_page': users.page
    }), 200

@admin.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    if 'is_active' in data:
        user.is_active = data['is_active']

    db.session.commit()
    return jsonify({'message': 'User updated successfully'}), 200

@admin.route('/stats', methods=['GET'])
@jwt_required()
@admin_required
def get_stats():
    total_users = User.query.filter_by(role='reader').count()
    total_translators = User.query.filter_by(role='translator').count()
    total_novels = Novel.query.count()
    
    return jsonify({
        'total_users': total_users,
        'total_translators': total_translators,
        'total_novels': total_novels
    }), 200
