"""
Names:  Vincent Damen, Marit Beerepoot, Jessy Bosman & Bart de Haan
Course: Zoekmachines
"""
import requests
import sys
import os


def print_help():
    print("How to use this script:")
    print("python send_data_to_elasticsearch.py folder/containing/the/data")


def handle_arguments(argv):
    argc = len(argv)
    if argc == 1:
        print("Error, no folder provided.")
        print_help()
        return None
    else:
        return argv[1]


def get_files(directory):
    """
    Returns all the files in a directory with the path located from pwd.
    """
    files = os.listdir(directory)
    out = []

    for f in files:
        out.append(directory + f)

    return out


def read_file(file_path):
    """
    Reads and returns the text in a file.
    """
    f = open(file_path, 'r')
    txt = f.read()
    f.close()
    return txt


def split_txt(txt, size=50000000):
    txt_lines = txt.splitlines()
    chunk = ""
    out = []

    for i in range(0, len(txt_lines), 2):
        if sys.getsizeof(chunk) >= size:
            out.append(chunk)
            chunk = ""

        new_item = "\n" + txt_lines[i] + "\n" + txt_lines[i + 1]
        chunk += new_item

    out.append(chunk)
    return out


def send_file_data(f):
    print("Going to send " + f)
    txt = read_file(f)
    txt_size = sys.getsizeof(txt)

    if txt_size > 50000000:
        print("Splitting the file up")
        txt = split_txt(txt)
    else:
        txt = [txt]

    i = 1
    for data in txt:
        print("Sending data chunk: " + str(i) + "/" + str(len(txt)))
        r = requests.post("http://localhost:9200/_bulk", data=data)
        print("Response: " + str(r))
        i += 1


def main():
    # Get all the data files in the directory.
    directory = handle_arguments(sys.argv)
    if directory is None:
        return

    # Get all the files in the directory.
    files = get_files(directory)
    print(files)

    # Send the content of every file to elasticsearch.
    for f in files:
        send_file_data(f)


if __name__ == "__main__":
    main()
