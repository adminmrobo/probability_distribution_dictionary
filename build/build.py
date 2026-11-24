import json,re,pathlib
src=pathlib.Path('tables.src.html').read_text()
sp=pathlib.Path('sprites.js').read_text()
data=pathlib.Path('data.json').read_text()
out=src.replace('/*@@SPRITES@@*/',sp).replace('/*@@DATA@@*/',data)
pathlib.Path('../tables.html').write_text(out)
print(len(out)//1024,'KB')


# ── 지식 색인 다시 덧붙이기 (kg/pages/, ai-lab-retrofit autokg) ──
# 빌드가 페이지를 다시 쓰면 덧붙인 #kg가 사라지므로 빌드 끝에서 다시 덧붙인다. kg/reapply.py가 없으면 아무것도 하지 않는다.
if __name__ == "__main__":
    import os as _os, sys as _sys, subprocess as _sp
    _r = _os.path.dirname(_os.path.abspath(__file__))
    for _i in range(3):
        if _os.path.exists(_os.path.join(_r, "kg", "reapply.py")): break
        _r = _os.path.dirname(_r)
    if _os.path.exists(_os.path.join(_r, "kg", "reapply.py")):
        _sp.run([_sys.executable, _os.path.join(_r, "kg", "reapply.py"), _r])
