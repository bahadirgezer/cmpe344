.globl _start

.equ M, 7

.data
D: .word 5,7,0, 8,24,0, 11,44,0, 11,18,0, 36,2,0, 63,27,0, 19,24,0

.text
gcd:

# Insert gcd function below.

	beq a0, x0, gcd_end	
	mv t0, a0
	rem a0, a1, a0
	mv a1, t0
	j gcd

	gcd_end:
	mv a0, a1 # load 1 or 2 depending on the result
	li a1, 1
	beq a0, a1, load_res
	li a0, 2

	load_res:

# Insert gcd function above.

	ret

coprime:

# Insert coprime function below.
	mv t2, ra # store the return address for _start
	
	coprime_loop:
	lw a0, 0(s0)
	lw a1, 4(s0)
	jal gcd
	sw a0, 8(s0) # store the return value of gcd in the stack
	addi s0, s0, 12
	blt s0, s1, coprime_loop 

	mv ra, t2 # reload the return address for _start

# Insert coprime function above.

	ret

_start:

# Insert _start function below.

	la s0, D  # Data address in s0
	li s1, M
	li t0, 12
	mul s1, s1, t0 
	add s1, s1, s0 	# s1 = 3 * M * 4 + D
	mv t3, ra
	jal coprime
	mv ra, t3
# Insert _start function above.

	ret

.end

# s0 = start of D
# s1 = end of D
# a0 = b
# a1 = a
