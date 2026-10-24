#include <SDL2/SDL.h>
#include <emscripten.h>
#ifdef __cplusplus
extern "C" {
#endif
void oga_sleep(unsigned);
unsigned oga_ticks(void);
Uint64 oga_counter(void);
int oga_playing(void);
void oga_set_playing(int);
void oga_ready(void);
void oga_present(SDL_Renderer*);
#ifdef __cplusplus
}
#endif
#define SDL_Delay(ms) oga_sleep(ms)
#define SDL_GetTicks() oga_ticks()
#define SDL_GetPerformanceCounter() oga_counter()
#define SDL_RenderPresent(r) oga_present(r)
