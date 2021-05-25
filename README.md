# RoundUp

Copy all files from a directory tree into a single folder using one Python 3 script.

---
## Quick Start

Move/copy RoundUp.py into the folder you want to RoundUp.

Double-click RoundUp.py if your OS lets you do that.
Otherwise type the following into a terminal.

```commandline
cd <your_directory>
python3 RoundUp.py
```

Follow the prompts, and you'll find your complete RoundUp in the folder called "RoundUp_Output".

---
## Usage and About

RoundUp was designed to automate a process I often have had to do manually.
Specifically, to deal with photos that were automatically organized into folders by programs against my will.

RoundUp by default will search the working directory and ALL of its subfolders (minus a few that I discuss in "Quirks")
for ANY files. ALL of those files will be copied (not moved) into a SINGLE directory called RoundUp_Output.

Here's a visual of what RoundUp does:
```
# BEFORE

My folder
  |---foo.txt
  |---bar.zip
  |---My other folder
        |---baz.html
  |---My other other folder
        |---qux.jar
        |---xyzzy.pdf

# AFTER

RoundUp_Output
  |---foo.txt
  |---bar.zip
  |---baz.html
  |---qux.jar
  |---xyzzy.pdf
  # Of course, your original folders are still there.
  # RoundUp_Output is a NEW folder containing copies of the designated files.
```

RoundUp will warn you if you attempt to RoundUp an abnormally large amount of data,
but YOU ARE ULTIMATELY RESPONSIBLE for ensuring you don't screw up your disk or accidentally copy an absurd amount of data.

If you want to RoundUp a different directory than the one RoundUp assumes you want, use do_path when prompted.

```commandline
# do_path="<path>"

python3 RoundUp.py
<...>
do_path="C:/my_folder"
```

If you only want to unwrap folders up to a certain depth, then you should utilize the preservation_depth functionality.

Setting the preservation_depth will cause RoundUp to RoundUp as usual until it reaches a depth into the directory tree equal to the preservation_depth.
At that point, RoundUp will not attempt to move any deeper into the tree and will instead fully copy any folders it encounters at that depth, rather than try to look inside them.

For example, a preservation_depth of 0 will preserve all immediate contents of the chosen directory, essentially copying the contents unchanged into RoundUp_Output (which is pretty useless).
A preservation_depth of 1 will RoundUp any immediate contents and any contents of immediate subfolders, but folders within those immediate subfolders will be fully copied. Et cetera, et cetera.
The default is a preservation_depth of -1 which does a RoundUp of all files and does not fully copy any folders.

```commandline
# RoundUp! preservation_depth=n

python3 RoundUp.py
<...>
RoundUp! preservation_depth=2
```

---

## Quirks

RoundUp isn't perfect. Here is a list of some of its known quirks.

- On Windows, folders with names starting with '.' are ignored (i.e., not copied or traversed into) because permission is always denied.
  I don't know if this is a bug or a feature with shutil.
- Folders named "__MACOSX" are also ignored for the same reason.
- RoundUp handles duplicate file names a bit weirdly. If a duplicate of an already-copied file is found, the duplicate will be copied as "(1)filename".
  The next duplicate will be "(2)filename". Past (9), however, behavior is weird and untested and you will end up with names like "(1)(9)(9)filename" instead of "(20)filename".
  When in doubt, add up the numbers, I guess. The best way to avoid this is to... not have more than 9 duplicate file names lol.
- At a depth == 0, files named "RoundUp.py" and folders named "RoundUp_Output" are ignored for obvious reasons.
  The RoundUp script *will* get copied if it is not named "RoundUp.py".
- RoundUp only copies. It does not move. Moving would probably require me to implement some security features to ensure your files are not accidentally lost and I am not qualified to do that.
- RoundUp is exceptionally verbose. I will not remove the print() statements so you can if you must.
- If you use RoundUp, you will instantaneously become an extremely cool individual.
