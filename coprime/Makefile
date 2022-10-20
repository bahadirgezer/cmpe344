all: compile disassemble run

compile: coprime.s
	riscv32-unknown-elf-gcc coprime.s -o coprime.elf -nostdlib
	echo "compiled..."
	
disassemble: coprime.elf
	riscv32-unknown-elf-objdump --disassemble coprime.elf > coprime.dis
	echo "disassembled..."

run: compile
	echo "running..."
	whisper --interactive coprime.elf
	