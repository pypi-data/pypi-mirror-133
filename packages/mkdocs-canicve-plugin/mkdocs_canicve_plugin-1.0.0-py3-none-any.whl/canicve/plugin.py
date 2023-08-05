#!/usr/bin/env python
"""
This plugin generates a coverage file as well as inserts markdown
at the beginning of a file that has coverage
"""

import json
import types

from collections  import defaultdict
from pathlib import Path
from re import search, DOTALL, MULTILINE
from yaml import load, FullLoader, YAMLError
from jinja2 import Environment, FileSystemLoader
from mkdocs.structure.files import File
from mkdocs.plugins import BasePlugin
from mkdocs.config.config_options import Type
from mkdocs.__main__ import log

class CanICVEPlugin(BasePlugin):
    """
    Creates "canicve.md" file containing a dynamic search bar for site data
    """

    config_scheme = (
        ('filename', Type(str, default='canicve.md')),
        ('folder', Type(str, default='aux/data')),
        ('link_base_DIRECT', Type(str, default='{}')),
        ('link_base_EDB', Type(str, default='https://www.exploit-db.com/exploits/{}')),
        ('link_base_GL', Type(str, default='https://gitlab.com/{}')),
        ('link_base_GH', Type(str, default='https://github.com/{}')),
        ('link_base_GHG', Type(str, default='https://gist.github.com/{}')),
        ('link_base_TENABLE', Type(str, default='https://www.tenable.com/cve/{}')),
        ('link_base_RHEL', Type(str, default='https://access.redhat.com/security/cve/{}')),
        ('link_base_DEBIAN', Type(str, default='https://security-tracker.debian.org/tracker/{}')),
        ('link_base_UBUNTU', Type(str, default='https://ubuntu.com/security/{}')),
        ('link_base_SUSE', Type(str, default='https://www.suse.com/security/cve/{}.html')),
        ('link_base_NVD', Type(str, default='https://nvd.nist.gov/vuln/detail/{}')),
        ('link_base_MITRE', Type(str, default='https://cve.mitre.org/cgi-bin/cvename.cgi?name={}')),
        ('link_base_CVD', Type(str, default='https://www.cvedetails.com/cve/{}')),
        ('link_base_ORACLE', Type(str, default='https://linux.oracle.com/cve/{}.html')),
        ('link_base_R7', Type(str, default='https://www.rapid7.com/db/?q={}')),
        ('link_base_MARC', Type(str, default='https://marc.info/?l=full-disclosure&s={}')),
        ('link_base_GENTOO', Type(str, default='https://bugs.gentoo.org/show_bug.cgi?id={}')),
        ('link_base_GHCS', Type(str, default='https://github.com/search?type=Code&q=%22{}%22')),
        ('template', Type(str)),
        ('css_name', Type(str, default='.md-button')),
    )

    def __init__(self):
        self.page_metadata = {}
        self.page_coveragedata = {}
        self.filename = "canicve.md"
        self.folder = "aux/data"
        self.template = None
        self.css_name = ".md-button"
        self.templ = None

    #pylint: disable=unused-argument
    def on_page_markdown(self, markdown, page, config, files):
        page_vulnerable = self.page_metadata.get(page.file.src_path, {}).get("vulnerable", False)

        if page_vulnerable:
            vulnerable_markdown = f"""## vulnerability Matrix
|     OS    |   OS Version   |  Architecture  |  Item Version  | Verified PoC Links | 
| --------- | -------------- | -------------- | -------------- | ------------------ | 
"""

            for entry in page_vulnerable:
                links = []

                for link in entry.links:
                    links.append(f"<a class='{self.css_name}' href='{link.url}' target='_blank'>{link.url}</a>")

                vulnerable_markdown += f"| {entry.os} | {entry.version} | {entry.arch} | {entry.version_string} | {' '.join(links)}" + "\n"

            markdown += "\n" + vulnerable_markdown + "\n"

        page_links = self.page_metadata.get(page.file.src_path, {}).get("links", False)

        if page_links:
            link_markdown = f"""## Links
| Type      | URL            |
| --------- | -------------- |
"""

            for link in page_links:
                link_markdown += f"| {link.type} | <a class='{self.css_name}' href='{link.url}' target='_blank'>{link.url}</a>" + "\n"

            markdown += "\n" + link_markdown + "\n"

        return markdown

    def on_config(self, config):
        """Load config options"""
        self.filename = Path(self.config.get("filename") or self.filename)
        self.folder = Path(self.config.get("folder") or self.folder)
        self.css_name = self.config.get("css_name")
        # Make sure that the coverage folder is absolute, and exists
        if not self.folder.is_absolute():
            self.folder = Path(config["docs_dir"]) / ".." / self.folder
        if not self.folder.exists():
            self.folder.mkdir(parents=True)

        if self.config.get("template"):
            self.template = Path(self.config.get("template"))
        if self.template is None:
            self.template = Path(__file__).parent.joinpath(
                "templates"
            ).joinpath("canicve.template")
        environment = Environment(
            loader=FileSystemLoader(searchpath=str(self.template.parent))
        )
        self.templ = environment.get_template(str(self.template.name))

    def process_link(self, link, cve):
        config_key = False
        config_value = False

        if isinstance(link, dict):
            config_key = list(link.keys())[0]
            config_value = list(link.values())[0]
                                    
        if isinstance(link, str):
            config_key = link
            config_value = cve
        
        link_config = self.config.get(f'link_base_{config_key}', False)

        link_entry = False

        if link_config:
            link_entry = types.SimpleNamespace(
                url=link_config.format(config_value),
            )

            if config_key in ["TENABLE", "R7", "NVD", "MITRE", "CVD", "MARC"]:
                link_entry.type = "Reference"
            elif config_key in ["RHEL", "DEBIAN", "UBUNTU" ,"SUSE", "ORACLE", "GENTOO"]:
                link_entry.type = "OS Advisory"
            elif config_key in ["DIRECT"]:
                link_entry.type = "Info"
            elif config_key in ["EDB", "GH", "GHG", "GHCS"]:
                link_entry.type = "PoC / Source"
            else:
                link_entry.type = "Unknown"

        return link_entry

    def on_files(self, files, config):
        """Generate the index page for coverage searching"""
        fa = {}

        for d in ("cve", "kernel", "software"):
            filepath = self.folder / Path(d)

            if not filepath.exists():
                filepath.mkdir(parents=True, exist_ok=True)
                
        for f in files:
            if f.src_path.endswith(".md"):
                self.page_metadata[f.src_path] = {
                    "metadata": get_metadata(f.src_path, config['docs_dir']),
                    "links": [],
                    "vulnerable": [],
                }
        
        kernel_data = []
        software_data = []

        for f, page_entry in self.page_metadata.items():
            
            if not page_entry.get("metadata", []):
                continue
            
            if "title" not in page_entry.get("metadata", []):
                page_entry.get("metadata", [])["title"] = page_entry.get("metadata", [])['filename'].split("/")[-1].strip('.md')

            data = page_entry.get("metadata", []).get("coverage", [])
            cve = False

            if data == []:
                return# TODO: log an error?

            cve = data.get('cve', False)
            
            if not cve:
                return# TODO: log an error?

            cve = cve.upper()

            basepath = self.folder / Path(f"cve/{cve}")

            if not basepath.exists():
                basepath.mkdir(parents=True, exist_ok=True)

            self.page_coveragedata[cve] = {"vulnerable": []}

            links = data.get('links', False)

            if links:
                for link in links:
                    page_entry.get("links").append(self.process_link(link, cve))

            vulnerable = data.get('vulnerable', False)

            if vulnerable:

                for d in vulnerable:

                    for os, k in d.items():

                        for e in k:

                            for version, x in e.items():

                                for arch in x.get('ARCHITECTURE'):

                                    KERNEL = x.get('KERNEL', False)
                                    SOFTWARE = x.get('SOFTWARE', False)
                                    data_array = False
                                    label = ""

                                    if KERNEL:
                                        data_array = KERNEL
                                        label = "kernel"
                                    
                                    if SOFTWARE:
                                        data_array = SOFTWARE
                                        label = "software"

                                    if data_array:

                                        filepath = self.folder / Path(f"./{label}/")

                                        if not filepath.exists():
                                            filepath.mkdir(parents=True, exist_ok=True)

                                        for dae in data_array:
                                            entry_links = []


                                            if isinstance(dae, dict):

                                                for _, links in dae.items():
                                                    for link in links:
                                                        entry_links.append(self.process_link(link, cve))

                                                dae = list(dae.keys())[0]

                                            page_entry.get("vulnerable").append(types.SimpleNamespace(os=os, version=version, arch=arch, version_string=dae, links=entry_links))

                                            self.page_coveragedata[cve]["vulnerable"].append({"o": os, "v": version, "a": arch, "k": dae})

                                            subk = dae.split('.')
                                            bfp = filepath / Path(f"{subk[0]}/{subk[1]}")

                                            if not bfp.exists():
                                                bfp.mkdir(parents=True, exist_ok=True)

                                            fn = bfp / Path(f"{dae}_{os}_{version}_{arch}")

                                            fa[str(fn)] = fn

                                            with open(fn, "a", encoding='utf-8') as fh:
                                                fh.write(f"{cve}\n")

                                            fn = filepath / Path(f"index.{label}")

                                            fa[str(fn)] = fn
                                            
                                            with open(fn, "a", encoding='utf-8') as fh:
                                                data = f"{dae}_{os}_{version}_{arch}"

                                                fh.write(f"{data}\n")

                                                if label == "kernel":
                                                    kernel_data.append(f"{data}")

                                                if label == "software":
                                                    software_data.append(f"{data}")

            fn = basepath / Path(f"./cve.json")

            fa[str(fn)] = fn

            with open(fn, "w", encoding='utf-8') as fh:
                fh.write(json.dumps(self.page_coveragedata[cve]))

        fn = self.folder / Path("./cve/index.cve")

        fa[str(fn)] = fn

        cve_data = []

        with open(fn, "w", encoding='utf-8') as fh:
            for cve in self.page_coveragedata.keys():
                fh.write(f"{cve}\n")
                cve_data.append(cve)

        fn = self.folder / Path(self.filename)

        fa[str(fn)] = fn

        with open(fn, "w", encoding='utf-8') as fh:
            fh.write(self.templ.render(
                cve=cve_data,
                kernel=kernel_data,
                software=software_data
            ))

        # add all of our generated files to the site build
        for s, fn in fa.items():
            files.append(File(
                path=fn.name,
                src_dir=str(fn.parent),
                dest_dir=config["site_dir"] + str(fn.parent).split('docs/../aux')[1],
                use_directory_urls=False
            ))

        # add our index.md file (generated from canicve.template)
        files.append(File(
            path=str(self.filename),
            src_dir=str(self.folder),
            dest_dir=config["site_dir"],
            use_directory_urls=False
        ))


    def on_build_error(self, error):
        print(error)


# Helper functions - thanks: https://github.com/ginsburgnm/mkdocs-plugin-tags/blob/master/tags/plugin.py#L120
def get_metadata(name, path):
    """Get the metadata off of a file"""
    filename = Path(path) / Path(name)

    if filename.exists():
        with filename.open() as fname:
            match_string = search(r"\A\s*---\n.*?\n---", fname.read(), flags=DOTALL | MULTILINE)
            if match_string:
                try:
                    metadata = match_string.group(0).strip('---')
                    meta = load(metadata, Loader=FullLoader)
                    meta.update(filename=name)
                    return meta
                except YAMLError as err:
                    log.error("Couldn't parse %s yaml due to %s", fname, err)
    return None
