"""
Authentication System pentru BAC Prep AI
JWT-based authentication cu Flask
"""

from functools import wraps
from flask import request, jsonify, current_app
import jwt
from datetime import datetime, timedelta
from models import db, User


def generate_token(user_id, expires_in=24):
    """
    Generează un JWT token pentru utilizator

    Args:
        user_id: ID-ul utilizatorului
        expires_in: Ore până la expirare (default 24h)

    Returns:
        JWT token string
    """
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=expires_in),
        'iat': datetime.utcnow()
    }
    return jwt.encode(
        payload,
        current_app.config['SECRET_KEY'],
        algorithm='HS256'
    )


def decode_token(token):
    """
    Decodează și validează un JWT token

    Args:
        token: JWT token string

    Returns:
        Payload dict sau None dacă invalid
    """
    try:
        payload = jwt.decode(
            token,
            current_app.config['SECRET_KEY'],
            algorithms=['HS256']
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token expirat
    except jwt.InvalidTokenError:
        return None  # Token invalid


def get_current_user():
    """
    Obține utilizatorul curent din token

    Returns:
        User object sau None
    """
    auth_header = request.headers.get('Authorization')

    if not auth_header:
        return None

    try:
        # Format: "Bearer <token>"
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        else:
            token = auth_header

        payload = decode_token(token)
        if payload:
            return User.query.get(payload['user_id'])
    except Exception:
        pass

    return None


def token_required(f):
    """
    Decorator pentru rute care necesită autentificare

    Usage:
        @app.route('/protected')
        @token_required
        def protected_route(current_user):
            return jsonify({'user': current_user.username})
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return jsonify({
                'error': 'missing_token',
                'message': 'Token de autentificare lipsă'
            }), 401

        try:
            # Format: "Bearer <token>"
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
            else:
                token = auth_header

            payload = decode_token(token)

            if not payload:
                return jsonify({
                    'error': 'invalid_token',
                    'message': 'Token invalid sau expirat'
                }), 401

            current_user = User.query.get(payload['user_id'])

            if not current_user:
                return jsonify({
                    'error': 'user_not_found',
                    'message': 'Utilizator inexistent'
                }), 401

            # Actualizează last_activity
            current_user.last_activity = datetime.utcnow()
            db.session.commit()

        except Exception as e:
            return jsonify({
                'error': 'auth_error',
                'message': f'Eroare de autentificare: {str(e)}'
            }), 401

        return f(current_user, *args, **kwargs)

    return decorated


def token_optional(f):
    """
    Decorator pentru rute unde autentificarea e opțională

    Usage:
        @app.route('/exercises')
        @token_optional
        def get_exercises(current_user):
            # current_user poate fi None
            if current_user:
                # utilizator autentificat
            else:
                # utilizator anonim
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        current_user = get_current_user()
        return f(current_user, *args, **kwargs)

    return decorated


# ============================================
# AUTH ROUTES BLUEPRINT
# ============================================

from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Înregistrare utilizator nou

    Body JSON:
        - email: string (required)
        - username: string (required)
        - password: string (required, min 6 chars)
        - profile: string (optional, M1 sau M2)

    Returns:
        - success: bool
        - user: dict
        - token: string
    """
    data = request.get_json()

    # Validare
    if not data:
        return jsonify({
            'error': 'no_data',
            'message': 'Date lipsă'
        }), 400

    email = data.get('email', '').strip().lower()
    username = data.get('username', '').strip()
    password = data.get('password', '')
    profile = data.get('profile', 'M1')

    # Validări
    if not email or '@' not in email:
        return jsonify({
            'error': 'invalid_email',
            'message': 'Email invalid'
        }), 400

    if not username or len(username) < 3:
        return jsonify({
            'error': 'invalid_username',
            'message': 'Username-ul trebuie să aibă minim 3 caractere'
        }), 400

    if not password or len(password) < 6:
        return jsonify({
            'error': 'invalid_password',
            'message': 'Parola trebuie să aibă minim 6 caractere'
        }), 400

    if profile not in ['M1', 'M2']:
        profile = 'M1'

    # Verifică dacă există deja
    if User.query.filter_by(email=email).first():
        return jsonify({
            'error': 'email_exists',
            'message': 'Acest email este deja înregistrat'
        }), 409

    if User.query.filter_by(username=username).first():
        return jsonify({
            'error': 'username_exists',
            'message': 'Acest username este deja folosit'
        }), 409

    # Creează utilizatorul
    user = User(
        email=email,
        username=username,
        profile=profile
    )
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    # Generează token
    token = generate_token(user.id)

    return jsonify({
        'success': True,
        'message': 'Cont creat cu succes!',
        'user': user.to_dict(),
        'token': token
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Autentificare utilizator

    Body JSON:
        - email: string (required) - poate fi email sau username
        - password: string (required)

    Returns:
        - success: bool
        - user: dict
        - token: string
    """
    data = request.get_json()

    if not data:
        return jsonify({
            'error': 'no_data',
            'message': 'Date lipsă'
        }), 400

    email_or_username = data.get('email', '').strip()
    password = data.get('password', '')

    if not email_or_username or not password:
        return jsonify({
            'error': 'missing_credentials',
            'message': 'Email/username și parola sunt obligatorii'
        }), 400

    # Caută utilizatorul după email sau username
    user = User.query.filter(
        (User.email == email_or_username.lower()) |
        (User.username == email_or_username)
    ).first()

    if not user or not user.check_password(password):
        return jsonify({
            'error': 'invalid_credentials',
            'message': 'Email/username sau parolă incorectă'
        }), 401

    # Actualizează last_activity
    user.last_activity = datetime.utcnow()
    db.session.commit()

    # Generează token
    token = generate_token(user.id)

    return jsonify({
        'success': True,
        'message': 'Autentificare reușită!',
        'user': user.to_dict(),
        'token': token
    })


@auth_bp.route('/me', methods=['GET'])
@token_required
def get_me(current_user):
    """
    Obține informații despre utilizatorul curent

    Returns:
        - user: dict cu toate datele utilizatorului
    """
    return jsonify({
        'success': True,
        'user': current_user.to_dict()
    })


@auth_bp.route('/me', methods=['PUT'])
@token_required
def update_me(current_user):
    """
    Actualizează profilul utilizatorului curent

    Body JSON (toate opționale):
        - username: string
        - profile: string (M1 sau M2)
        - password: string (noua parolă)
        - current_password: string (necesară pentru schimbarea parolei)

    Returns:
        - success: bool
        - user: dict
    """
    data = request.get_json()

    if not data:
        return jsonify({
            'error': 'no_data',
            'message': 'Date lipsă'
        }), 400

    # Update username
    if 'username' in data:
        new_username = data['username'].strip()
        if len(new_username) >= 3:
            # Verifică unicitatea
            existing = User.query.filter(
                User.username == new_username,
                User.id != current_user.id
            ).first()
            if existing:
                return jsonify({
                    'error': 'username_exists',
                    'message': 'Acest username este deja folosit'
                }), 409
            current_user.username = new_username

    # Update profile
    if 'profile' in data and data['profile'] in ['M1', 'M2']:
        current_user.profile = data['profile']

    # Update password
    if 'password' in data:
        current_password = data.get('current_password', '')
        if not current_user.check_password(current_password):
            return jsonify({
                'error': 'wrong_password',
                'message': 'Parola curentă este incorectă'
            }), 400

        new_password = data['password']
        if len(new_password) < 6:
            return jsonify({
                'error': 'invalid_password',
                'message': 'Parola nouă trebuie să aibă minim 6 caractere'
            }), 400

        current_user.set_password(new_password)

    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Profil actualizat!',
        'user': current_user.to_dict()
    })


@auth_bp.route('/refresh', methods=['POST'])
@token_required
def refresh_token(current_user):
    """
    Reîmprospătează token-ul

    Returns:
        - token: string (nou token)
    """
    new_token = generate_token(current_user.id)

    return jsonify({
        'success': True,
        'token': new_token
    })


@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    """
    Logout (client-side - doar confirmă)

    În practică, cu JWT, logout-ul se face pe client
    prin ștergerea token-ului din localStorage

    Returns:
        - success: bool
    """
    return jsonify({
        'success': True,
        'message': 'Deconectat cu succes!'
    })
