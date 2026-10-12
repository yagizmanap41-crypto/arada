"""
__init__.py — UYGULAMA FABRİKASI. Tüm parçaları birleştirir.
Sıra: ayarları yükle → CORS'u aç → veritabanını hazırla → rotaları kaydet.
"""
import os
from flask import Flask, jsonify, request
from config import config
from app.database import init_db


def create_app(config_name=None):
    app = Flask(__name__)

    # 1) Ayarları yükle (APP_ENV: development / production)
    config_name = config_name or os.environ.get('APP_ENV', 'default')
    app.config.from_object(config.get(config_name, config['default']))

    # 2) CORS: Wix sitesinin bu sunucuya erişmesine izin verir (sadece /api için)
    @app.after_request
    def cors_ekle(yanit):
        izinli = [o.strip() for o in app.config['CORS_ORIGINS'].split(',') if o.strip()]
        origin = request.headers.get('Origin')
        if request.path.startswith('/api') and origin and ('*' in izinli or origin in izinli):
            yanit.headers['Access-Control-Allow-Origin'] = '*' if '*' in izinli else origin
            yanit.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Admin-Key'
            yanit.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
            yanit.headers['Vary'] = 'Origin'
        return yanit

    # 3) Veritabanını hazırla (tablo yoksa oluşturur)
    init_db(app)

    # 4) Rotaları kaydet (circular import olmasın diye burada import edilir)
    from app.routes import api, sayfalar
    app.register_blueprint(sayfalar)
    app.register_blueprint(api, url_prefix='/api')

    # Canlılık kontrolü: sunucu ayakta mı?
    @app.route('/health')
    def health():
        return jsonify({'durum': 'aktif'})

    return app
