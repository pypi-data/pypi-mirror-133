import random

def quickSort(nums: list) -> list:
    """
    quickSort is basic data structure algorithm in list.

    Quick Sort is a sorting algorithm, which is commonly used in computer science. 
    Quick Sort is a divide and conquer algorithm. 

    Args:
        nums (list): [5, 8, 12, -1, 4, 3]

    Returns:
        list: [-1, 3, 4, 5, 8, 12]
    """
    
    if len(nums) <= 1:
        return nums
    
    pivot = random.choice(nums)
    lt = [v for v in nums if v < pivot]
    eq = [v for v in nums if v == pivot]
    gt = [v for v in nums if v > pivot]
    
    return quickSort(lt) + eq + quickSort(gt)