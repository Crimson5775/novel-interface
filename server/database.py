from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from config import Config

class Database:
    def __init__(self):
        self.client = None
        self.db = None

    def connect(self):
        try:
            self.client = MongoClient(Config.MONGO_URI)
            self.db = self.client.get_default_database()
            # Test the connection
            self.client.admin.command('ping')
            print("Successfully connected to MongoDB!")
            return True
        except ConnectionFailure:
            print("Failed to connect to MongoDB. Is it running?")
            return False

    def disconnect(self):
        if self.client:
            self.client.close()
            print("Disconnected from MongoDB")

    # User operations
    def get_user_by_id(self, user_id):
        return self.db.users.find_one({'_id': user_id})

    def get_user_by_username(self, username):
        return self.db.users.find_one({'username': username})

    def get_user_by_email(self, email):
        return self.db.users.find_one({'email': email})

    def create_user(self, user_data):
        return self.db.users.insert_one(user_data)

    # Novel operations
    def get_novel_by_id(self, novel_id):
        return self.db.novels.find_one({'_id': novel_id})

    def get_novels(self, skip=0, limit=20):
        return list(self.db.novels.find().skip(skip).limit(limit))

    def create_novel(self, novel_data):
        return self.db.novels.insert_one(novel_data)

    # Chapter operations
    def get_chapter_by_id(self, chapter_id):
        return self.db.chapters.find_one({'_id': chapter_id})

    def get_chapters_by_novel(self, novel_id, skip=0, limit=20):
        return list(self.db.chapters.find({'novel_id': novel_id}).skip(skip).limit(limit))

    def create_chapter(self, chapter_data):
        return self.db.chapters.insert_one(chapter_data)

    # Comment operations
    def get_comments_by_novel(self, novel_id, skip=0, limit=20):
        return list(self.db.comments.find({'novel_id': novel_id}).skip(skip).limit(limit))

    def create_comment(self, comment_data):
        return self.db.comments.insert_one(comment_data)

    # Rating operations
    def get_rating(self, user_id, novel_id):
        return self.db.ratings.find_one({'user_id': user_id, 'novel_id': novel_id})

    def create_rating(self, rating_data):
        return self.db.ratings.insert_one(rating_data)

    # User Permission operations
    def get_user_permissions(self, user_id):
        return self.db.user_permissions.find_one({'user_id': user_id})

    def create_user_permission(self, permission_data):
        return self.db.user_permissions.insert_one(permission_data)

# Create a global database instance
db = Database()
