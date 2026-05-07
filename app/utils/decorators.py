from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt, get_jwt_identity
from flask import jsonify
from app.models.product import Product

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get('role') != role and role != 'any':
                return jsonify({"msg": "Acesso negado: permissão insuficiente"}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def owner_or_admin_required():
    def decorator(f):
        @wraps(f)
        def decorated_function(product_id, *args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            current_user_id = int(get_jwt_identity())
            user_role = claims.get('role')

            product = Product.query.get_or_404(product_id)
            
            if user_role == 'admin' or product.user_id == current_user_id:
                return f(product, *args, **kwargs)
            return jsonify({"msg": "Acesso negado"}), 403
        return decorated_function
    return decorator