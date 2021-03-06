import glob
import json
import os
import os.path as op
import pathlib
import shutil
import subprocess
import sys
from datetime import datetime


def screenshot(config):
    """create screenshot of input files"""
    s = """
!============
!{input_name}
!============

{input_content}
"""

    text = ""
    text += s.format(
        input_name=pathlib.Path(config.DRAGON_INPUT_FILE).name,
        input_content=pathlib.Path(config.DRAGON_INPUT_FILE).read_text()
    )

    if hasattr(config, "DRAGON_INPUT_SUPPORT_FILES"):
        for file in sorted(config.DRAGON_INPUT_SUPPORT_FILES):
            text += s.format(
                    input_name=pathlib.Path(file).name,
                    input_content=pathlib.Path(file).read_text()
                )

    filename = f'{pathlib.Path(config.OUTPUT_DIR).name}.input'
    p = pathlib.Path(config.OUTPUT_DIR) / filename
    p.write_text(text)


def init(config):
    """initialize calculation"""
    # create output directory if missing
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)

    # cleanup previous calculation results
    files = glob.glob(op.join(config.OUTPUT_DIR, "*"))
    for f in files:
        os.remove(f)

    # remove old symlink and create new one
    if op.isfile(config.LIB_SYMLINK):
        os.remove(config.LIB_SYMLINK)

    try:
        os.symlink(config.LIB_FILE, config.LIB_SYMLINK)
    except FileExistsError:
        pass

    # copy input file into output directory
    shutil.copy(config.DRAGON_INPUT_FILE, config.OUTPUT_DIR)
    
    if hasattr(config, "DRAGON_INPUT_SUPPORT_FILES"):
        for file in config.DRAGON_INPUT_SUPPORT_FILES:
            shutil.copy(file, config.OUTPUT_DIR)

    # check all paths/files exist
    assert op.isdir(config.LIB_DIR) == True, "library directory missing"
    assert op.isfile(config.LIB_FILE) == True, "library file is missing"
    assert op.isfile(config.LIB_SYMLINK) == True, "symlink is missing"
    assert op.isfile(config.DRAGON_INPUT_FILE) == True, "dragon input file is missing"
    assert op.isfile(config.DRAGON_EXE) == True, "dragon exe is missing"

    # write config file
    with open(op.join(config.OUTPUT_DIR, "config.json"), "w") as f:
        f.write(json.dumps({k: v for k, v in dict(vars(config)).items() if not k.startswith('__')}, indent=4))

    screenshot(config)


def save_pid(file_dir, process_id):
    """save process id to file"""

    print("process id {}".format(process_id))
    file_name = op.join(file_dir, "{}.pid".format(process_id))
    with open(file_name, "w") as f:
        f.write("process id: {}".format(process_id))


def execute(config, background=True):
    """
    This script will immitate the following behavior
    
        $ /path/to/dragon_exe < file.in > file.out
    
    To run the script
    
        $ python3 run_dragon.py
    
    which will run the simulation in background 
    (default behavior set by `background=True`)
    and return the process id.
    To follow up the process use top
    
        $ top -p process-id

    or tail command

        $ tail -f -n +1 $(ls -td -- output*/ | head -n 1)*.result | nl

    To run in debug mode

        $ DEBUG=1 python3 run_dragon.py

    which will write the output of the simulation
    both to terminal and *.result file.
    """
    
    init(config)
    
    input_ = open(config.DRAGON_INPUT_FILE)
    output_ = open(config.DRAGON_OUTPUT_FILE, 'w')

    if background and 'DEBUG' not in os.environ:
        p = subprocess.Popen(
            config.DRAGON_EXE, 
            stdin=input_, 
            stdout=output_, 
            cwd=config.OUTPUT_DIR
        )
        save_pid(config.OUTPUT_DIR, p.pid)
    else:
        p = subprocess.Popen(
            config.DRAGON_EXE,
            stdout=subprocess.PIPE,
            stdin=input_,
            bufsize=1,
            universal_newlines=True,
            cwd=config.OUTPUT_DIR
        )
        for line in p.stdout:
            output_.write(line)
            print(line, end="")
            sys.stdout.flush()
            
        p.wait()
        if p.returncode != 0:
            raise subprocess.CalledProcessError(p.returncode, p.args)
    
    return p


class Config(object):
    CWD = os.getcwd()
    INPUT = list(pathlib.Path(CWD).glob('*.x2m'))[0].stem
    OUTPUT_DIR = op.join(CWD, "output" + "_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    LIB_DIR = os.getenv("DRAGON_LIB_DIR") or "/home/legha/bin/libraries/l_endian"
    LIB_FILE = op.join(LIB_DIR, "draglibJeff3p1p1SHEM295")
    LIB_SYMLINK = op.join(OUTPUT_DIR, "DLIB_295")
    DRAGON_EXE = os.getenv("DRAGON_EXE") or "/home/legha/bin/Version5_ev1849/Dragon/bin/Linux_x86_64/Dragon"
    DRAGON_INPUT_FILE_NAME = INPUT + ".x2m"
    DRAGON_INPUT_FILE = op.join(CWD, DRAGON_INPUT_FILE_NAME)
    DRAGON_INPUT_SUPPORT_FILES = [str(x) for x in pathlib.Path(CWD).glob('*.c2m')]
    DRAGON_OUTPUT_FILE = op.join(OUTPUT_DIR, INPUT + ".result")


execute(config=Config, background=True)  # .wait()
