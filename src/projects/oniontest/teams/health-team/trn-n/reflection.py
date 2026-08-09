def reflect(session_state):
    rep_count = session_state.get('rep_count', 0)
    errors = session_state.get('form_errors', [])
    
    summary = f"Session completed with {rep_count} reps."
    if errors:
        summary += f" Form issues noted: {', '.join(set(errors))}."
    else:
        summary += " Great form throughout!"
    
    return summary