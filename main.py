import hashlib
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASELINE_FILE = os.path.join(BASE_DIR, "baseline.json")


def resolve_path(path):
    path = path.strip().strip('"')

    if not os.path.isabs(path):
        path = os.path.join(BASE_DIR, path)

    return os.path.abspath(path)


# 1. Calculate SHA-256
def calculate_hash(file_path):
    sha256 = hashlib.sha256()

    try:
        with open(file_path, "rb") as file:
            while True:
                chunk = file.read(4096)

                if not chunk:
                    break

                sha256.update(chunk)

        return sha256.hexdigest()

    except OSError as error:
        print(f"ERROR: Cannot read file: {error}")
        return None


# 2. Load baseline
def load_baseline():
    try:
        with open(BASELINE_FILE, "r", encoding="utf-8") as file:
            hashes = json.load(file)

    except FileNotFoundError:
        return {}

    except json.JSONDecodeError:
        print("ERROR: Baseline file is corrupted!")
        raise

    except OSError as error:
        print(f"ERROR: Cannot read baseline: {error}")
        raise

    if not isinstance(hashes, dict):
        raise ValueError("Invalid baseline structure.")

    for path, digest in hashes.items():

        if not isinstance(path, str) or not isinstance(digest, str):
            raise ValueError("Invalid baseline entry.")

        if len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest.lower()):
            raise ValueError("Invalid SHA-256 hash.")

        hashes[path] = digest.lower()
    return hashes


# 3. Save baseline
def save_baseline(hashes):
    temp_file = BASELINE_FILE + ".tmp"

    try:
        with open(temp_file, "w", encoding="utf-8") as file:
            json.dump(hashes, file, indent=4)

        os.replace(temp_file, BASELINE_FILE)
        return True

    except (OSError, TypeError) as error:
        print(f"ERROR: Cannot save baseline: {error}")

        try:
            os.remove(temp_file)
        except FileNotFoundError:
            pass
        except OSError as cleanup_error:
            print(f"WARNING: Cannot remove temporary file: {cleanup_error}")

        return False


# 4. Register files
def register_files():
    hashes = load_baseline()

    print("\nEnter file paths (press Enter to finish).")

    while True:
        path = input("File path: ").strip()

        if not path:
            break

        path = resolve_path(path)

        if not os.path.exists(path):
            print("ERROR: Path does not exist!")
            continue

        if not os.path.isfile(path):
            print("ERROR: This is a directory, not a file!")
            continue

        file_hash = calculate_hash(path)

        if file_hash is None:
            continue

        hashes[path] = file_hash
        print("Registered:", path)

    if save_baseline(hashes):
        print("\nBaseline saved successfully.")
    else:
        print("\nBaseline could not be saved.")


# 5. Verify one file
def verify_file(file_path):
    if not file_path.strip():
        print("Please enter a file path.")
        return

    hashes = load_baseline()
    file_path = resolve_path(file_path)

    if file_path not in hashes:
        print("File not registered!")
        return

    if not os.path.isfile(file_path):
        print("WARNING: File is missing!")
        return

    current_hash = calculate_hash(file_path)

    if current_hash is None:
        return

    if current_hash == hashes[file_path]:
        print("INTEGRITY OK: No modification detected.")
    else:
        print("WARNING: File has been modified!")


# 6. Verify all files
def verify_all():
    hashes = load_baseline()

    if not hashes:
        print("No registered files.")
        return

    print("\n===== INTEGRITY REPORT =====")

    for path, original_hash in hashes.items():

        if not os.path.isfile(path):
            print("[MISSING]", path)
            continue

        current_hash = calculate_hash(path)

        if current_hash is None:
            print("[ACCESS ERROR]", path)
            continue

        if current_hash == original_hash:
            print("[OK]", path)
        else:
            print("[MODIFIED]", path)


# 7. List registered files
def list_files():
    hashes = load_baseline()

    if not hashes:
        print("No registered files.")
        return

    print("\n===== REGISTERED FILES =====")

    for index, path in enumerate(hashes, start=1):
        print(f"{index}. {path}")


# 8. Remove a file from baseline
def remove_file():
    file_path = input("Enter the path of the file to remove: ")

    if not file_path.strip():
        print("Please enter a file path.")
        return

    hashes = load_baseline()
    resolved_path = resolve_path(file_path)

    if resolved_path in hashes:
        del hashes[resolved_path]

        if save_baseline(hashes):
            print(f"File '{resolved_path}' removed from baseline.")
        else:
            print("Failed to update baseline.")

    else:
        print("File not registered!")


# 9. Main menu
def main():
    while True:
        print("\n" + "=" * 40)
        print("       FILE INTEGRITY CHECKER")
        print("=" * 40)
        print("1. Register files")
        print("2. Verify one file")
        print("3. Verify all files")
        print("4. List registered files")
        print("5. Remove a registered file")
        print("6. Exit")
        print("=" * 40)

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                register_files()
                pause()

            elif choice == "2":
                path = input("Enter file path: ").strip()
                verify_file(path)
                pause()

            elif choice == "3":
                verify_all()
                pause()

            elif choice == "4":
                list_files()
                pause()

            elif choice == "5":
                remove_file()
                pause()

            elif choice == "6":
                print("Goodbye!")
                break

            else:
                print("Invalid choice!")
                pause()

        except (OSError, json.JSONDecodeError, ValueError) as error:
            print(f"\nERROR: {error}")
            pause()


def pause():
    input("\nPress Enter to return to the main menu...")
    os.system("cls")


if __name__ == "__main__":
    main()
