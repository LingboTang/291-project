#---------------------------------------------------------------
# Assignment:           5
# Due Date:             April 7th, 2014
# Name:                 Lingbo Tang
# Unix ID:              lingbo
# Lecture Section:      B1
# Instructor:           Jacqueline smith
# Lab Section:          LAB H01
# Teaching Assistant:   Michael Mills
#---------------------------------------------------------------

#-----------------------Register Using---------------------------------------
# This function is the subroutine that coalesce the linked free chunck
# It will identify all the free chunck and check the size and next of a chunck
# If pointer + offset = next then coalesce happens
# Otherwise just keep checking
# It will return how much free chunck has been coalesced and rearrage the memory.
#
# Register Usage in clock:
#	a0:address of the free chunck
#	v0:sum of the number of the free chunck that has been coalesced
#	t8:counter
#	t4:previous size
#	t5:previous next
#	s1:next size
#	s2:next next
#---------------------------------------------------------------

# ------------------------------ program header ------------------------------ #
# This function is the subroutine that coalesce the linked free chunck
# It will identify all the free chunck and check the size and next of a chunck
# If pointer + offset = next then coalesce happens
# Otherwise just keep checking
# It will return how much free chunck has been coalesced and rearrage the memory.
#-------------------------------------------------------------------------------

# -------------------------- subroutine description -------------------------- #
# coalesce: main part of the subroutine,which initialize the first header
# merge: coalesce the two linked chunck
# checkstatus: when pointer + offset != next we have to check
#		if next is null or not.
# resetHdr:	After checking status,if next != NULL
#		set pointer to next and set the new size and new counter
# end:		if next == NULL just end the subroutine and return the sum
#-------------------------------------------------------------------------------

#===============================================================================

#-------------------------------------------------------------------------------
# coalesce: main part of the subroutine,which initialize the first header
#--------------------------------------------------------------------------------

coalesce:
	li $t8 0		#set the counters
	lw $t4 0($a0)		#get the first free header size
        lw $t5 4($a0)		#get the first free header next
	beqz $t5 end	#if next is null stop the subrountine
        sll $t4 $t4 2		#get the actual offset
	add $a0 $a0 $t4		#shift pointer by actual offset
        beq $a0 $t5 merge	#if pointer + offset = next address just coalesce them

#-------------------------------------------------------------------------------
# merge: coalesce the two linked chunck
#--------------------------------------------------------------------------------

merge:
        lw $s1 0($a0)		#get the size of the next free chunck
        lw $s2 4($a0)		#get the next of the next free chunck
	sub $a0 $a0 $t4		#set the pointer back to the previous
        srl $t4 $t4 2	 	#set the previous size back to the original scale
        add $t4 $t4 $s1		#add both size up to get the sum
        add $t5 $s2 $0		#current next become previous
        sw $t4 0($a0)		#save the new size to the previous chunck to coalesce
        sw $t5 4($a0)		#save the new next to the previous chunck to coalesce
	add $t8 $t8 1		#adding up the counter
        lw $t4 0($a0)		#get the new size
        lw $t5 4($a0)		#get the new next
        sll $t4 $t4 2		#get the actual new offset
        add $a0 $a0 $t4		#shift pointer by new actual offset
        beq $a0 $t5 merge	#if pointer + offset = next address just keep running the loop
	bne $a0 $t5 checkstatus	#if pointer + offset != next address just check the status
       	jr $ra       		#return the result!
  
#-------------------------------------------------------------------------------
# checkstatus: when pointer + offset != next we have to check
#		if next is null or not.
#--------------------------------------------------------------------------------

checkstatus:  
	beqz $t5 end	#if next is null stop the subroutine
	bnez $t5 resetHdr	#if next is not null set the pointer to new address

#-------------------------------------------------------------------------------
# resetHdr:	After checking status,if next != NULL
#		set pointer to next and set the new size and new counter
#--------------------------------------------------------------------------------

resetHdr:
	add $a0 $t5 $0		#set the poitner to new address
	add $t4 $0 $0		#set the size as the new chunck size
	sub $t8 $t8 1		#get rid of the effect of natural join
	j merge			#back to the loop
#---------------------------------------------------------------------------------
# end:	if next == NULL just end the subroutine and return the sum
#---------------------------------------------------------------------------------

end:
	addi $v0 $t8 0		#return the number of chunck which has been coalesced
	jr $ra			#return the result!
