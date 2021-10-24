//async function getAccount() {
//    var Web3 = require('web3');
//    var web3 = new Web3();
//    web3.setProvider(new web3.providers.HttpProvider('http://localhost:8545'));
//    var accounts = await web3.eth.getAccounts();
//    return accounts;
//}


var Web3 = require('web3');
var web3 = new Web3();
web3.setProvider(new web3.providers.HttpProvider('http://localhost:8545'));

let msg = 'Hello, signature';
let hash = web3.utils.sha3(msg);

console.log("message: " + msg);
console.log("message hash: " + hash);


var sha = '0x' + web3.utils.sha3("Hello");
/*アカウントのアドレス（ここではマイナーのアドレス)とハッシュ値を渡して署名(132文字)を作成*/
var sig = web3.eth.sign("0x797612037bac3c467ebc91bbf8c03cd8f9d9f902", sha);

//プレフィックス"0x"を取り除く
sig = sig.substr(2, sig.length);
//前半64文字にプレフィックス"0x"をつける
var r = '0x' + sig.substr(0, 64);
//後半64文字にプレフィックス"0x"をつける
var s = '0x' + sig.substr(64, 64);
//末尾２文字を１６進法に変換し２７を足す
var v = web3.toDecimal(sig.substr(128, 2)) + 27;

//アカウント作成
//var _account = web3.eth.personal.newAccount("konndoru33");
//console.log(_account)

