#!/usr/bin/env python3


def main():
    import sys
    try:
        from context_cli.core import main
        sys.exit(main(sys.argv))
    except BrokenPipeError:
        # Prevent any errors from showing up if we get a SIGPIPE (for example ctx ... | head)
        sys.stderr.close()
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(1)


if __name__ == '__main__':  # pragma: no cover
    main()
