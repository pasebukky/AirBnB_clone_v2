#!/usr/bin/python3
"""
    Fabric script that creates and distributes an archive to your web servers
"""

import os
from datetime import datetime
from fabric.api import *


env.hosts = ["100.25.148.28", "52.86.142.5"]
env.user = "ubuntu"


def do_pack():
    """ Generates a tgz archive path """
    local("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    output = "versions/web_static_{}.tgz".format(date)
    tgz_archive = local("tar -cvzf {} web_static".format(output))

    if tgz_archive.succeeded:
        return output
    else:
        return None


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


def deploy():
    """ Creates and distributes an archive to the web servers """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
