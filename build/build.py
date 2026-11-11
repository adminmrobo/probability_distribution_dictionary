import json,re,pathlib
src=pathlib.Path('tables.src.html').read_text()
sp=pathlib.Path('sprites.js').read_text()
data=pathlib.Path('data.json').read_text()
out=src.replace('/*@@SPRITES@@*/',sp).replace('/*@@DATA@@*/',data)
pathlib.Path('../tables.html').write_text(out)
print(len(out)//1024,'KB')
