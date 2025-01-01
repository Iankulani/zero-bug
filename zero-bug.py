# -*- coding: utf-8 -*-
"""
Created on Thurs Jan  1 11:42:47 2025

@author: IAN CARTER KULANI
"""

from colorama import Fore
import pyfiglet
import os
font=pyfiglet.figlet_format("ZERO BUG")
print(Fore.GREEN+font)

import re

# Function to read the assembly file
def read_file(file_path):
    """Reads the content of an assembly file."""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return None

# Function to save the modified assembly code to a file
def save_file(file_path, content):
    """Saves the modified assembly content to a new file."""
    with open(file_path, 'w') as file:
        file.write(content)
    print(f"File saved as {file_path}")

# Function to analyze assembly code for bugs
def analyze_code(code):
    """Analyzes assembly code for common bugs and issues."""
    bugs = []

    # Recognize assembly instructions (JMP, MOV, ADD, etc.)
    instructions = ["JMP", "ADD", "MOV", "MUL", "DIV"]
    for instr in instructions:
        if instr not in code:
            bugs.append(f"Warning: Missing {instr} instruction.")
    
    # Recognizing and detecting misuse of C-style keywords (e.g., int, float, char) in assembly code
    c_keywords = ["int", "float", "char", "double", "sizeof", "typedef", "register", "union", "for", "while", 
                  "struct", "static", "long", "short", "packed", "return", "goto"]
    
    for keyword in c_keywords:
        if keyword in code:
            bugs.append(f"Warning: C-style keyword '{keyword}' found in assembly code. This may indicate an issue.")

    # Check for jumps (e.g., 'JMP') without labels
    missing_labels = re.findall(r'\bJMP\b(?!\s+[A-Za-z_][A-Za-z0-9_]*)', code)
    if missing_labels:
        for _ in missing_labels:
            code = code.replace("JMP", "JMP DEFAULT_LABEL")  # Add a default label for simplicity
        bugs.append("Added default labels for 'JMP' statements.")

    # Check for common uninitialized register usage (e.g., using registers without initialization)
    uninitialized_registers = re.findall(r'(\b[A-Za-z]{2,3}\b)\s*,\s*\d+', code)  # e.g., MOV AX, 5
    if uninitialized_registers:
        for reg in uninitialized_registers:
            bugs.append(f"Warning: Potential uninitialized register usage for {reg}.")
    
    # Check for redundant NOP instructions (no operation)
    redundant_nops = re.findall(r'\bNOP\b\s*\n', code)
    if redundant_nops:
        code = re.sub(r'\bNOP\b\s*\n', '', code)  # Remove redundant NOPs
        bugs.append("Removed redundant 'NOP' instructions.")

    # Check for improper arithmetic usage (e.g., DIV by zero or misuse of instructions)
    if "DIV" in code:
        div_by_zero = re.findall(r'DIV\s*,\s*0', code)
        if div_by_zero:
            bugs.append("Warning: Division by zero detected in the code.")
    
    return code, bugs

# Function to prompt user for file path, read file, analyze, fix, and save
def main():
    print("Welcome to the Binary Analysis Tool!")

    # Prompt user for the path to the assembly file
    file_path = input("Enter the path to the assembly file: ").strip()

    # Read the file content
    code = read_file(file_path)
    
    if code:
        # Analyze and check for bugs
        modified_code, bugs = analyze_code(code)
        
        # Show the detected bugs to the user
        if bugs:
            print("\nDetected issues and bugs:")
            for bug in bugs:
                print(f"- {bug}")
        else:
            print("\nNo bugs detected. The code appears to be fine.")
        
        # Prompt the user for the path to save the modified file
        save_path = input("Enter the path to save the modified file: ").strip()
        save_file(save_path, modified_code)

if __name__ == "__main__":
    main()
