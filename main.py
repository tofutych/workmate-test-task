import sys

from services import execute_from_command_line


def main() -> None:
    if len(sys.argv) == 1:
        raise SystemExit(
            "Ошибка: отсутствуют обязательные аргументы. Используйте --help."
        )

    try:
        execute_from_command_line()
    except FileNotFoundError as e:
        print(e)


if __name__ == "__main__":
    main()
