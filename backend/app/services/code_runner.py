"""TRELLIS Sandboxed Code Runner Service Interface (Step 5 & Security Hardening).

Executes user code (Python, Java, JavaScript, C++, C) in an isolated,
resource-constrained environment:
1. BaseCodeRunner interface with isolated implementations:
   - Judge0Runner: Remote isolated Judge0 execution engine.
   - DockerRunner: Local isolated containerized execution with --network none,
     read-only filesystem, resource caps, and non-root execution.
   - LocalSubprocessRunner (dev-only): Strictly isolated subprocess with env={},
     temp directory, resource.setrlimit (POSIX), memory tracking, and output size caps.
2. Output comparison rule: Trims trailing whitespace per line.
3. No simulated execution: Missing compilers or runtimes return RUNNER_UNAVAILABLE, never ACCEPTED.
"""

from __future__ import annotations

import json
import logging
import os
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from app.core.config import settings

logger = logging.getLogger(__name__)

# Check if POSIX resource module is available
try:
    import resource  # type: ignore[import-not-found]
except ImportError:
    resource = None  # type: ignore[assignment]


@dataclass
class TestCaseResult:
    case_index: int
    is_hidden: bool
    verdict: str | None  # ACCEPTED, WRONG_ANSWER, RUNTIME_ERROR, TIME_LIMIT_EXCEEDED, MEMORY_LIMIT_EXCEEDED, COMPILATION_ERROR, RUNNER_UNAVAILABLE, or None (custom run)
    input_data: str
    expected_output: str
    actual_output: str
    runtime_ms: float
    memory_mb: float
    error_message: str | None = None
    is_custom: bool = False


@dataclass
class ExecutionResult:
    verdict: str | None  # ACCEPTED, WRONG_ANSWER, RUNTIME_ERROR, TIME_LIMIT_EXCEEDED, MEMORY_LIMIT_EXCEEDED, COMPILATION_ERROR, RUNNER_UNAVAILABLE, or None (custom run)
    passed_cases: int
    total_cases: int
    runtime_ms: float
    memory_mb: float
    score: float
    case_results: list[TestCaseResult] = field(default_factory=list)
    compile_error: str | None = None
    first_failing_case: dict[str, Any] | None = None
    custom_output: str | None = None


def normalize_output(text: str | None) -> str:
    """Trim trailing whitespace per line and strip outer whitespace."""
    if text is None:
        return ""
    lines = [line.rstrip() for line in text.strip().splitlines()]
    return "\n".join(lines).strip()


class BaseCodeRunner(ABC):
    """Abstract interface for sandboxed code execution engines."""

    MAX_OUTPUT_BYTES = 64 * 1024  # 64 KB stdout/stderr cap

    @abstractmethod
    def execute(
        self,
        code: str,
        language: str,
        test_cases: list[dict[str, Any]],
        time_limit_ms: int = 3000,
        memory_limit_mb: int = 256,
        mask_hidden_inputs: bool = False,
        is_custom_run: bool = False,
    ) -> ExecutionResult:
        """Execute source code against test cases within resource constraints."""
        pass


