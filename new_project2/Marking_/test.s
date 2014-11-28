##########################################################
# University of Alberta - Dept. of Computing Science
# Testing harness for lab HeapSpace
# 
# Author(s): Alejandro Ramírez Sanabria 
#		(ramirezs@ualberta.ca)
#			and
#	     Unknown (original file)
#
# Date: 03/26/2013
#
# Description: Testing harness for lab 5. It generates 
#  a description of the memory layout before and after
#  calling coalesce. These items can be later diff'ed 
#  to see if the output is the same as expected. 
#
########################################################### 


###########################################################
# Variables
#
# $s0 - the address of the free memory chunks
# $s1 - the starting address of the busy memory chunks
# $s2 - return value of coalesce
#
###########################################################

    .data
arena:
    .space 32768            # The space we're managing
fence:
    .word 0xffffffff
sizeb0:
    .word 0x0               # Same structure as chunk header, for zero'th busy chunk
addrb0:
    .word 0x0               # Note that both lists have been initialized as empty
sizef0:
    .word 0x0               # Same structure as chunk header, for zero'th free chunk
addrf0:
    .word 0x0

a0_backup:
    .word 0x0
s1_backup:
    .word 0x0

lblFree: 
	.asciiz "** Free memory - Before Coalesce **\n"
lblBusy:
	.asciiz "** Busy memory - Before Coalesce **\n"
lblFreeA: 
	.asciiz "** Free memory - After Coalesce **\n"
lblBusyA:
	.asciiz "** Busy memory - After Coalesce **\n"
lblSize:
	.asciiz "Element size: "
lblEmpty:
	.asciiz "No chunks in this memory location.\n"
lblPointer:
	.asciiz "Pointer to next element: "
newLine:
	.asciiz "\n"

Answer:
    .asciiz "\nNumber of chunks coalesced: "
    
    .text
    .globl main
    .globl coalesce
    
main:
    subu $sp, $sp, 4   # Adjust the stack to save $fp
    sw $fp, 0($sp)     # Save $fp
    move $fp, $sp      # $fp <-- $fp
    subu $sp, $sp, 4   # Adjust stadk to save $ra
    sw $ra, -4($fp)    # Save the return address ($ra)
    la $t7, sizeb0     # t7 will always have the address of the previous header

    # First, build the list of busy chunks
    
    # How many busy chunks are there?
    li $v0, 5
    syscall
    move $t0, $v0        # t0 will have the number of chunks to read

    # Skip to building free list if no busy chunks
    beq $t0, $0, skipB
    
    # Read the address offset of this chunk
busyHdr:
    li $v0, 5
    syscall
    move $t1, $v0

    # Calculate the absolute address
    la $t3, arena
    addu $t1, $t1, $t3

    # Write this into the header of the previous chunk
    sw $t1, 4($t7)

    # Read the size of this chunk
    li $v0, 5
    syscall
    move $t2, $v0

    # Write the header of this chunk
    sw $t2, 0($t1)   # size of chunk
    sw $0,  4($t1)   # set next NULL

    # Loop control
    add $t7, $t1, $0  # current becomes previous
    addi $t0, $t0, -1  # decrement count
    bnez $t0, busyHdr
    
skipB:
    la $t7, sizef0     # t7 will always have the address of the previous header

    # How many free chunks are there?
    li $v0, 5
    syscall
    move $t0, $v0        # t0 will have the number of chunks to read

    # Skip to end if none
    bne $t0, $0, freeHdr
    li $t0, 2
    sw $t0, sizef0
	la $a0, sizef0
	j skipF
   
    # Read the address offset of this chunk
