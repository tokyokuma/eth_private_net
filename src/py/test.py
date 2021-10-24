"""web3.pyテスト

web3.pyを使用してgethを操作する

"""

from web3 import Web3,HTTPProvider

#httpプロバイダーでノードに接続
web3 = Web3(HTTPProvider('http://localhost:8545'))

#contractのアドレス
address = web3.toChecksumAddress("0x00dc503b66639185ad781f777b3927f10315c756")

#abi情報
abi = [{"inputs":[],
        "name":"_myVar",
        "outputs":[{"internalType":"uint8","name":"","type":"uint8"}],
        "stateMutability":"view","type":"function"},
       {"inputs":[],
        "name":"getVar",
        "outputs":[{"internalType":"uint8","name":"","type":"uint8"}],
        "stateMutability":"view","type":"function"},
       {"inputs":[{"internalType":"uint8","name":"_var","type":"uint8"}],
        "name":"setVar","outputs":[],
        "stateMutability":"nonpayable",
        "type":"function"}]

#contractの取得
contract_instance = web3.eth.contract(address=address, abi=abi)

#contractに登録された数値を変更するトランザクションを生成
contract_instance.functions.setVar(10).transact({'from':web3.eth.accounts[0]})

#contractに登録された数値を取得
#print(contract_instance.functions.getVar().call())
