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

Toplam (N-1..N-72): [?] = 149, [OKUNAMADI] = 4 (aşağıdaki [?] sadeleştirmesi sonrası).

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

## Kararlar
- Bölge sınırları bolgeler.json'a uygulandı (N-49/N-50, N-50/N-51, N-52/N-53, N-60/N-61); okumalar ve ⚠ notları güncellendi:
  - N-49 sonu / N-50 başı: s.15 y=546.0 (N-50 y=550.0).
  - N-50'ye ikinci segment eklendi: s.16 y0=0→18.2 (N-51 başlangıcı); "* Böbrekler hiperpotasemiye 12 saatte cevap verirler…" notu N-50'ye alındı. N-51'de "yukarıda ; (135-145 mEq/L" soru satırının üst notu olarak kaldı.
  - N-52 sonu / N-53 başı: s.17 y=619.0 (N-53 y=623.0).
  - N-60 sonu / N-61 başı: s.21 y=255.0 (N-61 y=259.0); "Cockcroft - Gault Formülü" başlığı artık N-61'de.
  - N-68/N-69: kutu iki kayıtta da duruyor, N-69'a "> ⚠ bölge sınırında kutu, N-68 ile ortak" notu konuldu.
  - N-53 ve N-55 `text` alanları bolgeler.json'da zaten doğru ("Nefrotik Sendrom Tanı Kriterleri", "ABY'ni her şeyiyle anlat"; text_src "E"); önceki "yanlış" tespitim `textlayer.py` çıktısındaki metin katmanını JSON sanmamdandı. JSON değişmedi.
- [?] ölçütü sadeleştirildi (yalnız okunuşu gerçekten iki türlü olabilen rakam/doz/birim/ilaç adı; net okunanlarda [?] yok). Kaldırılan [?]: N-37: 39 · N-39: 24 · N-40: 22 · N-48: 15 · N-52: 44 · N-55: 36 = 180; ayrıca aynı ölçütle N-51: 23 · N-58: 4 · N-59: 11 · N-61: 4 · N-63: 20 · N-64: 20 = 82. Toplam kaldırılan: 262. Bundan sonra aynı ölçüt kullanılıyor.

## İlerleme günlüğü (otomatik)
- N-73..N-110 bitti (s.28–67). Kâğıt fotoğrafı sayfaları: s.28 alt (N-74), s.29, s.30, s.31 üstü (slayt altında kısmen örtülü), s.36 üst (N-80). Fotoğraflar 240–300 dpi parçalarla okundu.
- Tekrar eden slaytlar/taramalar (RPGN, Sekonder HT, Mogensen, Hiponatremi şeması vb.) farklı kayıtlarda aynı görsel olduğundan her kayıtta tekrar yazıldı (kaynakta tekrar).
- N-101b: bölge yalnız soru satırı (y 72–96); altındaki "132- RPGN nedenleri" soru satırı başka bir kayda ait → (cevap yok).
- N-82 düzeltildi: Ekzojen sebepler listesi (Kafein, Kokain, Alkol) ve son satır ("polisitemi ve hiperviskozite").
- Araçlar: tools/tile.py (parça kes), tools/strip.py (sayfa şeridi), tools/imgs.py (bölgedeki görseller), tools/yaz.py (yazıcı), tools/dogrula.py (kontrol).

## Nefroloji bitti (N-1..N-169; 172 kayıt: N-43 dosyada yok, N-101a/b, N-102a/b, N-103a/b, N-104a/b ikili)
- Toplam [?] = 213, [OKUNAMADI] = 19 (Nefroloji).
- Kalite kontrol (5 grup): N-137 ve N-150 görselle yeniden karşılaştırıldı (el yazısı notlar + slayt metni); fark yok. N-144 tablosunda bir rakam düzeltildi (G4 A1: 3 (0.6%)).
- Kâğıt fotoğrafları: N-161 (s.91, gölgeli, iki fotoğraf) ve N-167 (s.93, iki fotoğraf; sağ fotoğrafın sağ kenarı fotoğraf sınırında kesik → [kesik]/[OKUNAMADI]) 240–300 dpi parçalarla okundu; N-161'de siyahla çizilmiş bölüm üstü çizili olarak not edildi.
- N-145, N-146: yalnız soru; (cevap yok). N-24, N-25, N-32, N-35, N-14, N-65: cevap başka bir soruya gönderme.
- belirsiz sınır: N-160 (s.90) cevabı ile N-161 başlığı arasında bölge temiz; N-153 ve N-154 arasında "152. görsel" el yazısı notu sayfa üst kenarında (s.87 üst) N-153 bölgesinde değil N-154'e düşüyor; N-154'te not edildi.
- N-157/N-158 sınırı s.88 y=292: "Unutmayalım primer…" kutusu ve "Primer:" paragrafı metin katmanında tek satıra karışmıştı; görsele göre ayrıldı.

## Gastro (G-) — BAŞLADI, DURDU (kullanım limiti)
- bolgeler.json'a G-1..G-15 eklendi (s.95–105, tools/ekle.py ile); yalnız G-1 okundu (data/okumalar/G-1.md). G-2..G-15 okuması bekliyor.
- Belirsiz sınırlar: G-2 (s.96 başı → s.97 başındaki "kronik pankreatitin…" devamı dahil); G-5 ve G-7 (aynı hocanın ardışık yazılı paragrafları ayrı soru sayıldı); G-17/G-18 (s.105 y172 / y185: iki satırlık bitişik soru) henüz eklenmedi.
- Sıradaki grup: s.105–114 (başlangıçlar: s105 y23, y172, y185, y252; s107 y12, y487, y673; s108 y12, y401, y610; s110 y144, y235; s111 y8, y89, y178, y565; s112 y20; s113 y17, y288; s114 y15, y339, y472…); ardından s.115–196, Romatoloji, Hematoloji, Endokrin, Onkoloji, İmmünoloji.
- Araçlar: tools/ekle.py (bölge ekle), satirlar.py (görünür paragraf başları), tile.py, strip.py, imgs.py, yaz.py, dogrula.py.

