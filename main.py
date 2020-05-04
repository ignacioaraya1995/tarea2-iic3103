from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

def createID(element):
    idlist = []
    for e in element.find():
        idlist.append(e["id"])
    for i in range(1,10000):
        if i not in idlist:
            return i



URL = "https://tarea2-iic3103-araya.herokuapp.com"

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'heroku_st9ndd6k'
app.config['MONGO_URI'] = 'mongodb://ignacio:iic3103@ds145916.mlab.com:45916/heroku_st9ndd6k?RetryWrites=false'
mongo = PyMongo(app)
    
########### HAMBURGUESAS ###########

# [GET] HAMBURGUESAS
@app.route('/hamburguesa', methods=['GET'])
def getBurgers():
    print("\n[GET] HAMBURGUESAS\n")
    burgers = mongo.db.burger
    output = []
    for b in burgers.find():
        output.append({"id": b["id"], "nombre": b["nombre"], "precio": b["precio"], "descripcion": b["descripcion"], "imagen": b["imagen"], "ingredientes": b["ingredientes"]})
    return jsonify(output),200

# [POST] HAMBURGUESAS
@app.route('/hamburguesa', methods=['POST'])
def addBurger():
    print("\n[POST] HAMBURGUESAS\n")
    burgers = mongo.db.burger
    id = createID(burgers)
    try:
        nombre = request.json["nombre"]
        precio = request.json["precio"]
        descripcion = request.json["descripcion"]
        imagen = request.json["imagen"]
        ingredientes = []
    except KeyError:
        return "Input Invalido",400
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
    print("\n[GET] HAMBURGUESAS POR ID\n")
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
    print("\n[DELETE] HAMBURGUESA POR ID\n")
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
    print("\n[PATCH] ACTUALIZAR HAMBURGUESA POR ID\n")
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
    print("\n[GET] INGREDIENTES\n")
    ingredientes = mongo.db.ingredient
    output = []
    for b in ingredientes.find():
        output.append({"id": b["id"], "nombre": b["nombre"], "descripcion": b["descripcion"]})
    return jsonify(output),200

# [POST] INGREDIENTE
@app.route('/ingrediente', methods=['POST'])
def addIngredient():
    print("\n[POST] INGREDIENTE\n")
    ingredientes = mongo.db.ingredient
    id = createID(ingredientes)
    try:
        nombre = request.json["nombre"]
        descripcion = request.json["descripcion"]
    except KeyError:
        return "Input Invalido",400 
    if nombre != "" and descripcion != "" and type(nombre) == type("string") and type(descripcion) == type("string"):
        newingrediente = ingredientes.insert({"id": id, "nombre": nombre, "descripcion": descripcion})
        newingrediente2 = ingredientes.find_one({'_id': newingrediente})
        output = {"id": newingrediente2["id"], "nombre": newingrediente2["nombre"], "descripcion": newingrediente2["descripcion"]}
        return jsonify(output),201
    else:
        return "Input Invalido",400

# [GET] INGREDIENTES POR ID
@app.route('/ingrediente/<int:id>', methods=['GET'])
def getIngrediente(id):
    print("\n[GET] INGREDIENTES POR ID\n")
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
    print("\n[DELETE] INGREDIENTE POR ID\n")
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
    print("\n[DELETE] Remove an INGREDIENTE to a HAMBURGESA\n")
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
    print("\n[PUT] Add an INGREDIENTE to a HAMBURGESA\n")
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

if __name__ == '__main__':
    app.run()
