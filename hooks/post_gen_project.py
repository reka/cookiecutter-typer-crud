import subprocess
import sys


def main():
    print("\n\n")
    print("Project skeleton generated.")
    print("Running post_gen script.")

    if poetry_is_installed():
        poetry_install()
        run_isort()
        run_black()
        run_pytest()
        run_coverage()
    else:
        print_poetry_install_instructions()

    git_init_setting = "{{ cookiecutter.git_initial_commit }}"
    if git_init_setting == "y":
        git_init()

    if poetry_is_installed():
        run_cli()

    print("\n\npost_gen script finished.\n")


def poetry_is_installed():
    print("\nChecking that Poetry is available:")
    check_result = subprocess.run("poetry --version", shell=True)
    return check_result.returncode == 0


def poetry_install():
    print("\n\n******************poetry install************************\n\n")
    subprocess.run("poetry install", shell=True)


def run_isort():
    print("\n\n******************isort************************\n\n")
    subprocess.run("poetry run isort .", shell=True)


def run_black():
    print("\n\n******************black************************\n\n")
    subprocess.run("poetry run black .", shell=True)


def run_pytest():
    print("\n\n******************pytest************************\n\n")
    subprocess.run("poetry run pytest", shell=True)


def run_coverage():
    print("\n\n******************coverage************************\n\n")
    subprocess.run("poetry run make cov", shell=True)


def run_cli():
    print("\n\n******************cli************************\n\n")
    run_cmd("poetry run {{cookiecutter.project_name}} {{cookiecutter.model_name}} ls")


def run_cmd(cmd: str):
    print(cmd)
    subprocess.run(cmd, shell=True)


def print_poetry_install_instructions():
    print("\nPoetry not found.")
    print(
        "Install Poetry following the instructions at https://python-poetry.org/docs/#installation"
    )
    print("Then initialize this project with:")
    print('poetry install -E "tests typing lint docs"')


def git_init():
    print("\n\n******************git init************************\n\n")
    subprocess.run("git init", shell=True)
    subprocess.run("git add .", shell=True)

    commit_msg = "{{ cookiecutter.commit_message }}"
    subprocess.run(f'git commit -m "{commit_msg}"', shell=True)
    subprocess.run("git branch -M main", shell=True)


if __name__ == "__main__":
    sys.exit(main())
