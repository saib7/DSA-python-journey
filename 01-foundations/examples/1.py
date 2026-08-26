# Question: Given an array of integers and a number k, find the maximum sum of a contiguous subarray of size k.    
# Example: arr = [1, 12, 3, 4, -5], k = 3 => Output: 19 (sum of subarray [12, 3, 4])
def max_sum_subarray(arr, k):
    window_sum = sum(arr[:k])
    max_sum = window_sum
    for right in range(k, len(arr)):
        window_sum += arr[right] - arr[right - k]
        max_sum = max(max_sum, window_sum)
    return max_sum

if __name__ == "__main__":
    arr = [1, 12, 3, 4, -5]
    k = 3
    print(len(arr))  # Output: 5
    for i in range (0, len(arr)):
        print(arr[i])
    print(max_sum_subarray(arr, k))  #  Output: 19 (sum of subarray [12, 3, 4])

