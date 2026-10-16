# Görev: sözlü çıkmış PDF'inin okunması (2. aşama)

`kaynak.pdf` (433 sayfa) 7 dersin sözlü çıkmış sorularını birleştiriyor. Amaç: her sorunun cevabını görselden yazıya dökmek. Sonra ayrı bir oturumda kümeleme ve site yapılacak; bu görevin kapsamı yalnızca bölge + okuma.

## Dosyalar
- `kaynak.pdf` — repo kökünde, git'e ekleme (`.gitignore`).
- `data/bolumler.json` — bölüm (konu etiketi) → sayfa aralığı. Her sorunun `konu` alanı buradan gelir.
- `data/bolgeler.json` — soru kayıtları. **Nefroloji (N-) hazır, 172 kayıt: dokunma.** Diğer bölümler için sen ekleyeceksin.
- `data/sayfa_envanteri.csv` — sayfa başına metin katmanı türü (DAKTILO / KARISIK / OCR / YOK).
- `data/aday_satirlar_diger_bolumler.json` — metin katmanından bulunan olası soru satırları (SADECE İPUCU, hatalı olabilir; doğrulamadan kullanma).
- `data/ornek_okumalar.md` — **kalite standardı.** Başlamadan tamamını oku (5 sayfa: el yazısı, karışık, taranmış, kâğıt fotoğrafı, slayt).
- `data/okumalar/<id>.md` — senin çıktın, kayıt başına bir dosya.
- `PROGRESS.md` — ilerleme takibi (aşağıya bak).
- `tools/render.py` — `page <n> [dpi] [--grid]` sayfayı (isteğe bağlı pt cetvelli) PNG yapar; `region <id> [dpi]` bir kaydın bölgesini keser. Çıktılar `tmp/` içine gider, `tmp/` git'e girmez. Görselleri Read ile **kendin oku**.

## Numaralama ve kimlik (karar verildi)
- Nefroloji: dosyadaki numara korunur: `N-36`. 101–104 dosyada iki kez geçer: `N-101a` (s.57–61), `N-101b` (s.63–65). 43 numara dosyada yok.
- Diğer bölümlerde soru numarası yoksa ya da numaralar öğrenci listesine göre tekrar başlıyorsa, **bölüm içinde yazılış sırasına göre** sıra numarası ver: Gastro `G-1, G-2…`, Romatoloji `R-`, Hematoloji `H-`, Endokrin `E-`, Onkoloji `O-`, İmmünoloji `I-`. Dosyadaki özgün numara varsa `orijinal_no` alanında sakla (yoksa `null`).
- `konu` alanı = bölümün adı (`bolumler.json`).

## bolgeler.json şeması (bir kayıt)
`id, konu, no (sıra no), orijinal_no, dup, hoca, text (soru metni), text_src ("D" daktilo | "E" el yazısı), start {page, y}, end {page, y}, segments [{page, y0, y1}], pages [ilk, son]` — y değerleri PDF noktası (pt), sayfa 612×866.73 pt, y yukarıdan aşağı. Nefroloji kayıtlarına bak, aynısını üret.
Bölge kuralı: sorunun cevabı, kendi soru satırından **bir sonraki soru satırına kadar** (sayfa geçişleri dahil). Üst kenar boşluğundaki (y ≤ 80) boş kısımlar segmentlere alınmaz. Soru satırı = sorunun başladığı yer (el yazısı başlık da olabilir; ara başlıkları soru sayma).

## İş akışı (10'arlı gruplar)
**A) Nefroloji (N-)**: bölgeler hazır. 10 kayıtlık gruplarla (sıra no'ya göre) çalış.
**B) Diğer bölümler**: 10 SAYFALIK gruplarla çalış. Her grupta önce bölümle, sonra oku:
1. Sayfaları `render.py page <n> --grid` ile gör; soru başlangıçlarını görsel olarak bul (aday satırlar yardımcıdır; metin katmanı olmayan/OCR sayfalarda tamamen görsel). y'yi cetvelden pt olarak al.
2. Kayıtları `bolgeler.json`'a sıra numarasıyla ekle. Grup sınırında soru bir sonraki gruba taşıyorsa, o soruyu bir sonraki grupta tamamla (kaydı açık bırakıp PROGRESS.md'ye yaz).
3. Her kayıt için `render.py region <id>` ile bölgeyi gör ve oku.
Bölüm ilk sayfasındaki başlık ("GASTRO ÇIKMIŞ" vb.) soru değildir.

