def reflect(memories):
    
    if not memories:
        return "아직 충분한 기억이 없습니다."

    anxiety_count = 0
    loneliness_count = 0

    for memory in memories:

        if memory["emotion"] == "anxiety":
            anxiety_count += 1

        if memory["emotion"] == "loneliness":
            loneliness_count += 1

    if anxiety_count >= 3:
        return "최근 사용자는 반복적으로 불안을 표현하고 있습니다."

    if loneliness_count >= 3:
        return "최근 사용자는 외로움을 자주 표현하고 있습니다."

    return "현재 감정 상태는 비교적 안정적입니다."