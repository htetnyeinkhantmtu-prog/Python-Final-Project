from matching import find_all_matches


def display_results(logged_in_user):
    matches = find_all_matches(logged_in_user)

    print(f"\n--- Top  Matches for {logged_in_user} ---\n")

    for i, match in enumerate(matches, start=1):
        print(f"{i}. {match['username']}")
        print(f"   Compatibility: {match['score']}%")
        print(f"   Zodiac: {match['zodiac']}")
        print(f"   Morning/Night: {match['morning_or_night']}\n")
