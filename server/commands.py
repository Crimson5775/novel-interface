from flask.cli import with_appcontext
import click
from .models import db, User, UserPermission

@click.command('create-admin')
@with_appcontext
def create_admin():
    """Create an admin user"""
    # Check if admin already exists
    admin = User.query.filter_by(username='admin').first()
    if admin:
        click.echo('Admin user already exists')
        return

    # Create admin user
    admin = User(
        username='admin',
        email='admin@example.com',
        role='admin'
    )
    admin.set_password('admin123')
    
    # Create admin permissions
    permissions = UserPermission(
        user_id=admin.id,
        can_add_novels=True,
        can_edit_all_novels=True,
        can_delete_novels=True,
        can_manage_users=True
    )
    
    db.session.add(admin)
    db.session.add(permissions)
    db.session.commit()
    
    click.echo('Admin user created successfully')
