.globl _start

.equ M, 7

.data
D: .word 5,7,0, 8,24,0, 11,44,0, 11,18,0, 36,2,0, 63,27,0, 19,24,0

.text
gcd:

# Insert gcd function below.
	beq a0, x0, gcd_done
	lw t0, a0
	rem a0, a1, a0
	lw a1, t0
	j gcd

	gcd_done:
		lw a0, a1

# Insert gcd function above.

	ret

coprime:

# Insert coprime function below.
	lw t0, ra # store the return address for _start
	
	lw a0, -8(s1)
	lw a1, -4(s1)
	jal gcd
	lw (s1), a0 # store the return value of gcd in the stack
	add s1, s1, -12 
	bne s1, x0, coprime 

	lw  ra, t0 # reload the return address for _start

# Insert coprime function above.

	ret

_start:

# Insert _start function below.

	la s0, D                    # Data address in s0
	lw s1, M
	slli s1, s1, 2
	li t0, 3
	mul s1, s1, t0 
	add s1, s1, s0 	# s1 = 3 * M * 4 + D
	jal coprime

# Insert _start function above.

	ret

.end

# s0 = start of D
# s1 = end of D
# a0 = b
# a1 = a
