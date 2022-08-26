import pathlib
import sys


if __name__ == '__main__':
    app_dir = pathlib.Path(sys.argv[0]).absolute().parent
    with open("iptv parser.desktop", "w") as f:
        f.write("[Desktop Entry]\n")
        f.write("Type=Application\n")
        f.write("Name=IPTV Parser\n")
        f.write("Path={}\n".format(app_dir))
        f.write("Exec=python{} ./main.py\n".format(".".join(sys.version.split(" ")[0].split(".")[:2])))
        f.write("Icon={}\n".format(app_dir.joinpath("icon.png")))
