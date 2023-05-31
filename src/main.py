#!/usr/bin/env python3

import argparse

if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(
        prog='hashiwokakero', description='Hashi game in Python!', epilog='Requires a game board input file')

    # Append arguments
    parser.add_argument('-f', '--file', help='Input board file', required=True)
    parser.add_argument('-a', '--automatic', help='Play with automatic player', action='store_true')

    # Get arguments
    args = parser.parse_args()

    try:
        # Import and start game
        from hashiwokakero import hashiwokakero
        hashiwokakero(args.file, args.automatic)
        
    except FileNotFoundError as e:
        print(f"Error reading board file: {e.args}")
        
    except ValueError as e:
        print(f"Board file has invalid format: {e.args}")
        
    except AssertionError as e:
        print(f"Board file has invalid format!")
