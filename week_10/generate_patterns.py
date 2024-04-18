import random

def generate_pattern():
    pattern = []
    for _ in range(2):
        pattern.append((random.random(), random.random()))
    return pattern

def calculate_answer(pattern):
    # For demonstration purposes, let's calculate the sum of all the elements in the pattern
    answer = sum([pair[0] + pair[1] for pair in pattern])
    return answer

def generate_doubles(num_rows):
    rows = []
    answers = []
    for _ in range(num_rows):
        pattern = generate_pattern()
        answer = calculate_answer(pattern)
        row = ' '.join([f"{pair[0]},{pair[1]}," for pair in pattern])
        rows.append(row)
        answers.append(str(answer))
    return rows, answers

def save_to_file(data, filename):
    with open(filename, 'w') as f:
        f.write('\n'.join(data))

def main():
    num_rows = 20000
    rows, answers = generate_doubles(num_rows)
    save_to_file(rows, 'random_doubles.txt')
    save_to_file(answers, 'answers.txt')

if __name__ == "__main__":
    main()