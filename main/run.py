# -----------------------------------------------------------------------------
# PDF Downloader - Run Utility
# File:        run.py
# Description: App to run on console
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# System imports
# -----------------------------------------------------------------------------
import sys
import argparse
import pdf_downloader as pd

# -----------------------------------------------------------------------------
# Costants
# -----------------------------------------------------------------------------

APP_NAME = u"PDF Downloader"
APP_RELEASE = 2.2
APP_COPYRIGHT = u"GlobalData"
APP_YEAR = 2019

excel_file = None


# -----------------------------------------------------------------------------
# Log text on console
# -----------------------------------------------------------------------------
def log_text(text):
    print(u"{}".format(text))


# -----------------------------------------------------------------------------
# Log blank line on console
# -----------------------------------------------------------------------------
def log_newline():
    log_text(
        u"",
    )


# -----------------------------------------------------------------------------
# Log separator line on console
# -----------------------------------------------------------------------------
def log_separator():
    log_text(
        u"-----------------------------------------------------------------------------",
    )


# -----------------------------------------------------------------------------
# Log an Header with given text
# -----------------------------------------------------------------------------
def log_header(title):
    log_newline()
    log_separator()
    log_text(title)
    log_separator()


# -----------------------------------------------------------------------------
# Show the error on the console
# -----------------------------------------------------------------------------
def show_error(error_text):
    if error_text:
        log_newline()
        log_text("[ERROR]: {}".format(error_text))
        log_newline()
        exit()


# -----------------------------------------------------------------------------
# Show the help to the user
# -----------------------------------------------------------------------------
def app_help():
    global APP_NAME
    global APP_RELEASE
    global APP_COPYRIGHT
    global APP_YEAR

    log_text(
        u"{} {} - Lib version [{}] - Copyright {}".format(
            APP_NAME,
            APP_RELEASE,
            APP_COPYRIGHT,
            APP_YEAR,
        )
    )


# -----------------------------------------------------------------------------
# Run the app
# -----------------------------------------------------------------------------
def run():
    if excel_file:
        pd.main(excel_file)


# -----------------------------------------------------------------------------
# Initialize system based on parameters passed on command line
# -----------------------------------------------------------------------------
def init_system(app_args):
    global excel_file

    if app_args.excel_file:
        excel_file = app_args.excel_file
    else:
        print('missing input : excel file')
        sys.exit()


# ------------------------------------------------------------------------------
# Close the system
# -----------------------------------------------------------------------------
def close_system():
    pass


# -----------------------------------------------------------------------------
# Parse arguments on command line
# -----------------------------------------------------------------------------
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--excel_file', help='Provide excel file as input parameter')
    app_args = parser.parse_args()
    return app_args


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    app_help(),
    args = parse_args()
    init_system(args)
    run()
    exit()

# -----------------------------------------------------------------------------
# End Of File
# -----------------------------------------------------------------------------
