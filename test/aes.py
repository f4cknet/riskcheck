from Crypto.Cipher import AES
import base64
AESKEY = 'uBdUx82vPHkDKb284d7NkjFoNcKWBuka'  # 请修改 一定是 16位的字符串
AESIV = 'c558Gq0YQK2QUlMc'   # 和KEY保持一致即可
class AESTool:
    def __init__(self):
        self.key = AESKEY.encode('utf-8')
        self.iv = AESIV.encode('utf-8')

    def pkcs7padding(self, text):
        """
        明文使用PKCS7填充
        """
        bs = 16
        length = len(text)
        bytes_length = len(text.encode('utf-8'))
        padding_size = length if (bytes_length == length) else bytes_length
        padding = bs - padding_size % bs
        padding_text = chr(padding) * padding
        self.coding = chr(padding)
        return text + padding_text

    def aes_encrypt(self, content):
        """
        AES加密
        """
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        # 处理明文
        content_padding = self.pkcs7padding(content)
        # 加密
        encrypt_bytes = cipher.encrypt(content_padding.encode('utf-8'))
        # 重新编码
        result = str(base64.b64encode(encrypt_bytes), encoding='utf-8')
        return result

    def aes_decrypt(self, content):
        """
        AES解密
        """
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        content = base64.b64decode(content)
        text = cipher.decrypt(content).decode('utf-8')
        return self.pkcs7padding(text)


if __name__ == "__main__":
    aes_tool = AESTool()
    a = aes_tool.aes_encrypt("13655719712")

