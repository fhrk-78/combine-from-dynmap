import sys
import requests
from PIL import Image
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor

# Config

x_range = (-512, 512)
y_range = (-512, 512)
dynmap_url = f"http://torosaba.net:60016"
max_thread = 1
runmemorycheck = True

# Main Process

images = {}
atpe = ThreadPoolExecutor(max_workers=max_thread)

def fetch_image(x, y, maxv):
    url = f"{dynmap_url}/tiles/main/flat/1_1/z_{x}_{y}.jpg"
    response = requests.get(url)
    images[(x, y)] = Image.open(BytesIO(response.content))
    print(f"[Done] Image downloaded. X:{x}, Y:{y}, Total:{len(images.keys())}/{maxv}")

def create_image_grid(x_range, y_range, step):
    if runmemorycheck:
        print("[....] Trying to make image grid...")
        try:
            memorycheck = Image.new('RGB', ((abs(x_range[0]) * 128) + (abs(x_range[1]) * 128), (abs(x_range[0]) * 128) + (abs(x_range[1]) * 128)))
        except MemoryError:
            print("[!ERR] MemoryError occured.")
            sys.exit(1)
        del memorycheck

    maxv = x_range[1] * y_range[1]
    for x in range(x_range[0], x_range[1], step):
        for y in range(y_range[0], y_range[1], step):
            print(f"[{str(round((x + x_range[1]) / (x_range[1] * 2) * 100)).zfill(3)}%] Image added to Queue X:{x}, Y:{y}")
            atpe.submit(fetch_image, x, y, maxv)

    atpe.shutdown()

    print("[Done] All image downloaded.")

    max_x = max(k[0] for k in images.keys())
    min_x = min(k[0] for k in images.keys())
    max_y = max(k[1] for k in images.keys())
    min_y = min(k[1] for k in images.keys())

    print("[....] Please wait for setup complete.")

    grid_width = (max_x - min_x) // step + 1
    grid_height = (max_y - min_y) // step + 1

    final_image = Image.new('RGB', (grid_width * 128, grid_height * 128))

    print("[Done] Setup complete.")

    icount = 0
    for (x, y), img in images.items():
        icount += 1
        grid_x = (x - min_x) // step
        grid_y = (max_y - y) // step  # Y方向を逆に

        final_image.paste(img, (grid_x * 128, grid_y * 128))

        print(f"[....] Combining Images... X:{x}, Y:{y}")

    return final_image

# 結合画像を作成
result_image = create_image_grid(x_range, y_range, 2)
print("[Done] Image combined. Saving now.")
result_image.save('combined_image.png')
print(f"[Done] All complete.")
result_image.show()
