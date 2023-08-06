import os.path
import shutil
import yaml
from pathlib import Path

from jinja2 import Template, Environment


def render_string(s, config):
    tem = Environment().from_string(s)
    return tem.render(**config)


def is_template_str(s):
    return "{{" in s


def convert_item_path(path, config):
    new_path = render_string(path, config)
    shutil.move(path, new_path)
    return new_path


def convert_file_content(path, config):
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
    s_out = render_string(s, config)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(s_out)


def read_yaml(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)
def write_yaml(data,path):
    with open(path, 'w', encoding='utf-8') as f:
        return yaml.dump(data,f)

class CodeGenerator:
    def __init__(self, filetypes=None):
        if filetypes is None:
            filetypes = ['text/utf-8']
        self.filetypes = filetypes

    def should_file_be_converted(self, path: str):
        def is_utf8(path):
            "Returns a Unicode object on success, or None on failure"
            try:
                with open(path) as f:
                    data=f.read()
                    data.decode('utf-8')
                    return True
            except UnicodeDecodeError:
                return False
        if os.path.isfile(path):
            for tp in self.filetypes:
                if tp=='text/utf-8' and is_utf8(path):
                    return True
                elif path.endswith(tp):
                    return True
        return False
    def generate(self, template_path, target_path, config_dict: dict, overwrite=False,exists_ok=False):
        if os.path.exists(target_path):
            if overwrite:
                print('Removing %s' % (target_path))
                shutil.rmtree(target_path) if os.path.isdir(target_path) else os.remove(target_path)
            elif exists_ok:
                pass


        if os.path.isfile(template_path):
            shutil.copy(template_path, target_path)
        else:
            assert os.path.isdir(template_path)
            shutil.copytree(template_path, target_path,dirs_exist_ok=exists_ok)
        self.convert_(target_path, config_dict)

    def convert_(self, path, config: dict):
        print('Converting %s ' % (path))
        if is_template_str(path):
            path = convert_item_path(path, config)
        if os.path.isfile(path):
            if self.should_file_be_converted(path):
                convert_file_content(path, config)
            return
        else:
            items = os.listdir(path)
            for item in items:
                self.convert_(os.path.join(path, item), config)




def gencode(src,dst,maker,overwrite=False,exists_ok=False,**kwargs):

    cfg=read_yaml(maker) if maker else dict(params={})
    cfg['params'].update(kwargs)
    cg=CodeGenerator(
        filetypes=cfg['exts'] if 'exts' in cfg else ['text/utf-8'],
    )
    cg.generate(src,dst,cfg['params'],overwrite=overwrite,exists_ok=exists_ok)

def render(path,maker,**kwargs):
    cfg=read_yaml(maker) if maker else dict(params={})
    cfg['params'].update(kwargs)
    cg=CodeGenerator(
        filetypes=cfg['exts'] if 'exts' in cfg else ['text/utf-8'],
    )
    cg.convert_(path,cfg['params'])
