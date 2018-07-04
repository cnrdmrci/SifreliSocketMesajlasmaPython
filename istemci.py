# -- Istemci --
# -*- coding: utf-8 -*-
import socket,thread,sys,threading,base64,os
from pyDes import *
from Crypto.Cipher import AES
from Crypto import Random

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[:-ord(s[len(s)-1:])]

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

k = triple_des("DESCRYPTDESCRYPT", ECB, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
#giriş kontrolü
if(len(sys.argv)<3):
  print "Kullanım şekli : python istemci.py ip port"
  sys.exit()

HOST = sys.argv[1]
PORT = int(sys.argv[2])
BUFF = 4096
#ipv4 ve Tcp tanımlaması.
baglanti = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#baglanti.settimeout(2)

#Sunucuyla bağlantının kurulması.
try:
  baglanti.connect((HOST,PORT))
except:
  print "Sunucuya bağlanılamıyor."
  sys.exit()
ilk = baglanti.recv(1024)
print ilk

os.system("clear")

print '''
*************************************
*      Designed by Caner            *
*************************************
'''

name = raw_input("Adınız : ")
print "Hoşgeldin " + name
baglanti.send(name)
sifreleme = baglanti.recv(1024) #TDES 2,AES 3
if int(sifreleme) == 1:
	print "Server ile şifresiz bağlantı kuruldu.."
elif int(sifreleme) == 2:
	print "TDES şifreleme protokolü kullanılarak server bağlantısı kuruldu.."
elif int(sifreleme) == 3:
	print "AES şifreleme protokolü kullanılarak server bağlantısı kuruldu.."
def gonder(baglanti):
  while True:
    data = raw_input()
    if int(sifreleme) == 2:
       data = k.encrypt(data)
    if int (sifreleme) == 3:
       obj = AESCipher("qweqweqweqweqwe!")
       data = obj.encrypt(data)
       del obj
    baglanti.send(data)
#    if data == "exit":
#       baglanti.close()
#       sys.exit()

def al(baglanti):
  while True:
    data = baglanti.recv(BUFF)
    if int(sifreleme) == 2:
       data = k.decrypt(data)
    if int(sifreleme) == 3:
       obj = AESCipher("qweqweqweqweqwe!")
       data = obj.decrypt(data)
       del obj
    print data

read_thread = threading.Thread(target=gonder, args=(baglanti,))
read_thread.start()

write_thread = threading.Thread(target=al, args=(baglanti,))
write_thread.start()

