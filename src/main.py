from textnode import TextNode, TextType
import shutil
import os
from page import generate_page, generate_pages_recursive


def copy_recursive(source_path, dest_path, dry_run):
    if os.path.isfile(source_path):
        if dry_run:
            print(
                f"This would have run shutil.copy({source_path}, {dest_path})")
        else:
            print(f"Running shutil.copy({source_path}, {dest_path})")
            shutil.copy(source_path, dest_path)
    else:
        if not os.path.exists(dest_path):
            if dry_run:
                print(f"This would have run os.mkdir({dest_path})")
            else:
                print(f"Running os.mkdir({dest_path})")
                os.mkdir(dest_path)

        for child in os.listdir(source_path):
            child_source = os.path.join(source_path, child)
            child_dest = os.path.join(dest_path, child)
            print(f" * {child_source} -> {child_dest}")
            copy_recursive(child_source, child_dest, dry_run)


def copy_content(source_dir, target_dir, dry_run=True):
    if not os.path.isdir(source_dir):
        raise ValueError(f"source directory doesn't exist: {source_dir}")

    source_dir_abspath = os.path.abspath(source_dir)
    target_dir_abspath = os.path.abspath(target_dir)

    copy_recursive(source_dir_abspath, target_dir_abspath, dry_run)


def main():
    node = TextNode("This is some anchor text",
                    TextType.LINK, "https://www.boot.dev")
    print(node)

    # Get the directory where main.py is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Go up one level to the project root
    project_root = os.path.dirname(script_dir)

    static_dir = os.path.join(project_root, "static")
    public_dir = os.path.join(project_root, "public")
    content_dir = os.path.join(project_root, "content")
    template_path = os.path.join(project_root, "template.html")

    print("Deleting public directory...")
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)

    copy_content(static_dir, public_dir, dry_run=False)

    generate_pages_recursive(content_dir, template_path, public_dir)


if __name__ == "__main__":
    main()
