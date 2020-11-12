import time
from graphene import Field, List, ObjectType, String
from faker import Faker

fake = Faker()
Faker.seed(time.time())


class UserType(ObjectType):

    id = String()
    name = String()
    posts = Field(List(lambda: PostType))

    def resolve_id(parent, info):
        return parent.id

    def resolve_name(parent, info):
        return parent.name

    def resolve_posts(parent, info):
        return parent.posts


from .post_schema import PostType


class User:
    counter = 0

    def __init__(self, name=""):
        User.counter += 1
        self.id = User.counter
        self.name = name or fake.name()
        self.posts = []

    def add_post(self, post):
        self.posts.append(post)
        post.user = self

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "posts_url": f"/api/users/{self.id}/posts",
        }
