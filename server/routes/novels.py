from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from ..models import db, Novel, Chapter, User, Genre, NovelGenres
import os
from datetime import datetime

novels = Blueprint('novels', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_IMAGE_EXTENSIONS']

@novels.route('/', methods=['POST'])
@jwt_required()
def create_novel():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if user.role not in ['admin', 'translator']:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.form
    cover_image = request.files.get('cover_image')
    
    if cover_image and allowed_file(cover_image.filename):
        filename = secure_filename(cover_image.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], 'covers', filename)
        cover_image.save(filepath)
    else:
        filepath = None

    novel = Novel(
        title=data['title'],
        description=data['description'],
        cover_image=filepath,
        author_id=current_user_id
    )

    # Add genres
    if 'genres' in data:
        genre_ids = data.getlist('genres')
        genres = Genre.query.filter(Genre.id.in_(genre_ids)).all()
        novel.genres.extend(genres)

    db.session.add(novel)
    db.session.commit()

    return jsonify({
        'message': 'Novel created successfully',
        'novel_id': novel.id
    }), 201

@novels.route('/<int:novel_id>/chapters', methods=['POST'])
@jwt_required()
def add_chapter(novel_id):
    current_user_id = get_jwt_identity()
    novel = Novel.query.get_or_404(novel_id)
    
    if novel.author_id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    
    chapter = Chapter(
        title=data['title'],
        content=data['content'],
        chapter_number=data['chapter_number'],
        novel_id=novel_id
    )

    db.session.add(chapter)
    db.session.commit()

    return jsonify({
        'message': 'Chapter added successfully',
        'chapter_id': chapter.id
    }), 201

@novels.route('/', methods=['GET'])
def get_novels():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    query = Novel.query
    
    # Filter by genre
    genre_id = request.args.get('genre')
    if genre_id:
        query = query.join(NovelGenres).filter(NovelGenres.genre_id == genre_id)
    
    # Filter by status
    status = request.args.get('status')
    if status:
        query = query.filter(Novel.status == status)
    
    # Sort by
    sort_by = request.args.get('sort_by', 'updated_at')
    if sort_by == 'views':
        query = query.order_by(Novel.views.desc())
    elif sort_by == 'rating':
        query = query.order_by(Novel.rating.desc())
    else:
        query = query.order_by(Novel.updated_at.desc())
    
    novels = query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'novels': [{
            'id': n.id,
            'title': n.title,
            'description': n.description,
            'cover_image': n.cover_image,
            'status': n.status,
            'views': n.views,
            'rating': n.rating,
            'author': n.author.username,
            'genres': [g.name for g in n.genres],
            'updated_at': n.updated_at.isoformat()
        } for n in novels.items],
        'total': novels.total,
        'pages': novels.pages,
        'current_page': novels.page
    }), 200

@novels.route('/<int:novel_id>', methods=['GET'])
def get_novel(novel_id):
    novel = Novel.query.get_or_404(novel_id)
    
    # Increment view count
    novel.views += 1
    db.session.commit()
    
    return jsonify({
        'id': novel.id,
        'title': novel.title,
        'description': novel.description,
        'cover_image': novel.cover_image,
        'status': novel.status,
        'views': novel.views,
        'rating': novel.rating,
        'author': novel.author.username,
        'genres': [g.name for g in novel.genres],
        'chapters': [{
            'id': c.id,
            'title': c.title,
            'chapter_number': c.chapter_number,
            'created_at': c.created_at.isoformat()
        } for c in novel.chapters.order_by(Chapter.chapter_number).all()],
        'created_at': novel.created_at.isoformat(),
        'updated_at': novel.updated_at.isoformat()
    }), 200

@novels.route('/<int:novel_id>', methods=['PUT'])
@jwt_required()
def update_novel(novel_id):
    current_user_id = get_jwt_identity()
    novel = Novel.query.get_or_404(novel_id)
    
    if novel.author_id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    
    if 'title' in data:
        novel.title = data['title']
    if 'description' in data:
        novel.description = data['description']
    if 'status' in data:
        novel.status = data['status']
    
    novel.updated_at = datetime.utcnow()
    db.session.commit()

    return jsonify({'message': 'Novel updated successfully'}), 200

@novels.route('/<int:novel_id>/chapters/<int:chapter_id>', methods=['PUT'])
@jwt_required()
def update_chapter(novel_id, chapter_id):
    current_user_id = get_jwt_identity()
    novel = Novel.query.get_or_404(novel_id)
    chapter = Chapter.query.get_or_404(chapter_id)
    
    if novel.author_id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    
    if 'title' in data:
        chapter.title = data['title']
    if 'content' in data:
        chapter.content = data['content']
    
    chapter.updated_at = datetime.utcnow()
    novel.updated_at = datetime.utcnow()
    db.session.commit()

    return jsonify({'message': 'Chapter updated successfully'}), 200
