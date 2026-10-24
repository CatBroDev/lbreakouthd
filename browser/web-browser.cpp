// GPL-3.0-or-later. Browser integration: Old Games Archive / CatBroDev.
#include <SDL2/SDL.h>
#include <SDL2/SDL_mixer.h>
#include <emscripten.h>
#include <cstring>
#undef SDL_GetTicks
#undef SDL_GetPerformanceCounter
#undef SDL_Delay
#undef SDL_RenderPresent
static int paused=0,muted=1,stopping=0,playing=0;
static Uint32 pauseStart=0,pauseTotal=0;
static Uint64 counterStart=0,counterTotal=0;
static void gate(void*,Uint8* buffer,int length){if(muted||paused||stopping)std::memset(buffer,0,length);}
extern "C" {
EMSCRIPTEN_KEEPALIVE void oga_release(){SDL_ResetKeyboard();SDL_FlushEvents(SDL_KEYDOWN,SDL_MOUSEWHEEL);}
EMSCRIPTEN_KEEPALIVE int oga_paused(){return paused;}
EMSCRIPTEN_KEEPALIVE void oga_pause(int value){oga_release();if(value&&!paused){pauseStart=SDL_GetTicks();counterStart=SDL_GetPerformanceCounter();}if(!value&&paused){pauseTotal+=SDL_GetTicks()-pauseStart;counterTotal+=SDL_GetPerformanceCounter()-counterStart;}paused=value!=0;}
EMSCRIPTEN_KEEPALIVE void oga_mute(int value){muted=value!=0;}
static void requestQuit(){SDL_Event e={};e.type=SDL_QUIT;SDL_PushEvent(&e);}
EMSCRIPTEN_KEEPALIVE void oga_stop(){stopping=1;oga_pause(0);requestQuit();}
unsigned oga_ticks(){return (paused?pauseStart:SDL_GetTicks())-pauseTotal;}
Uint64 oga_counter(){return (paused?counterStart:SDL_GetPerformanceCounter())-counterTotal;}
int oga_playing(){return playing;}
void oga_set_playing(int value){playing=value;}
void oga_ready(){Mix_SetPostMix(gate,nullptr);EM_ASM(if(Module.onGameReady)Module.onGameReady(););}
void oga_sleep(unsigned ms){do{emscripten_sleep(paused?30:(ms?ms:1));if(stopping)requestQuit();}while(paused&&!stopping);}
void oga_present(SDL_Renderer*r){SDL_RenderPresent(r);oga_sleep(1);}
}
