Needs fonttools

```sh
sudo pacman -S python-fonttools
sudo pacman -S python-brotli
python3 genFac.py --feature out.fea
python3 apply.py out.fea NotoSans-Regular.ttf myFont.woff2
```
