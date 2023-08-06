import os

try:
    from .bobcat import Bobcat
except:
    from bobcat import Bobcat

def main():
    """Main entrypoint"""
    Bobcat(os.getenv("BOBCAT_IP_ADDRESS")).autopilot()


if __name__ == "__main__":
    main()
