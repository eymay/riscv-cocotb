#!/bin/zsh
llvm-mc --assemble --triple=riscv32 --filetype=obj <(echo "$1") -o "$2.elf"
llvm-objdump -d "$2".elf | tail -1 | awk '{print $2 " " $3 " " $4 " " $5}'
rm "$2.elf"
