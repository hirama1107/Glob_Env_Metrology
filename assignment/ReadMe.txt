# ReadMe

author: Tatsuya Hirama
edit: 2024/12/19

任意の座標を含んだSGLIの地表面反射率（h5）をダウンロードし、RED, NIR, NDVIの画像および指定したCrop_sizeの画像を出力するプログラム



# 構成
assignment
├ ReadMe
└ src
  ├ assighment_sgli.py
  ├ get_tileID.py
  ├ multi_process.sh
  ├ process.sh
  └ sglicod.py




# 説明
・ReadMe
これ

・assignment_sgli.py
主要プログラム。図をいじりたい場合はcreate_colormap, plot_and_save, plot_imageなどの関数をいじればいい。

・get_tileID.py
タイルのIDをとってくる。いじる必要はない。

・multi_process.sh
任意の期間で処理を行いたい場合に使用。srcディレクトリで`source multi_process.sh`で実行。
期間を変えるには,Parametersの所をいじればいい。MONTH, DAYは二桁で指定しないとバグる。

・process.sh
任意の時間のみで処理を行う場合に使用。srcディレクトリで`source process.sh`で実行。
MONTH, DAYは二桁で指定しないとバグる。

・sglicod.py
カジカジが書いたプログラム。ありがとう。


# 使い方
シェルスクリプト内のParametersをいじってあとは`source XXXX.sh`で実行。
wdにはassinmentのディレクトリを指定。
うまくいけばdata, outputというディレクトリが作成される。
outputには計6個の画像が出力される。
※ライブラリエラーが出たらpip install
