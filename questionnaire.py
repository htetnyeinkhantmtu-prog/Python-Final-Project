from storage import load_users, save_users


def questionnaire(username):

    print("\n" + "="*50)
    print("__________ Questionnaire __________")
    print("="*50)
    print("Please answer the following questions.\n")

    zodiac = input("What is your zodiac sign?: ").lower()

    morning_or_night = input(
        "Are you a morning person or a night person? Type morning or night: ").lower()

    music = int(input(
        "What type of music do you prefer? Choose one number:\n"
        "1. Pop\n2. Rock\n3. Classical\n4. K-pop\nYour choice: "
    ))

    activity = int(input(
        "Which activity do you enjoy more? Choose one number:\n"
        "1. Reading\n2. Sports\n3. Gaming\n4. Cooking\n5. Traveling\nYour choice: "
    ))

    personality = int(input(
        "Are you more introverted or extroverted? Choose one number:\n"
        "1. Introvert\n2. Extrovert\nYour choice: "
    ))

    mood = int(input(
        "What describes you best? Choose one number:\n"
        "1. Calm\n2. Energetic\n3. Talkative\n4. Quiet\nYour choice: "
    ))

    # Create answers dictionary
    answers = {
        "zodiac": zodiac,
        "morning_or_night": morning_or_night,
        "music": music,
        "activity": activity,
        "personality": personality,
        "mood": mood
    }

    # Save to auth.json
    data = load_users()
    for user in data["users"]:
        if user["username"] == username:
            user["questionnaire"] = answers
            user["profile_complete"] = True
            break

    save_users(data)

    print("\n✅ Questionnaire completed! Your answers have been saved.")

    return answers
