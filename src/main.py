from shutil import copytree, rmtree

from generator import generate_page_recursive


def static_to_public():
    try:
        rmtree("public")
        copytree("static", "public", dirs_exist_ok=True)
    except Exception as e:
        print(e)


def main():
    static_to_public()
    generate_page_recursive("content/", "templates/template.html", "public/")


main()
