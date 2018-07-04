#  -- Sunucu --
#-*- coding:utf-8 -*-

import socket,sys,thread,base64,os
from pyDes import * #TDES kütüphanesi
from Crypto.Cipher import AES #AES sifreleme kütüphanesi
from Crypto import Random
#sifre donusumu
BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[:-ord(s[len(s)-1:])]
#sifre fonksiyon tanımlaması
class AESCipher:
        def __init__(self,key):
                self.key = key
        def encrypt(self,raw):
                raw = pad(raw)
                iv = Random.new().read(AES.block_size)
                cipher = AES.new(self.key,AES.MODE_CBC,iv)
                return base64.b64encode(iv+cipher.encrypt(raw))
        def decrypt(self,enc):
                enc= base64.b64decode(enc)
                iv = enc[:16]
                cipher = AES.new(self.key,AES.MODE_CBC,iv)
                return unpad(cipher.decrypt(enc[16:]))

#TDES sifrelemesi
k = triple_des("DESCRYPTDESCRYPT", ECB, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
#tanım
HOST  = "127.0.0.1"
PORT  = 5300
BUF   = 4096
yukle = (HOST,PORT)
#sunucu dinleme bağlantısı
baglanti = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
baglanti.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
baglanti.bind(yukle)
baglanti.listen(5)
#kullanıcı adı
name = "bilinmeyen"
os.system("clear")
print "\n>>>Sunucu " +str(PORT) + ". port üzerinden kullanıma açık..<<<"
#oturumlarin tutulduğu liste.
BAGLANTI_LISTESI = []
#sifreleme seçimi
print '''
*****************************************
*          Designed by Caner            *
*****************************************
*Ne tür şifreleme yapmak istiyorsunuz?  *
* 1-) Şifresiz                          *
* 2-) TDES şifreleme                    *
* 3-) AES şifreleme                     *
*****************************************
Seçiminiz : '''
sifreleme = raw_input()
deger = 1
while deger:
    if sifreleme == '1':
	deger = 0
        print "Server şifresiz olarak kullanımda.."
    elif sifreleme == '2':
	deger = 0
	print "Server TDES şifreleme sistemiyle kullanımda.."
    elif sifreleme == '3':
	deger = 0
	print "Server AES şifreleme sistemiyle kullanımda.."
    else:
	print "Lütfen 1,2 yada 3 yazarak tercih yapınız!"
	sifreleme = raw_input()
#haberleşme fonksiyonu.
def islem(connection,address):
  print ">>" + str(address[0])+"("+str(address[1])+")" + " bağlandi.."
  connection.send(">>Sunucuya başarıyla bağlandınız.")
  name = connection.recv(1024)
  connection.send(sifreleme)
#yeni bağlantı olduğunda haber bildirisi.
  data = ">>" + str(address[0])+ " bağlandi.."
  for socket in BAGLANTI_LISTESI:
    if socket != connection:
      try:
          fo = open("kyt.txt","a")
          fo.write(data)
          fo.close()
          if int(sifreleme) == 2 :
             data = k.encrypt(data)
             socket.send(data)
             data = k.decrypt(data)
          elif int(sifreleme) == 3:
             obj = AESCipher("qweqweqweqweqwe!")
             data = obj.encrypt(data)
             socket.send(data)
             data = obj.decrypt(data)
             del obj
          else:
             socket.send(data)
      except:
          print ">>"+str(address[0])+" ayrıldı.."
          socket.close()
          BAGLANTI_LISTESI.remove(connection)
  while True:
    data = connection.recv(BUF)
    if int(sifreleme) == 2:
      data = k.decrypt(data)
    elif int(sifreleme) == 3:
      obj = AESCipher("qweqweqweqweqwe!")
      data = obj.decrypt(data)
      del obj
    data = name+" : "+data
    for socket in BAGLANTI_LISTESI:
      if socket != connection:
        try:
          fo = open("kyt.txt","a")
          fo.write(data)
          fo.close()
          if int(sifreleme) == 2:
             data = k.encrypt(data)
             socket.send(data)
             data = k.decrypt(data)
          elif int(sifreleme) == 3:
             obj = AESCipher("qweqweqweqweqwe!")
             data = obj.encrypt(data)
             socket.send(data)
             data = obj.decrypt(data)
             del obj
          else:
             socket.send(data)
        except:
          print ">>"+str(address[0])+" ayrıldı.."
          socket.close()
          BAGLANTI_LISTESI.remove(connection)
#    if data != (name+" : "+"exit"):
         
#bağlanti kabulü
while True:
	connection, address = baglanti.accept()
	BAGLANTI_LISTESI.append(connection)
	thread.start_new_thread(islem,(connection,address))