class Judge0Runner(BaseCodeRunner):
    """Production isolated execution via self-hosted or cloud Judge0 instance."""

    LANGUAGE_MAP = {
        "python": 71,  # Python (3.8.1 / 3.11)
        "py": 71,
        "python3": 71,
        "javascript": 63,  # JavaScript (Node.js 12.14.0+)
        "js": 63,
        "node": 63,
        "java": 62,  # Java (OpenJDK 13/21)
        "c": 50,  # C (GCC 9.2.0)
        "cpp": 54,  # C++ (GCC 9.2.0)
        "c++": 54,
    }

    def __init__(self, base_url: str | None = None, api_key: str | None = None):
        self.base_url = (base_url or settings.JUDGE0_URL).rstrip("/")
        self.api_key = api_key or settings.JUDGE0_API_KEY

    def execute(
        self,
        code: str,
        language: str,
        test_cases: list[dict[str, Any]],
        time_limit_ms: int = 3000,
        memory_limit_mb: int = 256,
        mask_hidden_inputs: bool = False,
        is_custom_run: bool = False,
    ) -> ExecutionResult:
        lang = language.lower().strip()
        lang_id = self.LANGUAGE_MAP.get(lang)
        if not lang_id:
            return ExecutionResult(
                verdict="COMPILATION_ERROR",
                passed_cases=0,
                total_cases=len(test_cases),
                runtime_ms=0,
                memory_mb=0,
                score=0,
                compile_error=f"Unsupported language '{language}' in Judge0 runner.",
            )

        timeout_sec = max(0.5, time_limit_ms / 1000.0)
        case_results: list[TestCaseResult] = []
        passed_count = 0
        total_weight = sum(float(tc.get("weight", 1.0)) for tc in test_cases) or 1.0
        earned_weight = 0.0
        max_runtime = 0.0
        max_memory = 0.0
        overall_verdict = "ACCEPTED" if not is_custom_run else None
        first_fail = None
        custom_out = None

        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["X-Auth-Token"] = self.api_key

        for idx, tc in enumerate(test_cases):
            input_text = str(tc.get("input_data", "")).strip()
            expected_text = str(tc.get("expected_output", "")).strip()
            is_hidden = bool(tc.get("is_hidden", False))
            is_custom = bool(tc.get("is_custom", False)) or is_custom_run
            weight = float(tc.get("weight", 1.0))

            payload = {
                "source_code": code,
                "language_id": lang_id,
                "stdin": input_text,
                "expected_output": expected_text if not is_custom else None,
                "cpu_time_limit": timeout_sec,
                "memory_limit": memory_limit_mb * 1024,  # KB
            }

            try:
                req = urllib.request.Request(
                    f"{self.base_url}/submissions?base64_encoded=false&wait=true",
                    data=json.dumps(payload).encode("utf-8"),
                    headers=headers,
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=timeout_sec + 5.0) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
            except (urllib.error.URLError, TimeoutError, OSError) as e:
                logger.error("Judge0 connection failed: %s", e)
                return ExecutionResult(
                    verdict="RUNNER_UNAVAILABLE",
                    passed_cases=0,
                    total_cases=len(test_cases),
                    runtime_ms=0,
                    memory_mb=0,
                    score=0,
                    compile_error=f"Judge0 code runner unavailable at {self.base_url}: {e}",
                )

            # Parse Judge0 status
            status_id = data.get("status", {}).get("id", 0)
            actual_stdout = (data.get("stdout") or "")[: self.MAX_OUTPUT_BYTES]
            actual_stderr = (data.get("stderr") or "")[: self.MAX_OUTPUT_BYTES]
            compile_output = data.get("compile_output") or ""
            runtime_ms = float(data.get("time") or 0.0) * 1000.0
            memory_mb = float(data.get("memory") or 0.0) / 1024.0

            max_runtime = max(max_runtime, runtime_ms)
            max_memory = max(max_memory, memory_mb)

            if is_custom:
                verdict = None
                custom_out = actual_stdout
                err = actual_stderr or None
            elif status_id == 3:  # Accepted
                actual_norm = normalize_output(actual_stdout)
                expected_norm = normalize_output(expected_text)
                if actual_norm == expected_norm:
                    verdict = "ACCEPTED"
                    passed_count += 1
                    earned_weight += weight
                    err = None
                else:
                    verdict = "WRONG_ANSWER"
                    err = None
            elif status_id == 4:  # Wrong Answer
                verdict = "WRONG_ANSWER"
                err = None
            elif status_id == 5:  # Time Limit Exceeded
                verdict = "TIME_LIMIT_EXCEEDED"
                err = "Time limit exceeded"
            elif status_id == 6:  # Compilation Error
                return ExecutionResult(
                    verdict="COMPILATION_ERROR",
                    passed_cases=0,
                    total_cases=len(test_cases),
                    runtime_ms=0,
                    memory_mb=0,
                    score=0,
                    compile_error=compile_output or actual_stderr,
                )
            elif status_id in {7, 8, 9, 10, 11, 12}:  # Runtime Errors
                verdict = "RUNTIME_ERROR"
                err = actual_stderr or "Runtime error"
            elif status_id == 13:  # Memory Limit Exceeded / Internal Error
                verdict = "MEMORY_LIMIT_EXCEEDED" if memory_mb >= memory_limit_mb else "RUNTIME_ERROR"
                err = "Memory limit exceeded" if verdict == "MEMORY_LIMIT_EXCEEDED" else "Internal error"
            else:
                verdict = "RUNTIME_ERROR"
                err = actual_stderr or "Execution failed"

            if not is_custom and verdict != "ACCEPTED" and overall_verdict == "ACCEPTED":
                overall_verdict = verdict

            display_input = "[HIDDEN TEST CASE INPUT]" if (is_hidden and mask_hidden_inputs) else input_text
            display_expected = "[HIDDEN EXPECTED OUTPUT]" if (is_hidden and mask_hidden_inputs) else expected_text
            display_actual = "[HIDDEN ACTUAL OUTPUT]" if (is_hidden and mask_hidden_inputs) else actual_stdout

            case_res = TestCaseResult(
                case_index=idx + 1,
                is_hidden=is_hidden,
                verdict=verdict,
                input_data=display_input,
                expected_output=display_expected,
                actual_output=display_actual,
                runtime_ms=round(runtime_ms, 2),
                memory_mb=round(memory_mb, 2),
                error_message=err,
                is_custom=is_custom,
            )
            case_results.append(case_res)

            if not is_custom and verdict != "ACCEPTED" and first_fail is None:
                first_fail = {
                    "case_index": idx + 1,
                    "is_hidden": is_hidden,
                    "verdict": verdict,
                    "input": display_input,
                    "expected": display_expected,
                    "actual": display_actual,
                    "error": err,
                }

        final_score = (earned_weight / total_weight) * 100.0 if not is_custom_run else 0.0

        return ExecutionResult(
            verdict=overall_verdict,
            passed_cases=passed_count,
            total_cases=len(test_cases),
            runtime_ms=round(max_runtime, 2),
            memory_mb=round(max_memory, 2),
            score=round(final_score, 2),
            case_results=case_results,
            first_failing_case=first_fail,
            custom_output=custom_out,
        )