## Okuma kuralları (aynen geçerli)
- Görünür (gerçek) metin katmanından gelen yazı: aynen al, değiştirme. Tespit: `pdftotext`/PDF'te `Tr 3` (görünmez) olan metin gizli OCR'dır, GÜVENME; olmayanlar gerçek daktilodur. Pratikte: el yazısı sayfalarda (OCR katmanlı) yalnız soru satırlarını ve yazılı kutuları katmandan al; gerisini görselden oku. Hatalı yazımlar ("atıhmını") olduğu gibi kalır.
- Ekran görüntüsündeki basılı yazı: görsel olarak oku.
- Dijital el yazısı: görsel oku. Çok sütunlu notlarda okuma sırasını koru. Oklar ve semboller (↑ ↓ ⇒ ↳) korunur.
- Kâğıt fotoğrafı veya okunamayan yer: `[OKUNAMADI]` yaz, ASLA tahmin etme.
- Emin olmadığın kelimeler, özellikle sayı, doz ve ilaç adları: `[?]` ile işaretle.
- Her parçayı kaynağına göre etiketle: `[DAKTİLO]` (gerçek metin katmanı), `[SLAYT]` (görüntü içindeki basılı yazı/tablo/tarama), `[EL YAZISI]`, `[OKUNAMADI]`.
- **OCR araçlarına (tesseract vb.) ve metin katmanındaki gizli OCR'a güvenme.** Görselleri kendin oku.
- Sarı/renkli vurgular okumaya taşınmaz (karar bekliyor: onaylanırsa `**…**`). Çizik/üstü çizili yerleri `[üstü çizili: …]` diye not et.
- Resim/diyagramda yazı yoksa tek satırda tarif et: `(resim: …)`.
- Kendi bilgini ekleme, eksik tamamlama, düzeltme yapma.
- Soru metni ile cevap ayrı yazılır. `data/ornek_okumalar.md` biçimini izle.

## Çıktı biçimi (`data/okumalar/<id>.md`)
```
---
id: G-12
konu: Gastroenteroloji
hoca: Kubilay Çınar   # yoksa —
sayfa: 114-115
orijinal_no: null
---
## Soru
[DAKTİLO] …
## Cevap
[SLAYT] …
[EL YAZISI] …
```
Cevabı boş olan soru: `## Cevap` altına `(cevap yok)` yaz. Bölge başka dersin içeriğine kaymışsa (yanlış sınır) `> ⚠` notu düş ve PROGRESS.md'ye yaz.

## İlerleme ve commit
- `PROGRESS.md`: bölüm bazında tablo/liste: bitmiş gruplar, açık bırakılan kayıtlar, toplam `[?]` ve `[OKUNAMADI]` sayısı, güvenilirlik notları (kopya, atlanan numara, bozuk sayfa).
- Her grup sonunda kendin doğrula (her kayıt için okumalar dosyası var mı, `bolgeler.json` geçerli JSON mı), sonra commit: `okuma: <ilk-id>..<son-id>`. Bitince push et.
- Tüm sayfaları tek oturumda/sohbette okumaya çalışma; bir grup bitince devam et, bağlam dolarsa PROGRESS.md'den sürdür.

## Sıra
1. N- (172 kayıt, ~17 grup). 2. Gastro (s.95–196). 3. Romatoloji (197–275). 4. Hematoloji (276–344). 5. Endokrin (345–418; s.345–367'de metin katmanı bozuk, tamamen görsel). 6. Onkoloji (419–428; tamamen görüntü). 7. İmmünoloji (429–433).
