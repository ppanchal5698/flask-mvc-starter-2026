"""Database connection and model tests."""

import pytest
from sqlalchemy import text

from app.core.extensions import db
from app.models.user import User


class TestDatabaseConnection:
    """Tests for database connection and basic operations."""

    def test_database_connection(self, app):
        """Test that the database connection is established."""
        with app.app_context():
            # Execute a simple query to verify connection
            result = db.session.execute(text('SELECT 1'))
            assert result.scalar() == 1

    def test_database_tables_created(self, app):
        """Test that database tables are created properly."""
        with app.app_context():
            # Check that the users table exists
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            assert 'users' in tables

    def test_database_session_active(self, app):
        """Test that database session is active and working."""
        with app.app_context():
            assert db.session is not None
            assert db.session.is_active


class TestUserModel:
    """Tests for User model database operations."""

    def test_create_user(self, app):
        """Test creating a new user in the database."""
        with app.app_context():
            user = User(
                username='testuser',
                email='test@example.com'
            )
            user.set_password('testpassword123')

            db.session.add(user)
            db.session.commit()

            assert user.id is not None
            assert user.username == 'testuser'
            assert user.email == 'test@example.com'

    def test_query_user(self, app):
        """Test querying a user from the database."""
        with app.app_context():
            # Create a user first
            user = User(
                username='queryuser',
                email='query@example.com'
            )
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()

            # Query the user
            queried_user = User.query.filter_by(username='queryuser').first()

            assert queried_user is not None
            assert queried_user.email == 'query@example.com'

    def test_user_password_hashing(self, app):
        """Test that user passwords are properly hashed."""
        with app.app_context():
            user = User(
                username='hashuser',
                email='hash@example.com'
            )
            user.set_password('mysecretpassword')

            db.session.add(user)
            db.session.commit()

            # Password should be hashed, not plain text
            assert user.password_hash != 'mysecretpassword'
            assert user.check_password('mysecretpassword') is True
            assert user.check_password('wrongpassword') is False

    def test_update_user(self, app):
        """Test updating a user in the database."""
        with app.app_context():
            user = User(
                username='updateuser',
                email='update@example.com'
            )
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()

            # Update the user
            user.email = 'newemail@example.com'
            db.session.commit()

            # Verify update
            updated_user = User.query.filter_by(username='updateuser').first()
            assert updated_user.email == 'newemail@example.com'

    def test_delete_user(self, app):
        """Test deleting a user from the database."""
        with app.app_context():
            user = User(
                username='deleteuser',
                email='delete@example.com'
            )
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()

            user_id = user.id

            # Delete the user
            db.session.delete(user)
            db.session.commit()

            # Verify deletion
            deleted_user = db.session.get(User, user_id)
            assert deleted_user is None

    def test_unique_username_constraint(self, app):
        """Test that duplicate usernames are not allowed."""
        with app.app_context():
            user1 = User(
                username='uniqueuser',
                email='unique1@example.com'
            )
            user1.set_password('password123')
            db.session.add(user1)
            db.session.commit()

            # Try to create another user with the same username
            user2 = User(
                username='uniqueuser',
                email='unique2@example.com'
            )
            user2.set_password('password123')
            db.session.add(user2)

            with pytest.raises(Exception):  # IntegrityError
                db.session.commit()

    def test_unique_email_constraint(self, app):
        """Test that duplicate emails are not allowed."""
        with app.app_context():
            user1 = User(
                username='emailuser1',
                email='sameemail@example.com'
            )
            user1.set_password('password123')
            db.session.add(user1)
            db.session.commit()

            # Try to create another user with the same email
            user2 = User(
                username='emailuser2',
                email='sameemail@example.com'
            )
            user2.set_password('password123')
            db.session.add(user2)

            with pytest.raises(Exception):  # IntegrityError
                db.session.commit()
