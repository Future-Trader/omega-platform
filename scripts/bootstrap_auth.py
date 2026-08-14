from generators.project import AUTH
from generators.file_writer import FileWriter

writer = FileWriter()


FILES = [
    "router.py",
    "service.py",
    "repository.py",
    "schemas.py",
    "dependencies.py",
    "security.py",
    "constants.py",
    "exceptions.py",
]


def main():

    print("=" * 60)
    print("OMEGA Authentication Bootstrap")
    print("=" * 60)

    for filename in FILES:

        writer.write(
            AUTH / filename,
            f'"""{filename}"""\n',
        )

    print("\nAuthentication scaffold created successfully.")


if __name__ == "__main__":
    main()