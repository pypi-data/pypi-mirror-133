import argparse
import glob
import os
from distutils.util import strtobool
from ./model import BiSeNet

import filetype
from tqdm import tqdm

import sys 
sys.path.append("..") 
from interfaces import parsing_face, parsing_faces

@parsing.command()
@parsing.argument('in_path')
@parsing.argument('out_path')
def main(in_path, out_path):
    # model_path = os.environ.get(
    #     "U2NETP_PATH",
    #     os.path.expanduser(os.path.join("~", ".u2net")),
    # )
    model_path='../.cache/face_parsing/79999_iter.pth'
    model=BiSeNet()
    model.load_state_dict(torch.load(model_path))
    


    r = lambda i: i.buffer.read() if hasattr(i, "buffer") else i.read()
    w = lambda o, data: o.buffer.write(data) if hasattr(o, "buffer") else o.write(data)

    if os.path.isdir(in_path):
        if os.path.isdir(out_path):
            out_folder = out_path
        else:
            out_folder = out_path.rsplit('/')[0]

        # input_paths = [full_paths[0]]
        input_paths = os.path.listdir(in_path)
        output_path = full_paths[1]

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        files = set()

        for path in input_paths:
            if os.path.isfile(path):
                files.add(path)
            else:
                input_paths += set(glob.glob(path + "/*"))

        for fi in tqdm(files):
            fi_type = filetype.guess(fi)

            if fi_type is None:
                continue
            elif fi_type.mime.find("image") < 0:
                continue

            with open(fi, "rb") as input:
                with open(
                    os.path.join(
                        output_path, os.path.splitext(os.path.basename(fi))[0] + ".png"
                    ),
                    "wb",
                ) as output:
                    w(
                        output,
                        parsing_face(
                            r(input)
                    )

    else:
        if os.path.isdir(out_path):
            out_path = os.path.join(output_path, os.path.splitext(os.path.basename(in_path))[0] + ".png"
        w(
            out_path,
            parsing_face(
                r(in_path)
            ),
        )


if __name__ == "__main__":
    main()
