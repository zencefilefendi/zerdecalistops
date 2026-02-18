> [!CW]
> Tam veri sızıntılarını (data breaches) Zencefil Efendi'ye yüklemek yasaktır. Sadece, herhangi bir kullanıcıyla ilişkilendirilebilecek PII (Kişisel Tanımlanabilir Bilgiler) içermeyen şifreleri yükleyebilirsiniz.

## Katkıda Bulunma

Eğer aklınızda eklenmesi gereken şeyler varsa, lütfen aşağıdaki yöntemlerden BİRİNİ kullanarak bize iletin:

* Bir "pull request" (çekme isteği) oluşturun.
* Projede bir "issue" (sorun/öneri) açın (linkleri ekleyin, biz inceleyip dahil edelim).

Bu listeler için mümkün olduğunca atıfta bulunulmalıdır. Eğer listenin sahibiyseniz veya orijinal yazarını biliyorsanız, lütfen bize bildirin ki hakkını teslim edelim.

## Wordlist İçeriği

Yeni bir Wordlist yüklüyorsanız, şu kurallara uyduğunuzdan emin olun:

### Baştaki eğik çizgileri (slash) kaldırın
Wordlist içeriklerinde satır başında eğik çizgi (`/`) kullanmayın. Bu, tüm kelime listelerinin aynı formatta olmasını sağlar ve dosya boyutunu düşük tutar.
- ❌ `/yol/dosya`
- ✅ `yol/dosya`


### Tekrarları kaldırın

