from matching import find_all_matches


def display_results(username):

    print("\n" + "="*60)
    print(f"         MATCHES FOR {username.upper()}")
    print("="*60)

    # get matches
    matches = find_all_matches(username)

    # completion check
    if matches is None:
        print("\n ERROR: You haven't taken the questionnaire yet!")
        print("Please select option 1 to take the questionnaire first.")
        return

    # no matches case
    if len(matches) == 0:
        print("\n No matches found yet.")
        print("Wait for other users to complete their questionnaires!")
        return

    # Display matches
    print(f"\n🎯 Found {len(matches)} compatible user(s):\n")
    print("-" * 60)
    print(f"{'#':<4} {'Username':<15} {'Score':<10} {'Zodiac':<12} {'Type':<15}")
    print("-" * 60)

    for i in range(len(matches)):
        match = matches[i]
        match_number = i + 1
        match_username = match["username"]
        match_score = match["score"]
        match_zodiac = match["zodiac"]
        match_type = match["morning_or_night"]

        if match_score >= 80:
            emoji = "💖"
        elif match_score >= 60:
            emoji = "😊"
        elif match_score >= 40:
            emoji = "👍"
        else:
            emoji = "🤔"

        print(f"{match_number:<4} {match_username:<15} {match_score:>5.1f}% {emoji:<4} {match_zodiac:<12} {match_type:<15}")

    print("-" * 60)
    print("\nRating Guide:")
    print("  💖 80%+ = Excellent Match")
    print("  😊 60-79% = Great Match")
    print("  👍 40-59% = Good Match")
    print("  🤔 Below 40% = OK Match")
    print()
