import random

lines = [line.strip() for line in open('data.txt', 'r', encoding='utf-8').readlines()]

units_indexes = {line.strip(): i for i, line in enumerate(lines) if 'U>' in line}

def get_unit_lines(unit_number):
    next_unit = f'U>{unit_number+1}'
    return lines[units_indexes[f'U>{unit_number}']:(units_indexes[next_unit] if next_unit in units_indexes else len(lines))]

def get_questions_lines(lines):
    indexes = [i for i, line in enumerate(lines) if 'Q>' in line]
    return [lines[index:(indexes[i+1] if i != len(indexes)-1 else len(lines))] for i, index in enumerate(indexes)]

def get_question(question_lines):
    question_text = question_lines[0].replace('Q>', '')
    correct_answer, incorrect_answers, image, part, topic = None, [], None, None, None
    for i, line in enumerate(question_lines):
        if 'N>' in line:
            incorrect_answers.append(line.replace('N>', '') + '<>' + question_lines[i+1].replace('E>', ''))
        elif 'Y>' in line:
            correct_answer = line.replace('Y>', '') + '<>' + question_lines[i+1].replace('E>', '')
        elif 'P>' in line:
            part = line.replace('P>', '')
        elif 'T>' in line:
            topic = line.replace('T>', '')
        elif 'I>' in line:
            image = line.replace('I>', '')
    return [question_text, correct_answer, incorrect_answers, image, part, topic]

def get_unit(unit_number):
    return get_questions_lines(get_unit_lines(unit_number))