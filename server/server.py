import time
import sys
from typing import List as ListType

from faker import Faker
from flask import Flask, jsonify, request
from flask_graphql import GraphQLView
from graphql_schema import Post, User, PostType, UserType
from graphene import Field, Int, List, ObjectType, Schema


fake = Faker()
Faker.seed(time.time())

app = Flask(__name__)

LIST_OF_POSTS: ListType[Post] = []
LIST_OF_USERS: ListType[User] = []

### GRAPHQL


class Query(ObjectType):
    users = Field(List(UserType))
    user = Field(UserType, id=Int(required=True))
    posts = Field(List(PostType))
    post = Field(PostType, id=Int(required=True))

    def resolve_users(parent, info):
        return LIST_OF_USERS

    def resolve_user(parent, info, id):
        filtered_values = list(filter(lambda x: x.id == id, LIST_OF_USERS))
        if filtered_values:
            return filtered_values[0]

    def resolve_posts(parent, info):
        return LIST_OF_POSTS

    def resolve_post(parent, info, id):
        filtered_values = list(filter(lambda x: x.id == id, LIST_OF_POSTS))
        if filtered_values:
            return filtered_values[0]


schema = Schema(query=Query)
app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql", graphiql=True, schema=schema),
)

### REST


@app.route("/api/posts/<int:id>", methods=["GET"])
def post(id: int):
    if request.method == "GET":
        post_results = list(filter(lambda x: x.id == id, LIST_OF_POSTS))
        if post_results:
            return jsonify(post_results[0].to_dict())
        return jsonify({})


@app.route("/api/posts", methods=["GET"])
def all_posts():
    if request.method == "GET":
        return jsonify([post.to_dict() for post in LIST_OF_POSTS])


@app.route("/api/users/<int:id>/posts", methods=["GET"])
def user_posts(id: int):
    if request.method == "GET":
        user_results = list(filter(lambda x: x.id == id, LIST_OF_USERS))
        if user_results:
            return jsonify([post.to_dict() for post in user_results[0].posts])
        return jsonify([])


@app.route("/api/users", methods=["GET"])
def all_users():
    if request.method == "GET":
        return jsonify([user.to_dict() for user in LIST_OF_USERS])


@app.route("/api/users/<int:id>", methods=["GET"])
def user(id: int):
    if request.method == "GET":
        user_results = list(filter(lambda x: x.id == id, LIST_OF_USERS))
        if user_results:
            return jsonify(user_results[0].to_dict())
        return jsonify({})


def generate_fake_data():
    users = [User() for _ in range(10)]
    posts = []
    for user in users:
        for _ in range(5):
            user.add_post(Post())
        posts.extend(user.posts)
    LIST_OF_POSTS.extend(posts)
    LIST_OF_USERS.extend(users)


if __name__ == "__main__":
    generate_fake_data()
    if len(sys.argv) > 1:
        port = sys.argv[1]
        host = "0.0.0.0"
    else:
        port = 5000
        host = "localhost"
    app.run(debug=True, port=port, host=host)
