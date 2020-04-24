from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

idBurgerCounter = 1
idIngretCounter = 1
URL = "heroku"

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 't2'
app.config['MONGO_URI'] = 'mongodb+srv://ignacioaraya:gamecube123@tarea2-uv28d.mongodb.net/t2?retryWrites=true&w=majority'
mongo = PyMongo(app)

    
########### HAMBURGUESAS ###########

# [GET] HAMBURGUESAS
@app.route('/hamburguesa', methods=['GET'])
def getBurgers():
    burgers = mongo.db.burger
    output = []
    for b in burgers.find():
        output.append({"id": b["id"], "nombre": b["nombre"], "precio": b["precio"], "descripcion": b["descripcion"], "imagen": b["imagen"], "ingredientes": b["ingredientes"]})
    return jsonify(output),200

# [POST] HAMBURGUESAS
@app.route('/hamburguesa', methods=['POST'])
def addBurger():
    burgers = mongo.db.burger
    global idBurgerCounter
    id = idBurgerCounter
    idBurgerCounter +=1
    nombre = request.json["nombre"]
    precio = request.json["precio"]
    descripcion = request.json["descripcion"]
    imagen = request.json["imagen"]
    ingredientes = []
    if nombre == "" or type(nombre) != type("string") or precio == "" or type(precio) != type(1) or descripcion == "" or type(descripcion) != type("string") or imagen == "" or type(imagen) != type("string"):
        return "Input Invalido",400
    else:
        newBurger = burgers.insert({"id": id, "nombre": nombre, "precio": precio, "descripcion": descripcion, "imagen": imagen, "ingredientes": ingredientes})
        newBurger2 = burgers.find_one({'_id': newBurger})
        output = {"id": newBurger2["id"], "nombre": newBurger2["nombre"], "precio": newBurger2["precio"], "descripcion": newBurger2["descripcion"], "imagen": newBurger2["imagen"], "ingredientes": newBurger2["ingredientes"]}
        return jsonify(output),201

# [GET] HAMBURGUESAS POR ID
@app.route('/hamburguesa/<int:id>', methods=['GET'])
def getBurger(id):
    burgers = mongo.db.burger
    b = burgers.find_one({"id": id})
    if type(id) != type(1):
        return "id invalido", 400
    if b == None:
        return "hamburguesa inexistente",404
    elif b:
        output = {"id": b["id"], "nombre": b["nombre"], "precio": b["precio"], "descripcion": b["descripcion"], "imagen": b["imagen"], "ingredientes": b["ingredientes"]}
        return jsonify(output),200
    else:
        return "id invalido", 400

# [DELETE] HAMBURGUESA POR ID
@app.route('/hamburguesa/<int:id>', methods=['DELETE'])
def deleteBurger(id):
    burgers = mongo.db.burger
    b = burgers.find_one({"id": id})
    if type(id) != type(1):
        return "hamburguesa inexistente",404
    if b == None:
        return "hamburguesa inexistente",404
    else:
        burgers.delete_one(b)
        return "hamburguesa eliminada",200

# [PATCH] ACTUALIZAR HAMBURGUESA POR ID
@app.route('/hamburguesa/<int:id>', methods=['PATCH'])
def updateBurger(id):
    burgers = mongo.db.burger
    b = burgers.find_one({"id": id})
    nombre = request.json["nombre"]
    precio = request.json["precio"]
    descripcion = request.json["descripcion"]
    imagen = request.json["imagen"]
    if type(id) != type(1):
        return "Parámetros inválidos", 400
    if b == None:
        return "hamburguesa inexistente", 404
    elif nombre == "" or precio == "" or descripcion == "" or imagen == "" or type(precio) == type("string"):
        return "Parámetros inválidos",400
    else:
        newvalues = { "$set": {"nombre": nombre, "precio":precio, "descripcion":descripcion, "imagen":imagen}}
        burgers.update_one(b, newvalues)
        output = {"id": b["id"], "nombre": nombre, "precio":precio, "descripcion":descripcion, "imagen":imagen, "ingredientes": b["ingredientes"]}
        return jsonify(output), 200

########### INGREDIENTES ###########

