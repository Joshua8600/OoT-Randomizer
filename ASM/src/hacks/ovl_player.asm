; Hacks in player overlay

.headersize(0x808301C0 - 0x00BCDB70)

.org 0x80834254
NNN_PATCH_1_START:
nop
nop
nop
nop
NNN_PATCH_1_END:

.org 0x80834268
NNN_PATCH_2_START:
ori     a0, r0, 0x6858
NNN_PATCH_2_END:

; Reloc (0x4094)

.org 0x80853858
NNN_PATCH_3_START:
nop
NNN_PATCH_3_END: