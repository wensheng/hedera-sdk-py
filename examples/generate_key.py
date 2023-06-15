from hedera import PrivateKey
# pri_key = PrivateKey.generate()
pri_key = PrivateKey.generateED25519()
pub_key = pri_key.getPublicKey()
print("Private Key: {}".format(pri_key.toString()))
print("Public Key: {}".format(pub_key.toString()))
