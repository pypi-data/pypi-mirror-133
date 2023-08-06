import os


def write_list_file(list_data,  output_filename, mode="w"):
    """ Write the given list to text file

    parameters:
    list_data (list): data as list
    output_filename (str): output file name, ie. output.txt 
    mode(str): file stream mode with default = "w"
    """
    try:
        ori_umask = os.umask(0)
        with open(output_filename, mode, os.O_RDWR | os.O_CREAT) as f:  # output file name
            if list_data:
                f.writelines(list_data)
    finally:
        os.umask(ori_umask)


def write_dbdata_file(data_as_list, output_filename, mode="w", header_as_list=[], delimiter="\t"):
    """ Export the data (list of tuples) to text file for records.

    parameters:
    data_as_list (list of tuples): row of data in tuples ie. [(row1),(row2) .. (rown)]
    output_filename (str): output file name, ie. output.txt 
    header_as_list (list): header as list if required, ie. ['column1', 'column2',  'column3'.. 'columnN']
    mode(str): file stream mode with default = "w"
    delimiter (str): default as tab delimiter
    """
    try:
        ori_umask = os.umask(0)
        with open(output_filename, mode, os.O_RDWR | os.O_CREAT) as fw:
            if len(header_as_list) > 0:  # if header
                fw.write(delimiter.join(str(item)
                                        for item in header_as_list)+"\n")
            for line in data_as_list:
                fw.write(delimiter.join(str(item) for item in line) + "\n")
    finally:
        os.umask(ori_umask)
