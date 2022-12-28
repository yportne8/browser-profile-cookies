import json, sqlite3
from base64 import b64decode
from http.cookiejar import Cookie, CookieJar
from ctypes import (create_string_buffer,
    memmove, byref, POINTER, Structure, 
    wintypes, windll, c_char, c_wchar_p)

from Crypto.Cipher import AES

from .paths import Profile, Browsers


class Profile(Profile):

    """_Extracts and decrypts browser profile cookies_

    Args:
        Profile (_type_): _cookiejar.paths.Profile_
    """


    KEYS = ["host_key", "is_secure", "expires_utc",
            "name", "encrypted_value"]
    DEFAULT_PROFILE_NAME = "default"


    class DataBlob(Structure):

        _fields_ = [('cbData', wintypes.DWORD),
                    ('pbData', POINTER(c_char))]


    class Failed2GetCipher(Exception):
        pass


    def __init__(self, browser: str = "edge", profile: str = None):
        """_defaults to the default profile for edge browser_

        Args:
            browser (str): _browser name_
            profile (str): _profile name_
        """
        if not profile: profile = self.DEFAULT_PROFILE_NAME
        super().__init__(browser, profile)

    @staticmethod
    def available_browsers():
        """_static method returns local Chromium browsers and paths_

        Returns:
            _dict_: _browser names and paths_
        """
        browsers = Browsers()
        browsers = browsers.browsers
        return browsers
        
    def __keydpapi(self):
        try:
            with open(self.localstate,'rb') as key:
                key = json.load(key)
                key = key['os_crypt']['encrypted_key']
                key = key.encode('utf-8')
            return b64decode(key)[5:]
        except:
            return None

    def __cipher(self):
        cipher = self.__keydpapi()
        if not cipher: raise self.Failed2GetCipher
       
        desc = c_wchar_p()
        unprotect = windll.crypt32.CryptUnprotectData
        b_in, b_ent, b_out = map(
                lambda x: self.DataBlob(len(x),
                create_string_buffer(x)),
                [cipher, b'', b''])
        unprotect(
            byref(b_in), byref(desc),
            byref(b_ent), None, None,
            0x01, byref(b_out))
        
        buffer = create_string_buffer(int(b_out.cbData))
        memmove(buffer, b_out.pbData, b_out.cbData)
        
        map(windll.kernel32.LocalFree, [desc, b_out.pbData])
        return buffer.raw

    def __decrypt(self, encrypted_value: bytes):
        encrypted_value = encrypted_value[3:]
        nonce, tag = encrypted_value[:12], encrypted_value[-16:]
        cipher = self.__cipher()

        aes = AES.new(cipher, AES.MODE_GCM, nonce=nonce)
        data = aes.decrypt_and_verify(encrypted_value[12:-16], tag)
        return data.decode()

    def __sql_query(self, domain: str):
        if domain and domain[0] != ".": domain = f".{domain}"
        
        criteria = self.KEYS[0]
        for key in self.KEYS[1:]: criteria += f", {key}"

        if domain:
            return (f"SELECT {criteria} FROM cookies WHERE host_key like ?;", (f"%{domain}%",))
        else:
            return (f"SELECT {criteria} FROM cookies", None)

    def __raw(self, raw: tuple) -> dict:
        cookie = {}
        for k, v in zip(self.KEYS, raw):
            cookie[k] = v
        
        if cookie["expires_utc"] == 0:
            cookie["expires_utc"] = None
        else:
            expires = cookie["expires_utc"]
            expires = min(int(expires), 32536799999000000)
            cookie["expires_utc"] = (expires/1000000)-11644473600
        
        value = cookie["encrypted_value"]
        cookie["encrypted_value"] = self.__decrypt(value)
        return Cookie(
            0, cookie["name"], cookie["encrypted_value"], 
            None, False, cookie["host_key"], True, True, "/",
            True, cookie["is_secure"], cookie["expires_utc"], 
            False, None, None, {})

    def available_profiles(self):
        """_returns available profiles and paths_

        Returns:
            _dict_: _profile names and paths_
        """
        return self.profiles

    def cookie(self, domain: str) -> CookieJar:
        """_returns a cookiejar with the cookies from the requested domain_

        Args:
            domain (str): _domain name_

        Returns:
            _CookieJar_: _http.cookiejar.CookieJar_
        """
        cookiejar = CookieJar()
        query, domain = self.__sql_query(domain)
        try:
            conn = sqlite3.connect(self.cookies)
            cur = conn.cursor()
            cur.execute(query,domain) if domain else cur.execute(query)
            for r in cur.fetchall():
                raw = self.__raw(r)
                print(raw)
                cookiejar.set_cookie(raw) 
    
            conn.close()    
            return cookiejar
        except Exception as e:
            try:
                conn.close()
            except:
                pass
            print("Exception", e)
        
    def cookie_string(self, domain: str):
        """_returns a str of the retrieved cookie for requested domain_

        Args:
            domain (str): _description_

        Returns:
            _type_: _description_
        """
        cookie = self.cookie(domain)
        domain = list(cookie._cookies.keys())[0]
        entries = cookie._cookies[domain]["/"]
        
        format = lambda x: f"{x.name}={x.value}" 
        return "; ".join(map(format, list(entries.values())))

    def cookiejar(self) -> CookieJar:
        """_returns the contents of the profile cookiejar_

        Returns:
            _CookieJar_: _http.cookiejar.CookieJar_
        """
        return self.cookie(None)