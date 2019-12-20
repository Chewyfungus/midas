#!/usr/bin/python3

from logger import Log

# Main Midas entry point
def main():
    l = Log("MainLogger")
    l.debug("stonks")
    l.info("stocks")
    l.warning("Stocks")
    l.error("STOCKS")
    l.critical("STOCKS!!!!!")


if __name__ == "__main__":
    main()
