"""sign.py

web3.pyを使用してEthereumで署名検証を実施

"""

import pprint
import sys
import time

import web3
from web3 import Web3,HTTPProvider
from web3.auto import w3
from eth_account.messages import  encode_defunct

def to_32byte_hex(val):
        return Web3.toHex(Web3.toBytes(val).rjust(32, b'\0'))

#httpプロバイダーでノードに接続
web3 = Web3(HTTPProvider('http://localhost:8545'))

#eth.account[0]の秘密鍵生成(geth keyfileから生成)
#eth_private_netからの相対パス
geth_keyfile_path = "./keystore/UTC--2021-10-24T10-02-46.357210877Z--364bed568ea914966e1195d16e93a56bb2fe6502"

with open(geth_keyfile_path) as keyfile:
    encrypted_key = keyfile.read()
    private_key = w3.eth.account.decrypt(encrypted_key, 'test01')

#print(private_key.hex())

#メッセージ作成
msg = "Hello"

#署名可能な形式にエンコード
message = encode_defunct(text=msg)

#署名生成
signed_message = w3.eth.account.sign_message(message, private_key=private_key)

#Contractでecrecoverを実行するためのデータ(引数用)を作成
ec_recover_args = (msghash, v, r, s) = (
        Web3.toHex(signed_message.messageHash),
        signed_message.v,
        to_32byte_hex(signed_message.r),
        to_32byte_hex(signed_message.s),
)

#contractのアドレス
address = web3.toChecksumAddress("0x8548919cbcd07de9e7714eda83b91fb8820e03cb")

#abi情報
abi = [{"inputs":[{"internalType":"bytes32","name":"msgh","type":"bytes32"},
                  {"internalType":"uint8","name":"v","type":"uint8"},
                  {"internalType":"bytes32","name":"r","type":"bytes32"},
                  {"internalType":"bytes32","name":"s","type":"bytes32"}],
        "name":"ecr","outputs":[{"internalType":"address","name":"sender","type":"address"}],
        "stateMutability":"pure","type":"function"}]

#contractの取得
contract_instance = web3.eth.contract(address=address, abi=abi)

#署名検証(ecr:ecrecover)実行に必要なgasの消費量を計算する
gas_estimate = contract_instance.functions.ecr(*ec_recover_args).estimateGas()
#print(f'Gas estimate to transact with setVar: {gas_estimate}')


if gas_estimate < 100000:
        
        #署名検証を実行するトランザクションを送信しハッシュを格納
        print("Sending transaction to ecr)\n")
        tx_hash = contract_instance.functions.ecr(*ec_recover_args).transact({'from':web3.eth.accounts[0]})
        
        #トランザクションがブロックに追加されるまで待つ
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        #print("Transaction receipt mined:")
        #pprint.pprint(dict(receipt))
        #print("\nWas transaction successful?")
        #pprint.pprint(receipt["status"])
        
        #復元されたアドレスを格納
        recover_address = contract_instance.functions.ecr(*ec_recover_args).call()
        print("Signer adress:_{0}".format(web3.eth.accounts[0]))
        print("Recover adress:_{0}".format(recover_address))
        
        #署名者のアドレスと復元されたアドレスが一致するか確認
        if(web3.eth.accounts[0] == recover_address):
                print("The addresses match. Varification OK")
        else:
                print("The addresses match. Varification OK")
        
else:
     print("Gas cost exceeds 100000")
