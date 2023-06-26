import main_dash
import main_tkinter

DEBUG: bool = False
RUNTYPE: str = "tkinter"


def main():
    match RUNTYPE:
        case "dash":
            main_dash.main()
        case "tkinter":
            main_tkinter.main()
        case _:
            raise ValueError(f"Invalid run type: {RUNTYPE}")


if __name__ == "__main__":
    main()
