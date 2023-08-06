import os
import re
import subprocess
import sys
from abc import ABC, abstractmethod

from pxpip.common import get_bucket_and_key, get_s3_url, get_recursive_file
from pxpip.logger import logger
from pxpip.s3_facade import download_file, upload_file

log = logger(__name__)


class Command(ABC):
    def __init__(self, p_args):
        self.p_args = p_args

    @abstractmethod
    def run(self, *args, **kwargs):
        pass


class S3InstallCommand(Command):
    def __init__(self, p_args=None, s3_url=None):
        super().__init__(p_args)
        self.s3_url = get_s3_url(p_args) if not s3_url else s3_url

    def run(self):
        s3_data = get_bucket_and_key(self.s3_url)
        log.info(f"<< pxpip >> << s3 bucket install >> {s3_data}")
        local_file = download_file(**s3_data)
        pip_command = PipProxyCommand(p_args=["install", local_file])
        pip_command.run()
        os.remove(local_file)


class InstallRecursiveCommand(Command):

    def run(self, *args, **kwargs):
        if recursive_file := get_recursive_file(self.p_args):
            log.info(f"<< pxpip >> << extracting s3 >> {recursive_file}")
            lines_to_proxy = []
            s3_ran = False
            with open(recursive_file) as rf:
                for line in rf.readlines():
                    if s3_url := get_s3_url([line]):
                        install_command = S3InstallCommand(s3_url=s3_url)
                        install_command.run()
                        s3_ran = True
                    else:
                        lines_to_proxy.append(line)

            if lines_to_proxy and s3_ran:
                temp_name = "./_requirements.txt"
                with open(temp_name, 'w') as wf:
                    wf.writelines(lines_to_proxy)

                self.p_args[2] = temp_name

            pip_command = PipProxyCommand(self.p_args)
            pip_command.run()
            if lines_to_proxy and s3_ran:
                log.info("Removing temp requirements file")
                os.remove(self.p_args[2])

        else:
            raise ValueError("No requirements file was supplied.")


class S3PublishCommand(Command):
    def __init__(self, p_args):
        super().__init__(p_args)
        self.s3_url = get_s3_url(p_args)

    def run(self):
        s3_data = get_bucket_and_key(self.s3_url)
        s3_data["file_path"] = self.p_args[1]
        log.info(f"pxpip >> publishing to S3 >> {s3_data}")
        upload_file(**s3_data)


class PipProxyCommand(Command):
    def __init__(self, p_args):
        super().__init__(p_args)

    def run(self):
        process = subprocess.Popen(
            [sys.executable, "-m", "pip", *self.p_args], stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )

        for line in iter(process.stdout.readline, b''):
            print(line.decode("utf-8").strip())
        if exitcode := process.wait():  # 0 means success
            raise ValueError(f"Pip could not process the passed arguments {self.p_args}. exit code : {exitcode}")


class CommandFactory:
    S3_INSTALL_REGEX = re.compile(r'install s3://([^/]+)/(.*?([^/]+)/?)')
    S3_PUBLISH_REGEX = re.compile(r'publish [a-zA-Z0-9./_-]+ s3://([^/]+)/(.*?([^/]+)/?)')
    RECURSIVE_INSTALL = re.compile(r'install -r ([a-zA-Z]+)(.*?([^/]+)/?)')

    @classmethod
    def get_command_class(cls, p_args: list[str]):
        p_str = " ".join(p_args)
        if cls.S3_INSTALL_REGEX.match(p_str):
            return S3InstallCommand(p_args)
        elif cls.RECURSIVE_INSTALL.match(p_str):
            return InstallRecursiveCommand(p_args)
        elif cls.S3_PUBLISH_REGEX.match(p_str):
            return S3PublishCommand(p_args)
        else:
            return PipProxyCommand(p_args)
