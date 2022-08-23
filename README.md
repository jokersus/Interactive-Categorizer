# Interactive image sorter
Shows you pics and you press category number

## Config:
Edit `main.py`
```python
IMAGE_VIEWER_COMMAND = 'feh -. "{}"'

SEARCH_PATH = Path('/home/user/somepath')
EXTENSIONS = ['jpg', 'jpeg', 'png', 'webp']

CATEGORIES = [
    Path('IRL'),
    Path('Art/sfw'),
    Path('Art/nsfw'),
]
```
`{}` is a placeholder for the file path.
Set the command to `xdg-open "{}"` or `open "{}"` to make it universal.

## Usage:
```
python main.py [-h] [--dry-run] [--copy]

-h, --help  show this help message and exit
--dry-run   Do not move, only print
--copy      Copy instead of moving
```