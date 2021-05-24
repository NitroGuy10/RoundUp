# RoundUp by NitroGuy10
# 23 May 2021


import os
import pathlib
import shutil


def is_ignored(path, depth):
    if path.name.startswith('.'):
        # I don't know if this is a bug or a feature,
        # but on Windows permission is always denied for folders with names starting with '.'
        return True
    elif path.name == "__MACOSX":
        return True
    elif depth == 0 and (path.name == "RoundUp.py" or path.name == "RoundUp_Output"):
        return True
    return False


def do_folder(folder_path, output_dir, depth, preservation_depth):
    for item in os.scandir(folder_path):
        if not is_ignored(item, depth):
            print("Item \"" + item.name + "\" found at depth", depth)
            if item.is_file():
                shutil.copy2(item, os.path.join(output_dir, item.name))
                print("Copying: \"" + item.name + "\"")
            elif item.is_dir(follow_symlinks=False):
                if preservation_depth == -1 or depth < preservation_depth:
                    # RoundUp as normal
                    do_folder(item, output_dir, depth + 1, preservation_depth)
                else:
                    # Preserve directory structure
                    print("Preservation depth reached: Copying whole directory: \"" + item.name + "\"")
                    shutil.copytree(item, os.path.join(output_dir, item.name))
        else:
            print("Ignoring: \"" + item.name + "\"")


def main(dir_to_roundup):
    print("Let's RoundUp!")

    print("We're gonna RoundUp: \"" + str(dir_to_roundup) + "\"")
    root_output_dir = os.path.join(dir_to_roundup, "RoundUp_Output")
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

    print("When you're sure you're ready, type \"RoundUp! [preservation_depth=-1]\" to begin. Or type exit to quit.")
    print("To choose a different directory, type do_path=\"<path>\"")
    preservation_depth = -1
    while True:
        user_input = input()
        if user_input.startswith("RoundUp!"):
            for command in user_input.split(" "):  # There is probably a better way to do this
                if command.startswith("preservation_depth="):
                    # preservation_depth: (folders at/beyond this depth will not be unwrapped) (0 is immediate contents)
                    # 0 to preserve everything, -1 to unwrap all
                    preservation_depth = int(command[19:])
            break
        elif user_input.startswith("do_path="):
            # Instead of the current directory, RoundUp a different path
            print("\n\n\n")
            main(pathlib.Path(user_input[8:].replace("\"", "")).absolute())
            return
        elif user_input == "exit":
            return

    print("Commencing RoundUp...")
    os.mkdir(root_output_dir)
    do_folder(dir_to_roundup, root_output_dir, 0, preservation_depth)
    print("All done!")


main(pathlib.Path().absolute())
