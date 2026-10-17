# Birleşik cevap yazma (aşama 3) ve site üretimi (aşama 4)

## Yapı
- `data/kumeler.txt`: konu başlıkları ve kümeler (`## Konu [Ders]` altında `- Küme başlığı :: id, id, ...`). Her kayıt tam bir kümede. Yeni kayıt (Endokrin, Onkoloji, İmmünoloji, Hematoloji'nin kalanı) eklenince ilgili kümeye eklenir ya da yeni küme açılır.
- Küme kimliği = kümenin ilk kaydının id'si, başına `c-` (ör. `c-N-2`). Kümenin ilk kaydı değişirse birleşik dosyanın adı da değişir.
- Kaynak harfleri kümedeki sıraya göredir: ilk id = A, ikinci = B... (`N-2, N-40, N-41, N-54, N-149` → A..E). Sırayı bozma; bozarsan harfler kayar.
- `data/birlesik/<küme_id>.md`: birleşik cevap. Yalnız birden fazla kayıtlı kümeler için. `python3 build_site.py --todo` yazılmamışları listeler.
- `python3 build_site.py` → `docs/index.html`. Harf hatalarını (kümede olmayan kaynak harfi) denetler ve hata verirse durur.
- Sayfa görüntüleri: `python3 tools/kirp.py kaynak.pdf` → `docs/img/<id>.webp` (170 dpi, değiştirilmemiş kırpma; var olanı atlar, yeni kayıtlar için yeniden çalıştır).
- Hematoloji kayıtları (H-9001, H-9002) yeniden numaralandırılınca (`tools/renumber.py H`) `data/kumeler.txt` içindeki H id'leri ve `docs/img/H-*.webp` yeniden üretilmeli.

## Kurallar (örnek: data/birlesik/c-N-2.md ve c-N-49.md)
1. Yalnızca kümedeki okumalarda (`data/okumalar/`) geçen bilgi yazılır. Kendi bilginle ekleme, düzeltme, tamamlama yok; yanlış görünse bile yazıldığı gibi.
2. Her madde sonuna kaynak etiketi: `[A]`, `[A, C]`. El yazısından okunmuş maddeler ayrı etiketlenir: `[B·el yazısı]`, `[B, D·el yazısı]`. Aynı maddeyi hem daktilo/slayt hem el yazısı kaynak veriyorsa iki ayrı etiket: `[A, E] [B, D·el yazısı]`.
3. Okumadaki `[?]` birleşik metinde de kalır. `[OKUNAMADI]` içerik olarak alınmaz.
4. Kaynaklar birbirini yalanlıyorsa ya da sayı/eşik/isim farklıysa, birleştirme yapmadan ilgili bölümün altında şu biçimde göster:
   `> ⚠ Kaynaklar çelişiyor: **Konu:** [A] "…"; [B] "…".`
   Hangisinin doğru olduğuna karar verme.
5. Bir kaynakta olup diğerlerinde olmayan ayrıntı atılmaz; yalnız o kaynağın etiketiyle yazılır.
6. Okumaların sorusundaki öğrenci anlatısı ("dedim", "sordu") cevap sayılmaz; yalnız `## Cevap` bölümünden birleştirilir. Cevap bölümü başka sorunun içeriğini taşıyorsa (kaynakta kayma) o kısmı alma, ⚠ not düş.
7. Biçim: `### Alt başlık`, `- madde`, gerekirse `| tablo |`. Kısa ve taranabilir; her madde kendi etiketini taşır.
8. `(cevap yok)` olan kaynaklar birleşikte görünmez; yalnız "Gerçek cevaplar" altında listelenir.
9. N-101a/b, N-102a/b... gibi aynı sorunun iki kopyası ayrı harf alır ama tek soru sayılır.

## Çalışma sırası
- `python3 build_site.py --todo` listesini yukarıdan aşağı (tekrar sayısı büyükten küçüğe) yap.
- Her 10 küme sonunda `python3 build_site.py` (hata yoksa) + commit: `birlesik: <ilk_küme>..<son_küme>`.
- Sonunda `docs/index.html` yeniden üretilip push'lanır.