# [GET] INGREDIENTES
@app.route('/ingrediente', methods=['GET'])
def getIngredients():
    ingredientes = mongo.db.ingredient
    output = []
    for b in ingredientes.find():
        output.append({"id": b["id"], "nombre": b["nombre"], "descripcion": b["descripcion"]})
    return jsonify(output),200

# [POST] INGREDIENTE (Revisar)
@app.route('/ingrediente', methods=['POST'])
def addIngredient():
    ingredientes = mongo.db.ingredient
    global idIngretCounter
    id = idIngretCounter
    idIngretCounter +=1
    nombre = request.json["nombre"]
    descripcion = request.json["descripcion"]
    if nombre == "" or descripcion == "" or type(nombre) != type("string") or type(descripcion) != type("string"):
        return "Input Invalido",400
    else:
        newingrediente = ingredientes.insert({"id": id, "nombre": nombre, "descripcion": descripcion})
        newingrediente2 = ingredientes.find_one({'_id': newingrediente})
        output = {"id": newingrediente2["id"], "nombre": newingrediente2["nombre"], "descripcion": newingrediente2["descripcion"]}
        return jsonify(output),201

# [GET] INGREDIENTES POR ID (Le falta el error 404 y 400)
@app.route('/ingrediente/<int:id>', methods=['GET'])
def getIngrediente(id):
    ingredientes = mongo.db.ingredient
    i = ingredientes.find_one({"id": id})
    if type(id) != type(1):
        return "id invalido", 400
    if i == None:
        return "ingrediente inexistente",404
    elif i:
        output = {"id": i["id"], "nombre": i["nombre"], "descripcion": i["descripcion"]}
        return jsonify(output),200
    else:
        return "id invalido",400

# [DELETE] INGREDIENTE POR ID
@app.route('/ingrediente/<int:id>', methods=['DELETE'])
def deleteIngrediente(id):
    ingredientes = mongo.db.ingredient
    i = ingredientes.find_one({"id": id})
    if type(id) != type(1):
        return "ingrediente inexistente", 404
    if i == None:
        return "ingrediente inexistente",404
    else:
        burgers = mongo.db.burger
        delIng = URL + "/ingrediente/" + str(id)
        for b in burgers.find():
            if delIng in b["ingredientes"]:
                return "Ingrediente no se puede borrar, se encuentra presente en una hamburguesa",409
        ingredientes.delete_one(i)
        return "ingrediente eliminado",200

########### MIX ###########

# [DELETE] Remove an INGREDIENTE to a HAMBURGESA
@app.route('/hamburguesa/<int:idH>/ingrediente/<int:idI>', methods=["DELETE"])
def removeIngredienteFromBurger(idH, idI):
    burgers = mongo.db.burger
    b = burgers.find_one({"id": idH})
    ingredientes = mongo.db.ingredient
    i = ingredientes.find_one({"id": idI})
    if b == None:
        return "Id de hamburguesa invalido", 400
    if i == None:
        return "Ingrediente inexistente en la hamburguesa",404
    global URL
    newIng = URL + "/ingrediente/" + str(idI)
    if newIng not in b["ingredientes"]:
        return "Ingrediente inexistente en la hamburguesa",404
    else:
        burgers.update({ "id": idH },{ "$pull": {"ingredientes": { "$in": [newIng]}}})
        return "Ingrediente retirado", 200

# [PUT] Add an INGREDIENTE to a HAMBURGESA
@app.route('/hamburguesa/<int:idH>/ingrediente/<int:idI>', methods=["PUT"])
def addIngredienteToBurger(idH, idI):
    burgers = mongo.db.burger
    b = burgers.find_one({"id": idH})
    ingredientes = mongo.db.ingredient
    i = ingredientes.find_one({"id": idI})
    if type(idH) != type(1) or type(idI) != type(1):
        return "Ingrediente inexsistente",404
    if b == None:
        return "Id de hamburguesa inválido", 400
    if i == None:
        return "Ingrediente inexsistente",404
    global URL
    newIng = URL + "/ingrediente/" + str(idI)
    if newIng not in b["ingredientes"]:
        burgers.update({ "id": idH },{ "$push": { "ingredientes": newIng }})
        return "Agreado de forma exitosa", 201
    else:
        return "Agreado de forma exitosa", 201

app.run()