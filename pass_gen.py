import argparse
import secrets


def time_it(function):
    """Decorator that times the execution of a function."""
    from time import time

    def wrapper(*args, **kwargs):
        before = time()
        result = function(*args, **kwargs)
        after = time()
        print("Execution of {} took {:.8f} seconds".format(
            function.__name__, (after - before)))

        return result

    return wrapper


def import_words(file_name):
    """Import words from textfile and store them in a dictionary."""
    with open(file_name) as word_list:
        words = []
        for line in word_list:
            number, word = line.strip().split("\t")
            words.append(word.strip())
        # print(f"Imported {(len(word_dict))} words")

    return words


def generate_word_list(n, source_file="wordlist.txt"):
    """Randomly choose <n> unique words from list."""
    WORDS = import_words(source_file)

    return [secrets.choice(WORDS) for w in range(n)]


def insert_special_char(phrase_words):
    """Replace random character of a random word in the pass phrase with a
    randomly selected character."""
    SPECIAL = [
        ["~", "!", "#", "$", "%", "^"],
        ["&", "*", "(", ")", "-", "="],
        ["+", "[", "]", "\\", "{", "}"],
        [":", ";", "\"", "\'", "<", ">"],
        ["?", "/", "0", "1", "2", "3"],
        ["4", "5", "6", "7", "8", "9"]]
    n = len(phrase_words)

    rand_i = secrets.randbelow(n)
    rand_w = phrase_words[rand_i]  # Random word
    rand_w_i = secrets.randbelow(len(rand_w))  # Random character

    rand_row = secrets.choice(SPECIAL)
    rand_special = secrets.choice(rand_row)

    # Replace char and word
    rand_w = rand_w[rand_w_i] + rand_special + rand_w[:rand_w_i+1]
    phrase_words[rand_i] = rand_w


def parse_commandline():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(prog="passgen")
    parser.add_argument("n", type=int, nargs="?", default=6,
                        help="number of words in the pass phrase (default=6)")
    parser.add_argument("--special", action="store_true",
                        help="""make pass phrase stronger by randomly inserting
                        a special character (default=false)""")
    parser.add_argument("--source", metavar="<file name>",
                        default="wordlist.txt",
                        help="use alternative word list to generate pass phrase")
    parser.add_argument("--separator", default=" ",
                        help="separator between words (default=" ")")

    return parser.parse_args()


def main():
    args = parse_commandline()
    phrase_words = generate_word_list(args.n, args.source)

    if args.special:
        insert_special_char(phrase_words)

    pass_phrase = args.separator.join([w for w in phrase_words])
    print(pass_phrase)

    if len(pass_phrase) < 17:
        print("""\nThe generated pass phrase is very short.
Try again to create a longer one.""")


if __name__ == "__main__":
    main()
