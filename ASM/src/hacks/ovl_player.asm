; Hacks in player overlay

.headersize(0x808301C0 - 0x00BCDB70)

.org 0x80834254
nop
nop
nop
nop

.org 0x80834268
ori     a0, r0, 0x6858

; Reloc (0x4094)
.org 0x80853858
nop