class DockerRunner(BaseCodeRunner):
    """Production isolated execution via docker containers with strict security constraints."""

    IMAGE_MAP = {
        "python": "python:3.11-alpine",
        "py": "python:3.11-alpine",
        "python3": "python:3.11-alpine",
        "javascript": "node:20-alpine",
        "js": "node:20-alpine",
        "node": "node:20-alpine",
        "java": "eclipse-temurin:21-alpine",
        "c": "gcc:13-alpine",
        "cpp": "gcc:13-alpine",
        "c++": "gcc:13-alpine",
    }

    def execute(
        self,
        code: str,
        language: str,
        test_cases: list[dict[str, Any]],
        time_limit_ms: int = 3000,
        memory_limit_mb: int = 256,
        mask_hidden_inputs: bool = False,
        is_custom_run: bool = False,
    ) -> ExecutionResult:
        docker_bin = shutil.which("docker")
        if not docker_bin:
            return ExecutionResult(
                verdict="RUNNER_UNAVAILABLE",
                passed_cases=0,
                total_cases=len(test_cases),
                runtime_ms=0,
                memory_mb=0,
                score=0,
                compile_error="Docker runner is unavailable: 'docker' CLI not found on system path.",
            )

        lang = language.lower().strip()
        image = self.IMAGE_MAP.get(lang)
        if not image:
            return ExecutionResult(
                verdict="COMPILATION_ERROR",
                passed_cases=0,
                total_cases=len(test_cases),
                runtime_ms=0,
                memory_mb=0,
                score=0,
                compile_error=f"Unsupported language '{language}' in Docker runner.",
            )

        timeout_sec = max(0.5, time_limit_ms / 1000.0)

        with tempfile.TemporaryDirectory(prefix="trellis_docker_") as tmpdir:
            # Write code to temp file inside tmpdir
            ext_map = {"python": ".py", "py": ".py", "javascript": ".js", "js": ".js", "java": ".java", "c": ".c", "cpp": ".cpp"}
            src_name = "Solution" + ext_map.get(lang, ".py")
            src_path = os.path.join(tmpdir, src_name)
            with open(src_path, "w", encoding="utf-8") as f:
                f.write(code)

            # Build execution command inside container
            if lang in {"python", "py", "python3"}:
                inner_cmd = ["python3", f"/work/{src_name}"]
            elif lang in {"javascript", "js", "node"}:
                inner_cmd = ["node", f"/work/{src_name}"]
            elif lang in {"java"}:
                inner_cmd = ["sh", "-c", f"javac /work/{src_name} -d /tmp && java -cp /tmp Solution"]
            elif lang in {"c"}:
                inner_cmd = ["sh", "-c", f"gcc -O2 /work/{src_name} -o /tmp/sol && /tmp/sol"]
            elif lang in {"cpp", "c++"}:
                inner_cmd = ["sh", "-c", f"g++ -O2 /work/{src_name} -o /tmp/sol && /tmp/sol"]
            else:
                inner_cmd = ["python3", f"/work/{src_name}"]

            # Test execution against test cases
            case_results: list[TestCaseResult] = []
            passed_count = 0
            total_weight = sum(float(tc.get("weight", 1.0)) for tc in test_cases) or 1.0
            earned_weight = 0.0
            max_runtime = 0.0
            overall_verdict = "ACCEPTED" if not is_custom_run else None
            first_fail = None
            custom_out = None

            for idx, tc in enumerate(test_cases):
                input_text = str(tc.get("input_data", "")).strip()
                expected_text = str(tc.get("expected_output", "")).strip()
                is_hidden = bool(tc.get("is_hidden", False))
                is_custom = bool(tc.get("is_custom", False)) or is_custom_run
                weight = float(tc.get("weight", 1.0))

                docker_cmd = [
                    docker_bin,
                    "run",
                    "--rm",
                    "-i",
                    "--network",
                    "none",
                    "--memory",
                    f"{memory_limit_mb}m",
                    "--cpus",
                    "1.0",
                    "--pids-limit",
                    "64",
                    "--read-only",
                    "--tmpfs",
                    "/tmp:rw,noexec,nosuid,size=64m",
                    "-v",
                    f"{tmpdir}:/work:ro",
                    image,
                ] + inner_cmd

                start_t = time.perf_counter()
                try:
                    proc = subprocess.run(
                        docker_cmd,
                        input=input_text,
                        capture_output=True,
                        text=True,
                        timeout=timeout_sec + 2.0,
                    )
                    elapsed_ms = (time.perf_counter() - start_t) * 1000.0
                    max_runtime = max(max_runtime, elapsed_ms)
                    stdout_str = proc.stdout[: self.MAX_OUTPUT_BYTES]
                    stderr_str = proc.stderr[: self.MAX_OUTPUT_BYTES]

                    if is_custom:
                        verdict = None
                        custom_out = stdout_str
                        err = stderr_str or None
                    elif proc.returncode == 137:  # Out of memory or killed by OOM
                        verdict = "MEMORY_LIMIT_EXCEEDED"
                        err = "Memory limit exceeded (OOM killed)"
                    elif proc.returncode != 0:
                        verdict = "RUNTIME_ERROR"
                        err = stderr_str or f"Non-zero exit code ({proc.returncode})"
                    else:
                        actual_norm = normalize_output(stdout_str)
                        expected_norm = normalize_output(expected_text)
                        if actual_norm == expected_norm:
                            verdict = "ACCEPTED"
                            passed_count += 1
                            earned_weight += weight
                            err = None
                        else:
                            verdict = "WRONG_ANSWER"
                            err = None

                except subprocess.TimeoutExpired:
                    elapsed_ms = timeout_sec * 1000.0
                    max_runtime = max(max_runtime, elapsed_ms)
                    verdict = "TIME_LIMIT_EXCEEDED"
                    err = "Time limit exceeded"
                    stdout_str = ""
                except Exception as ex:
                    logger.error("Docker runner exception: %s", ex)
                    return ExecutionResult(
                        verdict="RUNNER_UNAVAILABLE",
                        passed_cases=0,
                        total_cases=len(test_cases),
                        runtime_ms=0,
                        memory_mb=0,
                        score=0,
                        compile_error=f"Docker runner error: {ex}",
                    )

                if not is_custom and verdict != "ACCEPTED" and overall_verdict == "ACCEPTED":
                    overall_verdict = verdict

                display_input = "[HIDDEN TEST CASE INPUT]" if (is_hidden and mask_hidden_inputs) else input_text
                display_expected = "[HIDDEN EXPECTED OUTPUT]" if (is_hidden and mask_hidden_inputs) else expected_text
                display_actual = "[HIDDEN ACTUAL OUTPUT]" if (is_hidden and mask_hidden_inputs) else stdout_str

                case_results.append(
                    TestCaseResult(
                        case_index=idx + 1,
                        is_hidden=is_hidden,
                        verdict=verdict,
                        input_data=display_input,
                        expected_output=display_expected,
                        actual_output=display_actual,
                        runtime_ms=round(elapsed_ms, 2),
                        memory_mb=18.0,
                        error_message=err,
                        is_custom=is_custom,
                    )
                )

                if not is_custom and verdict != "ACCEPTED" and first_fail is None:
                    first_fail = {
                        "case_index": idx + 1,
                        "is_hidden": is_hidden,
                        "verdict": verdict,
                        "input": display_input,
                        "expected": display_expected,
                        "actual": display_actual,
                        "error": err,
                    }

            final_score = (earned_weight / total_weight) * 100.0 if not is_custom_run else 0.0

            return ExecutionResult(
                verdict=overall_verdict,
                passed_cases=passed_count,
                total_cases=len(test_cases),
                runtime_ms=round(max_runtime, 2),
                memory_mb=18.0,
                score=round(final_score, 2),
                case_results=case_results,
                first_failing_case=first_fail,
                custom_output=custom_out,
            )


