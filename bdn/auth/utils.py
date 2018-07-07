import sha3
import ethereum


def sig_to_vrs(sig):
    r = int(sig[2:66], 16)
    s = int(sig[66:130], 16)
    v = int(sig[130:], 16)
    return v, r, s


def hash_personal_message(msg):
    prefix = "\x19Ethereum Signed Message:\n" + str(len(msg))
    data = ''.join([prefix, msg]).encode('utf-8')
    return sha3.keccak_256(data).digest()


def recover_to_addr(msg, sig):
    msghash = hash_personal_message(msg)
    vrs = sig_to_vrs(sig)
    pub = ethereum.utils.ecrecover_to_pub(msghash, *vrs)
    return '0x' + sha3.keccak_256(pub).hexdigest()[24:]
