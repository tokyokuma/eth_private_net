# eth_private_net
## Ethereumで署名と検証を実施

## 環境
OS : Ubuntu20.04

Geth : 1.10.11-stable

言語 : python3,solidity

## 準備
```bash
$ git clone https://github.com/tokyokuma/eth_private_net.git
$ cd eth_private_net/
```
## 手順
## 1.Gethをプライベートネットで起動

### genesisブロックの初期化
```bash
$ geth --datadir ./ init ./myGenesis.json
```
### gethの起動
```bash
$ geth --networkid "15" --nodiscover --datadir ./ console 2>> ./geth_err.log
```
### アカウントの作成してマイニングテストし一旦gethを終了
```bash
> personal.newAccount("test01")
> miner.start()
> miner.stop()
> exit
```

## 2.コントラクトコードをコンパイルしbinとabiを取得
```bash
$ solc --abi --bin src/solc/contract_sign.sol
Binary:
608060405234801561001057600080fd5b5061028b806100206000396000f3fe608060405234801561001057600080fd5b506004361061002b5760003560e01c806319add5e314610030575b600080fd5b61004a6004803603810190610045919061012f565b610060565b60405161005791906101d7565b60405180910390f35b6000600185858585604051600081526020016040526040516100859493929190610210565b6020604051602081039080840390855afa1580156100a7573d6000803e3d6000fd5b505050602060405103519050949350505050565b600080fd5b6000819050919050565b6100d3816100c0565b81146100de57600080fd5b50565b6000813590506100f0816100ca565b92915050565b600060ff82169050919050565b61010c816100f6565b811461011757600080fd5b50565b60008135905061012981610103565b92915050565b60008060008060808587031215610149576101486100bb565b5b6000610157878288016100e1565b94505060206101688782880161011a565b9350506040610179878288016100e1565b925050606061018a878288016100e1565b91505092959194509250565b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b60006101c182610196565b9050919050565b6101d1816101b6565b82525050565b60006020820190506101ec60008301846101c8565b92915050565b6101fb816100c0565b82525050565b61020a816100f6565b82525050565b600060808201905061022560008301876101f2565b6102326020830186610201565b61023f60408301856101f2565b61024c60608301846101f2565b9594505050505056fea2646970667358221220a45ccd3b6fff6e161643fb561f118b42f288f68d9e1fa2e5335a4490adf73a7864736f6c63430008090033
Contract JSON ABI
[{"inputs":[{"internalType":"bytes32","name":"msgh","type":"bytes32"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"ecr","outputs":[{"internalType":"address","name":"sender","type":"address"}],"stateMutability":"pure","type":"function"}]
```

## 3.作成したアカウントのロックを解除/web3.pyから操作可能にしてgethを起動
```bash
$ geth --allow-insecure-unlock --unlock --http --http.port 8545 --http.api "web3,eth,net,personal" --http.corsdomain "*" --http.addr "0.0.0.0" --datadir ./ --nodiscover --networkid 15 console 2>> geth_err.log
※Password:test パスワードの入力を要求される
```

### Contractアカウントの作成
```bash
> var bin = "0x~"   //コンパイル時に出力されたBinaryにprefixを付加して変数に格納
> var abi = [~]     //コンパイル時に出力されたContract JSON ABIを格納
> var contract = eth.contract(abi)
//トランザクションを送信⇒マイニングしContractのアドレスを付加する
> var myContract = contract.new({ from: eth.accounts[0], data: bin})
> miner.start()     //
> myContract        //addressにアドレスが付加されていればOK
```
## 4.署名生成,署名検証を実施するpyファイルを実行
実行前にsign.pyを修正
24行目：keystore以下に生成された"UTC~"で始まるファイル目に置き換え

50行目：myContractに付加されたアドレスに置き換え

※terminalをもう一つ開き,eth_private_net以下でコマンドを実行
```bash
$ python ./src/py/sign.py
```
署名者アドレスとecrecoverにより復元されたアドレスが一致していれば
```bash
The addresses match. Varification OK
```
一致していなければ
```bash
The addresses match. Varification OK
```
が出力される

※注意
十分なetherを保有していないとgasが不足しエラーとなる
>Caller gas above allowance, capping      requested=125,100,486 cap=50,000,000