freeHdr:
    li $v0, 5
    syscall
    move $t1, $v0

    # Calcuate the absolute address
    la $t3, arena
    addu $t1, $t1, $t3

    # Write this into the header of the previous chunk
    sw $t1, 4($t7)

    # Read the size of this chunk
    li $v0, 5
    syscall
    move $t2, $v0

    # Write the header of this chunk
    sw $t2, 0($t1)   # size of chunk
    sw $0,  4($t1)   # set next NULL

    # Loop control
    add $t7, $t1, $0  # current becomes previous
    addi $t0, $t0, -1  # decrement count
    bnez $t0, freeHdr

    # Call coalesce
	lw $a0, addrf0

skipF:

    move $s0, $a0	#Free chunks
    lw 	$s1, addrb0	#Busy chunks

    # Print the free memory layout before coalesce
    la $a0 lblFree
    li $v0 4
    syscall 

    move $a0 $s0 
    jal printMemory

    # Print the busy memory layout before coalesce
    la $a0 lblBusy
    li $v0 4
    syscall 

    move $a0 $s1

    la $s1 s1_backup
    sw $a0 0($s1)
    move $s1 $a0 
 
    jal printMemory

    # Coalesce
    move $a0 $s0
    
    la $s0 a0_backup
    sw $a0 0($s0)
    move $s0 $a0
	
    jal coalesce
    
    move $s2, $v0 #Save the return value to use it later

    # Print the free memory layout after coalesce
    la $a0 lblFreeA
    li $v0 4
    syscall 

    #move $a0 $s0 
    
    la $s0 a0_backup
    lw $a0 0($s0)
    move $s0 $a0

    jal printMemory

    # Print the busy memory layout after coalesce
    la $a0 lblBusyA
    li $v0 4
    syscall 

    #move $a0 $s1 

    la $a0 s1_backup
    lw $s1 0($a0)
    move $a0 $s1    

    jal printMemory

    # Print the return value
    li $v0, 4
    la $a0, Answer
    syscall
 
    move $a0, $s2
    li $v0, 1
    syscall

    # Usual stuff at the end of the main
    lw $ra, -4($fp)
    addu $sp, $sp, 4
    lw $fp, 0($sp)
    addu $sp, $sp, 4

    jr $ra


###########################################################
# printMemory
#
# Author: Alejandro Ramirez Sanabria
# Date:	  26/March/2013
# CMPUT 229 Lab 5
#
# Description: This function prints the memory block list
#  starting at $a0
# 
###########################################################

# Variables
#=====================
# $s1 - The current pointer of the block being processed

printMemory:

    	subu $sp, $sp, 4   # Adjust the stack to save $fp
    	sw $fp, 0($sp)     # Save $fp
    	move $fp, $sp      # $fp <-- $fp
    	subu $sp, $sp, 8   # Adjust stadk to save $ra
    	sw $ra, -4($fp)    # Save the return address ($ra)
	sw $s1, -8($fp)

	move $s1 $a0 	#Copy the pointer the a0 pointer to $t5 
	beqz $s1 invalidPointerPM
loopPM:
	lw $t0 0($s1)	#Load the number of words
	lw $t1 4($s1) 	#Load the pointer to the next block

	# Print the size of the current block
	
	la $a0 lblSize
	li $v0 4
	syscall

	move $a0 $t0
	li $v0 1
	syscall

	la $a0 newLine
	li $v0 4
	syscall

	# Print the absolute address of the next block
	
	la $a0 lblPointer
	li $v0 4
	syscall

	move $a0 $t1
	li $v0 1
	syscall

	la $a0 newLine
	li $v0 4
	syscall


	beqz $t1 donePM 	#If the next pointer is zero, end.  
	move $s1 $t1
	j loopPM

invalidPointerPM:		#If $a0 is a null pointer, sthap!
	la $a0 lblEmpty
	li $v0 4
	syscall	


donePM:
	# Unwind
	lw $s1, -8($fp)
	lw $ra, -4($fp)
    	addu $sp, $sp, 8
    	lw $fp, 0($sp)
    	addu $sp, $sp, 4

   	jr $ra


#######################################################################
# Student code goes here 
######################################################################

