import os
import sys
import logging
from datetime import timedelta

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, request, jsonify, session, send_from_directory
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Import configurations
from config import config

# Import database
from src.models.user import db

# Import routes
from src.routes.auth import auth_bp
from src.routes.student import student_bp
from src.routes.parent import parent_bp
from src.routes.excel import excel_bp
from src.routes.admin import admin_bp

# Try to import AI routes
AI_AVAILABLE = False
try:
    from src.routes.ai import ai_bp
    AI_AVAILABLE = True
except ImportError as e:
    logging.warning(f"AI features not available: {e}")
    ai_bp = None

def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

    # Load configuration
    app.config.from_object(config[config_name])

    # Initialize database
    db.init_app(app)

    # Setup CORS with specific origins
    CORS(app, 
         origins=app.config.get('CORS_ORIGINS', ['http://localhost:3000']),
         supports_credentials=True,
         allow_headers=['Content-Type', 'Authorization'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])

    # Setup rate limiting
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )

    # Apply rate limiting to auth endpoints
    limiter.limit("5 per minute")(auth_bp)

    # Setup logging
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = logging.FileHandler('logs/app.log')
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Application startup')

    # Register blueprints with error handling
    try:
        app.register_blueprint(auth_bp, url_prefix='/api')
        app.register_blueprint(student_bp, url_prefix='/api')
        app.register_blueprint(parent_bp, url_prefix='/api')
        app.register_blueprint(excel_bp, url_prefix='/api')
        app.register_blueprint(admin_bp, url_prefix='/api/admin')

        if AI_AVAILABLE:
            app.register_blueprint(ai_bp, url_prefix='/api')
            app.logger.info('AI features enabled')
        else:
            app.logger.warning('AI features disabled')

    except Exception as e:
        app.logger.error(f'Error registering blueprints: {e}')
        raise

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        if request.path.startswith('/api/'):
            return jsonify({'error': 'API endpoint not found'}), 404
        return send_from_directory(app.static_folder, 'index.html')

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        app.logger.error(f'Server Error: {error}')
        return jsonify({'error': 'خطأ داخلي في الخادم'}), 500

    @app.errorhandler(429)
    def ratelimit_handler(e):
        return jsonify({'error': 'تم تجاوز الحد المسموح من الطلبات'}), 429

    # Security headers
    @app.after_request
    def after_request(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        if app.config.get('SESSION_COOKIE_SECURE'):
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response

    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'ai_available': AI_AVAILABLE,
            'version': '1.0.0'
        })

    @app.route('/')
    def serve_index():
        return send_from_directory(app.static_folder, 'index.html')

    @app.route('/<path:path>')
    def serve_static(path):
        try:
            return send_from_directory(app.static_folder, path)
        except:
            return send_from_directory(app.static_folder, 'index.html')

    # Initialize database tables
    with app.app_context():
        try:
            db.create_all()
            app.logger.info('Database tables created successfully')
        except Exception as e:
            app.logger.error(f'Error creating database tables: {e}')
            raise

    return app

if __name__ == '__main__':
    # Get configuration from environment
    config_name = os.environ.get('FLASK_ENV', 'development')
    app = create_app(config_name)

    # Run with appropriate settings
    port = int(os.environ.get('PORT', 5001))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = config_name == 'development'

    app.run(host=host, port=port, debug=debug)
