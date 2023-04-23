import subprocess
import sys


def main():
    print("Please choose the desired option:")
    print("1. Run SCRAPPER_CSV.py")
    print("2. Run SCRAPPER_SQL.py")
    print("3. Run SCRAPPER_API.py")
    print("4. Exit")

    choice = input("Enter the number of the chosen option: ")

    if choice == '1':
        subprocess.run([sys.executable, "SCRAPPER_CSV.py"])
    elif choice == '2':
        subprocess.run([sys.executable, "SCRAPPER_SQL.py"])
    elif choice == '3':
        subprocess.run([sys.executable, "SCRAPPER_API.py"])
    elif choice == '4':
        print("Goodbye!")
        return
    else:
        print("Invalid option. Please try again.")

    main()


if __name__ == "__main__":
    main()
