import subprocess
import shutil

STUB_MAIN = ["\nint main(int argc, char *argv[]) {",
             "\n   return 0;",
             "\n}"]
MISSING_MAIN = "undefined reference to `main'"


def add_main(filename):
    # copy the original source
    copy_filename = f"{filename.replace(".c", "")}_copy.c"
    shutil.copyfile(filename, copy_filename)

    # append a stub main() to the copy
    with open(copy_filename, "a") as f:
        f.writelines(STUB_MAIN)

    with open(copy_filename, "r") as f:
        # [debug] print entire file
        for line in f.readlines():
            print(line, end="")
        print()

    # return filename for later usage
    return copy_filename


def compile_prog(src_filename):
    success = False  # have we successfully compiled the program?
    src = src_filename

    while not success:
        try:
            # capture_output: capture stdout and stderr
            # check: check process exit status
            subprocess.run(["gcc", "-o", f"{src.replace(".c", ".o")}", src],
                           capture_output=True, check=True)
            success = True
        except subprocess.CalledProcessError as e:
            # gcc returned non-zero exit code

            # print contents of stderr
            error_msg = e.stderr.decode()
            print(f"compilation failed: {error_msg}")

            # TODO handle different cases for compilation failure
            if MISSING_MAIN in error_msg:
                # missing main()
                src = add_main(src)

    # return source filename (TODO clean up compiled objects + copies)
    return src
