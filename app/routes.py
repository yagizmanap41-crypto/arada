"""
routes.py — HTTP İSTEKLERİNİ KARŞILAR, DOĞRULAR, DOĞRU KATMANA YÖNLENDİRİR.
Burada SQL veya yapay zekâ kodu YOKTUR; sadece database.py ve ai_service.py fonksiyonları çağrılır.
"""
import hmac
from flask import Blueprint, current_app, jsonify, render_template, request
from app import database
from app.services.ai_service import ai_service, AIServiceError

sayfalar = Blueprint('sayfalar', __name__)   # /  ve  /dashboard
api = Blueprint('api', __name__)             # /api/... (önek create_app'te verilir)


def _hata(mesaj, kod):
    """Her hatayı aynı biçimde (basari: false) JSON olarak döndürür."""
    return jsonify({'basari': False, 'hata': mesaj}), kod


def _yetkili():
    """ADMIN_KEY tanımlıysa, gelen şifre ile karşılaştırır (güvenli karşılaştırma)."""
    beklenen = current_app.config.get('ADMIN_KEY', '')
    if not beklenen:
        return True   # şifre tanımlanmamış (yerel geliştirme)
    gelen = request.args.get('anahtar', '') or request.headers.get('X-Admin-Key', '')
    return hmac.compare_digest(gelen, beklenen)


# ---------------------------- SAYFALAR ----------------------------
@sayfalar.route('/')
def ana_sayfa():
    return render_template('index.html')


@sayfalar.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


# ------------------------------ API -------------------------------
@api.route('/sohbet', methods=['POST'])
def sohbet():
    veri = request.get_json(silent=True) or {}
    mesaj = (veri.get('mesaj') or '').strip()
    if not mesaj:
        return _hata('Lütfen bir mesaj yazın.', 400)
    if len(mesaj) > 1000:
        return _hata('Mesaj çok uzun (en fazla 1000 karakter).', 400)
    try:
        cevap = ai_service.yanit_uret(mesaj, veri.get('gecmis'))
    except AIServiceError:
        return _hata('Asistan şu an yanıt veremiyor, lütfen biraz sonra tekrar deneyin.', 503)
    return jsonify({'basari': True, 'cevap': cevap})


@api.route('/leads', methods=['POST'])
def lead_kaydet():
    veri = request.get_json(silent=True) or {}
    isim = (veri.get('isim') or '').strip()
    telefon = (veri.get('telefon') or '').strip()
    mesaj = (veri.get('mesaj') or '').strip()
    if not isim or not telefon:
        return _hata('İsim ve telefon zorunludur.', 400)
    if len(isim) > 100 or len(telefon) > 30 or len(mesaj) > 1000:
        return _hata('Girilen bilgilerden biri çok uzun.', 400)
    try:
        yeni_id = database.lead_ekle(isim, telefon, mesaj)
    except Exception:
        return _hata('Kayıt şu an yapılamadı, lütfen tekrar deneyin.', 500)
    return jsonify({'basari': True, 'id': yeni_id}), 201


@api.route('/leads', methods=['GET'])
def leadleri_getir():
    if not _yetkili():
        return _hata('Bu listeyi görmek için yönetici şifresi gerekir.', 401)
    try:
        leadler = database.tum_leadler()
    except Exception:
        return _hata('Liste şu an getirilemedi.', 500)
    for lead in leadler:
        lead['_id'] = str(lead['id'])   # Wix Repeater her kayıtta _id ister
    return jsonify({'basari': True, 'leadler': leadler})
