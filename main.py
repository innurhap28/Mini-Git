# 프로그램 시작점, REPL 실행

from mini_git import MiniGit

def run_cli():
    git = MiniGit()

    while True:
        try:
            command = input("mini-git> ")
        except (KeyboardInterrupt, EOFError):
            print()
            break

        if not command.strip():
            continue

        parts = command.split(maxsplit=1)
        cmd = parts[0].upper()

        if cmd in ("EXIT", "QUIT"):
            break

        try:
            if cmd == "INIT":
                if len(parts) != 2:
                    print("Invalied args")
                    continue
                git.init(parts[1])
                print("Initialized repository")

            elif cmd == "BRANCH":
                if len(parts) != 2:
                    print("Invalid args")
                    continue
                branch_name = parts[1].strip()
                git.branch(branch_name)
                print(f"Created branch '{branch_name}'.")

            elif cmd == "SWITCH":
                if len(parts) != 2:
                    print("Invalid args")
                    continue
                branch_name = parts[1].strip()
                git.switch(branch_name)
                print(f"Switched to branch '{branch_name}'.")

            elif cmd == "COMMIT":
                if len(parts) != 2:
                    print("Invalid args")
                    continue
                message = parts[1].strip()
                if (
                    len(message) >= 2
                    and message[0] == '"'
                    and message[-1] == '"'
                ):
                    message = message[1:-1]
                commit = git.commit(message)
                print(f"Committed {commit.hash}")

            elif cmd == "LOG":
                if len(parts) == 1:
                    commits = git.log()
                else:
                    option = parts[1]
                    if option == "--sort-by=date":
                        commits = git.log_sorted("date")
                    elif option == "--sort-by=author":
                        commits = git.log_sorted("author")
                    else:
                        print("Invalid args")
                        continue
                for commit in commits:
                    print(
                        f"{commit.hash} "
                        f"{commit.author} "
                        f"{commit.timestamp} "
                        f"{commit.message}"
                    )
            elif cmd == "PATH":
                if len(parts) != 2:
                    print("Invalid args")
                    continue
                args = parts[1].split()
                if len(args) != 2:
                    print("Invalid args")
                    continue
                result = git.path(args[0], args[1])

                if result is None:
                    print("No path")
                else:
                    print("->".join(result))

            elif cmd == "ANCESTORS":
                if len(parts) != 2:
                    print("Invalid args")
                    continue
                commits = git.ancestors(parts[1])
                for commit in commits:
                    print(commit.hash)

            elif cmd == "SEARCH":
                if len(parts) != 2:
                    print("Invalid args")
                    continue
                argument = parts[1]

                if argument.startswith("--author="):
                    author = argument[len("--author="):]
                    if not author:
                        print("Invalid args")
                        continue
                    commits = git.search(author=author)
                else:
                    commits = git.search(keyword=argument)

                for commit in commits:
                    print(
                        f"{commit.hash} "
                        f"{commit.author} "
                        f"{commit.timestamp} "
                        f"{commit.message}"
                    )

            else:
                print("Unknown command")

        except KeyError:
            print("Unknown commit")
        except ValueError as e:
            print(e)
        except RuntimeError as e:
            print(e)


def main():
    run_cli()

if __name__ == "__main__":
    main()