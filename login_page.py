from auth import register, login, username_valid, password_strength
from questionnaire import questionnaire
from matching import find_all_matches
from display import display_results


def display_password_requirements():
    print("\nPassword must include:")
    print("- At least 8 characters")
    print("- Uppercase + lowercase")
    print("- Number")
    print("- Special character (!@#$ etc.)\n")


def main_menu(username):

    while True:
        print("\n" + "="*50)
        print(f"    MATCHMAKER - Logged in as: {username}")
        print("="*50)
        print("1. Take Questionnaire")
        print("2. Find Matches")
        print("3. Logout")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            # Take questionnaire
            questionnaire(username)

        elif choice == "2":
            display_results(username)
            break

        elif choice == "3":
            # Logout
            print(f"\nGoodbye, {username}! 👋")
            break

        else:
            print("\n❌ Invalid choice. Please enter 1, 2, or 3.")


def login_interface():
    """Login/Register interface"""
    while True:
        print("\n=== Match Making Authentication ===")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        option = input("Enter option: ").strip()

        if option == "1":
            # Register
            while True:
                username = input("Choose a username: ").strip()
                valid, msg = username_valid(username)
                if valid:
                    break
                print(msg)
            display_password_requirements()
            while True:
                password = input("Choose a password: ")
                confirm = input("Confirm password: ")

                if password != confirm:
                    print("Passwords do not match.")
                    continue

                strong, msg = password_strength(password)
                if not strong:
                    print(msg)
                    continue
                break

            success, msg = register(username, password)
            print(msg)

        elif option == "2":
            username = input("Username: ").strip()
            password = input("Password: ")
            success, msg, logged_in_user = login(username, password)
            print(msg)

            if success:
                main_menu(logged_in_user)

        elif option == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid option.")


login_interface()

