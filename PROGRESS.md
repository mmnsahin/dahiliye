# İlerleme

## Araç notu
- Bu makinede `pdftoppm` yok; `tools/render.py` PyMuPDF (`pip install pymupdf`) ile yedeklendi. `python3` yerine `python` kullanılıyor.
- `tools/textlayer.py` + `tools/yaz_daktilo.py`: görünür metin katmanından iskelet üretir; her kayıt görselle karşılaştırılarak doğrulanır.
  - **Gizli OCR filtresi (düzeltildi):** `textlayer.py` ilk sürümde `get_text('blocks')` kullanıyordu; bu, render mode 3 (Tr 3) gizli OCR'ı da alıyor (ör. s.7'de 202 görünür / 1239 gizli karakter). Artık `get_texttrace()` ile yalnızca `type != 3` (görünür) karakterler alınır. N-1..N-10 çıktıları yeniden üretilip karşılaştırıldı: değişiklik yok (o sayfalarda gizli OCR yoktu).
- `tools/kes.py`: yüksek dpi bölge görselini okumak için üst üste binen parçalara böler (yoğun el yazısı sayfalar).
- Metin katmanındaki `ﬂ` ligatürü (N-40, "hedeﬂenmelidir") `fl` olarak yazıldı; tek kaynak-dışı değişiklik.

## Nefroloji (N-) — 172 kayıt
| Grup | Durum | [?] | [OKUNAMADI] |
|---|---|---|---|
| N-1..N-10 | bitti (s.1–2, saf daktilo) | 0 | 0 |
| N-11..N-20 | bitti (s.2–4, saf daktilo) | 1 | 0 |
| N-21..N-30 | bitti (s.4–6, saf daktilo) | 0 | 0 |
| N-31..N-40 | bitti (s.6–12; N-36..N-40 el yazısı/slayt/karışık) | 16 | 0 |
| N-41..N-45 | bitti (s.12–13; N-43 dosyada yok) | 3 | 0 |
| N-46..N-55 | bitti (s.13–19; yoğun el yazısı/slayt) | 175 | 3 |
| N-66..N-72 | bitti (s.23–27; N-70 s.24–26 taranmış/slayt) | 10 | 0 |
| N-56..N-65 | bitti (s.19–23) | 86 | 1 |

Toplam (N-1..N-72): [?] = 409, [OKUNAMADI] = 4.

Güvenilirlik notları:
- N-7: soru/cevap sayfa 1→2 geçişinde cümle ortasında bölünüyor; tek satıra birleştirildi.
- Sarı/mavi vurgular okumaya taşınmadı (karar bekliyor).
- N-19, N-20, N-33: metin sayfalarındaki yeşil el yazısı notlar ("3 Aktif", "24 saat", soru işareti) `[EL YAZISI]` olarak eklendi; yeşil çarpı/tik işaretleri yazıya alınmadı.
- N-24, N-25, N-32, N-35: cevap başka soruya gönderme ("8. soru", "13. soru", "10. Soru…"); olduğu gibi yazıldı.
- N-36..N-40: gizli OCR katmanı dolu sayfalar; soru satırı yalnız görünür katmandan alındı, geri kalanı görselden okundu.
- N-41 bölge sınırı düzeltildi: N-41 `y` 428.8→420.5, N-40/N-41 segment sınırı 424.8→416.5 (sağ üstteki hiperkalemi notu artık N-41 bölgesinde); ⚠ notu kaldırıldı.
- N-37: s.8 üst kenarında kesik 2 satırlık not ("ödem geçince ?…") ve tablo hizası belirsiz yerler; N-39: küçük slayt notları [?].
- N-38 cevabı yalnız soru satırı yanındaki tek satırlık el yazısı not.
- N-43 dosyada yok (bkz. başlangıç notu).

## [?] kuralı (el yazısı/slayt): ek tarama
Kural: el yazısında okunuşu iki türlü olabilen sayılar, her doz/birim, her ilaç adı ve ölçüm değeri `[?]`. Yalnız bu kategorilere bakıldı, başka bir şey değiştirilmedi.
ek [?]: N-20: 1 · N-36: 10 · N-37: 43 · N-39: 24 · N-40: 22 · N-41: 10 · N-42: 1 · N-44: 3 · N-45: 4 (toplam 118). N-19, N-33: 0.
Bu kural N-46'dan itibaren okurken baştan uygulanır.

