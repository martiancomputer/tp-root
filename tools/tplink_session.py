"""TP-Link cloud-UI (AX1500/AX10 v3) authenticated session library.
Replicates login crypto (SHA256/AES/RSA-v1.5/RSA-OAEP) + GDPR request
envelope (AES-CBC + HMAC-SHA256) + sysauth cookie handling.
"""
import base64, hashlib, json, random, sys, urllib.parse, urllib.request
import os
from Crypto.Cipher import AES, PKCS1_OAEP, PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA1, HMAC, SHA256

HOST = os.environ.get("TP_ROUTER_URL")
if not HOST:
    raise RuntimeError("Set TP_ROUTER_URL to an authorized router URL")
REF = f"{HOST}/webpages/index.html"
HDRS = {"Referer": REF, "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0"}

def quote(s):
    return urllib.parse.quote(str(s), safe="-_.!~*'()")

def raw_rsa(n_hex, e_hex, data: bytes) -> str:
    key = RSA.construct((int(n_hex, 16), int(e_hex, 16)))
    return PKCS1_v1_5.new(key).encrypt(data).hex().rjust(len(n_hex), "0")

def oaep(n_hex, e_hex, data: bytes) -> str:
    key = RSA.construct((int(n_hex, 16), int(e_hex, 16)))
    return PKCS1_OAEP.new(key, SHA1).encrypt(data).hex()

def api_cookie(path, fields, stok="", cookie=None):
    """Same as api but also returns Set-Cookie value."""
    url = f"{HOST}/cgi-bin/luci/;stok={stok}{path}"
    data = urllib.parse.urlencode(fields).encode()
    hdr = dict(HDRS)
    if cookie:
        hdr["Cookie"] = cookie
    req = urllib.request.Request(url, data=data, method="POST", headers=hdr)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            ck = r.headers.get("Set-Cookie")
            return r.status, r.read().decode(errors="replace"), (ck.split(";")[0] if ck else None)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(errors="replace"), None

def api(path, fields, stok="", cookie=None):
    st, body, _ = api_cookie(path, fields, stok, cookie)
    return st, body

class Session:
    def __init__(self, password):
        auth = json.loads(api("/login?form=auth", {"operation": "read"})[1])
        self.seq = auth["data"]["seq"]
        n1, e1 = auth["data"]["key"]
        keys = json.loads(api("/login?form=keys", {"operation": "read"})[1])
        n2, e2 = keys["data"]["password"]
        self.h = hashlib.sha256(("admin" + password).encode()).hexdigest()
        self.ak = "".join(random.choice("0123456789") for _ in range(16))
        self.ai = "".join(random.choice("0123456789") for _ in range(16))
        enc_pwd = raw_rsa(n2, e2, password.encode())
        plain = f"password={quote(enc_pwd)}&operation=login"
        ct = AES.new(self.ak.encode(), AES.MODE_CBC, self.ai.encode())
        pad = 16 - len(plain.encode()) % 16
        data_b64 = base64.b64encode(ct.encrypt(plain.encode() + bytes([pad]) * pad)).decode()
        s = f"k={self.ak}&i={self.ai}&h={self.h}&s={self.seq + len(data_b64)}"
        sign = "".join(oaep(n1, e1, s[i:i+53].encode()) for i in range(0, len(s), 53))
        st, body, cookie = api_cookie("/login?form=login", {"sign": sign, "data": data_b64})
        self.cookie = cookie
        resp = self.dec(body)
        if not resp.get("success"):
            raise SystemExit(f"LOGIN FAILED: {resp}")
        self.stok = resp.get("stok") or resp.get("data", {}).get("stok") or resp.get("result", {}).get("stok")
        print(f"LOGIN OK, resp keys={list(resp.keys())}", file=sys.stderr)
        if not self.stok:
            print("FULL RESP:", json.dumps(resp)[:500], file=sys.stderr)
            raise SystemExit("no stok in response")

    def dec(self, body):
        try:
            d = json.loads(body)
        except Exception:
            return {"raw": body}
        if isinstance(d.get("data"), str) and len(d.get("data", "")) > 20:
            try:
                blob = base64.b64decode(d["data"])
                if len(blob) % 16 == 0 and len(blob) > 0:
                    pt = AES.new(self.ak.encode(), AES.MODE_CBC, self.ai.encode()).decrypt(blob)
                    pt = pt[:-pt[-1]]
                    return json.loads(pt)
                return d
            except Exception as e:
                return {"decrypt_error": str(e), "raw": body[:200]}
        return d

    def call(self, path, fields, decrypt=True):
        st, body = api(path, fields, self.stok, self.cookie)
        return (self.dec(body) if decrypt else body)

    def enc_call(self, path, fields):
        """GDPR-encrypted request (post-login): AES body + HMAC sign, hash ratchet."""
        plain = "&".join(f"{quote(k)}={quote(v)}" for k, v in fields.items())
        ct = AES.new(self.ak.encode(), AES.MODE_CBC, self.ai.encode())
        pad = 16 - len(plain.encode()) % 16
        a = base64.b64encode(ct.encrypt(plain.encode() + bytes([pad]) * pad)).decode()
        h = hashlib.sha256(a.encode()).hexdigest()
        s = f"h={h}&s={self.seq + len(a)}"
        aeskey = f"k={self.ak}&i={self.ai}"
        sign = "".join(
            HMAC.new(aeskey.encode(), s[i:i+53].encode(), SHA256).hexdigest()
            for i in range(0, len(s), 53))
        st, body = api(path, {"sign": sign, "data": a}, self.stok, self.cookie)
        return self.dec(body)