## Gastro ilerleme (güncel)
- G-1..G-27 okundu (s.95–110; bolge: G-27 sonu s.111 y8'e kadar). [?]=36, [OKUNAMADI]=4 (Gastro, şimdilik).
- Belirsiz sınır: G-4/G-5/G-6/G-7 (aynı hocanın bitişik kısa soruları ayrı sayıldı); G-17 yalnızca "Yukarıda anlattım hepsini"; G-18 s.105–106 el yazısı ishal şeması.
- Sıradaki: s.111 başı (y8, 89, 178, 565) → s.112 y20 → s.113 y17, y288 → s.114 (y15, 339, 472…).

## Kalite kontrol (kâğıt fotoğrafı: ok/parantez/[?] taraması)
- N-74 düzeltildi (s.28–30 görselle yeniden karşılaştırıldı): "Böbrek korunması" → "Böbrek kanlanması [?]"; "Karama [?]" → "Kanama" (GİS'teki yazıyla aynı; GİS'te zaten "Kanama"); Prerenal ABH'de ok eşleşmeleri korundu (Hemoraji → Gerçek hipovolemi; GİS → diyare, kusma; Renal → yoğun diüretik; Cilt → yanıklar; 3. boşluk → hemorajik sıvı, bağırsak obstrüksiyonu); süslü parantez "Etkin arteriel dolaşım volümü azalması" hem Sistemik vazodilatasyon hem Renal vazokonstriksiyon için yazıldı; "ARB / RAS" → "ARS/ARB [?] / RAS"; gereksiz [?] kaldırıldı (%40-70, %5-10, 6-12 sn, 12-24 sn, "normalde de var artmış olabilir"); %10-30, "%30'unda", "Prömonitis" için [?] korundu.
- N-74'te aynı iki hata türü başka yerlerde de bulundu ve düzeltildi: (a) ATN Fizyopatolojisi (s.30) düz zincire çevrilmişti → ağaç yapısı geri kuruldu (Renal Hasar → Hemodinamik bozukluklar [Mezensiyal kontraksiyon→KUF↓; Vazokonstriksiyon→RPF↓,P↓; Medüller konjesyon→Tübüler hasar] ve Tübüler hasar [Tıkanma, Geri kaçak]; dört dal → GFR↓); (a) Etiyolojik sınıflama (s.28) Prerenal/Renal/Postrenal dalları ayrı satırlara ayrıldı; (a) "Ürik asit ve myeloma" parantez eşleşmesi (ürik asit → tümör lizis send.; myeloma → hafif zincirleri); (b) "antifriz?" yanına [?], "Top limeni" yanına [?] eklendi.
- Taranan diğer kâğıt fotoğrafı kayıtları: N-80, N-161, N-167, G-12 — okuma dosyalarında oklar zaten dal/dal yazılı, ek düzeltme yapılmadı (G-12 fotoğraf 1–7 için yalnız metinle gözden geçirme; görsel tekrar karşılaştırma yapılmadı).
- Kural: Gastro G-28'den itibaren kâğıt fotoğrafı sayfalarında oklarla bağlı öğeler ağaç/eşleşme olarak yazılacak, anlamsız çıkan kelimeye [?] konacak.
- ADIM 1 (bölge görseliyle satır satır karşılaştırma; N-80, N-161, N-167, G-12 + rastgele N-120, N-160):
  - N-80: (c) "psödobulber paralizi [?]" ve "DTR azalma [?]" okunaklı → [?] kaldırıldı.
  - N-161: (c) okunaklı sözcüklerden [?] kaldırıldı (Hiperparaproteinemi [yazım düzeltildi: görselde "Hiperparaproteinemi"], Gliserol tedavisi, 3. boşluğa sıvı kaybı, Akut BH, Demeklosiklin, V2 res); "Mannitol"→"Manitol" (el yazısı); "aşırı terleme yok [?]" → "aşırı terleme , yanık [?]" (görselde "yanık" okunuyor, tıbben mantıklı, [?] kaldı).
  - N-167: (c) "idrar miktarı artabilir. [?]" ve "DM [?]" kaldırıldı; kalan içerik görselle uyumlu.
  - G-12: (a) fotoğraf 1'deki Ü.Kolit | Crohn tablosu satır-satır eşleşmiş gibi yazılmıştı → iki ayrı sütun olarak yeniden yazıldı; (c) "%60-70 [?]" kaldırıldı; "İshal ikinden [?]" → "İshal ikveren [?]"; "Faktör 13 [?]", "Posit (%10-60) [?]", "Fertilitede Azalma (%50-98) [?]", "Gaita dethline [?]" tıbben şüpheli/rakam belirsiz olduğundan korundu. Foto 5–7 (sayfa 103) görselle uyumlu.
  - N-120 ve N-160 (rastgele): N-120 görselle birebir uyumlu, fark yok. N-160: (c) son el yazısı satırdaki iki [?] kaldırıldı ("Olgu sorusunu tersten sormuş aklında bulunsun.").
