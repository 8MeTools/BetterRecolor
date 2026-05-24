import os
import shutil


def remove_json_files(files):
    for path in files:
        os.remove(path)


def move_all_files(src_dir, dst_dir):
    os.makedirs(dst_dir, exist_ok=True)
    for name in os.listdir(src_dir):
        src = os.path.join(src_dir, name)
        dst = os.path.join(dst_dir, name)
        if os.path.isdir(src) and os.path.isdir(dst):
            move_all_files(src, dst)
            os.rmdir(src)
        else:
            if os.path.exists(dst):
                if os.path.isdir(dst):
                    shutil.rmtree(dst)
                else:
                    os.remove(dst)
            shutil.move(src, dst)
