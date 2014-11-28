# runTest.sh
# Author: 	Alejandro Ramírez-Sanabria
# Date:   	26-March-2013
#
# USAGE: 	sh runTest.sh LABFILE TESTFILE
#
# Same as previous scripts: it combines the testing harness
# and the student's subroutine into a single file and 
# executes it. It removes the first few lines with the spim
# information/version to prevent problems. 

rm -f testBuild.s
cat test.s > testBuild.s
cat $1 >> testBuild.s
spim -file testBuild.s < $2 | sed '1,5d'
