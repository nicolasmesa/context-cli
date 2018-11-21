#!/usr/bin/env python3


def main():
    from .core import UserException
    import sys
    try:
        from .core import main
        sys.exit(main(sys.argv))
    except UserException as e:
        sys.stderr.write(str(e) + '\n')
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(1)


if __name__ == '__main__':
    main()
