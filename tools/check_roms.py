import urllib.request
import os

games = [
    'dino',
    'sf2ce',
    'sf2',
    'snowbros',
    'goldnaxe',
    'mslug',
    'mslugx',
    'neogeo',
    'pang',
    'captcomm',
    'ffight',
    'tmnt',
    'simpsons',
    'punisher',
    '1942',
    '1943'
]

os.makedirs('s:/Proyectos/Nokia8010/roms_arcade', exist_ok=True)

headers = {'User-Agent': 'Mozilla/5.0'}

for g in games:
    url = f'https://archive.org/download/arcade_{g}/{g}.zip'
    dest = f's:/Proyectos/Nokia8010/roms_arcade/{g}.zip'
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            status = resp.status
            length = resp.headers.get('Content-Length')
            print(f'Checking {g}: status {status}, size {length} bytes')
    except Exception as e:
        print(f'Failed {g}: {e}')
