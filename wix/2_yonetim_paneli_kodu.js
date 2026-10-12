// WIX VELO – YÖNETİM PANELİ KODU
// ÖNEMLİ: Bu sayfayı Wix'te "gizli / şifreli sayfa" yapın; müşteri telefonları burada görünür.
// Elemanların ID'leri:
//   #inputAnahtar (metin kutusu – yönetici şifresi)  #btnYukle (buton)  #textDurum (metin)
//   #repeaterLeadler (Repeater). Repeater'ın içinde: #textIsim  #textTelefon  #textMesaj  #textTarih
import { fetch } from 'wix-fetch';

// BURAYI DEĞİŞTİRİN: Render adresiniz (sonunda / olmasın)
const API = 'https://SENIN-ADRESIN.onrender.com';

$w.onReady(function () {
  // Her satır (item) için metinleri doldurur. Kural: satır içinde $item kullanılır.
  $w('#repeaterLeadler').onItemReady(($item, itemData) => {
    $item('#textIsim').text = itemData.isim;          // en önemli sütun solda (F-Pattern)
    $item('#textTelefon').text = itemData.telefon;
    $item('#textMesaj').text = itemData.mesaj || '';
    $item('#textTarih').text = itemData.tarih;
  });
  $w('#btnYukle').onClick(yukle);
});

async function yukle() {
  $w('#textDurum').text = 'Yükleniyor...';
  try {
    const anahtar = encodeURIComponent($w('#inputAnahtar').value);
    const r = await fetch(`${API}/api/leads?anahtar=${anahtar}`, { method: 'get' });
    const veri = await r.json();
    if (veri.basari) {
      // Backend her kayıtta _id veriyor; Repeater için gerekli
      $w('#repeaterLeadler').data = veri.leadler;
      $w('#textDurum').text = veri.leadler.length + ' kayıt';
    } else {
      $w('#textDurum').text = veri.hata;
    }
  } catch (e) {
    $w('#textDurum').text = 'Liste alınamadı.';
  }
}
