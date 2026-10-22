EXAMPLES = [
    {
        'id': 'backtracking', 'title': 'The disappearing subsets', 'tag': 'BACKTRACKING',
        'description': 'Eight answers. One shared list. Follow the references to see why every subset disappears.',
        'source': '''def subsets(nums):
    results = []
    path = []

    def visit(start):
        results.append(path)
        for i in range(start, len(nums)):
            path.append(nums[i])
            visit(i + 1)
            path.pop()

    visit(0)
    return results

answer = subsets([1, 2, 3])
print(answer)''',
        'fix': {'before': 'results.append(path)', 'after': 'results.append(path.copy())', 'explanation': 'Store a snapshot of path. Appending path itself stores another reference to the same list; later pop() calls change what every reference sees.'},
        'expected': '[[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]\n'
    },
    {
        'id': 'bounds', 'title': 'One step too far', 'tag': 'ARRAYS & LOOPS',
        'description': 'The loop reaches an index that does not exist. Watch the last valid access become a failure.',
        'source': '''numbers = [4, 8, 15, 16]
total = 0

for i in range(len(numbers) + 1):
    total += numbers[i]

print(total)''',
        'fix': {'before': 'range(len(numbers) + 1)', 'after': 'range(len(numbers))', 'explanation': 'range stops before its upper bound. A four-element list has indices 0 through 3; adding one makes the loop attempt index 4.'},
        'expected': '43\n'
    },
    {
        'id': 'recursion', 'title': 'Inside the call stack', 'tag': 'RECURSION',
        'description': 'Each recursive call gets its own n. Follow the descent, then watch return values travel back up.',
        'source': '''def factorial(n):
    if n <= 1:
        return 1
    smaller = factorial(n - 1)
    result = n * smaller
    return result

answer = factorial(5)
print(answer)''',
        'expected': '120\n'
    }
]
