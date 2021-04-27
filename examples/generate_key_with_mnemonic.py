from hedera import Mnemonic

mnemonic = Mnemonic.generate24()
pri_key = mnemonic.toPrivateKey()
pub_key = pri_key.getPublicKey()

mnemonic12 = Mnemonic.generate12()
pri_key12 = mnemonic12.toPrivateKey()
pub_key12 = pri_key12.getPublicKey()

print("Mnemonic 24 word = ", mnemonic.toString())
print("Private Key = ", pri_key.toString())
print("Public Key = ", pub_key.toString())

print("Mnemonic 12 word = ", mnemonic12.toString())
print("Private Key = ", pri_key12.toString())
print("Public Key = ", pub_key12.toString())
