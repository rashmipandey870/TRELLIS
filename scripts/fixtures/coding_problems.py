"""TRELLIS Coding Problems Fixtures (24 Problems across 5 Languages).
Languages: Python (6), SQL (6), Java (4), JavaScript (4), C++ (4).
Includes starter codes, constraints, test cases, and reference solutions.
"""

from app.schemas.category import AssessmentCategory

CODING_PROBLEMS = [
    # =========================================================================
    # PYTHON (6 Problems)
    # =========================================================================
    {
        "title": "Two Sum Target Indices",
        "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target. You may assume that each input would have exactly one solution, and you may not use the same element twice. Return the answer sorted in ascending order.",
        "constraints": "2 <= nums.length <= 10^4\n-10^9 <= nums[i] <= 10^9\n-10^9 <= target <= 10^9",
        "difficulty": "EASY",
        "field": "Python",
        "marks": 10.0,
        "language": "python",
        "category": AssessmentCategory.CODING.value,
        "problem_type": "CODING",
        "starter_code_json": {
            "python": "def two_sum(nums: list[int], target: int) -> list[int]:\n    # Write your solution here\n    pass\n"
        },
        "reference_solution": "def two_sum(nums: list[int], target: int) -> list[int]:\n    seen = {}\n    for i, num in enumerate(nums):\n        diff = target - num\n        if diff in seen:\n            return [seen[diff], i]\n        seen[num] = i\n    return []\n",
        "test_cases": [
            {"input_data": "[2, 7, 11, 15]\n9", "expected_output": "[0, 1]", "is_hidden": False, "weight": 1.0},
            {"input_data": "[3, 2, 4]\n6", "expected_output": "[1, 2]", "is_hidden": False, "weight": 1.0},
            {"input_data": "[3, 3]\n6", "expected_output": "[0, 1]", "is_hidden": True, "weight": 2.0},
        ]
    },
    {
        "title": "Valid Parentheses",
        "description": "Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid. An input string is valid if: open brackets must be closed by the same type of brackets, and open brackets must be closed in the correct order.",
        "constraints": "1 <= s.length <= 10^4\ns consists of parentheses only '()[]{}'.",
        "difficulty": "EASY",
        "field": "Python",
        "marks": 10.0,
        "language": "python",
        "category": AssessmentCategory.CODING.value,
        "problem_type": "CODING",
        "starter_code_json": {
            "python": "def is_valid(s: str) -> bool:\n    # Write your solution here\n    pass\n"
        },
        "reference_solution": "def is_valid(s: str) -> bool:\n    stack = []\n    mapping = {')': '(', '}': '{', ']': '['}\n    for char in s:\n        if char in mapping:\n            top = stack.pop() if stack else '#'\n            if mapping[char] != top:\n                return False\n        else:\n            stack.append(char)\n    return not stack\n",
        "test_cases": [
            {"input_data": "()", "expected_output": "True", "is_hidden": False, "weight": 1.0},
            {"input_data": "()[]{}", "expected_output": "True", "is_hidden": False, "weight": 1.0},
            {"input_data": "(]", "expected_output": "False", "is_hidden": True, "weight": 1.0},
        ]
    },
    {
        "title": "Longest Substring Without Repeating Characters",
        "description": "Given a string s, find the length of the longest substring without repeating characters.",
        "constraints": "0 <= s.length <= 5 * 10^4\ns consists of English letters, digits, symbols and spaces.",
        "difficulty": "MEDIUM",
        "field": "Python",
        "marks": 15.0,
        "language": "python",
        "category": AssessmentCategory.CODING.value,
        "problem_type": "CODING",
        "starter_code_json": {
            "python": "def length_of_longest_substring(s: str) -> int:\n    # Write your solution here\n    pass\n"
        },
        "reference_solution": "def length_of_longest_substring(s: str) -> int:\n    used = {}\n    max_len = start = 0\n    for i, char in enumerate(s):\n        if char in used and start <= used[char]:\n            start = used[char] + 1\n        else:\n            max_len = max(max_len, i - start + 1)\n        used[char] = i\n    return max_len\n",
        "test_cases": [
            {"input_data": "abcabcbb", "expected_output": "3", "is_hidden": False, "weight": 1.0},
            {"input_data": "bbbbb", "expected_output": "1", "is_hidden": False, "weight": 1.0},
            {"input_data": "pwwkew", "expected_output": "3", "is_hidden": True, "weight": 2.0},
        ]
    },
    {
        "title": "Merge Overlapping Intervals",
        "description": "Given an array of intervals where intervals[i] = [start_i, end_i], merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.",
        "constraints": "1 <= intervals.length <= 10^4\nintervals[i].length == 2\n0 <= start_i <= end_i <= 10^4",
        "difficulty": "MEDIUM",
        "field": "Python",
        "marks": 15.0,
        "language": "python",
        "category": AssessmentCategory.CODING.value,
        "problem_type": "CODING",
        "starter_code_json": {
            "python": "def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:\n    # Write your solution here\n    pass\n"
        },
        "reference_solution": "def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:\n    intervals.sort(key=lambda x: x[0])\n    merged = []\n    for interval in intervals:\n        if not merged or merged[-1][1] < interval[0]:\n            merged.append(interval)\n        else:\n            merged[-1][1] = max(merged[-1][1], interval[1])\n    return merged\n",
        "test_cases": [
            {"input_data": "[[1,3],[2,6],[8,10],[15,18]]", "expected_output": "[[1, 6], [8, 10], [15, 18]]", "is_hidden": False, "weight": 1.0},
            {"input_data": "[[1,4],[4,5]]", "expected_output": "[[1, 5]]", "is_hidden": False, "weight": 1.0},
            {"input_data": "[[1,4],[0,4]]", "expected_output": "[[0, 4]]", "is_hidden": True, "weight": 2.0},
        ]
    },
    {
        "title": "LRU Cache Mechanism",
        "description": "Implement a Least Recently Used (LRU) cache class LRUCache with get(key) and put(key, value) in O(1) average time complexity.",
        "constraints": "1 <= capacity <= 3000\n0 <= key <= 10^4\n0 <= value <= 10^5\nAt most 2 * 10^5 calls will be made to get and put.",
        "difficulty": "HARD",
        "field": "Python",
        "marks": 20.0,
        "language": "python",
        "category": AssessmentCategory.CODING.value,
        "problem_type": "CODING",
        "starter_code_json": {
            "python": "class LRUCache:\n    def __init__(self, capacity: int):\n        pass\n\n    def get(self, key: int) -> int:\n        pass\n\n    def put(self, key: int, value: int) -> None:\n        pass\n"
        },
        "reference_solution": "from collections import OrderedDict\n\nclass LRUCache:\n    def __init__(self, capacity: int):\n        self.capacity = capacity\n        self.cache = OrderedDict()\n\n    def get(self, key: int) -> int:\n        if key not in self.cache:\n            return -1\n        self.cache.move_to_end(key)\n        return self.cache[key]\n\n    def put(self, key: int, value: int) -> None:\n        if key in self.cache:\n            self.cache.move_to_end(key)\n        self.cache[key] = value\n        if len(self.cache) > self.capacity:\n            self.cache.popitem(last=False)\n",
        "test_cases": [
            {"input_data": "put(1,1), put(2,2), get(1), put(3,3), get(2)", "expected_output": "[null, null, 1, null, -1]", "is_hidden": False, "weight": 1.0},
            {"input_data": "put(2,1), get(2), put(3,2), get(2), get(3)", "expected_output": "[null, 1, null, 1, 2]", "is_hidden": True, "weight": 2.0},
        ]
    },
    {
        "title": "Trapping Rain Water",
        "description": "Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.",
        "constraints": "n == height.length\n1 <= n <= 2 * 10^4\n0 <= height[i] <= 10^5",
        "difficulty": "HARD",
        "field": "Python",
        "marks": 20.0,
        "language": "python",
        "category": AssessmentCategory.CODING.value,
        "problem_type": "CODING",
        "starter_code_json": {
            "python": "def trap(height: list[int]) -> int:\n    # Write your solution here\n    pass\n"
        },
        "reference_solution": "def trap(height: list[int]) -> int:\n    if not height: return 0\n    l, r = 0, len(height) - 1\n    left_max, right_max = height[l], height[r]\n    water = 0\n    while l < r:\n        if left_max < right_max:\n            l += 1\n            left_max = max(left_max, height[l])\n            water += left_max - height[l]\n        else:\n            r -= 1\n            right_max = max(right_max, height[r])\n            water += right_max - height[r]\n    return water\n",
        "test_cases": [
            {"input_data": "[0,1,0,2,1,0,1,3,2,1,2,1]", "expected_output": "6", "is_hidden": False, "weight": 1.0},
            {"input_data": "[4,2,0,3,2,5]", "expected_output": "9", "is_hidden": True, "weight": 2.0},
        ]
    },

    # =========================================================================
    # SQL (6 Problems)
    # =========================================================================
    {
        "title": "Top Salaried Employee per Department",
        "description": "Write a SQL query to find employees who have the highest salary in each of the departments. Output department name, employee name, and salary.",
        "constraints": "Schema: Employee (id, name, salary, department_id), Department (id, name)",
        "difficulty": "MEDIUM",
        "field": "SQL",
        "marks": 15.0,
        "language": "sql",
        "category": AssessmentCategory.CODING.value,
        "problem_type": "SQL",
        "schema_ddl": "CREATE TABLE Department (id INT PRIMARY KEY, name VARCHAR(50));\nCREATE TABLE Employee (id INT PRIMARY KEY, name VARCHAR(50), salary INT, department_id INT REFERENCES Department(id));",
        "starter_code_json": {
            "sql": "-- Write your SQL query here\nSELECT \nFROM Employee e\nJOIN Department d ON e.department_id = d.id;\n"
        },
        "reference_solution": "WITH Ranked AS (\n    SELECT d.name AS Department, e.name AS Employee, e.salary AS Salary,\n           DENSE_RANK() OVER (PARTITION BY e.department_id ORDER BY e.salary DESC) AS rnk\n    FROM Employee e\n    JOIN Department d ON e.department_id = d.id\n)\nSELECT Department, Employee, Salary FROM Ranked WHERE rnk = 1;\n",
        "test_cases": [
            {"input_data": "SELECT * FROM Department; SELECT * FROM Employee;", "expected_output": "IT|Max|90000\nSales|Henry|80000", "is_hidden": False, "weight": 1.0},
            {"input_data": "SELECT COUNT(*) FROM Employee;", "expected_output": "7", "is_hidden": True, "weight": 1.0},
        ]
    },
    {
        "title": "Monthly Rolling Revenue Calculation",
        "description": "Write a SQL query to calculate a 3-month rolling average of revenue for each month from the Orders table, ordered chronologically.",
        "constraints": "Schema: Orders (order_id INT, order_date DATE, amount DECIMAL(10,2))",
        "difficulty": "HARD",
        "field": "SQL",
        "marks": 20.0,
        "language": "sql",
        "category": AssessmentCategory.CODING.value,
        "problem_type": "SQL",
        "schema_ddl": "CREATE TABLE Orders (order_id INT PRIMARY KEY, order_date DATE, amount NUMERIC(10,2));",
        "starter_code_json": {
            "sql": "-- Calculate 3-month rolling average\nSELECT \nFROM Orders;\n"
        },
        "reference_solution": "WITH MonthlySales AS (\n    SELECT DATE_TRUNC('month', order_date) AS month, SUM(amount) AS monthly_revenue\n    FROM Orders\n    GROUP BY 1\n)\nSELECT month, monthly_revenue,\n       AVG(monthly_revenue) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS rolling_3mo_avg\nFROM MonthlySales\nORDER BY month;\n",
        "test_cases": [
            {"input_data": "SELECT COUNT(*) FROM Orders;", "expected_output": "12", "is_hidden": False, "weight": 1.0},
        ]
    },
    {
        "title": "Duplicate Email Detection",
        "description": "Write a SQL query to report all the duplicate emails in a table named Person.",
        "constraints": "Schema: Person (id INT PRIMARY KEY, email VARCHAR(255))",
        "difficulty": "EASY",
        "field": "SQL",
        "marks": 10.0,
        "language": "sql",
        "category": AssessmentCategory.CODING.value,
        "problem_type": "SQL",
        "schema_ddl": "CREATE TABLE Person (id INT PRIMARY KEY, email VARCHAR(255));",
        "starter_code_json": {
            "sql": "-- Write your SQL query here\nSELECT email\nFROM Person\nGROUP BY email;\n"
        },
        "reference_solution": "SELECT email\nFROM Person\nGROUP BY email\nHAVING COUNT(email) > 1;\n",
        "test_cases": [
            {"input_data": "INSERT INTO Person VALUES (1, 'a@b.com'), (2, 'c@d.com'), (3, 'a@b.com');", "expected_output": "a@b.com", "is_hidden": False, "weight": 1.0},
        ]
    },
    {
        "title": "Consecutive Logins Retention",
        "description": "Find all learners who logged into the platform for at least 3 consecutive days. Output their learner_id.",
        "constraints": "Schema: Logins (learner_id INT, login_date DATE)",
        "difficulty": "HARD",
        "field": "SQL",
        "marks": 20.0,
        "language": "sql",
        "category": AssessmentCategory.CODING.value,
        "problem_type": "SQL",
        "schema_ddl": "CREATE TABLE Logins (learner_id INT, login_date DATE);",
        "starter_code_json": {
            "sql": "-- Find learners with >= 3 consecutive active days\nSELECT DISTINCT learner_id\nFROM Logins;\n"
        },
        "reference_solution": "WITH Grouped AS (\n    SELECT learner_id, login_date,\n           login_date - (ROW_NUMBER() OVER (PARTITION BY learner_id ORDER BY login_date)) * INTERVAL '1 day' AS grp\n    FROM (SELECT DISTINCT learner_id, login_date FROM Logins) t\n)\nSELECT learner_id\nFROM Grouped\nGROUP BY learner_id, grp\nHAVING COUNT(*) >= 3;\n",
        "test_cases": [
            {"input_data": "SELECT COUNT(*) FROM Logins;", "expected_output": "15", "is_hidden": False, "weight": 1.0},
        ]
    },
    {
        "title": "Orphan Records Audit Query",
        "description": "Write a query to identify any User record in Users that has no corresponding Profile in Profiles without using NOT IN.",
        "constraints": "Schema: Users (id INT PRIMARY KEY, email VARCHAR), Profiles (user_id INT PRIMARY KEY)",
        "difficulty": "EASY",
        "field": "SQL",
        "marks": 10.0,
        "language": "sql",
        "category": AssessmentCategory.CODING.value,
        "problem_type": "SQL",
        "schema_ddl": "CREATE TABLE Users (id INT PRIMARY KEY, email VARCHAR(100));\nCREATE TABLE Profiles (user_id INT PRIMARY KEY);",
        "starter_code_json": {
            "sql": "-- Identify Users with no matching Profile\nSELECT u.id, u.email\nFROM Users u;\n"
        },
        "reference_solution": "SELECT u.id, u.email\nFROM Users u\nLEFT JOIN Profiles p ON u.id = p.user_id\nWHERE p.user_id IS NULL;\n",
        "test_cases": [
            {"input_data": "SELECT COUNT(*) FROM Users;", "expected_output": "5", "is_hidden": False, "weight": 1.0},
        ]
    },
    {
        "title": "Department Average Salary Comparison",
        "description": "Write a SQL query to list all employees who earn strictly more than the average salary of their respective department.",
        "constraints": "Schema: Employees (emp_id INT, dept_id INT, salary NUMERIC)",
        "difficulty": "MEDIUM",
        "field": "SQL",
        "marks": 15.0,
        "language": "sql",
        "category": AssessmentCategory.CODING.value,
        "problem_type": "SQL",
        "schema_ddl": "CREATE TABLE Employees (emp_id INT PRIMARY KEY, dept_id INT, salary NUMERIC(10,2));",
        "starter_code_json": {
            "sql": "-- Find employees earning more than department average\nSELECT emp_id, salary\nFROM Employees e;\n"
        },
        "reference_solution": "SELECT e.emp_id, e.salary\nFROM Employees e\nWHERE e.salary > (\n    SELECT AVG(d.salary)\n    FROM Employees d\n    WHERE d.dept_id = e.dept_id\n);\n",
        "test_cases": [
            {"input_data": "SELECT COUNT(*) FROM Employees;", "expected_output": "8", "is_hidden": False, "weight": 1.0},
        ]
    },

    # =========================================================================
    # JAVA (4 Problems)
    # =========================================================================
    {
        "title": "Reverse a Singly Linked List",
        "description": "Given the head of a singly linked list, reverse the list, and return the reversed list head.",
        "constraints": "The number of nodes in the list is the range [0, 5000].\n-5000 <= Node.val <= 5000",
        "difficulty": "EASY",
        "field": "Java",
        "marks": 10.0,
        "language": "java",
        "category": AssessmentCategory.CODING.value,
        "problem_type": "CODING",
        "starter_code_json": {
            "java": "public class Solution {\n    public ListNode reverseList(ListNode head) {\n        // Implement in-place reversal\n        return null;\n    }\n}\n"
        },
        "reference_solution": "public class Solution {\n    public ListNode reverseList(ListNode head) {\n        ListNode prev = null;\n        ListNode curr = head;\n        while (curr != null) {\n            ListNode nextTemp = curr.next;\n            curr.next = prev;\n            prev = curr;\n            curr = nextTemp;\n        }\n        return prev;\n    }\n}\n",
        "test_cases": [
            {"input_data": "[1,2,3,4,5]", "expected_output": "[5,4,3,2,1]", "is_hidden": False, "weight": 1.0},
            {"input_data": "[1,2]", "expected_output": "[2,1]", "is_hidden": True, "weight": 1.0},
        ]
    },
    {
        "title": "Valid Palindrome with Alphanumeric Filter",
        "description": "A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward.",
        "constraints": "1 <= s.length() <= 2 * 10^5\ns consists only of printable ASCII characters.",
        "difficulty": "EASY",
        "field": "Java",
        "marks": 10.0,
        "language": "java",
        "category": AssessmentCategory.CODING.value,
        "problem_type": "CODING",
        "starter_code_json": {
            "java": "public class Solution {\n    public boolean isPalindrome(String s) {\n        // Your implementation here\n        return false;\n    }\n}\n"
        },
        "reference_solution": "public class Solution {\n    public boolean isPalindrome(String s) {\n        int i = 0, j = s.length() - 1;\n        while (i < j) {\n            while (i < j && !Character.isLetterOrDigit(s.charAt(i))) i++;\n            while (i < j && !Character.isLetterOrDigit(s.charAt(j))) j--;\n            if (Character.toLowerCase(s.charAt(i)) != Character.toLowerCase(s.charAt(j))) return false;\n            i++; j--;\n        }\n        return true;\n    }\n}\n",
        "test_cases": [
            {"input_data": "\"A man, a plan, a canal: Panama\"", "expected_output": "true", "is_hidden": False, "weight": 1.0},
            {"input_data": "\"race a car\"", "expected_output": "false", "is_hidden": True, "weight": 1.0},
        ]
    },
    {
        "title": "Binary Tree Level Order Traversal",
        "description": "Given the root of a binary tree, return the level order traversal of its nodes' values. (i.e., from left to right, level by level).",
        "constraints": "The number of nodes in the tree is in the range [0, 2000].\n-1000 <= Node.val <= 1000",
        "difficulty": "MEDIUM",
        "field": "Java",
        "marks": 15.0,
        "language": "java",
        "category": AssessmentCategory.CODING.value,
        "problem_type": "CODING",
        "starter_code_json": {
            "java": "import java.util.*;\npublic class Solution {\n    public List<List<Integer>> levelOrder(TreeNode root) {\n        // Breadth-First Search\n        return new ArrayList<>();\n    }\n}\n"
        },
        "reference_solution": "import java.util.*;\npublic class Solution {\n    public List<List<Integer>> levelOrder(TreeNode root) {\n        List<List<Integer>> res = new ArrayList<>();\n        if (root == null) return res;\n        Queue<TreeNode> q = new LinkedList<>();\n        q.add(root);\n        while (!q.isEmpty()) {\n            int size = q.size();\n            List<Integer> level = new ArrayList<>();\n            for (int i = 0; i < size; i++) {\n                TreeNode node = q.poll();\n                level.add(node.val);\n                if (node.left != null) q.add(node.left);\n                if (node.right != null) q.add(node.right);\n            }\n            res.add(level);\n        }\n        return res;\n    }\n}\n",
        "test_cases": [
            {"input_data": "[3,9,20,null,null,15,7]", "expected_output": "[[3],[9,20],[15,7]]", "is_hidden": False, "weight": 1.0},
        ]
    },
    {
        "title": "Thread-Safe Bounded Blocking Queue",
        "description": "Implement a thread-safe BoundedBlockingQueue with enqueue() and dequeue() methods using wait() and notifyAll() or ReentrantLock.",
        "constraints": "capacity > 0\nAll operations must block appropriately when queue is full or empty.",
        "difficulty": "HARD",
        "field": "Java",
        "marks": 20.0,
        "language": "java",
        "category": AssessmentCategory.CODING.value,
        "problem_type": "CODING",
        "starter_code_json": {
            "java": "public class BoundedBlockingQueue {\n    public BoundedBlockingQueue(int capacity) {}\n    public synchronized void enqueue(int element) throws InterruptedException {}\n    public synchronized int dequeue() throws InterruptedException { return 0; }\n    public synchronized int size() { return 0; }\n}\n"
        },
        "reference_solution": "import java.util.LinkedList;\nimport java.util.Queue;\n\npublic class BoundedBlockingQueue {\n    private final Queue<Integer> queue = new LinkedList<>();\n    private final int capacity;\n\n    public BoundedBlockingQueue(int capacity) {\n        this.capacity = capacity;\n    }\n\n    public synchronized void enqueue(int element) throws InterruptedException {\n        while (queue.size() == capacity) {\n            wait();\n        }\n        queue.add(element);\n        notifyAll();\n    }\n\n    public synchronized int dequeue() throws InterruptedException {\n        while (queue.isEmpty()) {\n            wait();\n        }\n        int val = queue.poll();\n        notifyAll();\n        return val;\n    }\n\n    public synchronized int size() {\n        return queue.size();\n    }\n}\n",
        "test_cases": [
            {"input_data": "capacity: 2, enqueue(1), enqueue(2), dequeue()", "expected_output": "1", "is_hidden": False, "weight": 1.0},
        ]
    },

    # =========================================================================
    # JAVASCRIPT (4 Problems)
    # =========================================================================
    {
        "title": "Debounce Function Implementation",
        "description": "Given a function fn and a time in milliseconds t, return a debounced version of that function. A debounced function is a function whose execution is delayed by t milliseconds and whose execution is cancelled if it is called again within that window.",
        "constraints": "0 <= t <= 1000\nCalls: at most 500",
        "difficulty": "MEDIUM",
        "field": "JavaScript",
        "marks": 15.0,
        "language": "javascript",
        "category": AssessmentCategory.CODING.value,
        "problem_type": "CODING",
        "starter_code_json": {
            "javascript": "function debounce(fn, t) {\n    // Return debounced closure\n    return function(...args) {};\n}\n"
        },
        "reference_solution": "function debounce(fn, t) {\n    let timerId;\n    return function(...args) {\n        clearTimeout(timerId);\n        timerId = setTimeout(() => fn.apply(this, args), t);\n    };\n}\n",
        "test_cases": [
            {"input_data": "t = 50, calls at 20ms, 50ms, 75ms", "expected_output": "fn executed once at 125ms", "is_hidden": False, "weight": 1.0},
        ]
    },
    {
        "title": "Flatten Deeply Nested Array",
        "description": "Given a multi-dimensional array arr and a depth n, return a flattened version of that array up to depth n without using Array.prototype.flat.",
        "constraints": "0 <= count of elements <= 10^5\n0 <= n <= 1000",
        "difficulty": "MEDIUM",
        "field": "JavaScript",
        "marks": 15.0,
        "language": "javascript",
        "category": AssessmentCategory.CODING.value,
        "problem_type": "CODING",
        "starter_code_json": {
            "javascript": "function flat(arr, n) {\n    // Custom recursive flattening\n    return [];\n}\n"
        },
        "reference_solution": "function flat(arr, n) {\n    if (n <= 0) return arr.slice();\n    const res = [];\n    for (const item of arr) {\n        if (Array.isArray(item)) {\n            res.push(...flat(item, n - 1));\n        } else {\n            res.push(item);\n        }\n    }\n    return res;\n}\n",
        "test_cases": [
            {"input_data": "[1, 2, 3, [4, 5, 6], [7, 8, [9, 10, 11], 12], [13, 14, 15]], n = 1", "expected_output": "[1, 2, 3, 4, 5, 6, 7, 8, [9, 10, 11], 12, 13, 14, 15]", "is_hidden": False, "weight": 1.0},
        ]
    },
    {
        "title": "Custom Promise.all Polyfill",
        "description": "Implement a custom promiseAll function that takes an array of promises and returns a single promise that resolves to an array of results or rejects on the first rejection.",
        "constraints": "Array contains 0 to 100 promises or non-promise values.",
        "difficulty": "HARD",
        "field": "JavaScript",
        "marks": 20.0,
        "language": "javascript",
        "category": AssessmentCategory.CODING.value,
        "problem_type": "CODING",
        "starter_code_json": {
            "javascript": "function promiseAll(functions) {\n    // Return custom Promise resolving all items\n    return new Promise((resolve, reject) => {});\n}\n"
        },
        "reference_solution": "function promiseAll(functions) {\n    return new Promise((resolve, reject) => {\n        if (functions.length === 0) return resolve([]);\n        const results = new Array(functions.length);\n        let resolvedCount = 0;\n        functions.forEach((fn, i) => {\n            Promise.resolve(typeof fn === 'function' ? fn() : fn)\n                .then(val => {\n                    results[i] = val;\n                    resolvedCount++;\n                    if (resolvedCount === functions.length) resolve(results);\n                })\n                .catch(reject);\n        });\n    });\n}\n",
        "test_cases": [
            {"input_data": "[() => new Promise(res => res(42)), () => new Promise(res => res('hello'))]", "expected_output": "[42, 'hello']", "is_hidden": False, "weight": 1.0},
        ]
    },
    {
        "title": "Deep Clone with Circular References",
        "description": "Implement a deepClone function in JavaScript that correctly handles nested objects, arrays, Dates, RegExps, and circular references.",
        "constraints": "Objects may contain circular references back to ancestors.",
        "difficulty": "HARD",
        "field": "JavaScript",
        "marks": 20.0,
        "language": "javascript",
        "category": AssessmentCategory.CODING.value,
        "problem_type": "CODING",
        "starter_code_json": {
            "javascript": "function deepClone(obj, hash = new WeakMap()) {\n    // Implement deep copy\n    return obj;\n}\n"
        },
        "reference_solution": "function deepClone(obj, hash = new WeakMap()) {\n    if (obj === null || typeof obj !== 'object') return obj;\n    if (obj instanceof Date) return new Date(obj);\n    if (obj instanceof RegExp) return new RegExp(obj);\n    if (hash.has(obj)) return hash.get(obj);\n    const copy = Array.isArray(obj) ? [] : Object.create(Object.getPrototypeOf(obj));\n    hash.set(obj, copy);\n    for (const key of Reflect.ownKeys(obj)) {\n        copy[key] = deepClone(obj[key], hash);\n    }\n    return copy;\n}\n",
        "test_cases": [
            {"input_data": "{ a: 1, b: { c: 2 } }", "expected_output": "{ a: 1, b: { c: 2 } }", "is_hidden": False, "weight": 1.0},
        ]
    },

    # =========================================================================
    # C++ (4 Problems)
    # =========================================================================
    {
        "title": "Custom Unique_Ptr Implementation",
        "description": "Implement a simplified RAII smart pointer class template MyUniquePtr<T> with move semantics and disabled copy semantics.",
        "constraints": "Must automatically free dynamically allocated heap memory on scope exit.",
        "difficulty": "MEDIUM",
        "field": "C++",
        "marks": 15.0,
        "language": "cpp",
        "category": AssessmentCategory.CODING.value,
        "problem_type": "CODING",
        "starter_code_json": {
            "cpp": "template <typename T>\nclass MyUniquePtr {\n    T* ptr;\npublic:\n    explicit MyUniquePtr(T* p = nullptr) : ptr(p) {}\n    ~MyUniquePtr() { delete ptr; }\n    // Implement move constructor and move assignment\n};\n"
        },
        "reference_solution": "template <typename T>\nclass MyUniquePtr {\n    T* ptr;\npublic:\n    explicit MyUniquePtr(T* p = nullptr) : ptr(p) {}\n    ~MyUniquePtr() { delete ptr; }\n    MyUniquePtr(const MyUniquePtr&) = delete;\n    MyUniquePtr& operator=(const MyUniquePtr&) = delete;\n    MyUniquePtr(MyUniquePtr&& other) noexcept : ptr(other.ptr) { other.ptr = nullptr; }\n    MyUniquePtr& operator=(MyUniquePtr&& other) noexcept {\n        if (this != &other) {\n            delete ptr;\n            ptr = other.ptr;\n            other.ptr = nullptr;\n        }\n        return *this;\n    }\n    T& operator*() const { return *ptr; }\n    T* operator->() const { return ptr; }\n    T* get() const { return ptr; }\n};\n",
        "test_cases": [
            {"input_data": "MyUniquePtr<int> p(new int(10)); *p;", "expected_output": "10", "is_hidden": False, "weight": 1.0},
        ]
    },
    {
        "title": "Fast String Tokenizer via String_View",
        "description": "Implement an allocation-free string tokenizer split(std::string_view str, char delimiter) returning std::vector<std::string_view>.",
        "constraints": "Zero heap allocations for substring segments.",
        "difficulty": "MEDIUM",
        "field": "C++",
        "marks": 15.0,
        "language": "cpp",
        "category": AssessmentCategory.CODING.value,
        "problem_type": "CODING",
        "starter_code_json": {
            "cpp": "#include <string_view>\n#include <vector>\n\nstd::vector<std::string_view> split(std::string_view str, char delim) {\n    std::vector<std::string_view> tokens;\n    // Implement non-allocating split\n    return tokens;\n}\n"
        },
        "reference_solution": "#include <string_view>\n#include <vector>\n\nstd::vector<std::string_view> split(std::string_view str, char delim) {\n    std::vector<std::string_view> tokens;\n    size_t start = 0;\n    while (start < str.size()) {\n        size_t end = str.find(delim, start);\n        if (end == std::string_view::npos) {\n            tokens.push_back(str.substr(start));\n            break;\n        }\n        tokens.push_back(str.substr(start, end - start));\n        start = end + 1;\n    }\n    return tokens;\n}\n",
        "test_cases": [
            {"input_data": "\"alpha,beta,gamma\", ','", "expected_output": "[\"alpha\", \"beta\", \"gamma\"]", "is_hidden": False, "weight": 1.0},
        ]
    },
    {
        "title": "Lock-Free Ring Buffer (Single Producer Single Consumer)",
        "description": "Implement a fixed-size lock-free ring buffer for SPSC concurrency using std::atomic<size_t> with memory_order_acquire / release.",
        "constraints": "Buffer capacity must be a power of two.",
        "difficulty": "HARD",
        "field": "C++",
        "marks": 20.0,
        "language": "cpp",
        "category": AssessmentCategory.CODING.value,
        "problem_type": "CODING",
        "starter_code_json": {
            "cpp": "#include <atomic>\n#include <vector>\n\ntemplate <typename T, size_t Capacity>\nclass SpscRingBuffer {\n    // Single Producer Single Consumer\n};\n"
        },
        "reference_solution": "#include <atomic>\n#include <array>\n\ntemplate <typename T, size_t Capacity>\nclass SpscRingBuffer {\n    static_assert((Capacity & (Capacity - 1)) == 0, \"Capacity must be power of two\");\n    std::array<T, Capacity> buffer;\n    alignas(64) std::atomic<size_t> head{0};\n    alignas(64) std::atomic<size_t> tail{0};\npublic:\n    bool push(const T& val) {\n        size_t current_tail = tail.load(std::memory_order_relaxed);\n        if (current_tail - head.load(std::memory_order_acquire) == Capacity) return false;\n        buffer[current_tail & (Capacity - 1)] = val;\n        tail.store(current_tail + 1, std::memory_order_release);\n        return true;\n    }\n    bool pop(T& val) {\n        size_t current_head = head.load(std::memory_order_relaxed);\n        if (current_head == tail.load(std::memory_order_acquire)) return false;\n        val = buffer[current_head & (Capacity - 1)];\n        head.store(current_head + 1, std::memory_order_release);\n        return true;\n    }\n};\n",
        "test_cases": [
            {"input_data": "push(10), push(20), pop()", "expected_output": "10", "is_hidden": False, "weight": 1.0},
        ]
    },
    {
        "title": "Compile-Time Fibonacci with C++20 Constexpr",
        "description": "Implement a constexpr/consteval function fibonacci(int n) that computes the nth Fibonacci number at compile-time with O(N) evaluation.",
        "constraints": "0 <= n <= 45",
        "difficulty": "EASY",
        "field": "C++",
        "marks": 10.0,
        "language": "cpp",
        "category": AssessmentCategory.CODING.value,
        "problem_type": "CODING",
        "starter_code_json": {
            "cpp": "constexpr long long fibonacci(int n) {\n    // Compute at compile time\n    return 0;\n}\n"
        },
        "reference_solution": "constexpr long long fibonacci(int n) {\n    if (n <= 1) return n;\n    long long a = 0, b = 1;\n    for (int i = 2; i <= n; ++i) {\n        long long c = a + b;\n        a = b;\n        b = c;\n    }\n    return b;\n}\n",
        "test_cases": [
            {"input_data": "n = 10", "expected_output": "55", "is_hidden": False, "weight": 1.0},
            {"input_data": "n = 20", "expected_output": "6765", "is_hidden": True, "weight": 1.0},
        ]
    }
]
