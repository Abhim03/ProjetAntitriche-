# exemple 2
def verifier_primes(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):  # noqa: SIM110
        if n % i == 0:
            return False
    return True


print(verifier_primes(29))


# exemple 2
def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):  # noqa: SIM110
        if num % i == 0:
            return False
    return True


print(is_prime(29))


# exemple 3
def contient_pair(nums):
    for num in nums:  # noqa: SIM110
        if num % 2 == 0:
            return True
    return False


liste_nums = [1, 3, 5, 2, 9]
print(contient_pair(liste_nums))


# exemple 3
def has_even(numbers):
    for number in numbers:  # noqa: SIM110
        if number % 2 == 0:
            return True
    return False


test_numbers = [7, 11, 15, 22, 17]
print(has_even(test_numbers))


# exemple 4
def length_of_longest_substring(s):
    char_index_map = {}
    start = max_length = 0

    for i, char in enumerate(s):
        if char in char_index_map and char_index_map[char] >= start:
            start = char_index_map[char] + 1
        char_index_map[char] = i
        max_length = max(max_length, i - start + 1)

    return max_length


# exemple 4


def longest_substring_length(input_str):
    index_by_char = {}
    begin = longest = 0
    for index, character in enumerate(input_str):
        if character in index_by_char and index_by_char[character] >= begin:
            begin = index_by_char[character] + 1
        index_by_char[character] = index
        longest = max(longest, index - begin + 1)
    return longest
