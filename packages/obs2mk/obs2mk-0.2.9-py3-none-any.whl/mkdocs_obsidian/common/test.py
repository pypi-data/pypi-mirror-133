import datetime
import pathlib
import os
import glob

from mkdocs_obsidian.common import config
vault = config.vault

oldest=datetime.datetime.now()
file_name = ""
for file in glob.iglob(f"{vault}/**", recursive=True):
    file = pathlib.Path(file)
    if os.path.basename(file).endswith('.md'):
        try:
            oldtest = datetime.datetime.fromtimestamp(file.stat().st_ctime)
            if oldtest < oldest:
                oldest = oldtest
                file_name=file
        except FileNotFoundError:
            pass
print(oldest, file_name)

