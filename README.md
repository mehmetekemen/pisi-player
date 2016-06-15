# pisi-player
Pisi Linux için Video Oynatıcı

## Uyarı!

Uygulama Pisi Linux üzerinde sorunsuz(!) çalışmaktadır. Başka dağıtımlarda çalışmama ihtimali olduysa, en büyük sebebi gstreamer'dır.
Çünkü pyqt-qt ses ve video oynatırken arkaplanda gstreamer kullanır.

## Kurulum

sudo python3 setup.py install

## Bağımlılıklar

python3-qt5, pyqt5tools(derleme - pyrcc5, pylupdate5, lrelease5), python3-setuptools(derleme) - (Farklı dağıtımlar için qtmultimedia paketi pyqt5 için kurulmalı.)

## Özellikler

* Ses seviyesini değiştirdiğinizde, bir sonraki girişte o ses seviyesinde başlıyor.
* İzlediğiniz video varken Pisi Player'ı kapattığınız da hangi videonun hangi sürede olduğunu kayıt ediyor ve bir sonraki açılışta kaldığınız yerden devam ediyor.
* Pisi Player kapandığında, o an ekrandaki konumu ve boyutu kayıt ediliyor ve tekrar açtığınızda boyut ve konumu hatırlıyor.
* Altyazı rengi, arkaplan rengi ve yazıtipi ayarlayanabiliyor.

Altyazı gösterme özelliği ile ilgili bilgiler kararlı değildir!

## Fare ve Klavye KısaYolları

* Sürükle-bırak ile video oynatabilir ve altyazı ekleyebilirsiniz(Video ile aynı dizin ve isimde olan altyazılar otomatik algılanır).
* Videoya Çift tıklama: Tam ekran veya tam ekrandan çıkış.
* Esc: Tam ekrandan çıkış.
* Ctrl+Q: Uygulamayı kapat.
* Ctrl+M: Sesi Kapat-Aç.
* Space: Durdur-Devam et.
* -(eksi): Sesi kıs.
* +(artı): Sesi Aç.
* Sağ ok: 10sn ileri
* Sol ok: 10sn geri
* Yukarı ok: 1dk ileri
* Aşağı ok: 1dk geri
* Fare tekerleği - yukarı: 1dk ileri
* Fare tekerleği - aşağı: 1dk geri

