def binary_search_lower_bound(left,right,value,L):
    
    while left <= right:
        mid = (left+right)//2
        if value == L[mid]:
            return mid
        elif value > L[mid]:
            left = mid+1
        else:
            right = mid -1
    return right

   





a = 0
L = [1,2,3,4,5,6,7,8,9]
left = 0 
right = len(L)-1
print(binary_search_lower_bound(left,right,a,L))
        