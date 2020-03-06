# Brain-kinematics-decoder
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](https://github.com/RyotaroNumata/Brain-kinematics-decoder/blob/master/LICENSE) <br>
Brain-kinematics-decoderは，脳表面に留置されたアレイ電極より記録された硬膜下皮質脳波(ECoG)から指先の屈曲進展運動を推定するシンプルなブレインコンピュータフェース(BCI)です．<br>


## デモ
デコーディング解析を用いて皮質脳波(ECoG)から指の屈曲，進展運動を推定します.<br>
このデモではBCI competion Ⅳより提供されているデータセットを用いています.<br>


![eventrelated](https://user-images.githubusercontent.com/60598478/75867436-f8527b00-5e49-11ea-8b41-971995cfa2fb.gif)

![tfviewer](https://user-images.githubusercontent.com/60598478/75867381-deb13380-5e49-11ea-92fa-87c573e9b654.gif)


![Brain-kinematics-decoder](https://user-images.githubusercontent.com/60598478/74128402-70010180-4c20-11ea-825c-846e36d016f9.gif)

## Major features
- GUI<br>
上記のデモのようにGUIベースで解析が可能なため，コードを記述する必要がほとんどありません.（願望）<br>
基本的には数値を入力してボタンクリックで使えるようにしたいと思う．
#

## インストール手法
### 実行のための環境について
- Linux， Windows (MacOS Xでは動くかわからない)
- Python 3.7

### Install Brain-Kinematics-Decoder
基本的に[Anaconda](https://www.anaconda.com/enterprise/)環境下であることが前提です<br>
anacondaが未インストールの場合は上記リンクよりダウンロードしてインストールしてください．<br>

a. 下記コマンド仮想環境と作り,作成した環境へ切り替える．

```shell
conda create -n BrainDecoder python=3.7 anaconda
conda activate BrainDecoder
```

b. [MNE-Python](https://anaconda.org/conda-forge/mne)をインストールします.

```shell
conda install -c conda-forge mne
```

c. Brain-kinematics-decoderのレポジトリをクローンします.

```shell
git clone https://github.com/RyotaroNumata/Brain-kinematics-decoder.git
cd Brain-kinematics-decoder
```
d. [BCI competition Ⅳ](http://www.bbci.de/competition/iv/) のデータセットのダウンロードには公式HPでのユーザ登録が必要です．<br>　登録した後Data sets 4をダウンロードします.

### データセットの準備 <br>
データセットをダウンロードしたあとに以下に示す構造でデータを配置します.<br>
```
Brain-kinematics-decoder
├── FileIO
├── Model
├── SignalProcessing
├── Utils
└── data
     └── BCI4
          └──subject_ECoG_data
```
## 解析をはじめる<br>
GUIベースでインタラクティブに解析実施する場合は，以下のコマンドをターミナルもしくはコマンドプロンプトで実行してください．<br>
```
python GUImain.py
```
また,　IDEで実行する場合は以下のコードを参照してください．そのまま実行もできます.
```
python Decodig_main.py
```
jupyter notebookもあります．こちら少々ですが解説付きです.
[jupyter demo](https://github.com/RyotaroNumata/Brain-kinematics-decoder/blob/master/Decoding_code_demo.ipynb)


## Licence

[MIT](https://github.com/RyotaroNumata/Brain-kinematics-decoder/blob/master/LICENSE)

## Author
沼田椋太郎<br>
[RyotaroNumata](https://github.com/RyotaroNumata)<br>
何か不明点等ありましたらお気軽に連絡してください