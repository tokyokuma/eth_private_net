exports.ecrecover = function (msgHash, v, r, s) {
  //r,sを結合させる
  const signature = Buffer.concat([exports.setLength(r, 32), exports.setLength(s, 32)], 64)
  const recovery = v - 27
  if (recovery !== 0 && recovery !== 1) {
    throw new Error('Invalid signature v value')
  }
  const senderPubKey = secp256k1.recover(msgHash, signature, recovery)
  return secp256k1.publicKeyConvert(senderPubKey, false).slice(1)
}