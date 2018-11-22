#!/usr/bin/env python3


def main():
    import sys
    try:
        from .core import main
        sys.exit(main(sys.argv))
    except KeyboardInterrupt:
        sys.exit(1)


if __name__ == '__main__':  # pragma: no cover
    main()
