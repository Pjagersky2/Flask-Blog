# Initial Database Test Script

This script creates a user and post table.  It also adds dummy data to each table.  This is only used to test early development on SQLAlchemy.

The script is as follows:

```python
from flaskblog import app, db
from flaskblog.models import Post, User

with app.app_context():
    db.create_all()

    user_1 = User(username="User1",
                  email="user1@test.com",
                  password="testing123")
    db.session.add(user_1)
    user_2 = User(username="User2",
                  email="user2@test.com",
                  password="testing123")
    db.session.add(user_2)
    db.session.commit()

    print(User.query.all())
    print(User.query.first())
    print(User.query.filter_by(username="User1").all())
    print(User.query.filter_by(username="User1").first())

    test_user_1 = User.query.filter_by(username="User1").first()
    print(test_user_1.id, test_user_1)

    user1 = User.query.get(1)
    user2 = User.query.get(2)
    print(user2)

    post_1 = Post(title="Blog 1", content="First blog post!", user_id=user1.id)
    post_2 = Post(title="Blog 2", content="Second blog post!", user_id=user1.id)
    post_3 = Post(title="Blog 3", content="Third blog post!", user_id=user2.id)
    db.session.add(post_1)
    db.session.add(post_2)
    db.session.add(post_3)
    db.session.commit()

    test_post = Post.query.first()
    print(test_post)

    test_user_2 = User.query.get(1)
    print(test_user_2.posts)
    print(test_user_2.posts[0].title)

    for post in test_user_2.posts:
        print(post)

    db.drop_all()

```
