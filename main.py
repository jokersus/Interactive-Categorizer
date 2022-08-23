import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

from pynput import keyboard

# ================= Config =================
IMAGE_VIEWER_COMMAND = 'feh -. "{}"'

SEARCH_PATH = Path('/home/user/somepath')
EXTENSIONS = ['jpg', 'jpeg', 'png', 'webp']

CATEGORIES = [
    Path('IRL'),
    Path('Art/sfw'),
    Path('Art/nsfw'),
]
# ==========================================

# ================= Setup ==================
parser = argparse.ArgumentParser(description='Interactively sorts images into categories')
parser.add_argument('--dry-run', help='Do not move, only print', action='store_true', default=False)
parser.add_argument('--copy', dest='sorter', help='Copy instead of moving', action='store_const', const=shutil.copy,
                    default=shutil.move)
args = parser.parse_args()

if args.dry_run:
    args.sorter = lambda file, cat: print(f'[DRY RUN] Sorted {file.name} into {cat}')

if not SEARCH_PATH.exists():
    sys.exit(f'Search dir "{SEARCH_PATH}" does not exist')

# Create sorted dirs
for c in CATEGORIES:
    c.mkdir(exist_ok=True, parents=True)
# ==========================================

print('=============== Categories ===============')
print('\n'.join([f'{i + 1}\t{c}' for i, c in enumerate(CATEGORIES)]))

for f in SEARCH_PATH.rglob('*'):
    ext = os.path.splitext(f)[1][1:]

    if ext.lower() not in EXTENSIONS:
        continue

    process = subprocess.Popen(IMAGE_VIEWER_COMMAND.format(f), shell=True)

    with keyboard.Events() as events:
        # Try to get correct category index
        while True:
            event = events.get()

            try:
                key = int(event.key.char)
                category = CATEGORIES[key - 1]  # For 0 index
                break
            except (AttributeError, ValueError):
                continue
            except IndexError:
                print(f'Category number {key} too large (max {len(CATEGORIES)})')
            finally:
                # For the key release event. Not very reliable
                events.get()

        # Move the file
        args.sorter(f, category / f.name)

    process.terminate()
