#!/usr/bin/python3
"""
    Fabric script that distributes an archive to your web servers,
    using the function do_deploy
"""

import os
from fabric.api import *


env.hosts = ["100.25.148.28", "52.86.142.5"]
env.user = "ubuntu"


def do_deploy(archive_path):
    """ Distributes an archive totwo specific web servers """
    if os.path.exists(archive_path):
        archive_filename = os.path.basename(archive_path)
        remote_tmp_path = "/tmp/{}".format(archive_filename)
        remote_extract_path = "/data/web_static/releases/{}".format(
            archive_filename[:-4])

        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(remote_extract_path))
        run("sudo tar -xzf {} -C {}/".format(remote_tmp_path,
                                             remote_extract_path))
        run("sudo rm {}".format(remote_tmp_path))
        run("sudo mv {}/web_static/* {}".format(remote_extract_path,
                                                remote_extract_path))
        run("sudo rm -rf {}/web_static".format(remote_extract_path))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(
            remote_extract_path))

        print("New version deployed!")
        return True

    return False
