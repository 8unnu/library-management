from src.database.database import session_maker, User


async def get_all_usernames():
    with session_maker() as db:
        users = db.query(User).all()
        try:
            usernames = [u.username for u in users]
            return usernames
        except Exception as exc:
            print(f"Error: {exc}")
            return []


async def get_user_password(username):
    with session_maker() as db:
        try:
            user = db.query(User).filter(User.username == username).first()
            return user.password
        except Exception as exc:
            print(f"Error: {exc}")
            pass