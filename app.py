#Importação/Import
from flask import Flask, request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import UserMixin,login_user,LoginManager,login_required,logout_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'minha_chave_123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

login_manager = LoginManager()
db = SQLAlchemy(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
CORS(app)

#Modelagem/Model
#Usuário/User - id, name, password
class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(50),nullable=False,unique=True)
    password = db.Column(db.String(50),nullable=False)

#Produto/Product - id, name, price, description
class Product(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    price = db.Column(db.Float,nullable=False)
    description = db.Column(db.Text,nullable=True)


#Rota de autenticação/Authentication route
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login',methods=['POST'])
def login():
    data = request.json

    user = User.query.filter_by(username=data.get('username')).first()
    
    if user and data.get('password') == user.password:
        login_user(user)
        return jsonify({"message":"Login realizado com sucesso/ Login successful"}),200
    return jsonify({"message":"Não autorizado, dados inválidos/ Unauthorized, invalid data"}),401

@app.route('/logout',methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message":"Logout realizado com sucesso/ Logout successful"}),200



#Rota para adicionar produtos/Route to add products
@app.route('/api/products/add',methods=['POST'])
@login_required
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
@login_required
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message":"Produto deletado com sucesso/ Product deleted successfully"}),200
    return jsonify({"message":"Produto não encontrado/ Product not found"}),404

#Rota para listar produto por id/Route to list product by id
@app.route('/api/products/<int:product_id>',methods=['GET'])
def get_product_details(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({
            "id":product.id,
            "name":product.name,
            "price":product.price,
            "description":product.description
            }),200
    return jsonify({"message":"Produto não encontrado/ Product not found"}),404

#Rota para atualizar um produto/Route to update a product
@app.route('/api/products/update/<int:product_id>',methods=['PUT'])
@login_required
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message":"Produto não encontrado/ Product not found"}),404
    
    data = request.json
    if 'name' in data:
        product.name = data["name"]
    
    if 'price' in data:
        product.price = data["price"]

    if 'description' in data:
        product.description = data["description"]

    db.session.commit()
    return jsonify({"message":"Produto atualizado com sucesso/ Product updated successfully"}),200

#Rota para listar todos os produtos/Route to list all products
@app.route('/api/products',methods=['GET'])
def get_products():
    products = Product.query.all()
    product_list = []
    for product in products:
        product_data = {
            "id":product.id,
            "name":product.name,
            "price":product.price
        }
        product_list.append(product_data)
    return jsonify(product_list),200
    
        

#Definir uma rota raiz / Define a root route
@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == "__main__":
    app.run(debug=True)