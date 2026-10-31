# Plan: XRAM / XPAGE

Status: `[PROPOSAL]`. Not implemented.

## Problem

The SAB 80C517A/83C517A-5 has 2 KiB of on-chip XRAM, enabled through `SYSCON.XMAP0` and
`SYSCON.XMAP1`. `XPAGE` supplies the upper address byte for `MOVX @Ri`.

Kuna's generic 8051 language has no `XRAM` space. `MOVX @DPTR` lowers to `EXTMEM`.

## What was tried

1. A pspec memory block for `EXTMEM:f800` — compiled; no output change.
2. An `XRAM` space plus a symbol at `XRAM:f800` — compiled; still `dat_f800`.
3. Conditional `ATDPTR` — SLEIGH rejected p-code labels in that pointer subtable.
4. Conditional `MOVX` constructors — compiled, but the fixture decompiled to only
   `return;`; the custom space is not surfaced.

## Proposed design

1. Add a C517A-specific `.slaspec`.
2. Define an `XRAM` space and map it to the on-chip window.
3. Select `XRAM` vs `EXTMEM` in the `MOVX` constructors.
4. Model `SYSCON.XMAP0/XMAP1` and `XPAGE` separately.
5. Add an `xram` option if emitted C changes.
6. Add a two-pass stage test with a `MOVX @DPTR` and a `MOVX @Ri` fixture.

## Acceptance

- A `MOVX @DPTR` to `0xf800` and above targets XRAM.
- A `MOVX @DPTR` below `0xf800` still targets EXTMEM.
- `MOVX @Ri` uses `XPAGE`.
- The option off preserves current output.

## Out of scope

- DPSEL
- banked 128 KiB images
- CCU/ADC/MDU behavior
