"""run.py — Sunucuyu başlatan giriş noktası.
Bilgisayarda:  python run.py        Canlıda (Render):  gunicorn run:app"""
import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(port=int(os.environ.get('PORT', 5000)), debug=app.config['DEBUG'])
