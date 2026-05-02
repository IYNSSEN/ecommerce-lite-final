from app.models import User, db


class UserRepository:
    def find_by_email(self, email):
        return User.query.filter_by(email=email.lower()).first()

    def create(self, email, password, role="user"):
        user = User(email=email.lower(), role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user
