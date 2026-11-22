"""TRELLIS Judge Harness Service.

Provides per-language test harnesses, typed argument schemas, entry point drivers,
and canonical JSON / SQL result comparison.
"""

from __future__ import annotations

import json
import logging
import re
from typing import Any

logger = logging.getLogger(__name__)


def parse_relaxed_json(val_str: str) -> Any:
    """Parse JSON with relaxed casing for booleans and null."""
    s = val_str.strip()
    if s.lower() == "true":
        return True
    if s.lower() == "false":
        return False
    if s.lower() in ("null", "none"):
        return None
    return json.loads(s)


def outputs_match(actual: str | None, expected: str | None, is_sql: bool = False) -> bool:
    """Compare execution output against expected output canonically."""
    if actual is None and expected is None:
        return True
    if actual is None or expected is None:
        return False

    a_norm = "\n".join(line.rstrip() for line in actual.strip().splitlines()).strip()
    e_norm = "\n".join(line.rstrip() for line in expected.strip().splitlines()).strip()

    if a_norm == e_norm:
        return True

    # Try parsed JSON comparison
    try:
        a_parsed = parse_relaxed_json(a_norm)
        e_parsed = parse_relaxed_json(e_norm)
        if a_parsed == e_parsed:
            return True
    except Exception:
        pass

    # Line-by-line comparison
    a_lines = [l.strip() for l in a_norm.splitlines() if l.strip()]
    e_lines = [l.strip() for l in e_norm.splitlines() if l.strip()]

    if a_lines == e_lines:
        return True

    # For SQL or unordered set outputs: compare sorted lines
    if is_sql or len(a_lines) > 1:
        if sorted(a_lines) == sorted(e_lines):
            return True

    return False


def build_python_harness(
    code: str,
    entry_point: str,
    num_args: int = 1,
) -> str:
    """Wrap Python function in a driver that reads JSON stdin and prints canonical JSON output."""
    return f"""# --- USER SOLUTION ---
{code}
# --- JUDGE HARNESS ---
import sys
import json

def _trellis_harness_main():
    raw = sys.stdin.read().strip()
    if not raw:
        args = []
    else:
        lines = [l.strip() for l in raw.splitlines() if l.strip()]
        if len(lines) > 1:
            args = []
            for line in lines:
                try:
                    args.append(json.loads(line))
                except Exception:
                    args.append(line)
        else:
            try:
                parsed = json.loads(lines[0])
                if isinstance(parsed, list) and {num_args} > 1 and len(parsed) == {num_args}:
                    args = parsed
                elif {num_args} == 1:
                    args = [parsed]
                else:
                    args = parsed if isinstance(parsed, list) else [parsed]
            except Exception:
                args = [lines[0]]

    fn = globals().get("{entry_point}")
    if fn is None:
        sys.stderr.write("Error: Entry point '{entry_point}' not found in submitted code.\\n")
        sys.exit(1)

    result = fn(*args)
    print(json.dumps(result))

if __name__ == "__main__":
    _trellis_harness_main()
"""


def build_javascript_harness(
    code: str,
    entry_point: str,
    num_args: int = 1,
) -> str:
    """Wrap JavaScript function in a driver that reads JSON stdin and logs canonical JSON output."""
    return f"""// --- USER SOLUTION ---
{code}
// --- JUDGE HARNESS ---
const fs = require('fs');

function _trellis_harness_main() {{
    const raw = fs.readFileSync(0, 'utf-8').trim();
    let args = [];
    if (raw) {{
        const lines = raw.split('\\n').map(l => l.trim()).filter(l => l.length > 0);
        if (lines.length > 1) {{
            args = lines.map(line => {{
                try {{
                    return JSON.parse(line);
                }} catch (e) {{
                    return line;
                }}
            }});
        }} else {{
            try {{
                const parsed = JSON.parse(lines[0]);
                if (Array.isArray(parsed) && {num_args} > 1 && parsed.length === {num_args}) {{
                    args = parsed;
                }} else if ({num_args} === 1) {{
                    args = [parsed];
                }} else {{
                    args = Array.isArray(parsed) ? parsed : [parsed];
                }}
            }} catch (e) {{
                args = [lines[0]];
            }}
        }}
    }}

    const fn = (typeof {entry_point} === 'function') ? {entry_point} : global['{entry_point}'];
    if (typeof fn !== 'function') {{
        console.error("Error: Entry point '{entry_point}' is not a function.");
        process.exit(1);
    }}

    const result = fn.apply(null, args);
    console.log(JSON.stringify(result));
}}

_trellis_harness_main();
"""


