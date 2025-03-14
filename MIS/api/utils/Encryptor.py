from Cryptodome.Cipher import AES
from base64 import b64encode, b64decode

class AESCipher:
    def __init__(self):
        self.key = '1234567890123456'.encode('utf-8')
        # Using a fixed IV to match C# behavior
        self.iv = b'\x00' * 16  # 16 bytes of zeros
        
    def encrypt(self, data: str) -> str:
        try:
            data = str(data)
            # Convert input string to bytes

            plain_bytes = data.encode('utf-8')

            # Calculate padding needed
            block_size = AES.block_size
            padding_length = block_size - (len(plain_bytes) % block_size)
            
            # Apply null padding
            padded_data = plain_bytes + (b'\x00' * padding_length)

            # Create cipher and encrypt
            cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
            encrypted_bytes = cipher.encrypt(padded_data)
            
            # Encode to base64 and return as string
            return b64encode(encrypted_bytes).decode('utf-8')
        except Exception as e:
            print(f"Encryption error: {str(e)}")
            return None
    
    def decrypt(self, encrypted_data: str) -> str:
        try:
            encrypted_bytes = b64decode(encrypted_data)
            cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
            decrypted_padded = cipher.decrypt(encrypted_bytes)
            # Remove null bytes
            return decrypted_padded.rstrip(b'\x00').decode('utf-8')
        except Exception as e:
            print(f"Decryption error: {str(e)}")
            return None