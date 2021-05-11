import hashlib

flag_tpl = "flxg{8G6so5g-FLXG-%s}"
secret_key = b"012uf:>FPL(!HNF128hf"

def hg_dynamic_flag(token):
    return flag_tpl % hashlib.sha256(('20486787gf'+token).encode()).hexdigest()[:10]