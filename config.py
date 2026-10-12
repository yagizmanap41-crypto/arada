"""
config.py — TÜM AYARLAR BURADA.
Gizli bilgiler (şifre, API anahtarı) koda yazılmaz; ".env" dosyasından okunur.
"""
import os
from dotenv import load_dotenv

# .env dosyasını okur. Bu satır olmazsa .env'deki değerler gelmez!
load_dotenv()

# --- Yapay zekânın "kim olduğunu" anlatan metin ---------------------------------
# Kodun geri kalanı HER İŞ İÇİN AYNIDIR; sadece bu metin işe göre değişir.
ARADA_BUSINESS_CONTEXT = """Sen ARADA'nın sohbet asistanısın. ARADA; insanların gün içindeki
boş zamanlarını (15 dakikadan birkaç saate kadar) süreye, bütçeye, ruh haline ve enerjiye göre
anlamlı aktivitelere çeviren bir web platformudur. Slogan: "Aradaki zamanı yaşa."

NASIL DAVRANIRSIN:
- Türkçe, samimi, kısa ve pozitif konuş. En fazla 3-4 cümle yaz. Yargılama; "verimli olmalısın" baskısı yapma.
- Önce kullanıcının ne kadar boş zamanı olduğunu sor. Gerekirse bütçesini ve ruh halini de öğren.
- En fazla 3 öneri sun. Öneriler genel aktivite türleri olsun (kısa yürüyüş, kafede mola, mini sergi gibi).
- Belirli bir mekan adı, adres, fiyat veya saat BİLMEDİĞİN için ASLA uydurma. Şehir/semt öğrenirsen
  genel öneri ver ve bunun örnek olduğunu belirt.
- Kullanıcı önerilerle ilgilenirse, ona özel öneriler için ad ve telefon bırakmasını nazikçe iste.
- ARADA dışındaki konularda (ödev, siyaset, tıbbi tavsiye vb.) kibarca konuya dön.
"""

class Config:
    """Her ortamda ortak olan ayarlar."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'gelistirme-icin-gizli-anahtar')
    DATABASE_URL = os.environ.get('DATABASE_URL', 'leads.db')   # SQLite dosyasının yolu
    AI_PROVIDER = os.environ.get('AI_PROVIDER', 'groq')
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')
    # NOT: Yönergedeki "llama-3.1-8b-instant" modeli 16 Ağustos 2026'da kapatıldı.
    GROQ_MODEL = os.environ.get('GROQ_MODEL', 'openai/gpt-oss-20b')
    BUSINESS_CONTEXT = os.environ.get('BUSINESS_CONTEXT', ARADA_BUSINESS_CONTEXT)
    ADMIN_KEY = os.environ.get('ADMIN_KEY', '')                  # boşsa panel şifresizdir (sadece yerelde)
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')           # virgülle ayrılmış adresler
    DEBUG = False


class DevelopmentConfig(Config):
    """Kendi bilgisayarınızda çalışırken."""
    DEBUG = True


class ProductionConfig(Config):
    """Canlıda (Render) çalışırken."""
    DEBUG = False


# APP_ENV değerine göre doğru sınıfı seçen sözlük
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
