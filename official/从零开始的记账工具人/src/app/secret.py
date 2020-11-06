import hashlib

secret_key = b"613a8321a1190e281ff6ae91f7"

def total_money(token):
    return int(hashlib.sha256(('dc91ea2aa6c0'+token).encode()).hexdigest()[:5],16)+1000000
