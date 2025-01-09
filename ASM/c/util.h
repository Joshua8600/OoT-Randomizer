#ifndef UTIL_H
#define UTIL_H

#include <n64.h>
#include "z64.h"

#define array_size(a) (sizeof(a) / sizeof(a[0]))

void heap_init();
void* heap_alloc(int bytes);

typedef struct {
    uint8_t* buf;
    uint32_t vrom_start;
    uint32_t size;
} file_t;

typedef void (*read_file_fn)(void* mem_addr, uint32_t vrom_addr,
        uint32_t size);
#define read_file ((read_file_fn)0x80000DF0)

void file_init(file_t* file);
void* resolve_actor_overlay_addr(void* addr, z64_actor_t* actor);
void* resolve_overlay_addr(void* addr, uint16_t overlay_id);
void* resolve_player_ovl_addr(void* addr);
void* resolve_kaleido_ovl_addr(void* addr);

extern void ZeldaArena_GetSizes(uint32_t* outMaxFree, uint32_t* outFree, uint32_t* outAlloc);

#endif
