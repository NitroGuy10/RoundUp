import os
import pathlib
import shutil


def is_unwrappable(path):  # TODO are there even any cases where this is applicable?
    return False


def is_ignored(path, depth):
    if path.name.startswith('.'):
        # I don't know if this is a bug or a feature but permission is always denied for folders starting with '.'
        return True
    elif path.name == "__MACOSX":
        return True
    elif depth == 0 and (path.name == "RoundUp.py" or path.name == "RoundUp_Output"):
        return True
    return False


def do_folder(folder_path, output_dir, depth):
    for item in os.scandir(folder_path):
        if not is_ignored(item, depth):
            if item.is_file() or is_unwrappable(item):
                shutil.copy2(item, os.path.join(output_dir, item.name))
                print("copying:", item.name)
            elif item.is_dir(follow_symlinks=False):
                new_dir = os.path.join(output_dir, item.name)
                print("making new directory:", new_dir)
                os.mkdir(new_dir)
                do_folder(item, new_dir, depth + 1)


def main():
    print("Let's RoundUp!")

    dir_to_roundup = pathlib.Path("C:\\Users\\naviy\\Desktop\\Programming\\RoundUp\\test_folder")
    print("We're gonna RoundUp: \"" + str(dir_to_roundup) + "\"")
    root_output_dir = dir_to_roundup.parent.joinpath("RoundUp_Output")
    print("Into: \"" + str(root_output_dir) + "\"\n")

    print("Calculating size of your RoundUp...")
    roundup_size = 0
    for root, dirs, files in os.walk(dir_to_roundup):
        for name in files:
            roundup_size += os.path.getsize(os.path.join(root, name))

    print("Your RoundUp size is:", roundup_size, "bytes")
    print("(or", roundup_size / 1000, "KB)")
    print("(or", roundup_size / 1000000, "MB)")
    print("(or", roundup_size / 1000000000, "GB)")
    print("IMPORTANT: Check to see if the above values make sense for what you are trying to RoundUp.\n")

    if roundup_size > 100000000000:
        print("You're moving/copying over 100 GB of files.\n"
              "THAT IS AN ABSOLUTELY FREAKING MASSIVE AMOUNT OF DATA!!!!!\n"
              "Be CERTAIN WITHOUT A SINGLE DOUBT that you have chosen the correct directory!!!\n")
    elif roundup_size > 10000000000:
        print("You're moving/copying over 10 GB of files. That's a LOT!\n"
              "Be CERTAIN that you have chosen the correct directory.\n")
    elif roundup_size > 1000000000:
        print("You're moving/copying over 1 GB of files.\n"
              "Be CERTAIN that you have chosen the correct directory.\n")

    print("When you're sure you're ready, type \"RoundUp! [max_depth=-1]\" to begin. Or type exit to quit.")
    while True:
        user_input = input()
        if user_input.startswith("RoundUp!"):
            break  # TODO implement max_depth (folders beyond this depth will not be unwrapped) (-1 to unwrap all)
        elif user_input == "exit":
            return

    print("Commencing RoundUp...")
    shutil.rmtree(root_output_dir)  # TODO for testing
    os.mkdir(root_output_dir)
    do_folder(dir_to_roundup, root_output_dir, 0)


main()
