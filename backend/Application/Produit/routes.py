from flask import Flask , request, jsonify, json, Response,Blueprint
import os
from sqlalchemy import select
from Application.__init__ import db,UPLOAD_FOLDER
from Application.models import produit_schema,produits_schema,Produit
from Application.Produit.utils import allowed_file
from werkzeug.utils import secure_filename

#Creating the blueprint
produit = Blueprint('produit',__name__)


#Routes
@produit.route('/produit/get', methods =['GET'])
def get_produits():
    produits= Produit.query.all()
    results = produits_schema.dump(produits)
    return jsonify(results)


@produit.route('/produit/get/<id>' , methods = ['GET'])
def get_produit(id):
    produit_to_get = Produit.query.get(id)
    return produit_schema.jsonify(produit_to_get)


@produit.route('/produit/getbycategorie/<cat_id>' , methods = ['GET'])
def get_produit_bycategorie(cat_id):
    produits_to_get = Produit.query.filter_by(categorie_id=cat_id)
    return produits_schema.jsonify(produits_to_get)

@produit.route('/produit/add' , methods=['POST'])
def add_produit():
    file = request.files['image']
    if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
    
    
    categorie = request.form.get('categorie_id')
    nom_produit = request.form.get('nom_produit')
    description = request.form.get('description')
    prix_produit = request.form.get('prix_produit')
    stock = request.form.get('stock') 
    produit = Produit(nom_produit=nom_produit,description=description, image=filename, categorie_id=categorie ,prix_produit=prix_produit,stock=stock)
    db.session.add(produit)
    db.session.commit()
    return produit_schema.jsonify(produit)



@produit.route('/produit/delete/<id>' , methods=['DELETE']) 
def delete_produit(id):
    produit_to_delete = Produit.query.get(id)
    db.session.delete(produit_to_delete)
    db.session.commit()
    return "object deleted successfully !"


@produit.route('/produit/update/<id>', methods=['PUT'])
def update_produit(id):
    produit_to_update=Produit.query.get(id)
    file = request.files['image']
    if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
    

    categorie = request.form.get('categorie')
    nom_produit = request.form.get('nom_produit')
    description = request.form.get('description')
    prix_produit = request.form.get('prix_produit')
    stock = request.form.get('stock') 
    produit_to_update.image = filename
    produit_to_update.categorie_id=categorie
    produit_to_update.nom_produit=nom_produit
    produit_to_update.description = description
    produit_to_update.prix_produit= prix_produit
    produit_to_update.stock = stock
    db.session.commit()
    return produit_schema.jsonify(produit_to_update)