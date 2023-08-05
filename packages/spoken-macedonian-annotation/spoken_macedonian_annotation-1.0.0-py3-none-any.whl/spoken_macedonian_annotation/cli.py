import argparse
from spoken_macedonian_annotation.annotate import MacAnnotator


def create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser('MacAnnotator',
                                     description='A commandline tool for annotation of spoken Macedonian')
    parser.add_argument('--infile', '-i', type=argparse.FileType('r', encoding='UTF-8'),
                        required=True)
    parser.add_argument('--mark_homonyms',
                        help='marks homonyms in the output',
                        action='store_true',
                        default=False)
    parser.add_argument('--mark_unknown',
                        help='marks unknown words in the output',
                        action='store_true',
                        default=False)
    parser.add_argument('--print_to_txt',
                        help='creates a .txt file and writes the output to it',
                        action='store_true',
                        default=False)

    return parser


def main():
    parser = create_argument_parser()
    args = parser.parse_args()

    if not any([args.infile, args.print_to_txt, args.mark_unknown, args.mark_homonyms]):
        print("No arguments chosen. Type --help to learn about the functionality of this package")
        exit(0)

    if not args.infile:
        print("No input chosen. Type --help to learn about the functionality of this package")
        exit(0)
    text = args.infile.read()
    args.infile.close()
    an = MacAnnotator(mark_homonyms=args.mark_homonyms,
                               mark_unknown_tokens=args.mark_unknown,
                               print_to_txt_file=args.print_to_txt)
    an.annotate(text)


if __name__ == '__main__':
    main()
