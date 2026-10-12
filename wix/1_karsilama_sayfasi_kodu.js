// WIX VELO – KARŞILAMA SAYFASI KODU
// Bu kodu Wix'te "karşılama sayfanızın" kod bölümüne yapıştırın (Dev Mode açık olmalı).
// Sayfadaki elemanların ID'leri AŞAĞIDAKİYLE BİREBİR AYNI olmalı:
//   #girisMesaj (metin kutusu)  #btnSor (buton)  #textCevap (metin)
//   #inputIsim (metin kutusu)   #inputTelefon (metin kutusu)  #btnKaydet (buton)  #textDurum (metin)
import { fetch } from 'wix-fetch';

// BURAYI DEĞİŞTİRİN: Render'ın size verdiği adres (sonunda / olmasın)
const API = 'https://SENIN-ADRESIN.onrender.com';

let gecmis = [];   // konuşma geçmişi; yapay zekâ önceki mesajları hatırlasın diye

$w.onReady(function () {
  $w('#btnSor').onClick(sor);
  $w('#btnKaydet').onClick(kaydet);
});

async function sor() {
  const mesaj = $w('#girisMesaj').value.trim();
  if (!mesaj) { return; }
  $w('#textCevap').text = 'Düşünüyorum... (ilk soruda 1 dakikaya kadar sürebilir)';
  try {
    const r = await fetch(`${API}/api/sohbet`, {
      method: 'post',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mesaj: mesaj, gecmis: gecmis })
    });
    const veri = await r.json();
    if (veri.basari) {
      $w('#textCevap').text = veri.cevap;
      gecmis.push({ role: 'user', content: mesaj }, { role: 'assistant', content: veri.cevap });
      $w('#girisMesaj').value = '';
    } else {
      $w('#textCevap').text = veri.hata;
    }
  } catch (e) {
    $w('#textCevap').text = 'Bağlantı kurulamadı, lütfen tekrar deneyin.';
  }
}

async function kaydet() {
  const isim = $w('#inputIsim').value.trim();
  const telefon = $w('#inputTelefon').value.trim();
  // Son kullanıcı mesajını "mesaj" alanına koyuyoruz (ne istediğini bilelim)
  const sonMesaj = gecmis.length >= 2 ? gecmis[gecmis.length - 2].content : '';
  try {
    const r = await fetch(`${API}/api/leads`, {
      method: 'post',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ isim: isim, telefon: telefon, mesaj: sonMesaj })
    });
    const veri = await r.json();
    $w('#textDurum').text = veri.basari ? 'Teşekkürler! Bilgilerin kaydedildi.' : veri.hata;
  } catch (e) {
    $w('#textDurum').text = 'Kaydedilemedi, lütfen tekrar deneyin.';
  }
}
