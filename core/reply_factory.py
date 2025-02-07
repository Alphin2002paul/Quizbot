from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST
from typing import Optional


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    """Records the user's answer for the current question."""
    if not answer:
        raise ValueError("Answer cannot be empty")
    
    current_question = session.get("current_question")
    if not current_question:
        raise ValueError("No current question found")
    
    # Store the answer
    session["answers"] = session.get("answers", {})
    session["answers"][current_question["id"]] = answer
    # Update question index
    session["current_question_index"] = session.get("current_question_index", 0) + 1

    return True, ""


def get_next_question(current_question_id):
    """Returns the next question or None if quiz is complete."""
    if current_question_id is None:
        return None, None

    # This function needs to be implemented to fetch the next question
    # based on the current_question_id.
    # For now, we'll return a placeholder.
    return "dummy question", -1


def generate_final_response(session):
    """Generates the final quiz result with score."""
    user_state = session.get("answers", {})
    total_questions = len(user_state)
    correct_answers = 0
    
    # Calculate score
    for question_id, answer in user_state.items():
        if answer.lower() == PYTHON_QUESTION_LIST[question_id]["correct_answer"].lower():
            correct_answers += 1
    
    score_percentage = (correct_answers / total_questions) * 100
    
    # Generate detailed response
    response = f"Quiz Complete!\n\n"
    response += f"You got {correct_answers} out of {total_questions} questions correct.\n"
    response += f"Your score: {score_percentage:.1f}%\n\n"
    
    # Add feedback based on score
    if score_percentage >= 90:
        response += "Excellent work! 🌟"
    elif score_percentage >= 70:
        response += "Good job! 👍"
    elif score_percentage >= 50:
        response += "Not bad, but there's room for improvement! 📚"
    else:
        response += "Keep practicing! You'll do better next time! 💪"
    
    return response
