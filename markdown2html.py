#!/usr/bin/python3
"""
script markdown2html.py that takes an argument 2 strings:

First argument is the name of the Markdown file
Second argument is the output file name
"""


def validate_bold(line):
    """
    Validate if bold or italic text.
    """
    index = line.find("**")
    res_str = ""

    if index != -1:
        res_str += line[:index] + "<b>"
        new_str = line[index + 2:]
        idx = new_str.find("**")
        if idx != -1:
            if idx + 1 == len(new_str):
                result += new_str[:idx] + "</b>\n"
            else:
                res_str += new_str[:idx] + "</b>"
                res_str += validate_bold(new_str[idx + 2:])

        else:
            res_str = line

    else:
        res_str = line

    final_str = validate_em(res_str)

    return final_str


def validate_em(line):
    """
    Validate if the line has italic text.
    """
    index = line.find("__")
    result = ""

    if index != -1:
        result += line[:index] + "<em>"
        new_str = line[index + 2:]
        idx = new_str.find("__")
        if idx != -1:
            if idx + 1 == len(new_str):
                result += new_str[:idx] + "</em>\n"
            else:
                result += new_str[:idx] + "</em>"
                result += validate_em(new_str[idx + 2:])

        else:
            result = line

    else:
        result = line

    return result


if __name__ == "__main__":
    import sys
    import os

    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        exit(1)
    if os.path.exists(sys.argv[1]) is False:
        sys.stderr.write("Missing {}\n".format(sys.argv[1]))
        exit(1)

    html_file = open(sys.argv[2], 'w')
    html_titles = {
        "######": ["<h6>", "</h6>"],
        "#####": ["<h5>", "</h5>"],
        "####": ["<h4>", "</h4>"],
        "###": ["<h3>", "</h3>"],
        "##": ["<h2>", "</h2>"],
        "#": ["<h1>", "</h1>"]
    }

    with open(sys.argv[1], "r") as md_file:
        lines = md_file.readlines()
        for i in range(len(lines)):
            line = validate_bold(lines[i])

            if line == "\n" and lines[i - 1] == "\n"\
                    or line == "\n" and lines[i + 1] == "\n":
                continue
            if line.startswith("#"):
                for title in html_titles:
                    if line.startswith(title):
                        html_file.write(html_titles[title][0] +
                                        line[len(title) + 1:-1] +
                                        html_titles[title][1] + "\n")
                        break
            elif line.startswith("- "):
                if i == 0 or lines[i - 1].startswith("- ") is False:
                    html_file.write("<ul>\n<li>" + line[2:-1] + "</li>\n")
                if i != 0 and lines[i - 1].startswith("- "):
                    html_file.write("<li>" + line[2:-1] + "</li>\n")
                if i == len(lines) - 1 or lines[i + 1].\
                        startswith("- ") is False:
                    html_file.write("</ul>\n")

            elif line.startswith("* "):
                if i == 0 or lines[i - 1].startswith("* ") is False:
                    html_file.write("<ol>\n<li>" + line[2:-1] + "</li>\n")
                if i != 0 and lines[i - 1].startswith("* "):
                    html_file.write("<li>" + line[2:-1] + "</li>\n")
                if i == len(lines) - 1 or lines[i + 1].\
                        startswith("* ") is False:
                    html_file.write("</ol>\n")

            else:
                if i != 0 and lines[i - 1] == "\n":
                    html_file.write("<p>\n" + line)
                if i == 0 and lines[i] != "\n":
                    html_file.write("<p>\n" + line)
                if i == len(lines) - 1 or lines[i + 1] == "\n":
                    html_file.write("</p>\n")
                if line != "\n" and i < len(lines) - 1\
                        and lines[i + 1] != "\n":
                    html_file.write("<br/>\n" + lines[i + 1])

    html_file.close()
    md_file.close()

    exit(0)
