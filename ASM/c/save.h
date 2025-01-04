#ifndef SAVE_H
#define SAVE_H
#include <stdbool.h>
#include "override.h"

// Struct for storing additional data in SRAM. This has to always be a multiple of 2 bytes long supposedly.
typedef struct {
    uint8_t silver_rupee_counts[0x16];
    bool collected_dungeon_rewards[8];
    uint8_t enemy_spawn_flags[8];
    uint8_t soul_enable_flags[8];
    uint8_t has_fishing_rod;
    uint8_t largest_fish_found[2]; // index 1 = child, index 0 = adult
    uint8_t has_loach;
    uint8_t password[6];
    override_t incoming_queue[3]; // Keep these at the end so it doesn't screw up anything which we defined in SaveContext.py

} extended_savecontext_static_t __attribute__ ((aligned (8)));


typedef union {
    uint32_t all;
    struct {
        uint16_t offset;
        uint8_t type;
        uint8_t value;
    };
} extended_initial_save_entry;


extern extended_initial_save_entry EXTENDED_INITIAL_SAVE_DATA;
extern extended_savecontext_static_t extended_savectx;

void SsSram_ReadWrite_Safe(uint32_t addr, void* dramAddr, size_t size, uint32_t direction);

#endif
