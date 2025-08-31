# Copyright 2025 qBraid
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
'''
This module provides a decorator, `qasm_pipe`, for functions that generate QASM program strings.
The decorator captures 'path' and 'quiet' keyword arguments, writes the returned QASM string to a file,
and optionally prints the file location.
Functions decorated with `qasm_pipe` must:
    1. Accept 'path' and 'quiet' as keyword arguments.
    2. Return a tuple of (file_name, program_string).
The decorator will:
    - Write the QASM string to "{file_name}.qasm" in the specified path (or current working directory if not provided).
    - Create the output directory if it does not exist.
    - Print the file location unless 'quiet' is True.
Typical usage:
    @qasm_pipe
    def generate_qasm(..., path=None, quiet=False):
        ...
        return file_name, program_string'''
import os
from functools import wraps
from typing import Callable


def qasm_pipe(func: Callable) -> Callable:
    """
    Decorator that captures path and quiet arguments from the decorated function,
    then writes the function's (file_name, program_string) output to a .qasm file.

    The decorated function should:
    1. Accept 'path' and 'quiet' as keyword arguments
    2. Return a tuple of (file_name, program_string)

    The decorator will create a file named "{file_name}.qasm" and write the program_string to it.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Extract path and quiet from kwargs, with defaults
        path = kwargs.pop('path', None)
        quiet = kwargs.pop('quiet', False)

        # Call the decorated function to get the tuple output
        file_name, program_string = func(*args, **kwargs)

        # Determine the full file path
        if path is None:
            output_path = os.path.join(os.getcwd(), f"{file_name}.qasm")
        else:
            # Create directory if it doesn't exist
            os.makedirs(path, exist_ok=True)
            output_path = os.path.join(path, f"{file_name}.qasm")

        # Write the program string to the file
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(program_string)

        if not quiet:
            print(f"QASM file created: {output_path}")

        return output_path

    return wrapper
