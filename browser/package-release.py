from pathlib import Path
import hashlib,json,os,shutil,sys,zipfile,gzip
lab=Path(__file__).resolve().parent;build=lab/'build'/sys.argv[1];src=lab/'author-source/lbreakouthd-1.2.4'
sdk=Path(os.environ.get('LBREAKOUT_EMSDK',str(lab/'emsdk')))/'upstream/emscripten'
assert '_oga_state' not in (build/'game.js').read_text()
licenses=lab/'licenses';licenses.mkdir(exist_ok=True)
shutil.copy2(sdk/'LICENSE',licenses/'Emscripten-MIT-NCSA.txt')
for name in ['sdl2','sdl2_image','sdl2_mixer','sdl2_ttf','libpng','zlib','freetype','harfbuzz','libjpeg']:
 folder=sdk/'cache/ports'/name
 if not folder.exists():continue
 paths=[p for p in folder.rglob('*') if p.is_file() and p.name.lower() in ['license','license.txt','copying','copyright','ftl.txt','readme.ijg']]
 for i,p in enumerate(sorted(paths)):shutil.copy2(p,licenses/(name+'-'+str(i)+'-'+p.name))
notice=(lab/'RELEASE-README.md').read_text(encoding='utf-8')
for p in sorted([p for folder in [src,licenses] for p in folder.rglob('*') if p.is_file() and (p.name.lower().startswith(('readme','license','copying','credits','sil-ofl')) or p.parent==licenses)]):
 notice+='\n\n=== '+p.relative_to(lab).as_posix()+' ===\n'+p.read_text(encoding='utf-8',errors='replace')
(build/'notices.txt').write_text(notice,encoding='utf-8');shutil.copy2(src/'COPYING',build/'COPYING.txt');shutil.copy2(lab/'RELEASE-README.md',build/'README.txt')
items=[p for folder in [src,lab/'web',licenses] for p in folder.rglob('*') if p.is_file()]
items += [lab/p for p in ['RELEASE-README.md','build-browser.py','package-release.py','web-browser.cpp','web-compat.h','control-reference.json','vendor/lbreakouthd-1.2.4.tar.gz','BUILD.md','accept-release.mjs','package.json']]
sha=lambda b:hashlib.sha256(b).hexdigest();items=sorted(set(items))
manifest=[{'path':p.relative_to(lab).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in items]
with zipfile.ZipFile(build/'source.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in items:
  info=zipfile.ZipInfo(p.relative_to(lab).as_posix(),date_time=(2026,10,24,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,p.read_bytes())
 z.writestr('SOURCE-MANIFEST.json',json.dumps(manifest,indent=2))
names=['index.html','game.js','game.wasm.bin','game.data.bin','bridge.js','input.js','persistence.js','COPYING.txt','README.txt','notices.txt','source.zip']
files=[{'path':n,'bytes':(build/n).stat().st_size,'sha256':sha((build/n).read_bytes())} for n in names]
(build/'release-manifest.json').write_text(json.dumps({'source':'1.2.4','containsTestExports':False,'files':files},indent=2))
print(json.dumps({'sourceFiles':len(items),'runtimeFiles':len(files),'preloadBytes':(build/'game.data.bin').stat().st_size,'preloadGzipBytes':len(gzip.compress((build/'game.data.bin').read_bytes())),'sourceBytes':(build/'source.zip').stat().st_size}))