class LocalSubprocessRunner(BaseCodeRunner):
    """Dev-only local subprocess execution with strict isolation: env={}, temp cwd, setrlimit."""

    def __init__(self):
        logger.warning(
            "SECURITY WARNING: Running code with dev-only LocalSubprocessRunner. "
            "Never use in production (TRELLIS_ENV != dev)!"
        )

    def execute(
        self,
        code: str,
        language: str,
        test_cases: list[dict[str, Any]],
        time_limit_ms: int = 3000,
        memory_limit_mb: int = 256,
        mask_hidden_inputs: bool = False,
        is_custom_run: bool = False,
    ) -> ExecutionResult:
        lang = language.lower().strip()
        timeout_sec = max(0.5, time_limit_ms / 1000.0)

        # Dispatch execution
        if lang in {"python", "py", "python3"}:
            return self._run_python(code, test_cases, timeout_sec, memory_limit_mb, mask_hidden_inputs, is_custom_run)
        elif lang in {"javascript", "js", "node"}:
            return self._run_javascript(code, test_cases, timeout_sec, memory_limit_mb, mask_hidden_inputs, is_custom_run)
        elif lang in {"c", "c++", "cpp"}:
            return self._run_compiled_c(code, lang, test_cases, timeout_sec, memory_limit_mb, mask_hidden_inputs, is_custom_run)
        elif lang in {"java"}:
            return self._run_java(code, test_cases, timeout_sec, memory_limit_mb, mask_hidden_inputs, is_custom_run)
        else:
            return ExecutionResult(
                verdict="COMPILATION_ERROR",
                passed_cases=0,
                total_cases=len(test_cases),
                runtime_ms=0,
                memory_mb=0,
                score=0,
                compile_error=f"Unsupported language '{language}'. Supported: Python, JavaScript, Java, C, C++.",
            )

    def _get_preexec_fn(self, timeout_sec: float, memory_limit_mb: int):
        """Set POSIX process limits for CPU, memory, file size, and process count."""
        if sys.platform == "win32" or resource is None:
            return None

        def _limits():
            # CPU time limit in seconds
            cpu_limit = max(1, int(timeout_sec) + 1)
            resource.setrlimit(resource.RLIMIT_CPU, (cpu_limit, cpu_limit + 1))
            # Address space / virtual memory in bytes
            mem_bytes = memory_limit_mb * 1024 * 1024
            resource.setrlimit(resource.RLIMIT_AS, (mem_bytes, mem_bytes))
            # File size limit (max 10MB file creation)
            resource.setrlimit(resource.RLIMIT_FSIZE, (10 * 1024 * 1024, 10 * 1024 * 1024))
            # Child process creation limit
            resource.setrlimit(resource.RLIMIT_NPROC, (64, 64))

        return _limits

    def _run_python(
        self,
        code: str,
        test_cases: list[dict[str, Any]],
        timeout_sec: float,
        memory_limit_mb: int,
        mask_hidden: bool,
        is_custom_run: bool,
    ) -> ExecutionResult:
        with tempfile.TemporaryDirectory(prefix="trellis_py_") as tmpdir:
            script_path = os.path.join(tmpdir, "solution.py")
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(code)

            return self._evaluate_cases(
                cmd=[sys.executable, script_path],
                cwd=tmpdir,
                test_cases=test_cases,
                timeout_sec=timeout_sec,
                memory_limit_mb=memory_limit_mb,
                mask_hidden=mask_hidden,
                is_custom_run=is_custom_run,
            )

    def _run_javascript(
        self,
        code: str,
        test_cases: list[dict[str, Any]],
        timeout_sec: float,
        memory_limit_mb: int,
        mask_hidden: bool,
        is_custom_run: bool,
    ) -> ExecutionResult:
        node_bin = shutil.which("node")
        if not node_bin:
            return ExecutionResult(
                verdict="RUNNER_UNAVAILABLE",
                passed_cases=0,
                total_cases=len(test_cases),
                runtime_ms=0,
                memory_mb=0,
                score=0,
                compile_error="Node.js runtime not found on system path.",
            )

        with tempfile.TemporaryDirectory(prefix="trellis_js_") as tmpdir:
            script_path = os.path.join(tmpdir, "solution.js")
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(code)

            # Node.js on Windows requires SystemRoot for CSPRNG crypto subsystem initialization
            node_env = {"SYSTEMROOT": os.environ.get("SYSTEMROOT", r"C:\Windows")} if sys.platform == "win32" else {}

            return self._evaluate_cases(
                cmd=[node_bin, script_path],
                cwd=tmpdir,
                test_cases=test_cases,
                timeout_sec=timeout_sec,
                memory_limit_mb=memory_limit_mb,
                mask_hidden=mask_hidden,
                is_custom_run=is_custom_run,
                proc_env=node_env,
            )

    def _run_compiled_c(
        self,
        code: str,
        lang: str,
        test_cases: list[dict[str, Any]],
        timeout_sec: float,
        memory_limit_mb: int,
        mask_hidden: bool,
        is_custom_run: bool,
    ) -> ExecutionResult:
        compiler = "g++" if "cpp" in lang or "c++" in lang else "gcc"
        compiler_bin = shutil.which(compiler) or shutil.which("clang") or shutil.which("cl")
        if not compiler_bin:
            return ExecutionResult(
                verdict="RUNNER_UNAVAILABLE",
                passed_cases=0,
                total_cases=len(test_cases),
                runtime_ms=0,
                memory_mb=0,
                score=0,
                compile_error=f"C/C++ compiler ('{compiler}') not found on system path.",
            )

        with tempfile.TemporaryDirectory(prefix="trellis_c_") as tmpdir:
            ext = ".cpp" if "cpp" in lang or "c++" in lang else ".c"
            src_file = os.path.join(tmpdir, f"solution{ext}")
            out_file = os.path.join(tmpdir, "solution.exe" if os.name == "nt" else "solution")

            with open(src_file, "w", encoding="utf-8") as f:
                f.write(code)

            compile_cmd = [compiler_bin, src_file, "-O2", "-o", out_file]
            try:
                c_proc = subprocess.run(
                    compile_cmd,
                    cwd=tmpdir,
                    env={},
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                if c_proc.returncode != 0:
                    return ExecutionResult(
                        verdict="COMPILATION_ERROR",
                        passed_cases=0,
                        total_cases=len(test_cases),
                        runtime_ms=0,
                        memory_mb=0,
                        score=0,
                        compile_error=c_proc.stderr[: self.MAX_OUTPUT_BYTES],
                    )
            except subprocess.TimeoutExpired:
                return ExecutionResult(
                    verdict="COMPILATION_ERROR",
                    passed_cases=0,
                    total_cases=len(test_cases),
                    runtime_ms=0,
                    memory_mb=0,
                    score=0,
                    compile_error="Compilation timed out.",
                )

            return self._evaluate_cases(
                cmd=[out_file],
                cwd=tmpdir,
                test_cases=test_cases,
                timeout_sec=timeout_sec,
                memory_limit_mb=memory_limit_mb,
                mask_hidden=mask_hidden,
                is_custom_run=is_custom_run,
            )

    def _run_java(
        self,
        code: str,
        test_cases: list[dict[str, Any]],
        timeout_sec: float,
        memory_limit_mb: int,
        mask_hidden: bool,
        is_custom_run: bool,
    ) -> ExecutionResult:
        javac = None
        java = None
        for cand_dir in [
            os.environ.get("JAVA_HOME"),
            r"C:\Program Files\Java\jdk-24",
            r"C:\Program Files\Java\jdk-21",
            r"C:\Program Files\Java\jdk-17",
        ]:
            if cand_dir and os.path.isdir(cand_dir):
                j_c = os.path.join(cand_dir, "bin", "javac.exe" if os.name == "nt" else "javac")
                j_r = os.path.join(cand_dir, "bin", "java.exe" if os.name == "nt" else "java")
                if os.path.isfile(j_c) and os.path.isfile(j_r):
                    javac = j_c
                    java = j_r
                    break

        if not javac:
            javac = shutil.which("javac")
        if not java:
            java = shutil.which("java")
        if not javac or not java:
            return ExecutionResult(
                verdict="RUNNER_UNAVAILABLE",
                passed_cases=0,
                total_cases=len(test_cases),
                runtime_ms=0,
                memory_mb=0,
                score=0,
                compile_error="Java compiler (javac) or runtime (java) not found on system path.",
            )

        with tempfile.TemporaryDirectory(prefix="trellis_java_") as tmpdir:
            src_file = os.path.join(tmpdir, "Solution.java")
            with open(src_file, "w", encoding="utf-8") as f:
                f.write(code)

            try:
                c_proc = subprocess.run(
                    [javac, src_file],
                    cwd=tmpdir,
                    env={},
                    capture_output=True,
                    text=True,
                    timeout=15,
                )
                if c_proc.returncode != 0:
                    return ExecutionResult(
                        verdict="COMPILATION_ERROR",
                        passed_cases=0,
                        total_cases=len(test_cases),
                        runtime_ms=0,
                        memory_mb=0,
                        score=0,
                        compile_error=c_proc.stderr[: self.MAX_OUTPUT_BYTES],
                    )
            except subprocess.TimeoutExpired:
                return ExecutionResult(
                    verdict="COMPILATION_ERROR",
                    passed_cases=0,
                    total_cases=len(test_cases),
                    runtime_ms=0,
                    memory_mb=0,
                    score=0,
                    compile_error="Java compilation timed out.",
                )

            return self._evaluate_cases(
                cmd=[java, f"-Xmx{memory_limit_mb}m", "-cp", tmpdir, "Solution"],
                cwd=tmpdir,
                test_cases=test_cases,
                timeout_sec=timeout_sec,
                memory_limit_mb=memory_limit_mb,
                mask_hidden=mask_hidden,
                is_custom_run=is_custom_run,
            )

    def _evaluate_cases(
        self,
        cmd: list[str],
        cwd: str,
        test_cases: list[dict[str, Any]],
        timeout_sec: float,
        memory_limit_mb: int,
        mask_hidden: bool,
        is_custom_run: bool,
        proc_env: dict[str, str] | None = None,
    ) -> ExecutionResult:
        case_results: list[TestCaseResult] = []
        passed_count = 0
        total_weight = sum(float(tc.get("weight", 1.0)) for tc in test_cases) or 1.0
        earned_weight = 0.0
        max_runtime = 0.0
        max_memory = 0.0
        overall_verdict = "ACCEPTED" if not is_custom_run else None
        first_fail = None
        custom_out = None

        preexec = self._get_preexec_fn(timeout_sec, memory_limit_mb)

        for idx, tc in enumerate(test_cases):
            input_text = str(tc.get("input_data", "")).strip()
            expected_text = str(tc.get("expected_output", "")).strip()
            is_hidden = bool(tc.get("is_hidden", False))
            is_custom = bool(tc.get("is_custom", False)) or is_custom_run
            weight = float(tc.get("weight", 1.0))

            start_t = time.perf_counter()
            try:
                proc = subprocess.run(
                    cmd,
                    input=input_text,
                    cwd=cwd,
                    env=proc_env if proc_env is not None else {},  # Empty environment: no leaked secrets or paths
                    capture_output=True,
                    text=True,
                    timeout=timeout_sec,
                    preexec_fn=preexec,
                )
                elapsed_ms = (time.perf_counter() - start_t) * 1000.0
                max_runtime = max(max_runtime, elapsed_ms)

                # Cap output bytes
                stdout_str = proc.stdout[: self.MAX_OUTPUT_BYTES]
                stderr_str = proc.stderr[: self.MAX_OUTPUT_BYTES]

                # Memory usage estimation
                mem_used = 12.0
                if resource and sys.platform != "win32":
                    try:
                        rusage = resource.getrusage(resource.RUSAGE_CHILDREN)
                        mem_used = rusage.ru_maxrss / 1024.0  # Linux KB to MB
                    except Exception:
                        mem_used = 12.0
                max_memory = max(max_memory, mem_used)

                if is_custom:
                    verdict = None
                    custom_out = stdout_str
                    err = stderr_str or None
                elif mem_used > memory_limit_mb or proc.returncode in {-9, 137}:
                    verdict = "MEMORY_LIMIT_EXCEEDED"
                    err = "Memory limit exceeded."
                elif proc.returncode != 0:
                    verdict = "RUNTIME_ERROR"
                    err = stderr_str[:500] if stderr_str else f"Non-zero exit code ({proc.returncode})"
                else:
                    actual_norm = normalize_output(stdout_str)
                    expected_norm = normalize_output(expected_text)
                    if actual_norm == expected_norm:
                        verdict = "ACCEPTED"
                        passed_count += 1
                        earned_weight += weight
                        err = None
                    else:
                        verdict = "WRONG_ANSWER"
                        err = None

            except subprocess.TimeoutExpired:
                elapsed_ms = timeout_sec * 1000.0
                max_runtime = max(max_runtime, elapsed_ms)
                verdict = "TIME_LIMIT_EXCEEDED" if not is_custom else None
                stdout_str = ""
                err = "Time limit exceeded."
            except Exception as ex:
                elapsed_ms = (time.perf_counter() - start_t) * 1000.0
                verdict = "RUNTIME_ERROR" if not is_custom else None
                stdout_str = ""
                err = str(ex)

            if not is_custom and verdict != "ACCEPTED" and overall_verdict == "ACCEPTED":
                overall_verdict = verdict

            display_input = "[HIDDEN TEST CASE INPUT]" if (is_hidden and mask_hidden) else input_text
            display_expected = "[HIDDEN EXPECTED OUTPUT]" if (is_hidden and mask_hidden) else expected_text
            display_actual = "[HIDDEN ACTUAL OUTPUT]" if (is_hidden and mask_hidden) else stdout_str

            case_res = TestCaseResult(
                case_index=idx + 1,
                is_hidden=is_hidden,
                verdict=verdict,
                input_data=display_input,
                expected_output=display_expected,
                actual_output=display_actual,
                runtime_ms=round(elapsed_ms, 2),
                memory_mb=round(max_memory, 2),
                error_message=err,
                is_custom=is_custom,
            )
            case_results.append(case_res)

            if not is_custom and verdict != "ACCEPTED" and first_fail is None:
                first_fail = {
                    "case_index": idx + 1,
                    "is_hidden": is_hidden,
                    "verdict": verdict,
                    "input": display_input,
                    "expected": display_expected,
                    "actual": display_actual,
                    "error": err,
                }

        final_score = (earned_weight / total_weight) * 100.0 if not is_custom_run else 0.0

        return ExecutionResult(
            verdict=overall_verdict,
            passed_cases=passed_count,
            total_cases=len(test_cases),
            runtime_ms=round(max_runtime, 2),
            memory_mb=round(max_memory, 2),
            score=round(final_score, 2),
            case_results=case_results,
            first_failing_case=first_fail,
            custom_output=custom_out,
        )


class CodeRunner:
    """Public gateway and factory for Sandboxed Code Execution."""

    _runner_instance: BaseCodeRunner | None = None

    @classmethod
    def get_runner(cls) -> BaseCodeRunner:
        """Instantiate runner based on CODE_RUNNER setting and TRELLIS_ENV."""
        runner_type = getattr(settings, "CODE_RUNNER", "local").lower().strip()
        env = getattr(settings, "TRELLIS_ENV", "dev").lower().strip()

        # In production, refuse to run if no isolated runner is configured
        if env != "dev" and runner_type not in {"judge0", "docker"}:
            raise RuntimeError(
                f"FATAL: Production environment (TRELLIS_ENV={env}) requires an isolated code runner "
                f"('judge0' or 'docker'). Local subprocess execution is forbidden."
            )

        if runner_type == "judge0":
            return Judge0Runner()
        elif runner_type == "docker":
            return DockerRunner()
        else:
            return LocalSubprocessRunner()

    @classmethod
    def execute(
        cls,
        code: str,
        language: str,
        test_cases: list[dict[str, Any]],
        time_limit_ms: int = 3000,
        memory_limit_mb: int = 256,
        mask_hidden_inputs: bool = False,
        is_custom_run: bool = False,
    ) -> ExecutionResult:
        """Execute code using the configured runner."""
        runner = cls.get_runner()
        return runner.execute(
            code=code,
            language=language,
            test_cases=test_cases,
            time_limit_ms=time_limit_ms,
            memory_limit_mb=memory_limit_mb,
            mask_hidden_inputs=mask_hidden_inputs,
            is_custom_run=is_custom_run,
        )
