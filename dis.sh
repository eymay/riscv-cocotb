#!/bin/zsh
llvm-mc-14 --assemble --triple=riscv32 --filetype=obj <(echo "$1") -o "$2.elf"
llvm-objdump-14 -d "$2".elf | tail -1 | awk '{print $2 " " $3 " " $4 " " $5}'
