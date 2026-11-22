"""TRELLIS Coding Problems Fixtures (24 Problems across 5 Languages).
Languages: Python (6), SQL (6), Java (4), JavaScript (4), C++ (4).
Includes starter codes, entry points, argument schemas, constraints,
>=2 examples, >=6 test cases (>=3 hidden), reference solutions, and wrong stubs.
"""

from app.schemas.category import AssessmentCategory

CODING_PROBLEMS = [   {   'argument_schema': [{'name': 'nums', 'type': 'list[int]'}, {'name': 'target', 'type': 'int'}],
        'category': 'Coding',
        'complexity_notes': 'Time: O(N) single pass hash table, Space: O(N) hash table storage.',
        'constraints': '2 <= nums.length <= 10^4\n'
                       '-10^9 <= nums[i] <= 10^9\n'
                       '-10^9 <= target <= 10^9\n'
                       'Exactly one valid answer exists.',
        'description': 'Given an array of integers nums and an integer target, return indices of the two numbers such '
                       'that they add up to target. You may assume that each input would have exactly one solution, '
                       'and you may not use the same element twice. Return the answer sorted in ascending order.',
        'difficulty': 'EASY',
        'entry_point': 'two_sum',
        'examples_json': [   {   'explanation': 'Because nums[0] + nums[1] == 9, we return [0, 1].',
                                 'input': 'nums = [2, 7, 11, 15], target = 9',
                                 'output': '[0, 1]'},
                             {   'explanation': 'Because nums[1] + nums[2] == 6, we return [1, 2].',
                                 'input': 'nums = [3, 2, 4], target = 6',
                                 'output': '[1, 2]'}],
        'field': 'Python',
        'language': 'python',
        'marks': 10.0,
        'problem_type': 'CODING',
        'reference_solution': 'def two_sum(nums: list[int], target: int) -> list[int]:\n'
                              '    seen = {}\n'
                              '    for i, num in enumerate(nums):\n'
                              '        diff = target - num\n'
                              '        if diff in seen:\n'
                              '            return sorted([seen[diff], i])\n'
                              '        seen[num] = i\n'
                              '    return []\n',
        'starter_code_json': {   'python': 'def two_sum(nums: list[int], target: int) -> list[int]:\n'
                                           '    # Return sorted indices [i, j] such that nums[i] + nums[j] == target\n'
                                           '    pass\n'},
        'test_cases': [   {   'expected_output': '[0, 1]',
                              'input_data': '[2, 7, 11, 15]\n9',
                              'is_hidden': False,
                              'weight': 1.0},
                          {   'expected_output': '[1, 2]',
                              'input_data': '[3, 2, 4]\n6',
                              'is_hidden': False,
                              'weight': 1.0},
                          {'expected_output': '[0, 1]', 'input_data': '[3, 3]\n6', 'is_hidden': False, 'weight': 1.0},
                          {   'expected_output': '[2, 4]',
                              'input_data': '[-1, -2, -3, -4, -5]\n-8',
                              'is_hidden': True,
                              'weight': 1.5},
                          {   'expected_output': '[0, 3]',
                              'input_data': '[0, 4, 3, 0]\n0',
                              'is_hidden': True,
                              'weight': 1.5},
                          {   'expected_output': '[3, 4]',
                              'input_data': '[100, 200, 300, 400, 500]\n900',
                              'is_hidden': True,
                              'weight': 2.0}],
        'title': 'Two Sum Target Indices',
        'wrong_stub': 'def two_sum(nums: list[int], target: int) -> list[int]:\n    return [0, 1]\n'},
    {   'argument_schema': [{'name': 's', 'type': 'str'}],
        'category': 'Coding',
        'complexity_notes': 'Time: O(N) single scan with stack, Space: O(N) stack auxiliary memory.',
        'constraints': "1 <= s.length <= 10^4\ns consists of parentheses only '()[]{}'.",
        'description': "Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if "
                       'the input string is valid.\n'
                       'An input string is valid if open brackets are closed by the same type of brackets and in the '
                       'correct order.',
        'difficulty': 'EASY',
        'entry_point': 'is_valid',
        'examples_json': [   {   'explanation': 'The parentheses open and close correctly.',
                                 'input': 's = "()"',
                                 'output': 'true'},
                             {   'explanation': 'All bracket pairs match and close in order.',
                                 'input': 's = "()[]{}"',
                                 'output': 'true'},
                             {'explanation': 'Mismatched bracket types.', 'input': 's = "(]"', 'output': 'false'}],
        'field': 'Python',
        'language': 'python',
        'marks': 10.0,
        'problem_type': 'CODING',
        'reference_solution': 'def is_valid(s: str) -> bool:\n'
                              '    stack = []\n'
                              "    mapping = {')': '(', '}': '{', ']': '['}\n"
                              '    for char in s:\n'
                              '        if char in mapping:\n'
                              "            top = stack.pop() if stack else '#'\n"
                              '            if mapping[char] != top:\n'
                              '                return False\n'
                              '        else:\n'
                              '            stack.append(char)\n'
                              '    return len(stack) == 0\n',
        'starter_code_json': {   'python': 'def is_valid(s: str) -> bool:\n'
                                           '    # Return True if parentheses match properly, False otherwise\n'
                                           '    pass\n'},
        'test_cases': [   {'expected_output': 'true', 'input_data': '"()"', 'is_hidden': False, 'weight': 1.0},
                          {'expected_output': 'true', 'input_data': '"()[]{}"', 'is_hidden': False, 'weight': 1.0},
                          {'expected_output': 'false', 'input_data': '"(]"', 'is_hidden': False, 'weight': 1.0},
                          {'expected_output': 'false', 'input_data': '"([)]"', 'is_hidden': True, 'weight': 1.5},
                          {'expected_output': 'true', 'input_data': '"{[]}"', 'is_hidden': True, 'weight': 1.5},
                          {'expected_output': 'false', 'input_data': '"((((((("', 'is_hidden': True, 'weight': 1.5}],
        'title': 'Valid Parentheses',
        'wrong_stub': 'def is_valid(s: str) -> bool:\n    return True\n'},
    {   'argument_schema': [{'name': 's', 'type': 'str'}],
        'category': 'Coding',
        'complexity_notes': 'Time: O(N) sliding window with character index hash map, Space: O(min(N, M)) where M is '
                            'alphabet size.',
        'constraints': '0 <= s.length <= 5 * 10^4\ns consists of English letters, digits, symbols and spaces.',
        'description': 'Given a string s, find the length of the longest substring without repeating characters.',
        'difficulty': 'MEDIUM',
        'entry_point': 'length_of_longest_substring',
        'examples_json': [   {   'explanation': 'The answer is "abc", with length 3.',
                                 'input': 's = "abcabcbb"',
                                 'output': '3'},
                             {   'explanation': 'The answer is "b", with length 1.',
                                 'input': 's = "bbbbb"',
                                 'output': '1'}],
        'field': 'Python',
        'language': 'python',
        'marks': 15.0,
        'problem_type': 'CODING',
        'reference_solution': 'def length_of_longest_substring(s: str) -> int:\n'
                              '    used = {}\n'
                              '    max_len = start = 0\n'
                              '    for i, char in enumerate(s):\n'
                              '        if char in used and start <= used[char]:\n'
                              '            start = used[char] + 1\n'
                              '        else:\n'
                              '            max_len = max(max_len, i - start + 1)\n'
                              '        used[char] = i\n'
                              '    return max_len\n',
        'starter_code_json': {   'python': 'def length_of_longest_substring(s: str) -> int:\n'
                                           '    # Return the maximum length of substring without repeating characters\n'
                                           '    pass\n'},
        'test_cases': [   {'expected_output': '3', 'input_data': '"abcabcbb"', 'is_hidden': False, 'weight': 1.0},
                          {'expected_output': '1', 'input_data': '"bbbbb"', 'is_hidden': False, 'weight': 1.0},
                          {'expected_output': '3', 'input_data': '"pwwkew"', 'is_hidden': False, 'weight': 1.0},
                          {'expected_output': '0', 'input_data': '""', 'is_hidden': True, 'weight': 1.5},
                          {'expected_output': '3', 'input_data': '"dvdf"', 'is_hidden': True, 'weight': 1.5},
                          {'expected_output': '5', 'input_data': '"anviaj"', 'is_hidden': True, 'weight': 2.0}],
        'title': 'Longest Substring Without Repeating Characters',
        'wrong_stub': 'def length_of_longest_substring(s: str) -> int:\n    return len(set(s))\n'},
    {   'argument_schema': [{'name': 'intervals', 'type': 'list[list[int]]'}],
        'category': 'Coding',
        'complexity_notes': 'Time: O(N log N) sorting intervals by start time, Space: O(N) output list.',
        'constraints': '1 <= intervals.length <= 10^4\nintervals[i].length == 2\n0 <= start_i <= end_i <= 10^4',
        'description': 'Given an array of intervals where intervals[i] = [start_i, end_i], merge all overlapping '
                       'intervals, and return an array of non-overlapping intervals that cover all intervals in the '
                       'input.',
        'difficulty': 'MEDIUM',
        'entry_point': 'merge_intervals',
        'examples_json': [   {   'explanation': 'Since intervals [1,3] and [2,6] overlap, merge them into [1,6].',
                                 'input': 'intervals = [[1,3],[2,6],[8,10],[15,18]]',
                                 'output': '[[1,6],[8,10],[15,18]]'},
                             {   'explanation': 'Intervals [1,4] and [4,5] overlap at boundary 4.',
                                 'input': 'intervals = [[1,4],[4,5]]',
                                 'output': '[[1,5]]'}],
        'field': 'Python',
        'language': 'python',
        'marks': 15.0,
        'problem_type': 'CODING',
        'reference_solution': 'def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:\n'
                              '    if not intervals:\n'
                              '        return []\n'
                              '    intervals.sort(key=lambda x: x[0])\n'
                              '    merged = [intervals[0]]\n'
                              '    for current in intervals[1:]:\n'
                              '        prev = merged[-1]\n'
                              '        if current[0] <= prev[1]:\n'
                              '            prev[1] = max(prev[1], current[1])\n'
                              '        else:\n'
                              '            merged.append(current)\n'
                              '    return merged\n',
        'starter_code_json': {   'python': 'def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:\n'
                                           '    # Merge all overlapping intervals and return result sorted\n'
                                           '    pass\n'},
        'test_cases': [   {   'expected_output': '[[1, 6], [8, 10], [15, 18]]',
                              'input_data': '[[1, 3], [2, 6], [8, 10], [15, 18]]',
                              'is_hidden': False,
                              'weight': 1.0},
                          {   'expected_output': '[[1, 5]]',
                              'input_data': '[[1, 4], [4, 5]]',
                              'is_hidden': False,
                              'weight': 1.0},
                          {   'expected_output': '[[0, 4]]',
                              'input_data': '[[1, 4], [0, 4]]',
                              'is_hidden': False,
                              'weight': 1.0},
                          {   'expected_output': '[[1, 4]]',
                              'input_data': '[[1, 4], [2, 3]]',
                              'is_hidden': True,
                              'weight': 1.5},
                          {   'expected_output': '[[1, 9]]',
                              'input_data': '[[6, 8], [1, 9], [2, 4], [4, 7]]',
                              'is_hidden': True,
                              'weight': 1.5},
                          {   'expected_output': '[[1, 10]]',
                              'input_data': '[[2, 3], [4, 5], [6, 7], [8, 9], [1, 10]]',
                              'is_hidden': True,
                              'weight': 2.0}],
        'title': 'Merge Overlapping Intervals',
        'wrong_stub': 'def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:\n    return intervals\n'},
    {   'argument_schema': [{'name': 'nums', 'type': 'list[int]'}],
        'category': 'Coding',
        'complexity_notes': 'Time: O(N) two pass prefix and suffix product, Space: O(1) auxiliary memory (excluding '
                            'output).',
        'constraints': '2 <= nums.length <= 10^5\n-30 <= nums[i] <= 30',
        'description': 'Given an integer array nums, return an array answer such that answer[i] is equal to the '
                       'product of all elements of nums except nums[i]. The product of any prefix or suffix of nums '
                       'fits in a 32-bit integer. Must run in O(N) time without using the division operation.',
        'difficulty': 'MEDIUM',
        'entry_point': 'product_except_self',
        'examples_json': [   {   'explanation': 'answer[0] = 2*3*4 = 24, answer[1] = 1*3*4 = 12, etc.',
                                 'input': 'nums = [1, 2, 3, 4]',
                                 'output': '[24, 12, 8, 6]'},
                             {   'explanation': 'Only the position with 0 has a non-zero product.',
                                 'input': 'nums = [-1, 1, 0, -3, 3]',
                                 'output': '[0, 0, 9, 0, 0]'}],
        'field': 'Python',
        'language': 'python',
        'marks': 15.0,
        'problem_type': 'CODING',
        'reference_solution': 'def product_except_self(nums: list[int]) -> list[int]:\n'
                              '    n = len(nums)\n'
                              '    res = [1] * n\n'
                              '    prefix = 1\n'
                              '    for i in range(n):\n'
                              '        res[i] = prefix\n'
                              '        prefix *= nums[i]\n'
                              '    suffix = 1\n'
                              '    for i in range(n - 1, -1, -1):\n'
                              '        res[i] *= suffix\n'
                              '        suffix *= nums[i]\n'
                              '    return res\n',
        'starter_code_json': {   'python': 'def product_except_self(nums: list[int]) -> list[int]:\n'
                                           '    # Compute product of all elements except self without division\n'
                                           '    pass\n'},
        'test_cases': [   {   'expected_output': '[24, 12, 8, 6]',
                              'input_data': '[1, 2, 3, 4]',
                              'is_hidden': False,
                              'weight': 1.0},
                          {   'expected_output': '[0, 0, 9, 0, 0]',
                              'input_data': '[-1, 1, 0, -3, 3]',
                              'is_hidden': False,
                              'weight': 1.0},
                          {'expected_output': '[3, 2]', 'input_data': '[2, 3]', 'is_hidden': False, 'weight': 1.0},
                          {'expected_output': '[0, 0]', 'input_data': '[0, 0]', 'is_hidden': True, 'weight': 1.5},
                          {   'expected_output': '[1, -1, 1, -1]',
                              'input_data': '[1, -1, 1, -1]',
                              'is_hidden': True,
                              'weight': 1.5},
                          {   'expected_output': '[24, 60, 30, 120, 40]',
                              'input_data': '[5, 2, 4, 1, 3]',
                              'is_hidden': True,
                              'weight': 2.0}],
        'title': 'Product of Array Except Self',
        'wrong_stub': 'def product_except_self(nums: list[int]) -> list[int]:\n    return [0] * len(nums)\n'},
    {   'argument_schema': [{'name': 'height', 'type': 'list[int]'}],
        'category': 'Coding',
        'complexity_notes': 'Time: O(N) two pointer approach, Space: O(1) auxiliary space.',
        'constraints': 'n == height.length\n1 <= n <= 2 * 10^4\n0 <= height[i] <= 10^5',
        'description': 'Given n non-negative integers representing an elevation map where the width of each bar is 1, '
                       'compute how much water it can trap after raining.',
        'difficulty': 'HARD',
        'entry_point': 'trap',
        'examples_json': [   {   'explanation': 'The elevation map traps 6 units of rainwater.',
                                 'input': 'height = [0,1,0,2,1,0,1,3,2,1,2,1]',
                                 'output': '6'},
                             {   'explanation': 'The elevation map traps 9 units of rainwater.',
                                 'input': 'height = [4,2,0,3,2,5]',
                                 'output': '9'}],
        'field': 'Python',
        'language': 'python',
        'marks': 20.0,
        'problem_type': 'CODING',
        'reference_solution': 'def trap(height: list[int]) -> int:\n'
                              '    if not height: return 0\n'
                              '    l, r = 0, len(height) - 1\n'
                              '    left_max, right_max = height[l], height[r]\n'
                              '    water = 0\n'
                              '    while l < r:\n'
                              '        if left_max < right_max:\n'
                              '            l += 1\n'
                              '            left_max = max(left_max, height[l])\n'
                              '            water += left_max - height[l]\n'
                              '        else:\n'
                              '            r -= 1\n'
                              '            right_max = max(right_max, height[r])\n'
                              '            water += right_max - height[r]\n'
                              '    return water\n',
        'starter_code_json': {   'python': 'def trap(height: list[int]) -> int:\n'
                                           '    # Calculate total water trapped\n'
                                           '    pass\n'},
        'test_cases': [   {   'expected_output': '6',
                              'input_data': '[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]',
                              'is_hidden': False,
                              'weight': 1.0},
                          {   'expected_output': '9',
                              'input_data': '[4, 2, 0, 3, 2, 5]',
                              'is_hidden': False,
                              'weight': 1.0},
                          {'expected_output': '7', 'input_data': '[3, 0, 2, 0, 4]', 'is_hidden': False, 'weight': 1.0},
                          {'expected_output': '0', 'input_data': '[1, 2, 3, 4, 5]', 'is_hidden': True, 'weight': 1.5},
                          {'expected_output': '0', 'input_data': '[5, 4, 3, 2, 1]', 'is_hidden': True, 'weight': 1.5},
                          {'expected_output': '2', 'input_data': '[2, 0, 2]', 'is_hidden': True, 'weight': 2.0}],
        'title': 'Trapping Rain Water',
        'wrong_stub': 'def trap(height: list[int]) -> int:\n    return 0\n'},
    {   'category': 'Coding',
        'complexity_notes': 'Time: O(N log N) grouping and window ranking, Space: O(N) temp sort buffer.',
        'constraints': 'Schema: Department (id INT, name TEXT), Employee (id INT, name TEXT, salary INT, department_id '
                       'INT)',
        'description': 'Write a SQL query to find employees who have the highest salary in each department. Output '
                       'department name, employee name, and salary.',
        'difficulty': 'MEDIUM',
        'examples_json': [   {   'explanation': 'Highest salary per department.',
                                 'input': "Department: (1, 'IT'), (2, 'Sales'); Employee: (1, 'Joe', 85000, 1), (2, "
                                          "'Henry', 80000, 2)",
                                 'output': 'IT|Joe|85000\nSales|Henry|80000'}],
        'field': 'SQL',
        'language': 'sql',
        'marks': 15.0,
        'problem_type': 'SQL',
        'reference_solution': 'SELECT d.name, e.name, e.salary\n'
                              'FROM Employee e\n'
                              'JOIN Department d ON e.department_id = d.id\n'
                              'WHERE e.salary = (SELECT MAX(e2.salary) FROM Employee e2 WHERE e2.department_id = '
                              'e.department_id);\n',
        'schema_ddl': 'CREATE TABLE Department (id INT, name TEXT); CREATE TABLE Employee (id INT, name TEXT, salary '
                      'INT, department_id INT);',
        'starter_code_json': {   'sql': '-- Write your SQL query here\n'
                                        'SELECT d.name, e.name, e.salary\n'
                                        'FROM Employee e\n'
                                        'JOIN Department d ON e.department_id = d.id;\n'},
        'test_cases': [   {   'expected_output': 'IT|Jim|90000\nIT|Max|90000\nSales|Henry|80000',
                              'input_data': 'CREATE TABLE Department (id INT, name TEXT);\n'
                                            'CREATE TABLE Employee (id INT, name TEXT, salary INT, department_id '
                                            'INT);\n'
                                            "INSERT INTO Department VALUES (1, 'IT'), (2, 'Sales');\n"
                                            "INSERT INTO Employee VALUES (1, 'Joe', 70000, 1), (2, 'Jim', 90000, 1), "
                                            "(3, 'Henry', 80000, 2), (4, 'Sam', 60000, 2), (5, 'Max', 90000, 1);",
                              'is_hidden': False,
                              'weight': 1.0},
                          {   'expected_output': 'Engineering|Alice|120000',
                              'input_data': 'CREATE TABLE Department (id INT, name TEXT);\n'
                                            'CREATE TABLE Employee (id INT, name TEXT, salary INT, department_id '
                                            'INT);\n'
                                            "INSERT INTO Department VALUES (1, 'Engineering');\n"
                                            "INSERT INTO Employee VALUES (1, 'Alice', 120000, 1), (2, 'Bob', 110000, "
                                            '1);',
                              'is_hidden': False,
                              'weight': 1.0},
                          {   'expected_output': 'HR|Clara|50000\nFinance|David|75000',
                              'input_data': 'CREATE TABLE Department (id INT, name TEXT);\n'
                                            'CREATE TABLE Employee (id INT, name TEXT, salary INT, department_id '
                                            'INT);\n'
                                            "INSERT INTO Department VALUES (1, 'HR'), (2, 'Finance');\n"
                                            "INSERT INTO Employee VALUES (1, 'Clara', 50000, 1), (2, 'David', 75000, "
                                            '2);',
                              'is_hidden': False,
                              'weight': 1.0},
                          {   'expected_output': 'Ops|A|60000\nOps|B|60000\nOps|C|60000',
                              'input_data': 'CREATE TABLE Department (id INT, name TEXT);\n'
                                            'CREATE TABLE Employee (id INT, name TEXT, salary INT, department_id '
                                            'INT);\n'
                                            "INSERT INTO Department VALUES (1, 'Ops');\n"
                                            "INSERT INTO Employee VALUES (1, 'A', 60000, 1), (2, 'B', 60000, 1), (3, "
                                            "'C', 60000, 1);",
                              'is_hidden': True,
                              'weight': 1.5},
                          {   'expected_output': 'Marketing|Solo|95000',
                              'input_data': 'CREATE TABLE Department (id INT, name TEXT);\n'
                                            'CREATE TABLE Employee (id INT, name TEXT, salary INT, department_id '
                                            'INT);\n'
                                            "INSERT INTO Department VALUES (1, 'Marketing');\n"
                                            "INSERT INTO Employee VALUES (1, 'Solo', 95000, 1);",
                              'is_hidden': True,
                              'weight': 1.5},
                          {   'expected_output': 'D1|E1|100\nD2|E2|200\nD3|E3|300',
                              'input_data': 'CREATE TABLE Department (id INT, name TEXT);\n'
                                            'CREATE TABLE Employee (id INT, name TEXT, salary INT, department_id '
                                            'INT);\n'
                                            "INSERT INTO Department VALUES (1, 'D1'), (2, 'D2'), (3, 'D3');\n"
                                            "INSERT INTO Employee VALUES (1, 'E1', 100, 1), (2, 'E2', 200, 2), (3, "
                                            "'E3', 300, 3);",
                              'is_hidden': True,
                              'weight': 2.0}],
        'title': 'Top Salaried Employee per Department',
        'wrong_stub': "SELECT 'IT', 'None', 0;\n"},
    {   'category': 'Coding',
        'complexity_notes': 'Time: O(N) grouping with hash aggregation, Space: O(N) distinct email table.',
        'constraints': 'Schema: Person (id INT, email TEXT)',
        'description': 'Write a SQL query to report all duplicate emails in a table named Person. Output only the '
                       'email column.',
        'difficulty': 'EASY',
        'examples_json': [   {   'explanation': "'a@b.com' appears more than once.",
                                 'input': "Person: (1, 'a@b.com'), (2, 'c@d.com'), (3, 'a@b.com')",
                                 'output': 'a@b.com'}],
        'field': 'SQL',
        'language': 'sql',
        'marks': 10.0,
        'problem_type': 'SQL',
        'reference_solution': 'SELECT email FROM Person GROUP BY email HAVING COUNT(email) > 1;\n',
        'schema_ddl': 'CREATE TABLE Person (id INT, email TEXT);',
        'starter_code_json': {'sql': '-- Write your SQL query here\nSELECT email\nFROM Person\nGROUP BY email;\n'},
        'test_cases': [   {   'expected_output': 'a@b.com',
                              'input_data': 'CREATE TABLE Person (id INT, email TEXT);\n'
                                            "INSERT INTO Person VALUES (1, 'a@b.com'), (2, 'c@d.com'), (3, 'a@b.com');",
                              'is_hidden': False,
                              'weight': 1.0},
                          {   'expected_output': '',
                              'input_data': 'CREATE TABLE Person (id INT, email TEXT);\n'
                                            "INSERT INTO Person VALUES (1, 'unique1@test.com'), (2, "
                                            "'unique2@test.com');",
                              'is_hidden': False,
                              'weight': 1.0},
                          {   'expected_output': 'x@y.com',
                              'input_data': 'CREATE TABLE Person (id INT, email TEXT);\n'
                                            "INSERT INTO Person VALUES (1, 'x@y.com'), (2, 'x@y.com'), (3, 'x@y.com');",
                              'is_hidden': False,
                              'weight': 1.0},
                          {   'expected_output': 'a@a.com\nb@b.com',
                              'input_data': 'CREATE TABLE Person (id INT, email TEXT);\n'
                                            "INSERT INTO Person VALUES (1, 'a@a.com'), (2, 'b@b.com'), (3, 'a@a.com'), "
                                            "(4, 'b@b.com');",
                              'is_hidden': True,
                              'weight': 1.5},
                          {   'expected_output': '',
                              'input_data': 'CREATE TABLE Person (id INT, email TEXT);',
                              'is_hidden': True,
                              'weight': 1.5},
                          {   'expected_output': 'user@trellis.io',
                              'input_data': 'CREATE TABLE Person (id INT, email TEXT);\n'
                                            "INSERT INTO Person VALUES (1, 'user@trellis.io'), (2, "
                                            "'user2@trellis.io'), (3, 'user@trellis.io'), (4, 'user3@trellis.io');",
                              'is_hidden': True,
                              'weight': 2.0}],
        'title': 'Duplicate Email Detection',
        'wrong_stub': 'SELECT email FROM Person;\n'},
    {   'category': 'Coding',
        'complexity_notes': 'Time: O(N) left join anti-pattern, Space: O(1) streaming join buffer.',
        'constraints': 'Schema: Users (id INT, email TEXT), Profiles (user_id INT)',
        'description': 'Write a SQL query to identify any User record in Users that has no corresponding Profile in '
                       'Profiles without using NOT IN. Output id and email.',
        'difficulty': 'EASY',
        'examples_json': [   {   'explanation': 'User 2 has no profile record.',
                                 'input': "Users: (1, 'u1@t.com'), (2, 'u2@t.com'); Profiles: (1)",
                                 'output': '2|u2@t.com'}],
        'field': 'SQL',
        'language': 'sql',
        'marks': 10.0,
        'problem_type': 'SQL',
        'reference_solution': 'SELECT u.id, u.email FROM Users u LEFT JOIN Profiles p ON u.id = p.user_id WHERE '
                              'p.user_id IS NULL;\n',
        'schema_ddl': 'CREATE TABLE Users (id INT, email TEXT); CREATE TABLE Profiles (user_id INT);',
        'starter_code_json': {'sql': '-- Write your SQL query here\nSELECT u.id, u.email\nFROM Users u;\n'},
        'test_cases': [   {   'expected_output': '2|c@d.com',
                              'input_data': 'CREATE TABLE Users (id INT, email TEXT);\n'
                                            'CREATE TABLE Profiles (user_id INT);\n'
                                            "INSERT INTO Users VALUES (1, 'a@b.com'), (2, 'c@d.com');\n"
                                            'INSERT INTO Profiles VALUES (1);',
                              'is_hidden': False,
                              'weight': 1.0},
                          {   'expected_output': '',
                              'input_data': 'CREATE TABLE Users (id INT, email TEXT);\n'
                                            'CREATE TABLE Profiles (user_id INT);\n'
                                            "INSERT INTO Users VALUES (1, 'x@y.com');\n"
                                            'INSERT INTO Profiles VALUES (1);',
                              'is_hidden': False,
                              'weight': 1.0},
                          {   'expected_output': '1|m@n.com\n2|o@p.com',
                              'input_data': 'CREATE TABLE Users (id INT, email TEXT);\n'
                                            'CREATE TABLE Profiles (user_id INT);\n'
                                            "INSERT INTO Users VALUES (1, 'm@n.com'), (2, 'o@p.com');",
                              'is_hidden': False,
                              'weight': 1.0},
                          {   'expected_output': '20|u20@t.com',
                              'input_data': 'CREATE TABLE Users (id INT, email TEXT);\n'
                                            'CREATE TABLE Profiles (user_id INT);\n'
                                            "INSERT INTO Users VALUES (10, 'u10@t.com'), (20, 'u20@t.com'), (30, "
                                            "'u30@t.com');\n"
                                            'INSERT INTO Profiles VALUES (10), (30);',
                              'is_hidden': True,
                              'weight': 1.5},
                          {   'expected_output': '',
                              'input_data': 'CREATE TABLE Users (id INT, email TEXT);\n'
                                            'CREATE TABLE Profiles (user_id INT);',
                              'is_hidden': True,
                              'weight': 1.5},
                          {   'expected_output': '1|first@t.com\n3|third@t.com',
                              'input_data': 'CREATE TABLE Users (id INT, email TEXT);\n'
                                            'CREATE TABLE Profiles (user_id INT);\n'
                                            "INSERT INTO Users VALUES (1, 'first@t.com'), (2, 'second@t.com'), (3, "
                                            "'third@t.com');\n"
                                            'INSERT INTO Profiles VALUES (2);',
                              'is_hidden': True,
                              'weight': 2.0}],
        'title': 'Orphan Records Audit Query',
        'wrong_stub': 'SELECT id, email FROM Users;\n'},
    {   'category': 'Coding',
        'complexity_notes': 'Time: O(N) correlated subquery or window average, Space: O(K) department averages table.',
        'constraints': 'Schema: Employees (emp_id INT, dept_id INT, salary NUMERIC)',
        'description': 'Write a SQL query to list all employees who earn strictly more than the average salary of '
                       'their respective department. Output emp_id and salary.',
        'difficulty': 'MEDIUM',
        'examples_json': [   {   'explanation': 'Employee 1 earns strictly more than department average 7000.',
                                 'input': 'Employees: (1, 10, 8000), (2, 10, 6000) -> Dept 10 avg is 7000.',
                                 'output': '1|8000'}],
        'field': 'SQL',
        'language': 'sql',
        'marks': 15.0,
        'problem_type': 'SQL',
        'reference_solution': 'SELECT emp_id, salary FROM Employees e WHERE salary > (SELECT AVG(salary) FROM '
                              'Employees e2 WHERE e2.dept_id = e.dept_id);\n',
        'schema_ddl': 'CREATE TABLE Employees (emp_id INT, dept_id INT, salary NUMERIC);',
        'starter_code_json': {'sql': '-- Write your SQL query here\nSELECT emp_id, salary\nFROM Employees;\n'},
        'test_cases': [   {   'expected_output': '2|200',
                              'input_data': 'CREATE TABLE Employees (emp_id INT, dept_id INT, salary NUMERIC);\n'
                                            'INSERT INTO Employees VALUES (1, 1, 100), (2, 1, 200), (3, 2, 500);',
                              'is_hidden': False,
                              'weight': 1.0},
                          {   'expected_output': '',
                              'input_data': 'CREATE TABLE Employees (emp_id INT, dept_id INT, salary NUMERIC);\n'
                                            'INSERT INTO Employees VALUES (1, 1, 150), (2, 1, 150);',
                              'is_hidden': False,
                              'weight': 1.0},
                          {   'expected_output': '3|150',
                              'input_data': 'CREATE TABLE Employees (emp_id INT, dept_id INT, salary NUMERIC);\n'
                                            'INSERT INTO Employees VALUES (1, 1, 50), (2, 1, 100), (3, 1, 150);',
                              'is_hidden': False,
                              'weight': 1.0},
                          {   'expected_output': '10|300\n30|800',
                              'input_data': 'CREATE TABLE Employees (emp_id INT, dept_id INT, salary NUMERIC);\n'
                                            'INSERT INTO Employees VALUES (10, 1, 300), (20, 1, 100), (30, 2, 800), '
                                            '(40, 2, 200);',
                              'is_hidden': True,
                              'weight': 1.5},
                          {   'expected_output': '',
                              'input_data': 'CREATE TABLE Employees (emp_id INT, dept_id INT, salary NUMERIC);',
                              'is_hidden': True,
                              'weight': 1.5},
                          {   'expected_output': '2|10000',
                              'input_data': 'CREATE TABLE Employees (emp_id INT, dept_id INT, salary NUMERIC);\n'
                                            'INSERT INTO Employees VALUES (1, 10, 5000), (2, 10, 10000), (3, 10, '
                                            '6000);',
                              'is_hidden': True,
                              'weight': 2.0}],
        'title': 'Department Average Salary Comparison',
        'wrong_stub': 'SELECT emp_id, salary FROM Employees;\n'},
    {   'category': 'Coding',
        'complexity_notes': 'Time: O(N log N) grouping and date sort, Space: O(M) monthly aggregates.',
        'constraints': 'Schema: Orders (order_id INT, order_date TEXT, amount NUMERIC)',
        'description': 'Write a SQL query to calculate total revenue per month from the Orders table, ordered '
                       'chronologically. Output month (formatted YYYY-MM) and total_revenue.',
        'difficulty': 'MEDIUM',
        'examples_json': [   {   'explanation': 'Grouped and summed by month.',
                                 'input': "Orders: (1, '2024-01-15', 500), (2, '2024-01-20', 300), (3, '2024-02-10', "
                                          '400)',
                                 'output': '2024-01|800\n2024-02|400'}],
        'field': 'SQL',
        'language': 'sql',
        'marks': 15.0,
        'problem_type': 'SQL',
        'reference_solution': "SELECT strftime('%Y-%m', order_date) AS month, SUM(amount) AS total_revenue\n"
                              'FROM Orders\n'
                              "GROUP BY strftime('%Y-%m', order_date)\n"
                              'ORDER BY month;\n',
        'schema_ddl': 'CREATE TABLE Orders (order_id INT, order_date TEXT, amount NUMERIC);',
        'starter_code_json': {   'sql': '-- Write your SQL query here\n'
                                        "SELECT strftime('%Y-%m', order_date) AS month, SUM(amount) AS total_revenue\n"
                                        'FROM Orders\n'
                                        'GROUP BY month\n'
                                        'ORDER BY month;\n'},
        'test_cases': [   {   'expected_output': '2024-01|250\n2024-02|200',
                              'input_data': 'CREATE TABLE Orders (order_id INT, order_date TEXT, amount NUMERIC);\n'
                                            "INSERT INTO Orders VALUES (1, '2024-01-15', 100), (2, '2024-01-20', 150), "
                                            "(3, '2024-02-05', 200);",
                              'is_hidden': False,
                              'weight': 1.0},
                          {   'expected_output': '2024-03|50',
                              'input_data': 'CREATE TABLE Orders (order_id INT, order_date TEXT, amount NUMERIC);\n'
                                            "INSERT INTO Orders VALUES (1, '2024-03-01', 50);",
                              'is_hidden': False,
                              'weight': 1.0},
                          {   'expected_output': '2024-05|1000',
                              'input_data': 'CREATE TABLE Orders (order_id INT, order_date TEXT, amount NUMERIC);\n'
                                            "INSERT INTO Orders VALUES (1, '2024-05-01', 300), (2, '2024-05-15', 700);",
                              'is_hidden': False,
                              'weight': 1.0},
                          {   'expected_output': '2023-11|10\n2023-12|20\n2024-01|30',
                              'input_data': 'CREATE TABLE Orders (order_id INT, order_date TEXT, amount NUMERIC);\n'
                                            "INSERT INTO Orders VALUES (1, '2023-11-10', 10), (2, '2023-12-01', 20), "
                                            "(3, '2024-01-01', 30);",
                              'is_hidden': True,
                              'weight': 1.5},
                          {   'expected_output': '',
                              'input_data': 'CREATE TABLE Orders (order_id INT, order_date TEXT, amount NUMERIC);',
                              'is_hidden': True,
                              'weight': 1.5},
                          {   'expected_output': '2024-06|600\n2024-07|600',
                              'input_data': 'CREATE TABLE Orders (order_id INT, order_date TEXT, amount NUMERIC);\n'
                                            "INSERT INTO Orders VALUES (1, '2024-06-10', 450), (2, '2024-07-15', 600), "
                                            "(3, '2024-06-25', 150);",
                              'is_hidden': True,
                              'weight': 2.0}],
        'title': 'Monthly Revenue Aggregate Calculation',
        'wrong_stub': "SELECT '2024-01', 0;\n"},
    {   'category': 'Coding',
        'complexity_notes': 'Time: O(N) grouping and filter, Space: O(C) customer tally table.',
        'constraints': 'Schema: Orders (order_id INT, customer_id INT, order_date TEXT)',
        'description': 'Write a SQL query to find customers who placed at least 2 distinct orders. Output customer_id '
                       'and total order count, ordered by order count descending.',
        'difficulty': 'EASY',
        'examples_json': [   {   'explanation': 'Customer 101 has 2 orders.',
                                 'input': "Orders: (1, 101, '...'), (2, 101, '...'), (3, 102, '...')",
                                 'output': '101|2'}],
        'field': 'SQL',
        'language': 'sql',
        'marks': 10.0,
        'problem_type': 'SQL',
        'reference_solution': 'SELECT customer_id, COUNT(order_id) AS total_orders\n'
                              'FROM Orders\n'
                              'GROUP BY customer_id\n'
                              'HAVING COUNT(order_id) >= 2\n'
                              'ORDER BY total_orders DESC, customer_id ASC;\n',
        'schema_ddl': 'CREATE TABLE Orders (order_id INT, customer_id INT, order_date TEXT);',
        'starter_code_json': {   'sql': '-- Write your SQL query here\n'
                                        'SELECT customer_id, COUNT(order_id) AS total_orders\n'
                                        'FROM Orders\n'
                                        'GROUP BY customer_id\n'
                                        'HAVING COUNT(order_id) >= 2\n'
                                        'ORDER BY total_orders DESC;\n'},
        'test_cases': [   {   'expected_output': '101|2',
                              'input_data': 'CREATE TABLE Orders (order_id INT, customer_id INT, order_date TEXT);\n'
                                            "INSERT INTO Orders VALUES (1, 101, '2024-01-01'), (2, 101, '2024-01-02'), "
                                            "(3, 102, '2024-01-01');",
                              'is_hidden': False,
                              'weight': 1.0},
                          {   'expected_output': '',
                              'input_data': 'CREATE TABLE Orders (order_id INT, customer_id INT, order_date TEXT);\n'
                                            "INSERT INTO Orders VALUES (1, 201, '2024-02-01'), (2, 202, '2024-02-02');",
                              'is_hidden': False,
                              'weight': 1.0},
                          {   'expected_output': '301|3',
                              'input_data': 'CREATE TABLE Orders (order_id INT, customer_id INT, order_date TEXT);\n'
                                            "INSERT INTO Orders VALUES (1, 301, '2024-03-01'), (2, 301, '2024-03-02'), "
                                            "(3, 301, '2024-03-03');",
                              'is_hidden': False,
                              'weight': 1.0},
                          {   'expected_output': '1|2\n2|2',
                              'input_data': 'CREATE TABLE Orders (order_id INT, customer_id INT, order_date TEXT);\n'
                                            "INSERT INTO Orders VALUES (1, 1, 'd1'), (2, 2, 'd2'), (3, 1, 'd3'), (4, "
                                            "2, 'd4');",
                              'is_hidden': True,
                              'weight': 1.5},
                          {   'expected_output': '',
                              'input_data': 'CREATE TABLE Orders (order_id INT, customer_id INT, order_date TEXT);',
                              'is_hidden': True,
                              'weight': 1.5},
                          {   'expected_output': '5|3\n6|2',
                              'input_data': 'CREATE TABLE Orders (order_id INT, customer_id INT, order_date TEXT);\n'
                                            "INSERT INTO Orders VALUES (1, 5, 'd1'), (2, 5, 'd2'), (3, 6, 'd3'), (4, "
                                            "5, 'd4'), (5, 6, 'd5');",
                              'is_hidden': True,
                              'weight': 2.0}],
        'title': 'Customer Loyalty Order Counter',
        'wrong_stub': 'SELECT customer_id, 1 FROM Orders;\n'},
    {   'argument_schema': [{'name': 's', 'type': 'String'}],
        'category': 'Coding',
        'complexity_notes': 'Time: O(N) two pointers from both ends, Space: O(1) in-place comparison.',
        'constraints': '1 <= s.length() <= 2 * 10^5\ns consists only of printable ASCII characters.',
        'description': 'A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and '
                       'removing all non-alphanumeric characters, it reads the same forward and backward.',
        'difficulty': 'EASY',
        'entry_point': 'isPalindrome',
        'examples_json': [   {   'explanation': '"amanaplanacanalpanama" is a palindrome.',
                                 'input': 's = "A man, a plan, a canal: Panama"',
                                 'output': 'true'},
                             {   'explanation': '"raceacar" is not a palindrome.',
                                 'input': 's = "race a car"',
                                 'output': 'false'}],
        'field': 'Java',
        'language': 'java',
        'marks': 10.0,
        'problem_type': 'CODING',
        'reference_solution': 'public class Solution {\n'
                              '    public boolean isPalindrome(String s) {\n'
                              '        int i = 0, j = s.length() - 1;\n'
                              '        while (i < j) {\n'
                              '            while (i < j && !Character.isLetterOrDigit(s.charAt(i))) i++;\n'
                              '            while (i < j && !Character.isLetterOrDigit(s.charAt(j))) j--;\n'
                              '            if (Character.toLowerCase(s.charAt(i)) != '
                              'Character.toLowerCase(s.charAt(j))) return false;\n'
                              '            i++; j--;\n'
                              '        }\n'
                              '        return true;\n'
                              '    }\n'
                              '}\n',
        'starter_code_json': {   'java': 'public class Solution {\n'
                                         '    public boolean isPalindrome(String s) {\n'
                                         '        // Return true if palindrome ignoring non-alphanumeric and case\n'
                                         '        return false;\n'
                                         '    }\n'
                                         '}\n'},
        'test_cases': [   {   'expected_output': 'true',
                              'input_data': '"A man, a plan, a canal: Panama"',
                              'is_hidden': False,
                              'weight': 1.0},
                          {'expected_output': 'false', 'input_data': '"race a car"', 'is_hidden': False, 'weight': 1.0},
                          {'expected_output': 'true', 'input_data': '" "', 'is_hidden': False, 'weight': 1.0},
                          {'expected_output': 'false', 'input_data': '"0P"', 'is_hidden': True, 'weight': 1.5},
                          {'expected_output': 'true', 'input_data': '"ab_a"', 'is_hidden': True, 'weight': 1.5},
                          {   'expected_output': 'true',
                              'input_data': '"Was it a car or a cat I saw?"',
                              'is_hidden': True,
                              'weight': 2.0}],
        'title': 'Valid Palindrome with Alphanumeric Filter',
        'wrong_stub': 'public class Solution {\n'
                      '    public boolean isPalindrome(String s) {\n'
                      '        return false;\n'
                      '    }\n'
                      '}\n'},
    {   'argument_schema': [{'name': 's', 'type': 'String'}],
        'category': 'Coding',
        'complexity_notes': 'Time: O(N) token splitting and StringBuilder reverse join, Space: O(N) word storage.',
        'constraints': '1 <= s.length <= 10^4\n'
                       "s contains English letters (upper-case and lower-case), digits, and spaces ' '.",
        'description': 'Given an input string s, reverse the order of the words. A word is defined as a sequence of '
                       'non-space characters. The words in s will be separated by at least one space. Return a string '
                       'of the words in reverse order concatenated by a single space with no leading or trailing '
                       'spaces.',
        'difficulty': 'MEDIUM',
        'entry_point': 'reverseWords',
        'examples_json': [   {   'explanation': 'Reversed words.',
                                 'input': 's = "the sky is blue"',
                                 'output': '"blue is sky the"'},
                             {   'explanation': 'Multiple spaces trimmed to single space.',
                                 'input': 's = "  hello world  "',
                                 'output': '"world hello"'}],
        'field': 'Java',
        'language': 'java',
        'marks': 15.0,
        'problem_type': 'CODING',
        'reference_solution': 'public class Solution {\n'
                              '    public String reverseWords(String s) {\n'
                              '        String[] parts = s.trim().split("\\\\s+");\n'
                              '        StringBuilder sb = new StringBuilder();\n'
                              '        for (int i = parts.length - 1; i >= 0; i--) {\n'
                              '            sb.append(parts[i]);\n'
                              '            if (i > 0) sb.append(" ");\n'
                              '        }\n'
                              '        return sb.toString();\n'
                              '    }\n'
                              '}\n',
        'starter_code_json': {   'java': 'public class Solution {\n'
                                         '    public String reverseWords(String s) {\n'
                                         '        // Reverse word order and normalize spacing\n'
                                         '        return "";\n'
                                         '    }\n'
                                         '}\n'},
        'test_cases': [   {   'expected_output': 'blue is sky the',
                              'input_data': '"the sky is blue"',
                              'is_hidden': False,
                              'weight': 1.0},
                          {   'expected_output': 'world hello',
                              'input_data': '"  hello world  "',
                              'is_hidden': False,
                              'weight': 1.0},
                          {   'expected_output': 'example good a',
                              'input_data': '"a good   example"',
                              'is_hidden': False,
                              'weight': 1.0},
                          {'expected_output': 'single', 'input_data': '"single"', 'is_hidden': True, 'weight': 1.5},
                          {   'expected_output': 'ARCHITECTURE SOFTWARE EPIC',
                              'input_data': '"EPIC SOFTWARE ARCHITECTURE"',
                              'is_hidden': True,
                              'weight': 1.5},
                          {   'expected_output': 'four three two one',
                              'input_data': '"  one   two   three   four  "',
                              'is_hidden': True,
                              'weight': 2.0}],
        'title': 'Reverse Words in a String',
        'wrong_stub': 'public class Solution {\n'
                      '    public String reverseWords(String s) {\n'
                      '        return s;\n'
                      '    }\n'
                      '}\n'},
    {   'argument_schema': [{'name': 'nums', 'type': 'int[]'}],
        'category': 'Coding',
        'complexity_notes': "Time: O(N) single pass Kadane's dynamic programming, Space: O(1) constant memory.",
        'constraints': '1 <= nums.length <= 10^5\n-10^4 <= nums[i] <= 10^4',
        'description': 'Given an integer array nums, find the subarray with the largest sum, and return its sum '
                       "(Kadane's Algorithm).",
        'difficulty': 'MEDIUM',
        'entry_point': 'maxSubArray',
        'examples_json': [   {   'explanation': 'The subarray [4,-1,2,1] has the largest sum 6.',
                                 'input': 'nums = [-2,1,-3,4,-1,2,1,-5,4]',
                                 'output': '6'},
                             {'explanation': 'Single element array.', 'input': 'nums = [1]', 'output': '1'}],
        'field': 'Java',
        'language': 'java',
        'marks': 15.0,
        'problem_type': 'CODING',
        'reference_solution': 'public class Solution {\n'
                              '    public int maxSubArray(int[] nums) {\n'
                              '        int maxSoFar = nums[0];\n'
                              '        int currentMax = nums[0];\n'
                              '        for (int i = 1; i < nums.length; i++) {\n'
                              '            currentMax = Math.max(nums[i], currentMax + nums[i]);\n'
                              '            maxSoFar = Math.max(maxSoFar, currentMax);\n'
                              '        }\n'
                              '        return maxSoFar;\n'
                              '    }\n'
                              '}\n',
        'starter_code_json': {   'java': 'public class Solution {\n'
                                         '    public int maxSubArray(int[] nums) {\n'
                                         "        // Kadane's algorithm\n"
                                         '        return 0;\n'
                                         '    }\n'
                                         '}\n'},
        'test_cases': [   {   'expected_output': '6',
                              'input_data': '[-2, 1, -3, 4, -1, 2, 1, -5, 4]',
                              'is_hidden': False,
                              'weight': 1.0},
                          {'expected_output': '1', 'input_data': '[1]', 'is_hidden': False, 'weight': 1.0},
                          {   'expected_output': '23',
                              'input_data': '[5, 4, -1, 7, 8]',
                              'is_hidden': False,
                              'weight': 1.0},
                          {'expected_output': '-1', 'input_data': '[-1]', 'is_hidden': True, 'weight': 1.5},
                          {'expected_output': '-1', 'input_data': '[-2, -1]', 'is_hidden': True, 'weight': 1.5},
                          {'expected_output': '15', 'input_data': '[1, 2, 3, 4, 5]', 'is_hidden': True, 'weight': 2.0}],
        'title': 'Maximum Subarray Sum',
        'wrong_stub': 'public class Solution {\n'
                      '    public int maxSubArray(int[] nums) {\n'
                      '        return 0;\n'
                      '    }\n'
                      '}\n'},
    {   'argument_schema': [{'name': 'tokens', 'type': 'String[]'}],
        'category': 'Coding',
        'complexity_notes': 'Time: O(N) single pass evaluation with operand stack, Space: O(N) stack auxiliary memory.',
        'constraints': '1 <= tokens.length <= 10^4\n'
                       "tokens[i] is either an operator ('+', '-', '*', '/') or an integer in the range [-200, 200].",
        'description': 'You are given an array of strings tokens that represents an arithmetic expression in a Reverse '
                       'Polish Notation (Postfix). Evaluate the expression and return an integer that represents the '
                       'value of the expression.',
        'difficulty': 'MEDIUM',
        'entry_point': 'evalRPN',
        'examples_json': [   {   'explanation': '((2 + 1) * 3) = 9',
                                 'input': 'tokens = ["2","1","+","3","*"]',
                                 'output': '9'},
                             {   'explanation': '(4 + (13 / 5)) = 6',
                                 'input': 'tokens = ["4","13","5","/","+"]',
                                 'output': '6'}],
        'field': 'Java',
        'language': 'java',
        'marks': 15.0,
        'problem_type': 'CODING',
        'reference_solution': 'import java.util.Stack;\n'
                              'public class Solution {\n'
                              '    public int evalRPN(String[] tokens) {\n'
                              '        Stack<Integer> stack = new Stack<>();\n'
                              '        for (String t : tokens) {\n'
                              '            if (t.equals("+")) {\n'
                              '                stack.push(stack.pop() + stack.pop());\n'
                              '            } else if (t.equals("-")) {\n'
                              '                int b = stack.pop();\n'
                              '                int a = stack.pop();\n'
                              '                stack.push(a - b);\n'
                              '            } else if (t.equals("*")) {\n'
                              '                stack.push(stack.pop() * stack.pop());\n'
                              '            } else if (t.equals("/")) {\n'
                              '                int b = stack.pop();\n'
                              '                int a = stack.pop();\n'
                              '                stack.push(a / b);\n'
                              '            } else {\n'
                              '                stack.push(Integer.parseInt(t));\n'
                              '            }\n'
                              '        }\n'
                              '        return stack.pop();\n'
                              '    }\n'
                              '}\n',
        'starter_code_json': {   'java': 'public class Solution {\n'
                                         '    public int evalRPN(String[] tokens) {\n'
                                         '        // Evaluate postfix expression using a stack\n'
                                         '        return 0;\n'
                                         '    }\n'
                                         '}\n'},
        'test_cases': [   {   'expected_output': '9',
                              'input_data': '["2", "1", "+", "3", "*"]',
                              'is_hidden': False,
                              'weight': 1.0},
                          {   'expected_output': '6',
                              'input_data': '["4", "13", "5", "/", "+"]',
                              'is_hidden': False,
                              'weight': 1.0},
                          {   'expected_output': '22',
                              'input_data': '["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]',
                              'is_hidden': False,
                              'weight': 1.0},
                          {'expected_output': '-1', 'input_data': '["3", "-4", "+"]', 'is_hidden': True, 'weight': 1.5},
                          {'expected_output': '18', 'input_data': '["18"]', 'is_hidden': True, 'weight': 1.5},
                          {   'expected_output': '14',
                              'input_data': '["5", "1", "2", "+", "4", "*", "+", "3", "-"]',
                              'is_hidden': True,
                              'weight': 2.0}],
        'title': 'Evaluate Reverse Polish Notation',
        'wrong_stub': 'public class Solution {\n'
                      '    public int evalRPN(String[] tokens) {\n'
                      '        return 0;\n'
                      '    }\n'
                      '}\n'},
    {   'argument_schema': [{'name': 'arr', 'type': 'Array'}, {'name': 'size', 'type': 'number'}],
        'category': 'Coding',
        'complexity_notes': 'Time: O(N) slicing sub-arrays, Space: O(N) result chunk container.',
        'constraints': '0 <= arr.length <= 10^5\n1 <= size <= arr.length + 1',
        'description': 'Given an array arr and a chunk size size, return a chunked array. A chunked array contains the '
                       'original elements in arr, but consists of subarrays each of length size. The length of the '
                       'last subarray may be less than size if arr.length is not evenly divisible by size.',
        'difficulty': 'EASY',
        'entry_point': 'chunk',
        'examples_json': [   {   'explanation': 'Each chunk has size 1.',
                                 'input': 'arr = [1, 2, 3, 4, 5], size = 1',
                                 'output': '[[1], [2], [3], [4], [5]]'},
                             {   'explanation': 'Last chunk contains the remaining 2 elements.',
                                 'input': 'arr = [1, 9, 6, 3, 2], size = 3',
                                 'output': '[[1, 9, 6], [3, 2]]'}],
        'field': 'JavaScript',
        'language': 'javascript',
        'marks': 10.0,
        'problem_type': 'CODING',
        'reference_solution': 'function chunk(arr, size) {\n'
                              '    const res = [];\n'
                              '    for (let i = 0; i < arr.length; i += size) {\n'
                              '        res.push(arr.slice(i, i + size));\n'
                              '    }\n'
                              '    return res;\n'
                              '}\n',
        'starter_code_json': {   'javascript': 'function chunk(arr, size) {\n'
                                               '    // Split arr into subarrays of length size\n'
                                               '    return [];\n'
                                               '}\n'},
        'test_cases': [   {   'expected_output': '[[1], [2], [3], [4], [5]]',
                              'input_data': '[1, 2, 3, 4, 5]\n1',
                              'is_hidden': False,
                              'weight': 1.0},
                          {   'expected_output': '[[1, 9, 6], [3, 2]]',
                              'input_data': '[1, 9, 6, 3, 2]\n3',
                              'is_hidden': False,
                              'weight': 1.0},
                          {   'expected_output': '[[8, 5, 3, 2, 6]]',
                              'input_data': '[8, 5, 3, 2, 6]\n6',
                              'is_hidden': False,
                              'weight': 1.0},
                          {'expected_output': '[]', 'input_data': '[]\n1', 'is_hidden': True, 'weight': 1.5},
                          {   'expected_output': '[[1, 2], [3, 4]]',
                              'input_data': '[1, 2, 3, 4]\n2',
                              'is_hidden': True,
                              'weight': 1.5},
                          {   'expected_output': '[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10]]',
                              'input_data': '[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\n4',
                              'is_hidden': True,
                              'weight': 2.0}],
        'title': 'Array Chunking Utility',
        'wrong_stub': 'function chunk(arr, size) {\n    return [arr];\n}\n'},
    {   'argument_schema': [{'name': 'arr', 'type': 'Array'}, {'name': 'n', 'type': 'number'}],
        'category': 'Coding',
        'complexity_notes': 'Time: O(N) recursive traversal of elements, Space: O(depth) call stack.',
        'constraints': '0 <= count of elements <= 10^5\n0 <= n <= 1000',
        'description': 'Given a multi-dimensional array arr and a depth n, return a flattened version of that array up '
                       'to depth n without using Array.prototype.flat.',
        'difficulty': 'MEDIUM',
        'entry_point': 'flat',
        'examples_json': [   {   'explanation': 'Depth 0 does not flatten any subarrays.',
                                 'input': 'arr = [1, 2, 3, [4, 5, 6], [7, 8, [9, 10, 11], 12], [13, 14, 15]], n = 0',
                                 'output': '[1, 2, 3, [4, 5, 6], [7, 8, [9, 10, 11], 12], [13, 14, 15]]'},
                             {   'explanation': 'Flattens one level of nested arrays.',
                                 'input': 'arr = [1, 2, 3, [4, 5, 6], [7, 8, [9, 10, 11], 12], [13, 14, 15]], n = 1',
                                 'output': '[1, 2, 3, 4, 5, 6, 7, 8, [9, 10, 11], 12, 13, 14, 15]'}],
        'field': 'JavaScript',
        'language': 'javascript',
        'marks': 15.0,
        'problem_type': 'CODING',
        'reference_solution': 'function flat(arr, n) {\n'
                              '    if (n <= 0) return arr.slice();\n'
                              '    const res = [];\n'
                              '    for (const item of arr) {\n'
                              '        if (Array.isArray(item)) {\n'
                              '            res.push(...flat(item, n - 1));\n'
                              '        } else {\n'
                              '            res.push(item);\n'
                              '        }\n'
                              '    }\n'
                              '    return res;\n'
                              '}\n',
        'starter_code_json': {   'javascript': 'function flat(arr, n) {\n'
                                               '    // Flatten nested array up to depth n without '
                                               'Array.prototype.flat\n'
                                               '    return [];\n'
                                               '}\n'},
        'test_cases': [   {   'expected_output': '[1, 2, 3, [4, 5, 6], [7, 8, [9, 10, 11], 12], [13, 14, 15]]',
                              'input_data': '[1, 2, 3, [4, 5, 6], [7, 8, [9, 10, 11], 12], [13, 14, 15]]\n0',
                              'is_hidden': False,
                              'weight': 1.0},
                          {   'expected_output': '[1, 2, 3, 4, 5, 6, 7, 8, [9, 10, 11], 12, 13, 14, 15]',
                              'input_data': '[1, 2, 3, [4, 5, 6], [7, 8, [9, 10, 11], 12], [13, 14, 15]]\n1',
                              'is_hidden': False,
                              'weight': 1.0},
                          {   'expected_output': '[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]',
                              'input_data': '[[1, 2, 3], [4, 5, 6], [7, 8, [9, 10, 11], 12], [13, 14, 15]]\n2',
                              'is_hidden': False,
                              'weight': 1.0},
                          {'expected_output': '[]', 'input_data': '[]\n5', 'is_hidden': True, 'weight': 1.5},
                          {   'expected_output': '[1, 2, [3, [4]]]',
                              'input_data': '[1, [2, [3, [4]]]]\n1',
                              'is_hidden': True,
                              'weight': 1.5},
                          {   'expected_output': '[1, 2, 3, 4]',
                              'input_data': '[1, [2, [3, [4]]]]\n3',
                              'is_hidden': True,
                              'weight': 2.0}],
        'title': 'Flatten Deeply Nested Array',
        'wrong_stub': 'function flat(arr, n) {\n    return arr;\n}\n'},
    {   'argument_schema': [{'name': 'obj', 'type': 'Object|Array'}],
        'category': 'Coding',
        'complexity_notes': 'Time: O(N) recursive traversal of all nested properties, Space: O(N) cleaned copy.',
        'constraints': 'obj is a valid JSON object or array\n2 <= JSON.stringify(obj).length <= 10^5',
        'description': 'Given an object or array obj, return a compact object. A compact object is the same as the '
                       'original object, except with keys containing falsy values removed. This operation applies to '
                       'the object and any nested objects. Arrays should have their falsy values filtered out. Values '
                       'considered falsy are false, 0, "", null, undefined, and NaN.',
        'difficulty': 'MEDIUM',
        'entry_point': 'compactObject',
        'examples_json': [   {   'explanation': 'All falsy values removed from array.',
                                 'input': 'obj = [null, 0, false, 1]',
                                 'output': '[1]'},
                             {   'explanation': "Key 'a' removed and nested false filtered out.",
                                 'input': 'obj = {"a": null, "b": [false, 1]}',
                                 'output': '{"b": [1]}'}],
        'field': 'JavaScript',
        'language': 'javascript',
        'marks': 15.0,
        'problem_type': 'CODING',
        'reference_solution': 'function compactObject(obj) {\n'
                              "    if (obj === null || typeof obj !== 'object') return obj;\n"
                              '    if (Array.isArray(obj)) {\n'
                              '        return obj.filter(Boolean).map(compactObject);\n'
                              '    }\n'
                              '    const res = {};\n'
                              '    for (const key in obj) {\n'
                              '        const val = compactObject(obj[key]);\n'
                              '        if (Boolean(val)) {\n'
                              '            res[key] = val;\n'
                              '        }\n'
                              '    }\n'
                              '    return res;\n'
                              '}\n',
        'starter_code_json': {   'javascript': 'function compactObject(obj) {\n'
                                               '    // Recursively filter out falsy values\n'
                                               '    return obj;\n'
                                               '}\n'},
        'test_cases': [   {   'expected_output': '[1]',
                              'input_data': '[null, 0, false, 1]',
                              'is_hidden': False,
                              'weight': 1.0},
                          {   'expected_output': '{"b": [1]}',
                              'input_data': '{"a": null, "b": [false, 1]}',
                              'is_hidden': False,
                              'weight': 1.0},
                          {   'expected_output': '[5, [], [16]]',
                              'input_data': '[null, 0, 5, [0], [false, 16]]',
                              'is_hidden': False,
                              'weight': 1.0},
                          {'expected_output': '{}', 'input_data': '{}', 'is_hidden': True, 'weight': 1.5},
                          {   'expected_output': '{}',
                              'input_data': '{"x": 0, "y": "", "z": false}',
                              'is_hidden': True,
                              'weight': 1.5},
                          {   'expected_output': '{"valid": true, "data": ["ok", 42]}',
                              'input_data': '{"valid": true, "data": ["ok", null, 42]}',
                              'is_hidden': True,
                              'weight': 2.0}],
        'title': 'Compact Object Filter',
        'wrong_stub': 'function compactObject(obj) {\n    return obj;\n}\n'},
    {   'argument_schema': [{'name': 'obj', 'type': 'Object|Array'}],
        'category': 'Coding',
        'complexity_notes': 'Time: O(N) structural recursion, Space: O(N) fresh copy allocation.',
        'constraints': 'Input contains nested JSON-serializable primitives, objects, and arrays.',
        'description': 'Implement a deepClone function in JavaScript that creates a deep copy of nested plain objects '
                       'and arrays without mutating the original input.',
        'difficulty': 'HARD',
        'entry_point': 'deepClone',
        'examples_json': [   {   'explanation': 'Deep copy of nested dictionary.',
                                 'input': 'obj = {"a": 1, "b": {"c": 2}}',
                                 'output': '{"a": 1, "b": {"c": 2}}'}],
        'field': 'JavaScript',
        'language': 'javascript',
        'marks': 20.0,
        'problem_type': 'CODING',
        'reference_solution': 'function deepClone(obj) {\n'
                              "    if (obj === null || typeof obj !== 'object') return obj;\n"
                              '    if (Array.isArray(obj)) {\n'
                              '        return obj.map(deepClone);\n'
                              '    }\n'
                              '    const copy = {};\n'
                              '    for (const key of Object.keys(obj)) {\n'
                              '        copy[key] = deepClone(obj[key]);\n'
                              '    }\n'
                              '    return copy;\n'
                              '}\n',
        'starter_code_json': {   'javascript': 'function deepClone(obj) {\n'
                                               '    // Create a deep copy of obj\n'
                                               '    return obj;\n'
                                               '}\n'},
        'test_cases': [   {   'expected_output': '{"a": 1, "b": {"c": 2}}',
                              'input_data': '{"a": 1, "b": {"c": 2}}',
                              'is_hidden': False,
                              'weight': 1.0},
                          {   'expected_output': '[1, [2, 3], {"x": 4}]',
                              'input_data': '[1, [2, 3], {"x": 4}]',
                              'is_hidden': False,
                              'weight': 1.0},
                          {'expected_output': '42', 'input_data': '42', 'is_hidden': False, 'weight': 1.0},
                          {'expected_output': '[]', 'input_data': '[]', 'is_hidden': True, 'weight': 1.5},
                          {   'expected_output': '{"empty": {}, "arr": []}',
                              'input_data': '{"empty": {}, "arr": []}',
                              'is_hidden': True,
                              'weight': 1.5},
                          {   'expected_output': '{"users": [{"id": 1, "roles": ["admin", "user"]}]}',
                              'input_data': '{"users": [{"id": 1, "roles": ["admin", "user"]}]}',
                              'is_hidden': True,
                              'weight': 2.0}],
        'title': 'Deep Object Clone',
        'wrong_stub': 'function deepClone(obj) {\n    return null;\n}\n'},
    {   'argument_schema': [{'name': 'nums', 'type': 'std::vector<int>'}],
        'category': 'Coding',
        'complexity_notes': 'Time: O(N) two pointers in-place, Space: O(1) constant auxiliary memory.',
        'constraints': '1 <= nums.length <= 10^4\n-2^31 <= nums[i] <= 2^31 - 1',
        'description': "Given an integer array nums, move all 0's to the end of it while maintaining the relative "
                       'order of the non-zero elements. Return the modified vector.',
        'difficulty': 'EASY',
        'entry_point': 'moveZeroes',
        'examples_json': [   {   'explanation': 'Zeroes shifted to end maintaining non-zero ordering.',
                                 'input': 'nums = [0, 1, 0, 3, 12]',
                                 'output': '[1, 3, 12, 0, 0]'}],
        'field': 'C++',
        'language': 'cpp',
        'marks': 10.0,
        'problem_type': 'CODING',
        'reference_solution': '#include <vector>\n'
                              '\n'
                              'std::vector<int> moveZeroes(std::vector<int> nums) {\n'
                              '    int insertPos = 0;\n'
                              '    for (int i = 0; i < (int)nums.size(); ++i) {\n'
                              '        if (nums[i] != 0) {\n'
                              '            nums[insertPos++] = nums[i];\n'
                              '        }\n'
                              '    }\n'
                              '    while (insertPos < (int)nums.size()) {\n'
                              '        nums[insertPos++] = 0;\n'
                              '    }\n'
                              '    return nums;\n'
                              '}\n',
        'starter_code_json': {   'cpp': '#include <vector>\n'
                                        '\n'
                                        'std::vector<int> moveZeroes(std::vector<int> nums) {\n'
                                        '    // Shift zeroes to end and return\n'
                                        '    return nums;\n'
                                        '}\n'},
        'test_cases': [   {   'expected_output': '[1, 3, 12, 0, 0]',
                              'input_data': '0 1 0 3 12',
                              'is_hidden': False,
                              'weight': 1.0},
                          {'expected_output': '[0]', 'input_data': '0', 'is_hidden': False, 'weight': 1.0},
                          {'expected_output': '[1, 2, 3]', 'input_data': '1 2 3', 'is_hidden': False, 'weight': 1.0},
                          {'expected_output': '[1, 0, 0]', 'input_data': '0 0 1', 'is_hidden': True, 'weight': 1.5},
                          {   'expected_output': '[4, 5, 6, 0, 0]',
                              'input_data': '4 0 5 0 6',
                              'is_hidden': True,
                              'weight': 1.5},
                          {   'expected_output': '[0, 0, 0, 0, 0]',
                              'input_data': '0 0 0 0 0',
                              'is_hidden': True,
                              'weight': 2.0}],
        'title': 'Move Zeroes in Array',
        'wrong_stub': '#include <vector>\n'
                      '\n'
                      'std::vector<int> moveZeroes(std::vector<int> nums) {\n'
                      '    return nums;\n'
                      '}\n'},
    {   'argument_schema': [{'name': 's', 'type': 'std::string'}, {'name': 'delim', 'type': 'char'}],
        'category': 'Coding',
        'complexity_notes': 'Time: O(N) single scan string parsing, Space: O(N) token vector storage.',
        'constraints': '0 <= s.length <= 10^5',
        'description': 'Implement a string tokenizer splitString(std::string s, char delim) returning '
                       'std::vector<std::string> splitting by delimiter.',
        'difficulty': 'MEDIUM',
        'entry_point': 'splitString',
        'examples_json': [   {   'explanation': 'Splits by comma.',
                                 'input': 's = "alpha,beta,gamma", delim = \',\'',
                                 'output': '["alpha", "beta", "gamma"]'}],
        'field': 'C++',
        'language': 'cpp',
        'marks': 15.0,
        'problem_type': 'CODING',
        'reference_solution': '#include <string>\n'
                              '#include <vector>\n'
                              '#include <sstream>\n'
                              '\n'
                              'std::vector<std::string> splitString(std::string s, char delim) {\n'
                              '    std::vector<std::string> tokens;\n'
                              '    std::stringstream ss(s);\n'
                              '    std::string item;\n'
                              '    while (std::getline(ss, item, delim)) {\n'
                              '        tokens.push_back(item);\n'
                              '    }\n'
                              '    return tokens;\n'
                              '}\n',
        'starter_code_json': {   'cpp': '#include <string>\n'
                                        '#include <vector>\n'
                                        '\n'
                                        'std::vector<std::string> splitString(std::string s, char delim) {\n'
                                        '    // Split string into tokens\n'
                                        '    return {};\n'
                                        '}\n'},
        'test_cases': [   {   'expected_output': '["alpha", "beta", "gamma"]',
                              'input_data': 'alpha,beta,gamma',
                              'is_hidden': False,
                              'weight': 1.0},
                          {'expected_output': '["single"]', 'input_data': 'single', 'is_hidden': False, 'weight': 1.0},
                          {   'expected_output': '["one", "two"]',
                              'input_data': 'one,two',
                              'is_hidden': False,
                              'weight': 1.0},
                          {   'expected_output': '["a", "b", "c", "d", "e"]',
                              'input_data': 'a,b,c,d,e',
                              'is_hidden': True,
                              'weight': 1.5},
                          {   'expected_output': '["TRELLIS", "ENTERPRISE", "PLATFORM"]',
                              'input_data': 'TRELLIS,ENTERPRISE,PLATFORM',
                              'is_hidden': True,
                              'weight': 1.5},
                          {   'expected_output': '["hello", "world"]',
                              'input_data': 'hello,world',
                              'is_hidden': True,
                              'weight': 2.0}],
        'title': 'String Delimiter Tokenizer',
        'wrong_stub': '#include <string>\n'
                      '#include <vector>\n'
                      '\n'
                      'std::vector<std::string> splitString(std::string s, char delim) {\n'
                      '    return {};\n'
                      '}\n'},
    {   'argument_schema': [{'name': 's', 'type': 'std::string'}, {'name': 't', 'type': 'std::string'}],
        'category': 'Coding',
        'complexity_notes': 'Time: O(N) frequency counting with 26-element array, Space: O(1) constant alphabet '
                            'buffer.',
        'constraints': '1 <= s.length, t.length <= 5 * 10^4\ns and t consist of lowercase English letters.',
        'description': 'Given two strings s and t, return true if t is an anagram of s, and false otherwise. An '
                       'Anagram is a word formed by rearranging the letters of a different word, using all the '
                       'original letters exactly once.',
        'difficulty': 'EASY',
        'entry_point': 'isAnagram',
        'examples_json': [   {   'explanation': 'Contains identical letter counts.',
                                 'input': 's = "anagram", t = "nagaram"',
                                 'output': 'true'},
                             {   'explanation': 'Letters do not match.',
                                 'input': 's = "rat", t = "car"',
                                 'output': 'false'}],
        'field': 'C++',
        'language': 'cpp',
        'marks': 10.0,
        'problem_type': 'CODING',
        'reference_solution': '#include <string>\n'
                              '#include <vector>\n'
                              '\n'
                              'bool isAnagram(std::string s, std::string t) {\n'
                              '    if (s.length() != t.length()) return false;\n'
                              '    int count[26] = {0};\n'
                              '    for (size_t i = 0; i < s.length(); ++i) {\n'
                              "        count[s[i] - 'a']++;\n"
                              "        count[t[i] - 'a']--;\n"
                              '    }\n'
                              '    for (int i = 0; i < 26; ++i) {\n'
                              '        if (count[i] != 0) return false;\n'
                              '    }\n'
                              '    return true;\n'
                              '}\n',
        'starter_code_json': {   'cpp': '#include <string>\n'
                                        '\n'
                                        'bool isAnagram(std::string s, std::string t) {\n'
                                        '    // Check if t is an anagram of s\n'
                                        '    return false;\n'
                                        '}\n'},
        'test_cases': [   {   'expected_output': 'true',
                              'input_data': 'anagram nagaram',
                              'is_hidden': False,
                              'weight': 1.0},
                          {'expected_output': 'false', 'input_data': 'rat car', 'is_hidden': False, 'weight': 1.0},
                          {'expected_output': 'true', 'input_data': 'listen silent', 'is_hidden': False, 'weight': 1.0},
                          {'expected_output': 'false', 'input_data': 'a ab', 'is_hidden': True, 'weight': 1.5},
                          {'expected_output': 'false', 'input_data': 'ab a', 'is_hidden': True, 'weight': 1.5},
                          {'expected_output': 'true', 'input_data': 'secure rescue', 'is_hidden': True, 'weight': 2.0}],
        'title': 'Valid Anagram Verification',
        'wrong_stub': '#include <string>\n\nbool isAnagram(std::string s, std::string t) {\n    return false;\n}\n'},
    {   'argument_schema': [{'name': 'n', 'type': 'int'}],
        'category': 'Coding',
        'complexity_notes': 'Time: O(N) iterative dynamic programming, Space: O(1) two variable accumulator.',
        'constraints': '0 <= n <= 45',
        'description': 'Compute the nth Fibonacci number F(n) where F(0) = 0, F(1) = 1, and F(n) = F(n-1) + F(n-2) for '
                       'n >= 2.',
        'difficulty': 'EASY',
        'entry_point': 'fibonacci',
        'examples_json': [   {'explanation': 'F(2) = F(1) + F(0) = 1 + 0 = 1.', 'input': 'n = 2', 'output': '1'},
                             {'explanation': 'F(10) = 55.', 'input': 'n = 10', 'output': '55'}],
        'field': 'C++',
        'language': 'cpp',
        'marks': 10.0,
        'problem_type': 'CODING',
        'reference_solution': 'long long fibonacci(int n) {\n'
                              '    if (n <= 0) return 0;\n'
                              '    if (n == 1) return 1;\n'
                              '    long long a = 0, b = 1;\n'
                              '    for (int i = 2; i <= n; ++i) {\n'
                              '        long long c = a + b;\n'
                              '        a = b;\n'
                              '        b = c;\n'
                              '    }\n'
                              '    return b;\n'
                              '}\n',
        'starter_code_json': {   'cpp': 'long long fibonacci(int n) {\n'
                                        '    // Return nth Fibonacci number\n'
                                        '    return 0;\n'
                                        '}\n'},
        'test_cases': [   {'expected_output': '1', 'input_data': '2', 'is_hidden': False, 'weight': 1.0},
                          {'expected_output': '55', 'input_data': '10', 'is_hidden': False, 'weight': 1.0},
                          {'expected_output': '0', 'input_data': '0', 'is_hidden': False, 'weight': 1.0},
                          {'expected_output': '1', 'input_data': '1', 'is_hidden': True, 'weight': 1.5},
                          {'expected_output': '6765', 'input_data': '20', 'is_hidden': True, 'weight': 1.5},
                          {'expected_output': '832040', 'input_data': '30', 'is_hidden': True, 'weight': 2.0}],
        'title': 'Nth Fibonacci Number Calculation',
        'wrong_stub': 'long long fibonacci(int n) {\n    return 0;\n}\n'}]
