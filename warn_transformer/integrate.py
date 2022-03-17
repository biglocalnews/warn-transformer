import logging

logger = logging.getLogger(__name__)


def run():
    # Download the current database

    # Read in the current database

    # Read in new consolidated.csv file

    # Knock out all rows in the new file
    # that are unchanged from the current database

    # Compare the remaining rows against the current
    # database and measure their similarity.

    # If the similarity meets our threshold,
    # mark the record as an amendment

    # If the row in the new file doesn't meet
    # our threshold, mark it as a new record.

    # Overwrite the amendments, storing the old versions somewhere ...

    # Insert the new records with today's timestamp
    pass


if __name__ == "__main__":
    run()
