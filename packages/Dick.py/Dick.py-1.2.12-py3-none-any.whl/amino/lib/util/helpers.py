import json
#import requests
from hashlib import sha1
from functools import reduce
from base64 import b85decode, b64decode
import names
import random
import hmac
import platform,socket,re,uuid 
def device():
    hw=(names.get_full_name()+str(random.randint(0,10000000))+platform.version()+platform.machine()+names.get_first_name()+socket.gethostbyname(socket.gethostname())+':'.join(re.findall('..', '%012x' % uuid.getnode()))+platform.processor())
    identifier=sha1(hw.encode('utf-8')).digest()
    mac = hmac.new(bytes.fromhex('76b4a156aaccade137b8b1e77b435a81971fbd3e'), b"\x32" + identifier, sha1)
    return (f"32{identifier.hex()}{mac.hexdigest()}").upper()

def generate_device_info():
    try:
        deviceId=device()
    except Exception:
        deviceId = "32D8F914018AECAD0BE91416046A62E520099E06688CDD3EF50E4B0C4F9E5EEBDBE466FC68A9D239DD"

    return {
        "device_id": deviceId,
        "device_id_sig": "Aa0ZDPOEgjt1EhyVYyZ5FgSZSqJt",
        "user_agent": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-G973N Build/beyond1qlteue-user 5; com.narvii.amino.master/3.4.33562)"
    }

# okok says: please use return annotations :(( https://www.python.org/dev/peps/pep-3107/#return-values

def decode_sid(sid: str) -> dict:
    return json.loads(b64decode(reduce(lambda a, e: a.replace(*e), ("-+", "_/"), sid + "=" * (-len(sid) % 4)).encode())[1:-20].decode())

def sid_to_uid(SID: str) -> str: return decode_sid(SID)["2"]

def sid_to_ip_address(SID: str) -> str: return decode_sid(SID)["4"]