## N-46..N-55 güvenilirlik / bölge notları
- ⚠ N-49: cevap el yazısının son satırları bölge alt kenarında yarım kesik (N-50 üst kenarına taşıyor); tam sayfadan okundu. Önerilen düzeltme: N-49/N-50 sınırı (sayfa 15) y=542.7 → ~546.0 (N-50 `y` ~546.7 → ~550.0). JSON'a dokunulmadı.
- ⚠ N-50: üst kenarda N-49'dan taşan çizgiler var (içerik değil). N-51: sayfa 16 üst kenarında (y<18) "… verirler , hipopotasemiye 7-14 günde yanıt)" satırı yarım kesik, hiçbir bölgeye girmiyor.
- ⚠ N-52/N-53: sayfa 17'de N-52'nin slaytı (KBH Komplikasyonlar ve Tedavisi) ve üstüne eklenmiş Osteopeni metninin son satırı sınırda (y=605) kesiliyor; önerilen sınır ~y=616. N-53 kaydının `text` alanı ("osteoporozun tersine bir hastalık değildir.") yanlış: gerçek soru el yazısı başlık "53- Nefrotik Sendrom Tanı Kriterleri" (`text_src` "E" olmalı). JSON'a dokunulmadı.
- N-47: bölgede yalnız soru var, cevap yok ("(cevap yok)"; sağ kenarda el yazısı ? işareti). N-55 de soru satırı el yazısı başlık ("55- ABY'ni her seviyle anlat"); bolgeler.json'daki `text` boş/uyumsuz olabilir.
- N-52: sayfa 17 alt kısmında çok küçük el yazısı notlar; okunamayanlar [OKUNAMADI], şüpheliler [?]. Bu kayıtta ve N-55 s.19'da slayt üzerindeki küçük el yazısı notların bir kısmı tam okunamadı.
- N-46: sayfa 13 üst kenardaki "(8.? – 10.5 mg/dL)" notunda "8."den sonraki rakam yazılmamış.
- [?] kuralı (sayı/doz/birim/ilaç) N-46'dan itibaren baştan uygulandı.

## N-56..N-65 notlar
- ⚠ N-60/N-61 sınırı (s.21, y≈272): N-61'in başlığı "Cockcroft - Gault Formülü" N-60 bölgesinin son satırlarında kalıyor; önerilen sınır ~y=262 (N-61 `y` ~276 civarı → ~266). JSON'a dokunulmadı.
- N-58 / N-48: aynı "Hematüri Nedenleri" slaytı iki kayıtta da tam yazıldı (kaynakta tekrar).
- N-59 / N-63 / N-52: KBH ve KDIGO notları sayfalar arasında birebir tekrar; her kayıt bağımsız okundu.
- N-65: cevap yalnızca "⇒ bunu yukarıda anlatmıştım ben de".

## N-66..N-72 notlar — DURDUM (N-73/N-74 kâğıt fotoğrafı, onay bekliyor)
- ⚠ N-68/N-69 sınırı (s.23, y=615.6): hipokomplementemi listesi (yeşil kutu, y≈587-637) sınırı ortadan kesiyor; kutu iki kayıtta da yazıldı. Önerilen sınır ~y=585 (N-68 end / N-69 start) — N-69 sorusu ise y=615.6'da başlıyor, yani soru satırı kutunun altında; sınır düzeltmesi N-68/N-69'un soru başlangıcını değil kutuyu hangi kayda ait sayacağınıza bağlı (karar bekliyor).
- N-70: s.24 üst kısım DAKTİLO (katman), tablo ve Mogensen tarama görüntüsü [SLAYT]; s.25 örnek okumadaki ile aynı, s.26 tarama. Sayfa başı/sonu sınırları temiz.
- N-72: soru satırındaki pembe oklar (ca ↓ p ↑ pth ↑) [EL YAZISI] olarak not edildi.
- Sonraki: N-73 (s.28) ve N-74 (s.28–31) kâğıt fotoğrafı sayfaları; talimat gereği burada durdum.
