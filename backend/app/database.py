from flask_pymongo import PyMongo
from bson import ObjectId

mongo = PyMongo()

def init_db(app):
    mongo.init_app(app)

def get_user_by_username(username):
    return mongo.db.users.find_one({"username": username})

def get_user_by_id(user_id):
    return mongo.db.users.find_one({"_id": ObjectId(user_id)})

def create_user(username, email, password_hash):
    user_id = mongo.db.users.insert_one({
        "username": username,
        "email": email,
        "password_hash": password_hash
    }).inserted_id
    return str(user_id)

def get_websites_by_user_id(user_id):
    return list(mongo.db.websites.find({"user_id": user_id}))

def create_website(url, name, check_interval, user_id):
    website_id = mongo.db.websites.insert_one({
        "url": url,
        "name": name,
        "check_interval": check_interval,
        "user_id": user_id
    }).inserted_id
    return str(website_id)

def update_website(website_id, data):
    mongo.db.websites.update_one(
        {"_id": ObjectId(website_id)},
        {"$set": data}
    )

def delete_website(website_id):
    mongo.db.websites.delete_one({"_id": ObjectId(website_id)})