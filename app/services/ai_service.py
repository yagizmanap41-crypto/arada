"""
ai_service.py — YAPAY ZEKÂ ÇAĞRILARI. AI İSTEKLERİ SADECE BU DOSYADA YAPILIR.
Bu dosya Flask'ı, HTTP rotalarını veya veritabanını BİLMEZ; sadece yapay zekâ ile konuşur.
"""
import requests
from config import Config

GROQ_URL = 'https://api.groq.com/openai/v1/chat/completions'
MAKS_GECMIS = 10  # yapay zekâya en fazla son 10 mesajı gönderiyoruz


class AIServiceError(Exception):
    """Yapay zekâ servisinde bir sorun olduğunda fırlatılan özel hata."""


class AIService:
    def _sistem_talimati(self):
        """Yapay zekânın kişiliğini (BUSINESS_CONTEXT) config'den okur."""
        return Config.BUSINESS_CONTEXT

    def _mesajlari_hazirla(self, mesaj, gecmis):
        """Groq'un beklediği sıra: önce sistem talimatı, sonra geçmiş, en sonda yeni mesaj."""
        mesajlar = [{'role': 'system', 'content': self._sistem_talimati()}]
        for parca in (gecmis or [])[-MAKS_GECMIS:]:
            # Sadece güvenli rolleri ve metinleri kabul et
            if isinstance(parca, dict) and parca.get('role') in ('user', 'assistant') \
                    and isinstance(parca.get('content'), str):
                mesajlar.append({'role': parca['role'], 'content': parca['content'][:1000]})
        mesajlar.append({'role': 'user', 'content': mesaj})
        return mesajlar

    def _groq_cagir(self, mesajlar):
        """Groq API'sine requests.post ile istek atar ve cevap metnini döndürür."""
        basliklar = {
            'Authorization': f'Bearer {Config.GROQ_API_KEY}',
            'Content-Type': 'application/json',
        }
        govde = {
            'model': Config.GROQ_MODEL,
            'messages': mesajlar,
            'temperature': 0.6,
            # Yeni modeller önce "düşünür"; düşünme de bu sınıra dahildir, o yüzden geniş tutuldu
            'max_completion_tokens': 1024,
        }
        try:
            yanit = requests.post(GROQ_URL, headers=basliklar, json=govde, timeout=30)
            yanit.raise_for_status()
            icerik = yanit.json()['choices'][0]['message'].get('content') or ''
        except (requests.RequestException, KeyError, IndexError, ValueError) as hata:
            raise AIServiceError(f'Groq çağrısı başarısız: {hata}') from hata
        icerik = icerik.strip()
        if not icerik:
            raise AIServiceError('Yapay zekâ boş cevap döndürdü.')
        return icerik

    def yanit_uret(self, mesaj, gecmis=None):
        """Kullanıcı mesajına yapay zekâdan cevap üretir."""
        # Anahtar yoksa çökmek yerine "demo modu" cevabı ver
        if not Config.GROQ_API_KEY:
            return ('[Demo modu] Yapay zekâ anahtarı tanımlı değil. '
                    'Şunu yazdınız: "' + mesaj[:80] + '"')
        return self._groq_cagir(self._mesajlari_hazirla(mesaj, gecmis))


# Dosya sonunda tek bir örnek; diğer dosyalar bunu import eder
ai_service = AIService()
