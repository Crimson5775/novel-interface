import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.app import create_app
from server.models import db, User, UserPermission

def create_admin_account():
    app = create_app()
    
    with app.app_context():
        # Check if admin already exists
        admin = User.query.filter_by(role='admin').first()
        if admin:
            print("Admin account already exists!")
            return

        # Create admin user
        admin = User(
            username='admin',
            email='admin@example.com',
            role='admin',
            is_active=True
        )
        admin.set_password('admin123')  # You should change this password

        # Create admin permissions
        db.session.add(admin)
        db.session.commit()

        permissions = UserPermission(
            user_id=admin.id,
            can_add_novels=True,
            can_edit_all_novels=True,
            can_delete_novels=True,
            can_manage_users=True
        )

        # Save to database
        db.session.add(permissions)
        db.session.commit()

        print("Admin account created successfully!")
        print("Username: admin")
        print("Password: admin123")
        print("Please change these credentials after first login!")

if __name__ == '__main__':
    create_admin_account()
