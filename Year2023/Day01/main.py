from evaluator import TestDataEvaluatorPart1


def evaluate():
    with open("./test_data.txt", "r") as file:
        lines = file.readlines()
    evaluator = TestDataEvaluatorPart1(lines)
    result = evaluator.evaluate_calibration_data()
    print("Result is", result)


if __name__ == "__main__":
    evaluate()
