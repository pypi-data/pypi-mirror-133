# -*-coding:utf-8 -*-
u"""
:创建时间: 2021/12/19 10:44
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:QQ: 2921251087
:爱发电: https://afdian.net/@Phantom_of_the_Cang
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127

"""
from __future__ import unicode_literals, print_function

from abc import abstractmethod

import ast
import os
import locale

import astunparse

from pyeal.res import BaseRes

from pyeal.module_data import ModuleData


def replace_node(rn, t, key):
    if hasattr(rn, "body"):
        if isinstance(rn.body, list):
            body = []
            for n in rn.body:
                if isinstance(n, t):
                    body.append(key(n))
                else:
                    body.append([n])
            rn.body = [ii for i in body for ii in i]
            for n in rn.body:
                replace_node(n, t, key)


class BuilderBase(object):
    def __init__(self, source, target):
        """
        :type source: BaseRes
        :type target: BaseRes
        """
        self.source = source
        self.target = target

    @abstractmethod
    def build(self):
        pass


class EncapsulationBuilder(BuilderBase):
    """打包编译器"""

    def __init__(self, source, target, name, code, exec_file_name="exec.py"):
        """
        :type source: BaseRes
        :type target: BaseRes
        :type name: unicode
        :type exec_file_name: unicode
        """
        super(EncapsulationBuilder, self).__init__(source, target)
        self.name = name
        self.code = code
        self.exec_file_name = exec_file_name
        self.module_data = ModuleData(self.source)

    def target_name(self, p):
        return "{}_{}".format(self.name, p)

    def target_path(self, p):
        return "{}_{}".format(self.name, p)

    def compile_import_node(self, n, m):
        alias_list = []
        for i in n.names:
            if m is None:
                r_find_name = None
            else:
                r_find_name = self.module_data.relative_find_module(i.name, m)
            name = self.module_data.find_module(i.name)
            if r_find_name is None and name is not None:
                target_name = self.target_name(name)
                alias_list.append(ast.alias(asname=name.split(".")[0],
                                            name=target_name.split(".")[0]))
                alias_list.append(ast.alias(asname=i.asname,
                                            name=target_name))
            else:
                alias_list.append(i)
        return [ast.Import(names=[i]) for i in alias_list]

    def compile_import_from_node(self, n, m):
        if n.level == 0:
            nodes = []
            if m is None:
                r_find_name = None
            else:
                r_find_name = self.module_data.relative_find_module(n.module, m)
            name = self.module_data.find_module(n.module)
            if r_find_name is None and name is not None:
                nodes.append(ast.ImportFrom(level=0,
                                            module=self.target_name(name),
                                            names=n.names))
            else:
                nodes.append(n)
            return nodes
        else:
            return [n]

    def compile_module(self, code, m):
        """
        :type code: bytes
        :type m: unicode|None
        :return:
        """
        node = ast.parse(code)

        replace_node(node, ast.Import, key=lambda n: self.compile_import_node(n, m))
        replace_node(node, ast.ImportFrom, key=lambda n: self.compile_import_from_node(n, m))
        code = astunparse.unparse(node)
        return code.encode("utf-8")

    def build(self):
        compiled = set()
        for m, f in self.module_data.module_name_and_paths():
            if f in compiled:
                continue
            compiled.add(f)
            code = self.source.read(f)
            code = self.compile_module(code, m)
            self.target.write(self.target_path(f), code)
        code = self.compile_module(self.code, None)
        self.target.write(self.exec_file_name, code)
        for f in self.source.files():
            if not f in compiled:
                self.target.write(f, self.source.read(f))


class InstallBuilder(BuilderBase):
    PATH = os.path.dirname(os.path.abspath(__file__))
    with open(os.sep.join((PATH, "mel_template_lib.mel")), "rb") as f:
        mel_template_lib_code = f.read().decode("utf-8")
    mel_template = r'''startInstall(
    "exec(compile(open(plugin_path+" + <<exec_file_name>> + ",'rb').read(), plugin_path+" + <<exec_file_name>> + ", 'exec'), globals(), locals())", 
    <<ann>>, 
    "dist/log.ico", 
    <<plugin_path>>
    );'''

    def __init__(self, source, target, log, ann, install_mel_name="install.mel", exec_file_name="exec.py"):
        super(InstallBuilder, self).__init__(source, target)
        self.install_mel_name = install_mel_name
        self.exec_file_name = exec_file_name
        self.log = log
        self.ann = ann

    def build(self):
        plugin_path = "dist/plugin"
        for f in self.source.files():
            self.target.write(self.target.sep().join((plugin_path, f)), self.source.read(f))
        t = self.mel_template
        t = t.replace("<<exec_file_name>>", '"\'{}\'"'.format(self.exec_file_name))
        t = t.replace("<<ann>>", '"{}"'.format(self.ann))
        t = t.replace("<<plugin_path>>", '"{}/"'.format(plugin_path))
        # 以系统编码写入安装文件
        self.target.write(self.install_mel_name, (self.mel_template_lib_code + t).encode(locale.getpreferredencoding()))
        self.target.write(self.target.sep().join(("dist", "log.ico")), self.log)


if __name__ == "__main__":
    from pyeal.res import LocalRes, DirectoryRes

    root = r"D:\backup_to_cloud\dev\python_for_maya\package\seal\test"
    src = LocalRes(root + r"\src")
    build = LocalRes(root + r"\build")
    mid = DirectoryRes(build, "mid")
    d0 = DirectoryRes(mid, "0")
    dist = DirectoryRes(build, "dist")
    EncapsulationBuilder(src,
                         d0,
                         "test_seal_name",
                         u'''import main
from main import main
main()''').build()
    InstallBuilder(d0, dist, "", "这是一段注释~").build()
