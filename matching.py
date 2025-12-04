from storage import load_users

# point mapping

def calculate_match_score(user1_answers, user2_answers):

    if not user1_answers or not user2_answers:
        return 0

    total_points = 0

    total_points += 15 if user1_answers["zodiac"] == user2_answers["zodiac"] else 0

    total_points += 15 if user1_answers["morning_or_night"] == user2_answers["morning_or_night"] else 0

    music_diff = abs(user1_answers["music"] - user2_answers["music"])
    music_points = {0: 20, 1: 10}
    total_points += music_points.get(music_diff, 0)

    activity_diff = abs(user1_answers["activity"] - user2_answers["activity"])
    activity_points = {0: 20, 1: 10, 2: 5}
    total_points += activity_points.get(activity_diff, 0)

    total_points += 15 if user1_answers["personality"] == user2_answers["personality"] else 0

    mood_diff = abs(user1_answers["mood"] - user2_answers["mood"])
    mood_points = {0: 15, 1: 7}
    total_points += mood_points.get(mood_diff, 0)

    return round(total_points, 2)


def find_all_matches(username):

    data = load_users()
    all_users = data["users"]

    # Find current user
    current_user = None
    for user in all_users:
        if user["username"] == username:
            current_user = user
            break

    # Check if user completed questionnaire
    if not current_user or not current_user.get("profile_complete", False):
        return None

    my_answers = current_user["questionnaire"]
    matches = []

    for other_user in all_users:
        # Skip self and incomplete profiles
        if other_user["username"] == username:
            continue
        if not other_user.get("profile_complete", False):
            continue

        their_answers = other_user["questionnaire"]
        score = calculate_match_score(my_answers, their_answers)

        matches.append({
            "username": other_user["username"],
            "score": score,
            "zodiac": their_answers["zodiac"],
            "morning_or_night": their_answers["morning_or_night"]
        })

    for i in range(len(matches)):
        for j in range(i + 1, len(matches)):
            if matches[i]["score"] < matches[j]["score"]:

                temp = matches[i]
                matches[i] = matches[j]
                matches[j] = temp

    return matches
