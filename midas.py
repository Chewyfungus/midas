#!/usr/bin/python3
key = open("bin/API/key.txt")
from logger import Log

# Main Midas entry point
def main():
    l = Log("MainLogger")
    l.debug("stonks")
    l.info("stocks")
    l.warning("Stocks")
    l.error("STOCKS")
    l.critical("STOCKS!!!!!")

    l.info(key.read())


if __name__ == "__main__":
    main()
