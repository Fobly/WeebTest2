import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        # First try reading as text
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                print(f"File content (text mode):")
                for i, line in enumerate(file):
                    if i >= 5:
                        break
                    print(line, end='')
        except UnicodeDecodeError:
            # If text fails, read as binary
            with open(file_path, 'rb') as file:
                print(f"\nFile appears to be binary. First 5 lines (hex representation):")
                for i in range(5):
                    line = file.readline()
                    if not line:
                        break
                    print(line.hex(' ', 1))  # Show hex representation with space between bytes

    except FileNotFoundError:
        print(f"Error: File not found at path '{file_path}'")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()