# Plan: DPSEL / eight data pointers

Status: `[PROPOSAL]`. Not implemented.

## Problem

The SAB 80C517A/83C517A-5 has eight 16-bit data pointers. `DPSEL` bits 0–2 select the
pointer used by `MOV DPTR`, `INC DPTR`, `MOVX @DPTR` and `MOVC @A+DPTR`.

Kuna models one `DPL/DPH` pair. Code that writes `DPSEL` is decompiled as if the bank
never changed.

## Why the spec cannot fix it

`8051_main.sinc` has a `DUAL_DPTR` path for two pointers, but:

- it covers at most two banks,
- it swaps on `INC`/`DEC`, not on `DPSEL` writes,
- a `processor_spec` can name `DPSEL` but cannot change instruction p-code.

A spike using `DUAL_DPTR` compiled but produced:

```c
DPSEL = 1;
dat_1234 = 0;
```

for a `MOV DPSEL,#1; MOV DPTR,#1234h; MOVX @DPTR,A` sequence.

## Proposed design

1. Add a C517A-specific `.slaspec`.
2. Define `DPTR0`–`DPTR7` as 16-bit registers.
3. Add a 3-bit context field for the selected bank.
4. Handle the direct `MOV DPSEL,#imm` case; fall back to DPTR0 for unknown writes.
5. Add `dptrbank` as an option, default **off**.
6. Add a two-pass stage test for off/on.

## Acceptance

- The bank-select fixture emits the selected DPTR.
- Unknown/dynamic `DPSEL` writes are reported, not silently guessed.
- `dptrbank` off preserves current output.
- Existing 8051 targets are unchanged.

## Out of scope

- banked 128 KiB images
- interrupt-time DPSEL changes
- XRAM/XPAGE
- SFR names
