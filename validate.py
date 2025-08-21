#!/bin/python3
from result_output import ResultOutput
import re
import os
import sys
import json
import time
import shutil
import importlib
import importlib.util
from sys import platform
import string
import random
import requests
import signal
import subprocess
import psutil

def generate_random_string(length):
    letters = string.ascii_letters + string.digits
    random_string = "".join(random.choice(letters) for _ in range(length))
    return random_string

class Activity:
    def __init__(self):
        # No additional initialization is needed.
        pass

    def testcase1(self):
        """Check if wintel.txt contains 'API=' keyword using PowerShell Invoke-Command"""
        self.result_output.update_pre_result(
            description="Check if wintel.txt contains 'API=' keyword via PowerShell remote command",
            expected="wintel.txt should contain 'API=' keyword"
        )
        try:
            # PowerShell command to execute on remote VM
            ps_command = """Invoke-Command -VMName 'WinSer' -Credential (New-Object System.Management.Automation.PSCredential('WINTEL\\Administrator',(ConvertTo-SecureString 'Root123$' -AsPlainText -Force))) -ScriptBlock { Get-Content "C:\\Users\\Administrator\\Desktop\\wintel.txt" }"""
            
            # Execute PowerShell command
            process = subprocess.Popen(
                ['powershell', '-Command', ps_command],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                text=True
            )
            
            stdout, stderr = process.communicate(timeout=30)
            
            # Check if command executed successfully
            if process.returncode != 0:
                self.result_output.update_result(
                    result=0,
                    actual="Failed to execute PowerShell command or access wintel.txt",
                    comment=f"PowerShell error: {stderr.strip()}" if stderr.strip() else "Command execution failed",
                    marks="10",
                    marks_obtained="0"
                )
                return
            
            # Check if the content contains "API="
            file_content = stdout.strip()
            if not file_content:
                self.result_output.update_result(
                    result=0,
                    actual="wintel.txt is empty or not accessible",
                    comment="No content retrieved from wintel.txt",
                    marks="10",
                    marks_obtained="0"
                )
                return
            
            # Search for "API=" in the content
            if "API=" in file_content:
                self.result_output.update_result(
                    result=1,
                    actual="wintel.txt contains 'API=' keyword",
                    comment="Successfully found 'API=' in wintel.txt",
                    marks="10",
                    marks_obtained="10"
                )
            else:
                self.result_output.update_result(
                    result=0,
                    actual="wintel.txt does not contain 'API=' keyword",
                    comment="'API=' keyword not found in file content",
                    marks="10",
                    marks_obtained="0"
                )
                
        except subprocess.TimeoutExpired:
            self.result_output.update_result(
                result=-1,
                actual="PowerShell command timed out",
                comment="Command execution exceeded 30 seconds timeout",
                marks="10",
                marks_obtained="0"
            )
        except Exception as e:
            self.result_output.update_result(
                result=-1,
                actual="Error executing PowerShell command",
                comment=f"Exception: {str(e)}",
                marks="10",
                marks_obtained="0"
            )

def parse_arguments(args):
    """Parse different argument formats and return standardized JSON"""
    try:
        # Handle JSON format arguments
        if args.startswith('{') and args.endswith('}'):
            return args
        
        # Handle UID script args format (#UID_SCRIPT_ARGS)
        if args.startswith('#'):
            # Extract token from UID format
            token = args[1:]  # Remove the # prefix
            return json.dumps({"token": token})
        
        # Handle colon-separated format (legacy)
        if ':' in args:
            args = args.replace('{', '').replace('}', '')
            parts = args.split(':')
            if len(parts) >= 2:
                return json.dumps({"token": parts[1]})
        
        # Default case - treat as token
        return json.dumps({"token": args})
        
    except Exception:
        # Fallback to empty token
        return json.dumps({"token": ""})

def start_tests(args):
    """Initialize and run all test cases"""
    # Parse arguments to standardized JSON format
    parsed_args = parse_arguments(args)
    
    # Initialize ResultOutput and Activity instances
    test_object = ResultOutput(parsed_args, Activity)
    challenge_test = Activity()
    challenge_test.result_output = test_object

    # Execute test case
    challenge_test.testcase1()

    # Get final results and return as JSON
    final_result = test_object.result_final()
    return final_result

def main():
    """Main entry point handling different command line formats"""
    try:
        # Handle different command line argument formats
        if len(sys.argv) < 2:
            args = '{"token":""}'
        elif len(sys.argv) == 2:
            args = sys.argv[1]
        elif len(sys.argv) == 3:
            # Handle -json flag format
            if sys.argv[1] == '-json':
                args = sys.argv[2]
            else:
                # Platform-specific handling (legacy)
                if platform == "win32":
                    args = sys.argv[2] if len(sys.argv) > 2 else sys.argv[1]
                else:
                    args = sys.argv[1]
        else:
            args = sys.argv[1]
        
        # Execute tests and print results
        result = start_tests(args)
        print(result)
        
    except Exception as e:
        # Fallback error handling - still return valid JSON
        error_result = {
            "metadata": {"schema": "2.0"},
            "context": {"token": "", "args": ""},
            "summary": {"totalTests": 1, "Passed": 0, "Failed": 0, "Errored": 1},
            "testCases": [{
                "index": 0,
                "testCase": "System Error",
                "expected": "Script execution",
                "actual": f"Error: {str(e)}",
                "status": -1,
                "comments": "Script execution failed",
                "ref": "",
                "marks": "10",
                "marksObtained": "0"
            }],
            "evaluation": {"status": 0, "message": ""}
        }
        print(json.dumps(error_result, indent=1))

if __name__ == "__main__":
    main()
