import hashlib
import random
import time
import uuid

PUBLIC_KEY = "a2ffa5c9be07488bbb04a3a47d3c5f6a"


def sha1(x: str):
    return hashlib.sha1(x.encode()).hexdigest()


def generate_mac_address():
    as_hex = f"{uuid.getnode():012x}"
    return ":".join(as_hex[i: i + 2] for i in range(0, 12, 2))


def generate_nonce(miwifi_type=0):
    return f"{miwifi_type}_{generate_mac_address()}_{int(time.time())}_{int(random.random() * 1000)}"


def generate_password_hash(nonce, password):
    return sha1(nonce + sha1(password + PUBLIC_KEY))
