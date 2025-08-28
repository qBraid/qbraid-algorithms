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
        with open(output_path, 'w') as file:
            file.write(program_string)
        
        if not quiet:
            print(f"QASM file created: {output_path}")
        
        return output_path
        
    return wrapper

