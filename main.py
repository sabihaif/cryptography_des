from Crypto.Cipher import DES


from des import DES as MyDES
from helpers import Helpers


if __name__ == '__main__':
    key = "secret_k"
    text = "Hello world today is my first day"
    my_des = MyDES()
    des = DES.new(key, DES.MODE_ECB)
    encrypted_text = des.encrypt(Helpers.add_padding(text))

    my_encrypted_text = my_des.encrypt(key, text, padding=True)
    my_decrypted_text = my_des.decrypt(key, my_encrypted_text)
    print("Encrypted by my algorithm: ", my_encrypted_text)
    print("Decrypted by my algorithm: ", my_decrypted_text)

    print("Encrypted", encrypted_text)
    print("Decrypted", des.decrypt(encrypted_text))
