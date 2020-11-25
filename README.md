# ボットデスくん

![私がボットデス](https://github.com/sakots/botdesu/blob/main/ico136.png?raw=true)

ポケモンマストドン「[ポケマス](https://pokemon.mastportal.info/)」のさらに一部界隈で有名な、pythonで動くマストドンのマルコフ連鎖botです。

## 概要

おれはしゅうまい君が作りたかったんだよ…

## ここがすごいぞボットデス

エラーで止まっても自分でそれを把握して勝手に再起動する
- ホストドン側でエラーが出ることが多いので導入しました

## 使い方（下準備）

- MeCab
  - インストール必須。mecab-ipadic-NEologdあたりの辞書を用意すると良いです。
- botをユーザー登録するためのマストドンアカウント
  - そりゃ必要ですわな。その後アカウント→開発から mastodon-api の `client_id` `access_token` `client_secret` あたりがないと動かないですよ。
- .envファイルの設定
  - マストドンでbotを動かすための設定を書いてあるファイルです。プログラム内に直接書くのは気がひけるので分けました。

## 使い方（Python編）

- 以下をpythonで使えるようにpipとか使ってなんとかする。
  - MeCab
  - Mastodon
  - load_dotenv
  - schedule
- 他なにか足りなければ動かしたときに「おいこれがねえぞ」ってエラーが出るのでそれ見て適宜導入してください。

## 気になる点

- やっぱなんかソースきれいではない

---

特に指定がない限り、ボットデスくんのすべてのコンテンツは[クリエイティブ・コモンズ 表示 - 継承3.0ライセンス](https://creativecommons.org/licenses/by-sa/3.0/deed.ja) の元で利用可能だと思います。
