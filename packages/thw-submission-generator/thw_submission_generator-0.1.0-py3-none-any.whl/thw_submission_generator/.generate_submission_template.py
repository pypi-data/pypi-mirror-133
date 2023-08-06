#!/usr/bin/env python

import sys
import textwrap

from ruamel import yaml


def write(st):
    sys.stdout.write(st)


def print_section_header(title):
    write("[/TD][/TR][TR][TD][H3][color=#CCAA00]" + title + "[/color][/H3][/TD][/TR][TR][TD]\n")


def get_paragraph(paragraph):
    p = paragraph.strip().replace('\n', ' ').replace('\t', '')
    return textwrap.fill(p, width=90) + "\n\n"


def print_paragraph(paragraph):
    write(get_paragraph(paragraph))


def print_header(map_name, author):
    write("[CENTER]\n[TABLE][TR][TD]\n[CENTER]\n[H3][color=#60A600]")
    write(map_name)
    write("[/color][/H3]\n[color=#CCAA00][B]A map by ")
    write(author)
    write("[/B][/color]\n\n")


def print_contents(introduction, screenshots, icon_table, repo_uri, changelog, credits, contributing):
    write("[BOX=Contents]")
    if introduction:
        write("* Introduction\n")
    if screenshots:
        write("* Screenshots\n")
    if icon_table:
        write(f"* {icon_table['title']}\n")
    if repo_uri:
        write("* Version Control\n")
    if changelog:
        write("* Changelog\n")
    if credits:
        write("* Credits\n")
    if contributing:
        write("* Contributing\n")
    write("[/BOX]\n[/CENTER]\n\n")


def print_introduction(introduction):
    if introduction:
        print_section_header("Introduction")
        for paragraph in introduction.split("\n\n"):
            print_paragraph(paragraph)


def print_screenshots(screenshots):
    if screenshots:
        print_section_header("Screenshots")
        write("\n\n")
        for shot in screenshots:
            write("[hidden=" + shot["caption"] + "]\n[img]" + shot["uri"] + "[/img]\n[/hidden]\n\n")


def print_icon_table(icon_table):
    if icon_table:
        print_section_header(icon_table["title"])
        write("\n\n[TABLE]\n")
        for row in icon_table["contents"]:
            write("[TR]\n[TD][img]" + row["uri"] + "[/img][/TD]\n[TD]")
            write(get_paragraph(row["caption"]).strip())
            write("[/TD]\n[/TR]\n")
        write("[/TABLE]\n\n")


def print_repository_uri(repo_uri):
    if repo_uri:
        print_section_header("Version Control")
        write("\n\n")
        print_paragraph(
            "All iterations of this map are maintained in a public git repository at [url]" + repo_uri + "[/url]"
        )


def write_log_item(log):
    write("[color=#ffcc00]" + log["version"] + "[/color] [color=#999999]" + log["date"] + "[/color]:\n[list]")
    for point in log["changes"]:
        write(get_paragraph("[*] " + point)[0:-2] + "\n")
    write("[/list]\n\n")


def print_changelog(changelog):
    if changelog:
        print_section_header("Changelog")
        write("\n\n")
        for log in changelog[0:5]:
            write_log_item(log)

        if changelog[5:]:
            write("[hidden=Older Changes]")
            for log in changelog[5:]:
                write_log_item(log)

            write("[/hidden]")


def print_credits(credits):
    if credits:
        print_section_header("Credits")
        print_paragraph(", ".join(credits))


def print_contributing(contributing):
    if contributing:
        print_section_header("Contributing")
        print_paragraph(contributing)


def print_footer():
    write("[/TD][/TR][/TABLE]\n[/CENTER]\n")


def main():
    if not len(sys.argv) > 1:
        sys.exit("Usage: ./.generate_submission_template.py config.yaml")
    with open(sys.argv[1], 'r') as f:
        config = yaml.load(f.read(), Loader=yaml.Loader)

        print_header(config["map_name"], config["author"])
        print_contents(
            config["introduction"],
            config["screenshots"],
            config["icon_table"],
            config["repo_uri"],
            config["changelog"],
            config["credits"],
            config["contributing"]
        )
        print_introduction(config["introduction"])
        print_screenshots(config["screenshots"])
        print_icon_table(config["icon_table"])
        print_repository_uri(config["repo_uri"])
        print_changelog(config["changelog"])
        print_credits(config["credits"])
        print_contributing(config["contributing"])
        print_footer()


if __name__ == '__main__':
    main()
