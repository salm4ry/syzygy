"""C compilation helpers"""

import logging
import subprocess
import shutil

# set up logging
logging.basicConfig()
logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)  # set log level for main

STUB_MAIN = ["\nint main(int argc, char *argv[]) {",
             "\n   return 0;",
             "\n}"]
MISSING_MAIN = "undefined reference to `main'"
OBJ_NAME = "syzygy_obj.tmp"  # always use the same object filename


def add_main(filename):
    """Append a stub main() to a copy of the provided file"""
    # copy the original source
    copy_filename = f"{filename.replace(".c", "")}_copy.c"
    shutil.copyfile(filename, copy_filename)

    # append a stub main() to the copy
    with open(copy_filename, "a", encoding="ascii") as f:
        f.writelines(STUB_MAIN)

    with open(copy_filename, "r", encoding="ascii") as f:
        # [debug] print entire file
        for line in f.readlines():
            logger.debug("%s", line.rstrip())

    # return filename for later usage
    return copy_filename


def compile_prog(src_filename):
    """Compile a C program, adding in a stub main() if omitted

    Return:
        - source filename on success
        - None on error
    """
    success = False  # have we successfully compiled the program?
    src = src_filename

    while not success:
        try:
            # capture_output: capture stdout and stderr
            # check: check process exit status
            subprocess.run(["gcc", "-o", OBJ_NAME, src],
                           capture_output=True, check=True)
            # clean object file
            subprocess.run(["rm", OBJ_NAME], check=True)

            # exit loop
            success = True
        except subprocess.CalledProcessError as e:
            # gcc returned non-zero exit code

            # print contents of stderr
            error_msg = e.stderr.decode()
            logger.error("compilation failed: %s", error_msg)

            if MISSING_MAIN in error_msg:
                # missing main(): append to a copy of the source file,
                # returning the name of the copied source
                src = add_main(src)
            else:
                # compilation failed for another reason- don't attempt to fix
                src = None
                break

    # clean copied source file
    if src is not None and "copy" in src:
        subprocess.run(["rm", src], check=False)

    return src
