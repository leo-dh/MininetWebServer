import time
from graphene import Field, Int, ObjectType, String
from faker import Faker

fake = Faker()
Faker.seed(time.time())


class PostType(ObjectType):
    id = Int()
    title = String()
    content = String()
    user = Field(lambda: UserType)

    def resolve_id(parent, info):
        return f"{parent.id}"

    def resolve_title(parent, info):
        return parent.title

    def resolve_content(parent, info):
        return parent.content

    def resolve_user(parent, info):
        return parent.user


from .user_schema import UserType


class Post:
    counter = 0

    def __init__(self, title="", content=""):
        Post.counter += 1
        self.id = Post.counter
        self.title = title or fake.sentence(nb_words=10)
        self.content = content or fake.paragraph(nb_sentences=5)
        self.user = None

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "user_url": f"/api/users/{self.user.id}",
        }
