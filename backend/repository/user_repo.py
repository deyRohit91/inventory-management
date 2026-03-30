from db import models

def get_user_by_username(db, username):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db, username, password):
    user = models.User(username=username, password=password)
    db.add(user)
    db.commit()
    return user