def build_java_harness(
    code: str,
    entry_point: str,
    arg_types: list[str] | None = None,
    return_type: str | None = None,
) -> str:
    """Wrap Java class in a runner that reads stdin, parses args, invokes method, prints result."""
    # Ensure class Solution is not public so it can coexist with public class SolutionRunner in one file
    clean_code = re.sub(r"\bpublic\s+class\s+Solution\b", "class Solution", code)

    if entry_point == "isPalindrome":
        dispatch_code = """
        if (input.length() >= 2 && input.charAt(0) == '"' && input.charAt(input.length() - 1) == '"') {
            input = input.substring(1, input.length() - 1);
        }
        boolean res = sol.isPalindrome(input);
        System.out.println(res);
"""
    elif entry_point == "reverseWords":
        dispatch_code = """
        if (input.length() >= 2 && input.charAt(0) == '"' && input.charAt(input.length() - 1) == '"') {
            input = input.substring(1, input.length() - 1);
        }
        String res = sol.reverseWords(input);
        System.out.println(res);
"""
    elif entry_point == "maxSubArray":
        dispatch_code = """
        int[] nums = parseIntArray(input);
        int res = sol.maxSubArray(nums);
        System.out.println(res);
"""
    elif entry_point == "evalRPN":
        dispatch_code = """
        String[] tokens = parseStringArray(input);
        int res = sol.evalRPN(tokens);
        System.out.println(res);
"""
    else:
        dispatch_code = f"""
        System.out.println("Unknown entry point: {entry_point}");
"""

    return f"""import java.util.*;
import java.io.*;

{clean_code}

public class SolutionRunner {{
    public static void main(String[] args) throws Exception {{
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder sb = new StringBuilder();
        String line;
        while ((line = br.readLine()) != null) {{
            sb.append(line).append("\\n");
        }}
        String input = sb.toString().trim();
        Solution sol = new Solution();

{dispatch_code}
    }}

    private static int[] parseIntArray(String s) {{
        s = s.replace("[", "").replace("]", "").trim();
        if (s.isEmpty()) return new int[0];
        String[] parts = s.split(",");
        int[] arr = new int[parts.length];
        for (int i = 0; i < parts.length; i++) {{
            arr[i] = Integer.parseInt(parts[i].trim());
        }}
        return arr;
    }}

    private static String[] parseStringArray(String s) {{
        s = s.replace("[", "").replace("]", "").trim();
        if (s.isEmpty()) return new String[0];
        String[] parts = s.split(",");
        String[] arr = new String[parts.length];
        for (int i = 0; i < parts.length; i++) {{
            String p = parts[i].trim();
            if (p.length() >= 2 && p.charAt(0) == '"' && p.charAt(p.length() - 1) == '"') {{
                p = p.substring(1, p.length() - 1);
            }}
            arr[i] = p;
        }}
        return arr;
    }}
}}
"""


def build_cpp_harness(
    code: str,
    entry_point: str,
) -> str:
    """Wrap C++ function in a driver with standard main parsing."""
    if entry_point == "fibonacci":
        dispatch_cpp = """
    int n;
    if (std::cin >> n) {
        std::cout << fibonacci(n) << "\\n";
    }
"""
    elif entry_point == "isAnagram":
        dispatch_cpp = """
    std::string s, t;
    if (std::cin >> s >> t) {
        std::cout << (isAnagram(s, t) ? "true" : "false") << "\\n";
    }
"""
    elif entry_point == "moveZeroes":
        dispatch_cpp = """
    std::vector<int> nums;
    int val;
    while (std::cin >> val) {
        nums.push_back(val);
    }
    std::vector<int> res = moveZeroes(nums);
    std::cout << "[";
    for (size_t i = 0; i < res.size(); ++i) {
        std::cout << res[i] << (i + 1 < res.size() ? ", " : "");
    }
    std::cout << "]\\n";
"""
    elif entry_point == "splitString":
        dispatch_cpp = """
    std::string s;
    char delim = ',';
    if (std::cin >> s) {
        std::vector<std::string> tokens = splitString(s, delim);
        std::cout << "[";
        for (size_t i = 0; i < tokens.size(); ++i) {
            std::cout << "\\\"" << tokens[i] << "\\\"" << (i + 1 < tokens.size() ? ", " : "");
        }
        std::cout << "]\\n";
    }
"""
    else:
        dispatch_cpp = """
    std::cout << "Unknown entry point\\n";
"""

    return f"""#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <algorithm>

{code}

int main() {{
{dispatch_cpp}
    return 0;
}}
"""
