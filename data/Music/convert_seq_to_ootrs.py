import os
from zipfile import ZipFile

for dirpath, _, filenames in os.walk(os.path.dirname(os.path.abspath(__file__)), followlinks=True):
    for fname in filenames:
        if fname.endswith('.meta') and os.path.isfile(os.path.join(dirpath, f'{fname[:-5]}.seq')):
            music_name = fname[:-5]
            print(f'Converting {music_name} in {dirpath}')
            try:
                with ZipFile(os.path.join(dirpath, f'{music_name}.ootrs'), mode='w') as ootrs:
                    for zname in [f'{music_name}.meta', f'{music_name}.seq']:
                        ootrs.write(os.path.join(dirpath, zname))
            except FileNotFoundError as ex:
                raise FileNotFoundError(f'Missing meta or seq file for: "{music_name}". This should never happen')