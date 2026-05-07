from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.product import Product
from app import db
from app.utils.decorators import role_required, owner_or_admin_required

products_bp = Blueprint('products', __name__)

# Listar todos
@products_bp.route('/', methods=['GET'])
@jwt_required()
def get_products():
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'description': p.description,
        'price': p.price,
        'user_id': p.user_id
    } for p in products])

# Criar (apenas Admin)
@products_bp.route('/', methods=['POST'])
@jwt_required()
@role_required('admin')
def create_product():
    data = request.get_json()
    current_user_id = get_jwt_identity()
    
    product = Product(
        name=data['name'],
        description=data.get('description'),
        price=float(data['price']),
        user_id=int(current_user_id)
    )
    db.session.add(product)
    db.session.commit()
    
    return jsonify({"msg": "Produto criado com sucesso", "id": product.id}), 201

# Buscar um
@products_bp.route('/<int:product_id>', methods=['GET'])
@jwt_required()
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'user_id': product.user_id
    })

# Atualizar (dono ou admin)
@products_bp.route('/<int:product_id>', methods=['PUT'])
@jwt_required()
@owner_or_admin_required()
def update_product(product, product_id):
    data = request.get_json()
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = float(data.get('price', product.price))
    db.session.commit()
    return jsonify({"msg": "Produto atualizado com sucesso"})

# Deletar (dono ou admin)
@products_bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required()
@owner_or_admin_required()
def delete_product(product, product_id):
    db.session.delete(product)
    db.session.commit()
    return jsonify({"msg": "Produto excluído com sucesso"})