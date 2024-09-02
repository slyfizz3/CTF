from ctypes import windll, c_void_p, byref, create_string_buffer, c_ulong
import itertools
def make_encrypt(ss, k1):
    # Initialize handles
    h1 = c_void_p()
    if windll.advapi32.CryptAcquireContextA(byref(h1), 0, 0, 24, 4026531840):
        try:
            # Create a hash object
            h2 = c_void_p()
            if windll.advapi32.CryptCreateHash(h1, 32771, 0, 0, byref(h2)):  # CALG_SHA256
                try:
                    # Hash the key
                    if windll.advapi32.CryptHashData(h2, k1, len(k1), 0):
                        # Derive a key from the hash
                        h3 = c_void_p()
                        if windll.advapi32.CryptDeriveKey(h1, 26126, h2, 0, byref(h3)):  # CALG_AES_256
                            try:
                                # Prepare data for encryption
                                buffer_size = len(ss) + 16  # Ensure buffer is large enough
                                encrypted_data = create_string_buffer(buffer_size)
                                encrypted_data[:len(ss)] = ss  # Copy the input data into the buffer
                                c_len = c_ulong(len(ss))
                                
                                # Encrypt the data
                                if windll.advapi32.CryptEncrypt(h3, 0, True, 0, encrypted_data, byref(c_len), buffer_size):
                                    print("Encryption successful")
                                    return encrypted_data.raw[:c_len.value]
                                else:
                                    print("Encryption failed")
                            finally:
                                # Destroy the derived key
                                windll.advapi32.CryptDestroyKey(h3)
                        else:
                            print("Key derivation failed")
                finally:
                    # Destroy the hash object
                    windll.advapi32.CryptDestroyHash(h2)
        finally:
            # Release the cryptographic context
            windll.advapi32.CryptReleaseContext(h1, 0)



def make_decrypt(encrypted_data, k1):
    # Initialize handles
    h1 = c_void_p()
    if windll.advapi32.CryptAcquireContextA(byref(h1), 0, 0, 24, 4026531840):
        try:
            # Create a hash object
            h2 = c_void_p()
            if windll.advapi32.CryptCreateHash(h1, 32771, 0, 0, byref(h2)):  # CALG_SHA256
                try:
                    # Hash the key
                    if windll.advapi32.CryptHashData(h2, k1, len(k1), 0):
                        # Derive a key from the hash
                        h3 = c_void_p()
                        if windll.advapi32.CryptDeriveKey(h1, 26126, h2, 0, byref(h3)):  # CALG_AES_256
                            try:
                                # Prepare buffer for decryption
                                buffer_size = len(encrypted_data)  # Size should match the encrypted data size
                                decrypted_data = create_string_buffer(buffer_size)
                                decrypted_data[:len(encrypted_data)] = encrypted_data
                                c_len = c_ulong(len(encrypted_data))
                                
                                # Decrypt the data
                                if windll.advapi32.CryptDecrypt(h3, 0, True, 0, decrypted_data, byref(c_len)):
                                    return decrypted_data.raw[:c_len.value]
                                else:
                                    return None
                            finally:
                                # Destroy the derived key
                                windll.advapi32.CryptDestroyKey(h3)
                        else:
                            print("Key derivation failed")
                finally:
                    # Destroy the hash object
                    windll.advapi32.CryptDestroyHash(h2)
        finally:
            # Release the cryptographic context
            windll.advapi32.CryptReleaseContext(h1, 0)


def fixstr(a):
    return a.encode('utf8')
encrypted = bytes.fromhex('73E3679507CC8197F665FD5B46F55321CF89BB828CD7BB424B181734D468709709D49085868CDA1B9892B947999E4F64')

def test_k1(k1):
    k1=fixstr(k1)
    decrypted_data = make_decrypt(encrypted, k1)
    if decrypted_data:
        if b"4248466c616759" in decrypted_data or b"BHFlagY" in decrypted_data:
            print(k1,decrypted_data)



def brute_force():
    ranges = [range(7), range(3), range(9), range(6), range(9), range(8), range(4), range(5)]
    
    for combination in itertools.product(*ranges):
        k1 = ''.join(map(str, combination))
        if test_k1(k1):
            print(f"Found valid k1: {k1}")
            return k1  
            break
    print("No valid k1 found.")
    return None


brute_force()
