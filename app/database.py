"""
database.py — VERİTABANI İŞLEMLERİ. SQL SADECE BU DOSYADA YAZILIR.
Müşteri adaylarını (lead) SQLite'a kaydeder ve listeler.
"""
import sqlite3
from flask import current_app


def get_db():
    """Veritabanına bağlanır. Satırlara sütun adıyla erişilir (satir['isim'])."""
    baglanti = sqlite3.connect(current_app.config['DATABASE_URL'])
    baglanti.row_factory = sqlite3.Row
    return baglanti


def init_db(app):
    """'leads' tablosunu oluşturur (zaten varsa dokunmaz). create_app içinde çağrılır."""
    with app.app_context():
        baglanti = get_db()
        try:
            baglanti.execute(
                """
                CREATE TABLE IF NOT EXISTS leads (
                    id      INTEGER PRIMARY KEY AUTOINCREMENT,
                    isim    TEXT NOT NULL,
                    telefon TEXT NOT NULL,
                    mesaj   TEXT,
                    tarih   TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            baglanti.commit()
        finally:
            baglanti.close()


def lead_ekle(isim, telefon, mesaj=''):
    """Yeni kayıt ekler, yeni kaydın id'sini döndürür.
    GÜVENLİK: değerler SQL metnine eklenmez; '?' yer tutucusu kullanılır (SQL Injection koruması)."""
    baglanti = get_db()
    try:
        imlec = baglanti.execute(
            "INSERT INTO leads (isim, telefon, mesaj) VALUES (?, ?, ?)",
            (isim, telefon, mesaj),
        )
        baglanti.commit()
        return imlec.lastrowid
    finally:
        baglanti.close()


def tum_leadler():
    """Tüm kayıtları en yeniden en eskiye doğru, sözlük listesi olarak döndürür."""
    baglanti = get_db()
    try:
        satirlar = baglanti.execute(
            "SELECT id, isim, telefon, mesaj, tarih FROM leads ORDER BY id DESC"
        ).fetchall()
        return [dict(satir) for satir in satirlar]
    finally:
        baglanti.close()
