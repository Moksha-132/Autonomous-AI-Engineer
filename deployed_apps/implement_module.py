import random

def bubble_sort(arr):
    n = len(arr)
    # Create a copy to avoid modifying the original list in place if needed, 
    # but standard bubble sort usually sorts in place.
    sorted_list = arr.copy()
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if sorted_list[j] > sorted_list[j + 1]:
                sorted_list[j], sorted_list[j + 1] = sorted_list[j + 1], sorted_list[j]
                swapped = True
        if not swapped:
            break
    return sorted_list

def run_demonstration():
    # Test Case 1: Random integers as requested
    test_list_1 = [random.randint(1, 100) for _ in range(10)]
    print("--- Test Case 1: 10 Random Integers ---")
    print(f"Before: {test_list_1}")
    result_1 = bubble_sort(test_list_1)
    print(f"After:  {result_1}\n")

    # Test Case 2: Already sorted
    test_list_2 = [1, 2, 3, 4, 5]
    print("--- Test Case 2: Already Sorted ---")
    print(f"Before: {test_list_2}")
    result_2 = bubble_sort(test_list_2)
    print(f"After:  {result_2}\n")

    # Test Case 3: Reverse sorted
    test_list_3 = [50, 40, 30, 20, 10]
    print("--- Test Case 3: Reverse Sorted ---")
    print(f"Before: {test_list_3}")
    result_3 = bubble_sort(test_list_3)
    print(f"After:  {result_3}\n")

    # Test Case 4: List with duplicates
    test_list_4 = [7, 2, 7, 3, 2, 1, 1]
    print("--- Test Case 4: Duplicates ---")
    print(f"Before: {test_list_4}")
    result_4 = bubble_sort(test_list_4)
    print(f"After:  {result_4}\n")

if __name__ == "__main__":
    run_demonstration()
