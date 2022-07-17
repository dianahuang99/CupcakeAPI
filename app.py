"""Flask app for Cupcakes"""
from flask import Flask, render_template, redirect, flash, session, jsonify, request
from pkg_resources import register_namespace_handler
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///cupcakes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "secret"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/api/cupcakes')
def show_cupcakes():
    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)

@app.route('/api/cupcakes/<int:cupcake_id>')
def show_one_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id).serialize()
    return jsonify(cupcake=cupcake)

@app.route('/api/cupcakes', methods=['POST'])
def add_new_cupcake():
    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = request.json['image']
    cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image or None)
    db.session.add(cupcake)
    db.session.commit()
    
    response_json = jsonify(cupcake=cupcake.serialize())
    return (response_json, 201)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = request.json['flavor']
    cupcake.size = request.json['size']
    cupcake.rating = request.json['rating']
    cupcake.image = request.json.get('image', cupcake.image)
    db.session.commit()
    
    return (jsonify(cupcake=cupcake.serialize()))

@app.route('/api/cupcakes/<int:cupcake_id>', methods=["DELETE"])
def delete_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    
    return (jsonify(message='deleted'))