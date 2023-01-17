import questions
import inquirer
import utils


def main():
    """
    Dynamically selects the question class to load and execute.
    """
    classes = utils.get_classes(questions)

    # Provide the user with a choice of which class to execute.
    question = (inquirer.prompt([
        inquirer.List('question',
                      message="Select the question to execute",
                      choices=list(classes.keys()))
    ]))

    if question is None:
        return exit(1)

    # Select the class, initialize it and call the 'main' function for that
    # class.
    target = classes[question['question']]
    target().main()


if __name__ == '__main__':
    main()
