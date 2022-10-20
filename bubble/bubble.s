.globl _start            

.section .data          
V: .word 3, 1, 4, 0, 3, 2, 4                

.section .text            
_start:                   
  li t1, 0                # t1 is the index i -- outer loop
  li t6, 0                # t6 is the length of the list
  la s0, V                # s0 stores the address of the array V
  mv s1, s0

COUNTER_LOOP:
  lw t2, (s1)             # load the next element of the array in the t2 register
  beq t2, x0, INIT        # check if the next element is zero
  add t6, t6, 1           # increment t6
  add s1, s1, 4           # s1 points to the next value in the array
  j COUNTER_LOOP          # continue to loop

INIT:
  add t6, t6, -1          # decrement t6 as the index t1 starts from zero

OUTER_LOOP:
  beq t1, t6, DONE        # if t1 == t6 program terminates i.e i == length
  add t2, t1, 0           # t2 is equal to t1 i.e i = j
  mv t0, s0               # t0 stores the address of the array
  j INNER_LOOP

OUTER_LOOP_HELPER:
  add t1, t1, 1           # increment t1 before continuing with the next iteration of the outer loop
  j OUTER_LOOP

INNER_LOOP:
  beq t2, t6, OUTER_LOOP_HELPER   # if j == lentgh jump to outer loop, helper is to adjust variables
  add t3, t0, 4                   # t3 is the address of the next element, i.e the next byte
  lw t4, (t0)                     # move the value in address t0 to t4
  lw t5, (t3)                     # move the value in address t3 to t5
  bge t4, t5, SWAP                # check if swap is needed
  blt t4, t5, INNER_LOOP_HELPER   # if no swap continue to loop

SWAP:
  sw t5, (t0)                     # swap the two values in the array
  sw t4, (t3)
  j INNER_LOOP_HELPER

INNER_LOOP_HELPER:
  add t0, t0, 4                   # before the next iteration increment the array pointer 
  add t2, t2, 1                   # increment the inner loop counter
  j INNER_LOOP

DONE: 
  add x0, x0, 0

âˆ
