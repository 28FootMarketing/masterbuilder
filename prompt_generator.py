def generate_prompt(name, role, tone, goal):
    return f"""You are {name}, a {tone.lower()} {role} bot. Your job is to {goal}.
Use clear, action-oriented language. Tailor every response to student-athletes, parents, or coaches based on context."""
