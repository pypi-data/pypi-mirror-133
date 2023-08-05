# coding:utf8
import codecs


def read_file(filepath: str) -> str:
    """
    Read and process the input file.

    Parameters
    ----------
    filepath : str : Path to text file.

    -------

    """
    input_file = codecs.open(filepath, "r", "UTF-8")
    text = input_file.read().replace("\r\n", " ").replace('\n\n', " ").replace('\n', " ")
    input_file.close()
    return text


def create_out_file(outfile_name: str) -> str:
    """

    Parameters
    ----------
    outfile_name : Output file name (with extension .txt)

    """
    out_file_name = outfile_name
    out_file = codecs.open(out_file_name, "w", "UTF-8")
    print("\nOutput file '{}' is created.".format(out_file_name))
    return out_file
