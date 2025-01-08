# combine-from-dynmap

- Python: 3.12.6

If Windows:

```ps
> py -3.12 -m venv .venv
> .\.venv\Scripts\activate
(.venv) > pip install -r requirements.txt
```

Dynmapから拡大画像を結合して高解像度地図画像を生成するコード

よほどインターネットがつよつよでなければ平行スレッド数は1~2にすることをおすすめします

```py
import requests
from PIL import Image
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor

# Config

# === Note ===
# タイル座標は偶数である必要があります。
# また、1タイル座標は8チャンクx8チャンクになっているはずです。(よくわからん)

x_range = (-128, 128)                     # 開始タイルのタプル (X1, X2)
y_range = (-128, 128)                     # 終了タイルのタプル (Y1, Y2)
dynmap_url = f"http://torosaba.net:60016" # Dynmapのドメイン名
max_thread = 1                            # ダウンロードの最大並行スレッド数
memorycheck = True                        # ダウンロード前に念の為、キャンバスを試しに作ります。それをスキップするにはFalseに設定してください。

# MemoryCheckはあくまでもキャンバスサイズを試算して作成するだけです。実際はダウンロードも行うのでそれ以上のメモリが必要です。

# Main Process

# ...
```
