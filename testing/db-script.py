from flaskblog import app, db
from flaskblog.models import Post, User

with app.app_context():
    db.create_all()

    user_1 = User(username="Peter",
                  email="peter@test.com",
                  password="testing123")
    db.session.add(user_1)
    user_2 = User(username="Adam",
                  email="adam@test.com",
                  password="testing123")
    db.session.add(user_2)
    db.session.commit()

    print(User.query.all())
    print(User.query.first())
    print(User.query.filter_by(username="Peter").all())
    print(User.query.filter_by(username="Peter").first())

    test_user_1 = User.query.filter_by(username="Peter").first()
    print(test_user_1.id, test_user_1)

    peter = User.query.get(1)
    adam = User.query.get(2)
    print(adam)

    post_1 = Post(title="Blog 1", content="First blog post!", user_id=peter.id)
    post_2 = Post(title="Blog 2", content="Second blog post!", user_id=peter.id)
    post_3 = Post(title="Blog 3", content="Third blog post!", user_id=adam.id)
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
