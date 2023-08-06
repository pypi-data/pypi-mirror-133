import os

from .bobcat import Bobcat


def main():
    """Main entrypoint"""
    bobcat = Bobcat(os.getenv("BOBCAT_IP_ADDRESS"))
    bobcat.autopilot()


if __name__ == "__main__":
    main()
