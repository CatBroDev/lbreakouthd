from pathlib import Path
import os,sys,shutil,subprocess,json,time,hashlib,tarfile
lab=Path(__file__).resolve().parent;src=lab/'author-source/lbreakouthd-1.2.4';out=lab/'build'/sys.argv[1];out.mkdir(parents=True,exist_ok=False)
archive=lab/'vendor/lbreakouthd-1.2.4.tar.gz'
if not src.exists():
 assert hashlib.sha256(archive.read_bytes()).hexdigest()=='4732c3852ba0030fecca65689591ac582c86af46b1a21b274640ffc6cd8fc826'
 src.parent.mkdir(exist_ok=True)
 with tarfile.open(archive) as tar:tar.extractall(src.parent,filter='data')

shutil.copytree(src,out/'src');src=out/'src';sdk=Path(os.environ.get('LBREAKOUT_EMSDK',str(lab/'emsdk')));env=dict(os.environ,EM_CONFIG=str(sdk/'.emscripten'),EMSDK_PYTHON=sys.executable,TEMP=str(out),TMP=str(out),EMCC_CORES='4')
shutil.copy2(lab/'web-compat.h',out/'compat.h')
p=src/'src/config.cpp';t=p.read_text();t=t.replace('\tmode = 0;','\tmode = 1;');p.write_text(t)
p=src/'src/tools.cpp';t=p.read_text();t=t.replace('return string(getenv("HOME")?getenv("HOME"):".");','return string("/persistent_data");');p.write_text(t)
# Native checkpoint and shutdown paths, never synthesize game progress.
p=src/'src/view.h';s=p.read_text();s=s.replace('public:\n\tView(', 'public:\n\tvoid browserCheckpoint(){if(oga_playing()&&!editor.testRequested())saveGame();cgame.saveHiscores();config.save();}\n\tView(');p.write_text(s)
p=src/'src/view.cpp';s=p.read_text();s=s.replace('void View::run()\n{','void View::run()\n{\n\toga_set_playing(1);');s=s.replace('\tupdateResumeGameTooltip();\n\n\tfade();','\toga_set_playing(0);\n\tupdateResumeGameTooltip();\n\n\tfade();');p.write_text(s)
p=src/'src/main.cpp';s=p.read_text();s=s.replace('int main(int argc', 'static View *oga_view=nullptr;\nstatic ClientGame *oga_game=nullptr;\nextern "C" EMSCRIPTEN_KEEPALIVE void oga_checkpoint(){if(oga_view)oga_view->browserCheckpoint();}\n#ifdef OGA_DIAGNOSTIC\nextern "C" EMSCRIPTEN_KEEPALIVE int oga_state(int i){Game*g=oga_game?oga_game->getGameContext():nullptr;const Uint8*k=SDL_GetKeyboardState(nullptr);switch(i){case 0:return g?g->paddles[0]->x:-1;case 1:return g?g->paddles[0]->score:-1;case 2:return oga_playing();case 3:return k[SDL_SCANCODE_RIGHT];case 4:return k[SDL_SCANCODE_SPACE];case 5:return g?g->paddles[0]->attached_ball_count:-1;case 6:return g?g->bricks_left:-1;default:return 0;}}\n#endif\nint main(int argc');s=s.replace('\tview.runMenu();','\toga_view=&view;oga_game=&cgame;oga_ready();\n\tview.runMenu();\n\toga_view=nullptr;oga_game=nullptr;');p.write_text(s)
shutil.copy2(lab/'web-browser.cpp',src/'src/web-browser.cpp')
p=src/'src/sdl.cpp';s=p.read_text();s=s.replace('SDL_SetTextureBlendMode(newtex, SDL_BLENDMODE_BLEND);','SDL_BlendMode originalBlend;\n\tSDL_GetTextureBlendMode(tex, &originalBlend);\n\tSDL_SetTextureBlendMode(newtex, originalBlend);');p.write_text(s)
data=out/'data';data.mkdir();
for name in ['levels','themes']:shutil.copytree(src/'src'/name,data/name,ignore=shutil.ignore_patterns('Makefile*','*.svg','.DS_Store'))
shutil.copy2(src/'src/empty.hscr',data/'lbreakouthd.hscr')
flags=(['-DOGA_DIAGNOSTIC'] if '--state' in sys.argv else [])+['-O1','-sUSE_SDL=2','-sUSE_SDL_IMAGE=2','-sSDL2_IMAGE_FORMATS=["png","jpg"]','-sUSE_SDL_MIXER=2','-sSDL2_MIXER_FORMATS=[]','-sUSE_SDL_TTF=2','-include',str(out/'compat.h'),'-I'+str(src),'-I'+str(src/'src'),'-I'+str(src/'libgame'),'-DPACKAGE_NAME="LBreakoutHD"','-DPACKAGE_VERSION="1.2.4"','-DDATADIR="/data"','-DSRC_DIR="/data"','-DHISCOREDIR="/persistent_data"','-DCONFIGDIR=".lbreakouthd"','-DCONFIG_DIR_NAME=".lbreakouthd"','-Wno-int-conversion','-Wno-implicit-function-declaration']
objects=[];start=time.monotonic();log=(out/'build.log').open('w')
for f in sorted([* (src/'src').glob('*.cpp'),*(src/'libgame').glob('*.c')]):
 o=out/(f.parent.name+'-'+f.stem+'.o');compiler='em++.py' if f.suffix=='.cpp' else 'emcc.py'
 cmd=[sys.executable,str(sdk/'upstream/emscripten'/compiler),*flags,*(['-std=c++11'] if f.suffix=='.cpp' else []),'-c',str(f),'-o',str(o)]
 r=subprocess.run(cmd,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=180)
 if r.returncode:log.close();print((out/'build.log').read_text()[-4000:]);sys.exit(r.returncode)
 objects.append(o)
cmd=[sys.executable,str(sdk/'upstream/emscripten/em++.py'),*[str(p) for p in objects],*flags,'-sASYNCIFY','-sASYNCIFY_STACK_SIZE=131072','-sSTACK_SIZE=1048576','-sALLOW_MEMORY_GROWTH=1','-sFORCE_FILESYSTEM=1','-sEXPORTED_RUNTIME_METHODS=["FS","IDBFS","callMain","addRunDependency","removeRunDependency"]','-sEXIT_RUNTIME=1','-lidbfs.js','--preload-file',str(data)+'@/data','-o',str(out/'game.js')]
r=subprocess.run(cmd,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=120);log.close();result={'exitCode':r.returncode,'units':len(objects),'seconds':round(time.monotonic()-start,1)};(out/'build-result.json').write_text(json.dumps(result));print(json.dumps(result))
if r.returncode:print((out/'build.log').read_text()[-4000:]);sys.exit(r.returncode)
for p in (lab/'web').iterdir():shutil.copy2(p,out/p.name)
for ext in ['wasm','data']:shutil.copy2(out/('game.'+ext),out/('game.'+ext+'.bin'))
