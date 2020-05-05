import os # belirtilen dizine ve dosyalarına erişebilmek için os kütüphanesi içe aktarılır.
from cryptography.fernet import Fernet # Hash üretip Dosyaları şifrelememize ve çözmemize yaran kütüphane
import platform

"""
fidye.py betiği ile ürettiğimiz anahtar unutulmaması için key.txt isimli dosyaya kaydedilmişti.
Bu dosya açılıp içeriği okunduktan sonra key değişkenine aktarılıp Fernet sınıfında kullanılır.

"""
f = open("key.txt","r")
key = f.read()
print(key)

ferNet = Fernet(key) # Burada oluşan anahtarı Fernet sınıfına verip bir değişkene atıyoruz. Böylelikle şifreleme ve çözme işlemlerini yapabiliriz.

# print("***********************"*3)

"""
coz fonksiyonunda parametre olarak alttaki for döngüsünün içinde aldığımız dosya yollarını vererek
bu dosyaların içeriğini öncelikle okuyoruz. Sonra daha önceden şifrelenmiş olan dosyaları anahtar yardımıyla çözüyoruz.
Çözülmüş dosyaları yani en baştaki normal halini yeniden dosya üzerine yazıyoruz. Ve dosyaların şifresi 
çözülmüş, eski haline dönmüş oluyor.
"""

def coz(dosya):
    with open(dosya,"rb") as readFile:
        okunanDosya = readFile.read()
    
    with open(dosya,"wb") as writeFile:
        try:
            cozulmusHal = ferNet.decrypt(okunanDosya)
            writeFile.write(cozulmusHal)
            writeFile.close()
            readFile.close()
        except:
            print("Bir hata olustu")


"""
Öncelikle kullandığımız işletim sistemine göre kodların çalışabilmesi için gereken kontroller yapılmıştır.
os kütüphanesinin içinde walk isimli fonksiyona şifrelenmesini istediğimiz dosyaların bulunduğu dizini
veriyoruz. Bu dizini Linux'ta verirken "/" ile, Windows'ta ise "\" ile dizinleri belirtmemiz gerekiyor. Bu fonksiyon 3 ayrı değer döner. İlk değer dosya yolunu, ikincisi boş bir liste, üçüncüsü ise
dizinde bulunan dosyaları listeler.

Bu şekilde os.walk() fonksiyonunu for döngüsüne sokarak 3 ayrı değere de erişmiş oluyoruz.
Akabinde 3. olarak dönen değer olan files parametresi dosyaları bir liste içinde barındırıyor.
Bu listede dosya isimlerine tek tek erişebilmek için bunları bir for döngüsüne sokuyoruz.
Sonra tam dosyaların tam yolunu verebilmemiz için path ile dosyaların isimlerini birleştirip bir değişkene atıyoruz.
Ve bulduğumuz dosyaları barındıran değişkeni şifrelenen dosyaları çözmek için kullanacağımız 
coz() fonksiyonuna parametre olarak veriyoruz.
"""

if platform.system() == "Windows":
    for path,gereksiz,files in os.walk(os.getcwd()+"\sifrele"):
        #print(path,gereksiz,files)
        for dosyalar in files:
            dosyaYolu = path + "\\" + dosyalar
            coz(dosyaYolu)
elif platform.system() == "Linux":
    for path,gereksiz,files in os.walk(os.getcwd()+"/sifrele"): 
        #print(path,gereksiz,files)
        for dosyalar in files:
            dosyaYolu = path + "/" + dosyalar
            coz(dosyaYolu)
else:
    print("Kullandığınız işletim sistemi bu program tarafından desteklenmiyor.")

