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
    """ Generates .tgz archive from the contents of the web_static folder """
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    time_format = "%Y%m%d%H%M%S"
    output = "versions/web_static_{}.tgz".format(
        datetime.utcnow().strftime(time_format))
    try:
        print("Packing web_static to {}".format(output))
        local("tar -cvzf {} web_static".format(output))
        size = os.stat(output).st_size
        print("web_static packed: {} -> {} Bytes".format(output, size))
    except Exception:
        output = None
    return output


def do_deploy(archive_path):
    """ Distributes an archive totwo specific web servers """
    if not os.path.exists(archive_path):
        return False
    try:
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
    except Exception as e:
        return False


def deploy():
    """ Creates and distributes an archive to the web servers """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