> [!IMPORTANT]
> Windows kullanıyorsanız, bu komutları kullanmak için [Cygwin](https://cygwin.com/) yüklemeniz gerekebilir.

Herhangi bir wordlist'teki tekrar eden satırları şu komutla temizleyebilirsiniz:
- Linux: `sort -u wordlistiniz.txt --output temiz_dosya.txt`
- Windows (Powershell): `&"C:\cygwin64\bin\sort.exe" -u wordlistiniz.txt --output temiz_dosya.txt`

Eğer satırların sırası önemliyse (örneğin olasılığa göre sıralanmış şifrelerse), şu komutu kullanın:
- Linux: `gawk '!seen[$0]++' wordlistiniz.txt > temiz_dosya.txt`
- Windows (Powershell): `&"C:\cygwin64\bin\gawk.exe" '!seen[$0]++' wordlistiniz.txt > temiz_dosya.txt`

### Belirsiz satırları kaldırın

`index.html` ve `.git` gibi çok yaygın satırlar içeren amaca özel wordlist'ler, hedefte "false positive" sonuçlara yol açabilir. Yüklemeden önce bu satırları kaldırmanız önerilir.


### Değişken (placeholder) kullanmayı düşünün

Eğer wordlist URL parametreleri içeriyorsa, bu parametreleri yer tutucularla (placeholder) değiştirmek ve dokümantasyonda belirtmek daha yararlı olabilir.

Örneğin:
- ❌ `yol/auth?password=parola123`
- ✅ `yol/auth?password={PASSWORD_PLACEHOLDER}`


## Klasör İsimlendirme

Klasörler "Train Case" şemasında isimlendirilmelidir, örneğin: `File-System`.

## README Dosyaları

Eğer Zencefil Efendi'ye yepyeni bir wordlist yüklüyorsanız, bulunduğu klasörün `README.md` dosyasına bir giriş eklenmelidir. Klasörde `README.md` yoksa oluşturabilirsiniz.

Genel kurallar şunlardır:
1. Başlık olarak wordlist'in dosya adını kullanın.
2. Wordlist çok spesifikse, başlığın altına `Kullanım amacı:` ekleyin.
> ## zafiyet-taramasi_j2ee-siteler_WEB-INF.txt
> Kullanım amacı: Hassas J2EE dosyalarını keşfetmek ve LFI zafiyetlerini sömürmek.

3. Kaynağa link verin: `Kaynak: example.com/harika-wordlist`
4. Referans linki ekleyin: `Referans: example.com/nasil-hackledim`.

Genel bir referans için [Web-Content](Discovery/Web-Content) klasöründeki README'ye bakabilirsiniz.


## Conventional Commits (Pull Request'ler için isteğe bağlı)

Katkı sağlayan tüm commit'lerin [Conventional-Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) sözdizimini kullanması teşvik edilir.

> Conventional Commits, commit mesajları için hafif bir kural setidir. Otomatik araçlar yazmayı kolaylaştırır ve SemVer ile uyumludur.
>
> Commit mesajı şöyle olmalıdır:
```xml
<tür>[kapsam]: <açıklama>

[isteğe bağlı gövde]

[isteğe bağlı altbilgi]
```

Örneğin:
```
feat(wordlist): Google tarafından hazırlanan "raft" wordlist'leri eklendi
```

Aşağıdaki akış şeması, commit mesajınız için en iyi sözdizimini seçmenize yardımcı olacaktır:

```mermaid
flowchart TD
	start(Bir commit yaptınız) --> f1
	f1{Bir wordlist'i etkiliyor mu?}
	f1 --> |EVET| q1A{Tamamen yeni bir\nwordlist mi\nyüklediniz?}

	q1A --> |EVET| q1A_opt1(Şunu kullanın:\nfeat&lpar;wordlist&rpar;: "WORDLIST_ADI" eklendi, Yazar: YAZAR_ADI)
	q1A --> |HAYIR| q1B{Mevcut bir wordlist'e\nyeni içerik\nmi eklediniz?}
	
	q1B --> |EVET| q1B_opt1(Şunu kullanın:\nfeat&lpar;wordlist&rpar;: "WORDLIST_ADI" dosyasına _____ eklendi)
	q1B --> |HAYIR| q1C{Mevcut wordlist'teki\nbir hatayı\nmi düzelttiniz?}
	
	q1C --> |EVET| q1C_end(Şunu kullanın:fix&lpar;wordlist&rpar;: "WORDLIST_ADI" dosyasında _____ düzeltildi\nfix&lpar;wordlist&rpar;: "WORDLIST_ADI" dosyasından _____ kaldırıldı)
	q1C --> |HAYIR| q1D{Tüm wordlistleri\nküçük bir şekilde etkileyen\nbüyük bir işlem mi yaptınız?\nÖrneğin: \n- Tüm wordlistleri taşıma\n- Satır sonlarını değiştirme}

	q1D --> |EVET| q1D_end(Şunu kullanın:\nchore&lpar;wordlist&rpar;: _____\n\nÖrneğin:\n\nchore&lpar;wordlist&rpar;: Tüm dosya uzantısı listeleri /Fuzzing/File-Extensions/ altına taşındı)
	q1D --> |HAYIR| support1(Hangi türü kullanacağınızı proje yöneticisine sorun)

	f1 --> |HAYIR| f2{Bir README dosyasını\netkiliyor mu?}

	f2 --> |EVET| q2A{Yeni bir README\nmi oluşturdunuz?}

	q2A --> |EVET| q2A_end(Şunu kullanın:\nfeat&lpar;docs&rpar;: ______ için dokümantasyon oluşturuldu)
	q2A --> |HAYIR| q2B{Yazım hatası mı düzelttiniz?\nİfadeyi mi\niyileştirdiniz?}

	q2B --> |EVET| q2B_end(Şunu kullanın:\nchore&lpar;docs&rpar;: _____ dokümanında yazım hatası düzeltildi)
	q2B --> |HAYIR| q2C{Mevcut bir README'ye\nyeni içerik mi\neklediniz?}

	q2C --> |EVET| q2C_end(Şunu kullanın:\nfeat&lpar;docs&rpar;: ______ için dokümantasyon eklendi)
	q2C --> |HAYIR| q2D{README'deki yanlış\nbir bilgiyi mi\ndüzelttiniz?}

	q2D --> |EVET| q2D_end(Şunu kullanın:\nfix&lpar;docs&rpar;: _____ düzeltildi\n\nÖrneğin:\nfix&lpar;docs&rpar;: raft.txt için yazar adı düzeltildi)
	q2D --> |HAYIR| support2(Hangi türü kullanacağınızı proje yöneticisine sorun)


	f2 --> |HAYIR| q3A{CICD (otomasyon)\nüreçlerini etkiliyor mu?}

	q3A --> |EVET| q3B{Tamamen yeni bir\notomasyon mu\nyarattınız?}
	q3A --> |HAYIR| support3(Hangi türü kullanacağınızı proje yöneticisine sorun)

	q3B --> |EVET| q3B_end(Şunu kullanın:\nfeat&lpar;cicd&rpar;: ______ oluşturuldu)
	q3B --> |HAYIR| q3C{Mevcut otomasyondaki\nbir hatayı mı\ndüzelttiniz?}

	q3C --> |EVET| q3C_end(Şunu kullanın:\nfix&lpar;cicd&rpar;: "OTOMASYON_ADI" içinde ______ düzeltildi)
	q3C --> |HAYIR| q3D{Mevcut otomasyona\nyeni bir özellik mi\neklediniz?}

	q3D --> |EVET| q3D_end(Şunu kullanın:\nfeat&lpar;cicd&rpar;: "OTOMASYON_ADI"na _____ eklendi)
	q3D --> |HAYIR| q3E{Şunlardan birini mi yaptınız:\n- Yazım hatası düzeltme\n- Dosya taşıma\n- Yorum satırı ekleme}

	q3E --> |EVET| q3E_end(Şunu kullanın:\nchore&lpar;cicd&rpar;: "OTOMASYON_ADI" içinde yazım hatası düzeltildi)
	q3E --> |HAYIR| support4(Hangi türü kullanacağınızı proje yöneticisine sorun)
```