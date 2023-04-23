import inferior

question_lines = inferior.get_unit(1)

question = inferior.get_question(question_lines[-1])

print(question)
