import argparse
import logging
import os
import sys

def main_locust():
    """ Performance test with locust: parse command line options and run commands.
    """
    try:
        import locusts
    except ImportError:
        print("Locust is not installed, exit.")
        exit(1)

    sys.argv[0] = 'locust'
    if len(sys.argv) == 1:
        sys.argv.extend(["-h"])

    if sys.argv[1] in ["-h", "--help", "-V", "--version"]:
        locusts.main()
        sys.exit(0)

    try:
        testcase_index = sys.argv.index('-f') + 1
        assert testcase_index < len(sys.argv)
    except (ValueError, AssertionError):
        print("Testcase file is not specified, exit.")
        sys.exit(1)

    testcase_file_path = sys.argv[testcase_index]
    sys.argv[testcase_index] = locusts.parse_locustfile(testcase_file_path)

    if "--full-speed" in sys.argv:
        locusts.run_locusts_at_full_speed(sys.argv)
    else:
        locusts.main()

if __name__ == '__main__':
    main_locust()