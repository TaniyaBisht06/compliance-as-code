import ast
import os
import sys

violations = []
passed = []

# Read application configuration
with open("config.py", "r") as file:
    config_code = file.read()

tree = ast.parse(config_code)

# Policy 1: No hardcoded API keys
api_key_safe = True

for node in ast.walk(tree):
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "API_KEY":
                if isinstance(node.value, ast.Constant):
                    api_key_safe = False

if api_key_safe:
    passed.append("No hardcoded API keys")
else:
    violations.append("Hardcoded API key detected")

# Policy 2: Debug mode must be disabled
debug_safe = True

for node in ast.walk(tree):
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "DEBUG":
                if isinstance(node.value, ast.Constant) and node.value.value is True:
                    debug_safe = False

if debug_safe:
    passed.append("Debug mode disabled")
else:
    violations.append("Debug mode is enabled")

# Policy 3: Logging must use a separate file
with open("app.py", "r") as file:
    app_code = file.read()

app_tree = ast.parse(app_code)

logging_safe = False

for node in ast.walk(app_tree):
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Attribute):
            if node.func.attr == "basicConfig":
                for keyword in node.keywords:
                    if keyword.arg == "filename":
                        if keyword.value is not None:
                            if isinstance(keyword.value, ast.Constant):
                                if "logs/" in str(keyword.value.value).replace("\\", "/"):
                                    logging_safe = True

if logging_safe:
    passed.append("Separate application logging enabled")
else:
    violations.append("Separate application logging not configured")

# Generate compliance report
report = []

report.append("COMPLIANCE CHECK REPORT")
report.append("-----------------------")

if violations:
    report.append("STATUS: NON-COMPLIANT")
else:
    report.append("STATUS: COMPLIANT")

for item in passed:
    report.append("[PASS] " + item)

for item in violations:
    report.append("[FAIL] " + item)

report_text = "\n".join(report)

print(report_text)

with open("compliance-report.txt", "w") as file:
    file.write(report_text)

# Fail pipeline if violations exist
if violations:
    sys.exit(1)

sys.exit(0)
