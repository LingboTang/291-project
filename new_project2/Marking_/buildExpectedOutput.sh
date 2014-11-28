rm -f tests/*.out 
for f in tests/*.in
do
echo "Running $f"
./runTest.sh ../Solution/coalesce.s $f >> ${f%.in}.out
done
