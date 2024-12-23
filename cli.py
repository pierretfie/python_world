import argparse

def main():
    parser = argparse.ArgumentParser(description="Secure File Encryption Tool")
    parser.add_argument("mode", choices=["encrypt", "decrypt"], help="Mode of operation")
    parser.add_argument("file", help="Path to the file")
    parser.add_argument("password", help="Password for encryption/decryption")
    args = parser.parse_args()
    
    if args.mode == "encrypt":
        encrypt_file(args.file, args.password)
        print(f"File Hash: {hash_file(args.file)}")
    elif args.mode == "decrypt":
        decrypt_file(args.file, args.password)

if __name__ == "__main__":
    main()