from datetime import datetime
from bson import ObjectId
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data.get('_id', ''))
        self.username = user_data.get('username', '')
        self.email = user_data.get('email', '')
        self.password_hash = user_data.get('password_hash', '')
        self.role = user_data.get('role', 'user')
        self.is_active = user_data.get('is_active', True)
        self.created_at = user_data.get('created_at', datetime.utcnow())
        self.last_login = user_data.get('last_login', datetime.utcnow())
        self.permissions = user_data.get('permissions', {})

    @staticmethod
    def create_user(username, email, password, role='user'):
        return {
            'username': username,
            'email': email,
            'password_hash': generate_password_hash(password),
            'role': role,
            'is_active': True,
            'created_at': datetime.utcnow(),
            'last_login': datetime.utcnow(),
            'permissions': {}
        }

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active,
            'permissions': self.permissions
        }

class Novel:
    def __init__(self, novel_data):
        self.id = str(novel_data.get('_id', ''))
        self.title = novel_data.get('title', '')
        self.author = novel_data.get('author', '')
        self.description = novel_data.get('description', '')
        self.cover_image = novel_data.get('cover_image', '')
        self.categories = novel_data.get('categories', [])
        self.status = novel_data.get('status', 'ongoing')
        self.created_at = novel_data.get('created_at', datetime.utcnow())
        self.updated_at = novel_data.get('updated_at', datetime.utcnow())
        self.views = novel_data.get('views', 0)
        self.rating = novel_data.get('rating', 0.0)
        self.total_ratings = novel_data.get('total_ratings', 0)

    @staticmethod
    def create_novel(title, author, description, cover_image='', categories=None):
        return {
            'title': title,
            'author': author,
            'description': description,
            'cover_image': cover_image,
            'categories': categories or [],
            'status': 'ongoing',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'views': 0,
            'rating': 0.0,
            'total_ratings': 0
        }

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'description': self.description,
            'cover_image': self.cover_image,
            'categories': self.categories,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'views': self.views,
            'rating': self.rating,
            'total_ratings': self.total_ratings
        }

class Chapter:
    def __init__(self, chapter_data):
        self.id = str(chapter_data.get('_id', ''))
        self.novel_id = str(chapter_data.get('novel_id', ''))
        self.title = chapter_data.get('title', '')
        self.content = chapter_data.get('content', '')
        self.chapter_number = chapter_data.get('chapter_number', 0)
        self.translator_id = str(chapter_data.get('translator_id', ''))
        self.status = chapter_data.get('status', 'draft')
        self.created_at = chapter_data.get('created_at', datetime.utcnow())
        self.updated_at = chapter_data.get('updated_at', datetime.utcnow())
        self.views = chapter_data.get('views', 0)

    @staticmethod
    def create_chapter(novel_id, title, content, chapter_number, translator_id):
        return {
            'novel_id': ObjectId(novel_id),
            'title': title,
            'content': content,
            'chapter_number': chapter_number,
            'translator_id': ObjectId(translator_id),
            'status': 'draft',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'views': 0
        }

    def to_dict(self):
        return {
            'id': self.id,
            'novel_id': self.novel_id,
            'title': self.title,
            'content': self.content,
            'chapter_number': self.chapter_number,
            'translator_id': self.translator_id,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'views': self.views
        }

class Genre:
    def __init__(self, genre_data):
        self.id = str(genre_data.get('_id', ''))
        self.name = genre_data.get('name', '')
        self.description = genre_data.get('description', '')

    @staticmethod
    def create_genre(name, description):
        return {
            'name': name,
            'description': description
        }

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

class Comment:
    def __init__(self, comment_data):
        self.id = str(comment_data.get('_id', ''))
        self.content = comment_data.get('content', '')
        self.user_id = str(comment_data.get('user_id', ''))
        self.novel_id = str(comment_data.get('novel_id', ''))
        self.chapter_id = str(comment_data.get('chapter_id', ''))
        self.created_at = comment_data.get('created_at', datetime.utcnow())
        self.updated_at = comment_data.get('updated_at', datetime.utcnow())

    @staticmethod
    def create_comment(content, user_id, novel_id, chapter_id):
        return {
            'content': content,
            'user_id': ObjectId(user_id),
            'novel_id': ObjectId(novel_id),
            'chapter_id': ObjectId(chapter_id),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'user_id': self.user_id,
            'novel_id': self.novel_id,
            'chapter_id': self.chapter_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class Rating:
    def __init__(self, rating_data):
        self.user_id = str(rating_data.get('user_id', ''))
        self.novel_id = str(rating_data.get('novel_id', ''))
        self.rating = rating_data.get('rating', 0)
        self.created_at = rating_data.get('created_at', datetime.utcnow())

    @staticmethod
    def create_rating(user_id, novel_id, rating):
        return {
            'user_id': ObjectId(user_id),
            'novel_id': ObjectId(novel_id),
            'rating': rating,
            'created_at': datetime.utcnow()
        }

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'novel_id': self.novel_id,
            'rating': self.rating,
            'created_at': self.created_at
        }

class Notification:
    def __init__(self, notification_data):
        self.id = str(notification_data.get('_id', ''))
        self.user_id = str(notification_data.get('user_id', ''))
        self.title = notification_data.get('title', '')
        self.message = notification_data.get('message', '')
        self.type = notification_data.get('type', '')
        self.is_read = notification_data.get('is_read', False)
        self.created_at = notification_data.get('created_at', datetime.utcnow())

    @staticmethod
    def create_notification(user_id, title, message, type):
        return {
            'user_id': ObjectId(user_id),
            'title': title,
            'message': message,
            'type': type,
            'is_read': False,
            'created_at': datetime.utcnow()
        }

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'message': self.message,
            'type': self.type,
            'is_read': self.is_read,
            'created_at': self.created_at
        }

class UserPermission:
    def __init__(self, permission_data):
        self.id = str(permission_data.get('_id', ''))
        self.user_id = str(permission_data.get('user_id', ''))
        self.can_add_novels = permission_data.get('can_add_novels', False)
        self.can_edit_all_novels = permission_data.get('can_edit_all_novels', False)
        self.can_delete_novels = permission_data.get('can_delete_novels', False)
        self.can_manage_users = permission_data.get('can_manage_users', False)
        self.created_at = permission_data.get('created_at', datetime.utcnow())
        self.updated_at = permission_data.get('updated_at', datetime.utcnow())

    @staticmethod
    def create_permission(user_id, can_add_novels, can_edit_all_novels, can_delete_novels, can_manage_users):
        return {
            'user_id': ObjectId(user_id),
            'can_add_novels': can_add_novels,
            'can_edit_all_novels': can_edit_all_novels,
            'can_delete_novels': can_delete_novels,
            'can_manage_users': can_manage_users,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'can_add_novels': self.can_add_novels,
            'can_edit_all_novels': self.can_edit_all_novels,
            'can_delete_novels': self.can_delete_novels,
            'can_manage_users': self.can_manage_users,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
