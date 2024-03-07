#!/usr/bin/python3
"""
    Fabric script that creates and distributes an archive to your web servers
"""

import os
from datetime import datetime
from fabric.api import *


env.hosts = ["100.25.148.28", "52.86.142.5"]


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
    if not os.path.isfile(archive_path):
        return False

    archive_filename = archive_path.split("/")[-1]
    name = archive_filename.split(".")[0]

    remote_tmp_path = "/tmp/{}".format(archive_filename)
    remote_extract_path = "/data/web_static/releases/{}/".format(name)

    if put(archive_path, remote_tmp_path).failed:
        return False
    if run("rm -rf {}".format(remote_extract_path)).failed:
        return False
    if run("mkdir -p {}".format(remote_extract_path)).failed:
        return False
    if run("tar -xzf {} -C {}".format(remote_tmp_path,
                                      remote_extract_path)).failed:
        return False
    if run("rm {}".format(remote_tmp_path)).failed:
        return False
    if run("mv {}/web_static/* {}".format(remote_extract_path,
                                          remote_extract_path)).failed:
        return False
    if run("rm -rf {}/web_static".format(remote_extract_path)).failed:
        return False
    if run("rm -rf /data/web_static/current").failed:
        return False
    if run("ln -s {} /data/web_static/current"
       .format(remote_extract_path)).failed:
        return False
    return True


def deploy():
    """ Creates and distributes an archive to the web servers """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
