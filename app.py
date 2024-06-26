#Importação/Import
from flask import Flask, request,jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

db = SQLAlchemy(app)

#Modelagem/Model
#Produto/Product - id, name, price, description
class Product(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    price = db.Column(db.Float,nullable=False)
    description = db.Column(db.Text,nullable=True)

#Rota para adicionar produtos/Route to add products
@app.route('/api/products/add',methods=['POST'])
def add_product():
    data = request.json
    if 'name' in data and 'price' in data:
        product = Product(name =data["name"], price =data["price"], description =data.get("description",""))
        db.session.add(product)
        db.session.commit()
        return jsonify({"message":"Produto adicionado com sucesso/ Product added successfully"}),200
    return jsonify({"message":"Dados do produto inválidos/ Invalid product data"}),400

#Rota para deletar um produto/Route to delete a product
@app.route('/api/products/delete/<int:product_id>',methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message":"Produto deletado com sucesso/ Product deleted successfully"}),200
    return jsonify({"message":"Produto não encontrado/ Product not found"}),404



#Definir uma rota raiz / Define a root route
@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == "__main__":
    app.run(debug=True)