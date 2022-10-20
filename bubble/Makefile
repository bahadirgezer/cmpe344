all: compile disassemble run

compile: bubble.s
	riscv32-unknown-elf-gcc bubble.s -o bubble.elf -nostdlib
	echo "compiled..."
	
disassemble: bubble.elf
	riscv32-unknown-elf-objdump --disassemble bubble.elf > bubble.dis
	echo "disassembled..."

run: compile
	echo "running..."
	whisper --interactive bubble.elf
	