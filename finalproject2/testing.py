def binary_search_lower_bound(key,L):
    left,right=0,len(L)-1
    if left>right:
        return None
    while left<=right:
        mid=(left+right)//2
        if key==L[mid]:
            return mid
        elif key<L[mid]:
            right=mid-1
            if right<0:
                return 0
            lower_b=mid
        elif key>L[mid]:
            left=mid+1
            if left>len(L)-1:
                return len(L)-1
            lower_b=mid
    return lower_b





key = 1.5
L = [1,2,3,4,5,6,7,8,9]
print(binary_search_lower_bound(key,L))