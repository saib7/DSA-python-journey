#Question: Given an array of integers and a number k, find the maximum sum of a contiguous subarray of size k.



def max_sum_subarray(arr, k):
    window_sum = sum(arr[:k])
    max_sum = window_sum
    for right in range(k, len(arr)):
        window_sum += arr[right] - arr[right - k]
        max_sum = max(max_sum, window_sum)
    return max_sum


if __name__ == "__main__":
    arr = [1, 2, 3, 4, 5]
    k = 3
    print(max_sum_subarray(arr, k))  # Output: 12 (3 + 4 + 5)