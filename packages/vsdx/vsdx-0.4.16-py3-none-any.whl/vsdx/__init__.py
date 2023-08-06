from __future__ import annotations
import zipfile
import shutil
import os
import re
from enum import IntEnum
from jinja2 import Template
from typing import Optional, List, Dict

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element

import xml.dom.minidom as minidom   # minidom used for prettyprint

from vsdx.geometry import Geometry

namespace = "{http://schemas.microsoft.com/office/visio/2012/main}"  # visio file name space
ext_prop_namespace = '{http://schemas.openxmlformats.org/officeDocument/2006/extended-properties}'
vt_namespace = '{http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes}'
r_namespace = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'
document_rels_namespace = "{http://schemas.openxmlformats.org/package/2006/relationships}"
cont_types_namespace = '{http://schemas.openxmlformats.org/package/2006/content-types}'


# utility functions
def to_float(val: str):
    try:
        if val is None:
            return
        return float(val)
    except ValueError:
        return 0.0


class PagePosition(IntEnum):
    FIRST =  0
    LAST  = -1
    END   = -1
    AFTER = -2
    BEFORE= -3


class VisioFile:
    """Represents a vsdx file

    :param filename: filename the :class:`VisioFile` was created from
    :type filename: str
    :param pages: a list of pages in the VisioFile
    :type pages: list of :class:`Page`
    :param master_pages: a list of master pages in the VisioFile
    :type master_pages: list of :class:`Page`

    Contains :class:`Page`, :class:`Shape`, :class:`Connect` and :class:`Cell` sub-classes
    """
    def __init__(self, filename, debug: bool = False):
        """VisioFile constructor

        :param filename: the vsdx file to load and create the VisioFile object from
        :type filename: str
        :param debug: enable/disable debugging
        :type debug: bool, default to False
        """
        self.debug = debug
        self.filename = filename
        if debug:
            print(f"VisioFile(filename={filename})")
        file_type = self.filename.split('.')[-1]  # last text after dot
        if not file_type.lower() == 'vsdx':
            raise TypeError(f'Invalid File Type:{file_type}')

        self.directory = os.path.abspath(filename)[:-5]
        self.pages_xml = None  # type: ET.ElementTree
        self.pages_xml_rels = None  # type: ET.ElementTree
        self.content_types_xml = None  # type: ET.ElementTree
        self.app_xml = None  # type: ET.ElementTree
        self.document_xml = None  # type: ET.ElementTree
        self.document_xml_rels = None  # type: ET.ElementTree
        self.pages = list()  # type: List[VisioFile.Page]  # list of Page objects, populated by open_vsdx_file()
        self.master_pages = list()  # type: List[VisioFile.Page]  # list of Page objects, populated by open_vsdx_file()
        self.open_vsdx_file()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_vsdx()

    @staticmethod
    def pretty_print_element(xml: Element) -> str:
        if type(xml) is Element:
            return minidom.parseString(ET.tostring(xml)).toprettyxml()
        elif type(xml) is ET.ElementTree:
            return minidom.parseString(ET.tostring(xml.getroot())).toprettyxml()
        else:
            return f"Not an Element. type={type(xml)}"

    def open_vsdx_file(self):
        with zipfile.ZipFile(self.filename, "r") as zip_ref:
            zip_ref.extractall(self.directory)

        # load each page file into an ElementTree object
        self.load_pages()
        self.load_master_pages()

    def _pages_filename(self):
        page_dir = f'{self.directory}/visio/pages/'
        pages_filename = page_dir + 'pages.xml'  # pages.xml contains Page name, width, height, mapped to Id
        return pages_filename

    @property
    def _masters_folder(self):
        path = f"{self.directory}/visio/masters"
        return path

    def load_pages(self):
        rel_dir = f'{self.directory}/visio/pages/_rels/'
        page_dir = f'{self.directory}/visio/pages/'

        rel_filename = rel_dir + 'pages.xml.rels'
        rels = file_to_xml(rel_filename).getroot()  # rels contains page filenames
        self.pages_xml_rels = file_to_xml(rel_filename)  # store pages.xml.rels so pages can be added or removed
        if self.debug:
            print(f"Relationships({rel_filename})", VisioFile.pretty_print_element(rels))
        relid_page_dict = {}

        for rel in rels:
            rel_id = rel.attrib['Id']
            page_file = rel.attrib['Target']
            relid_page_dict[rel_id] = page_file

        pages_filename = self._pages_filename()  # pages contains Page name, width, height, mapped to Id
        pages = file_to_xml(pages_filename).getroot()  # this contains a list of pages with rel_id and filename
        self.pages_xml = file_to_xml(pages_filename)  # store xml so pages can be removed
        if self.debug:
            print(f"Pages({pages_filename})", VisioFile.pretty_print_element(pages))

        for page in pages:  # type: Element
            rel_id = page[1].attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']
            page_name = page.attrib['Name']

            page_path = page_dir + relid_page_dict.get(rel_id, None)

            new_page = VisioFile.Page(file_to_xml(page_path), page_path, page_name, self)
            self.pages.append(new_page)

            if self.debug:
                print(f"Page({new_page.filename})", VisioFile.pretty_print_element(new_page.xml.getroot()))

        self.content_types_xml = file_to_xml(f'{self.directory}/[Content_Types].xml')
        # TODO: add correctness cross-check. Or maybe the other way round, start from [Content_Types].xml
        #       to get page_dir and other paths...

        self.app_xml = file_to_xml(f'{self.directory}/docProps/app.xml')  # note: files in docProps may be missing
        self.document_xml = file_to_xml(f'{self.directory}/visio/document.xml')
        self.document_xml_rels = file_to_xml(f'{self.directory}/visio/_rels/document.xml.rels')

    def load_master_pages(self):
        # get data from /visio/masters folder
        master_rel_path = f'{self.directory}/visio/masters/_rels/masters.xml.rels'

        master_rels_data = file_to_xml(master_rel_path)
        master_rels = master_rels_data.getroot() if master_rels_data else []
        if self.debug:
            print(f"Master Relationships({master_rel_path})", VisioFile.pretty_print_element(master_rels))

        # populate relid to master path
        relid_to_path = {}
        for rel in master_rels:
            master_id = rel.attrib.get('Id')
            master_path = f"{self.directory}/visio/masters/{rel.attrib.get('Target')}"  # get path from rel
            relid_to_path[master_id] = master_path

        # load masters.xml file
        masters_path = f'{self.directory}/visio/masters/masters.xml'
        masters_data = file_to_xml(masters_path)  # contains more info about master page (i.e. Name, Icon)
        masters = masters_data.getroot() if masters_data else []

        # for each master page, create the VisioFile.Page object
        for master in masters:
            rel_id = master.find(f"{namespace}Rel").attrib[f"{r_namespace}id"]
            master_id = master.attrib['ID']

            master_path = relid_to_path[rel_id]

            master_page = VisioFile.Page(file_to_xml(master_path), master_path, master_id, self)
            self.master_pages.append(master_page)

            if self.debug:
                print(f"Master({master_path}, id={master_id})", VisioFile.pretty_print_element(master_page.xml.getroot()))

        return

    def get_page(self, n: int) -> VisioFile.Page:
        try:
            return self.pages[n]
        except IndexError:
            return None

    def get_page_names(self):
        return [p.name for p in self.pages]

    def get_page_by_name(self, name: str):
        """Get page from VisioFile with matching name

                :param name: The name of the required page
                :type name: str

                :return: :class:`Page` object representing the page (or None if not found)
                """
        for p in self.pages:
            if p.name == name:
                return p

    def get_master_page_by_id(self, id: str):
        """Get master page from VisioFile with matching ID.

        Referred by :attr:`Shape.master_ID`.

                :param id: The ID of the required master
                :type id: str

                :return: :class:`Page` object representing the master page (or None if not found)
                """
        for m in self.master_pages:
            if m.name == id:
                return m

    def remove_page_by_index(self, index: int):
        """Remove zero-based nth page from VisioFile object

        :param index: Zero-based index of the page
        :type index: int

        :return: None
        """

        # remove Page element from pages.xml file - zero based index
        # todo:  similar function by page id, and by page title
        page = self.pages_xml.find(f"{namespace}Page[{index+1}]")
        if page:
            self.pages_xml.getroot().remove(page)
            page = self.pages[index]  # type: VisioFile.Page
            self._remove_page_from_app_xml(page.name)
            del self.pages[index]

    def _update_pages_xml_rels(self, new_page_filename: str) -> str:
        '''Updates the pages.xml.rels file with a reference to the new page and returns the new relid
        '''

        max_relid = max(self.pages_xml_rels.getroot(), key=lambda rel: int(rel.attrib['Id'][3:]), default=None)  # 'rIdXX' -> XX
        max_relid = int(max_relid.attrib['Id'][3:]) if max_relid is not None else 0
        new_page_relid = f'rId{max_relid + 1}'  # Most likely will be equal to len(self.pages)+1

        new_page_rel = {
            'Target': new_page_filename,
            'Type'  : 'http://schemas.microsoft.com/visio/2010/relationships/page',
            'Id'    : new_page_relid
        }
        self.pages_xml_rels.getroot().append(Element('{http://schemas.openxmlformats.org/package/2006/relationships}Relationship', new_page_rel))

        return new_page_relid

    def _get_new_page_name(self, new_page_name: str) -> str:
        i = 1
        while new_page_name in self.get_page_names():
            new_page_name = f'{new_page_name}-{i}'  # Page-X-i
            i += 1

        return new_page_name

    def _get_max_page_id(self) -> int:
        page_with_max_id = max(self.pages_xml.getroot(), key=lambda page: int(page.attrib['ID']))
        max_page_id = int(page_with_max_id.attrib['ID'])

        return max_page_id

    def _get_index(self, *, index: int, page: VisioFile.Page or None):
        if type(index) is PagePosition:  # only update index if it is relative to source page
            if index == PagePosition.LAST:
                index = len(self.pages)
            elif index == PagePosition.FIRST:
                index = 0
            elif page:  # need page for BEFORE or AFTER
                orig_page_idx = self.pages.index(page)
                if index == PagePosition.BEFORE:
                    # insert new page at the original page's index
                    index = orig_page_idx
                elif index == PagePosition.AFTER:
                    # insert new page after the original page
                    index = orig_page_idx + 1
            else:
                index = len(self.pages)  # default to LAST if invalid Position/page combination

        return index

    def _add_content_types_override(self, part_name_path: str, content_type: str):
        content_types = self.content_types_xml.getroot()

        content_types_attribs = {
            'PartName': part_name_path,
            'ContentType': content_type,
        }
        override_element = Element(f'{cont_types_namespace}Override', content_types_attribs)
        # find existing elements with same content_type
        matching_overrides = content_types.findall(
            f'{cont_types_namespace}Override[@ContentType="{content_type}"]'
        )
        if len(matching_overrides):  # insert after similar elements
            idx = list(content_types).index(matching_overrides[-1])
            content_types.insert(idx+1, override_element)
        else:  # add at end of list
            content_types.append(override_element)

    def _update_content_types_xml(self, new_page_filename: str):
        # todo: use generic function above
        content_types = self.content_types_xml.getroot()

        content_types_attribs = {
            'PartName'   : f'/visio/pages/{new_page_filename}',
            'ContentType': 'application/vnd.ms-visio.page+xml'
        }
        content_types_element = Element(f'{cont_types_namespace}Override', content_types_attribs)

        # add the new element after the last such element
        # first find the index:
        all_page_overrides = content_types.findall(
            f'{cont_types_namespace}Override[@ContentType="application/vnd.ms-visio.page+xml"]'
        )
        idx = list(content_types).index(all_page_overrides[-1])

        # then add it:
        content_types.insert(idx+1, content_types_element)

    def document_rels(self) -> List[Element]:
        rels = self.document_xml_rels.findall(f'{document_rels_namespace}Relationship')
        return rels

    def _add_document_rel(self, rel_type: str, target: str):
        rel_ids = [int(str(r.attrib.get('Id')).replace('rId', '')) for r in self.document_rels()]
        new_rel = Element(f"{document_rels_namespace}Relationship",
                          {
                              "Id": f"rId{max(rel_ids)+1}",
                              "Type": rel_type,
                              "Target": target,
                          })
        self.document_xml_rels.getroot().append(new_rel)

    def _style_sheets(self) -> Element:
        # return StyleSheets element from document.xml
        return self.document_xml.getroot().find(f'{namespace}StyleSheets')

    def _get_styles_name_list(self) -> List[str]:
        return [s.attrib.get('Name','') for s in self._style_sheets().findall(f'{namespace}StyleSheet')]

    def _get_style_by_name(self, name: str) -> Element:
        stylesheet = self._style_sheets().find(f"{namespace}StyleSheet[@Name = '{name}']")
        return stylesheet

    def _get_style_by_id(self, ID: str) -> Element:
        stylesheet = self._style_sheets().find(f"{namespace}StyleSheet[@ID = '{ID}']")
        return stylesheet

    def _heading_pairs(self) -> Element:
        # return HeadingPairs element from app.xml
        return self.app_xml.getroot().find(f'{ext_prop_namespace}HeadingPairs')

    def _titles_of_parts(self) -> Element:
        # return TitlesOfParts element from app.xml
        return self.app_xml.getroot().find(f'{ext_prop_namespace}TitlesOfParts')

    def _titles_of_parts_list(self) -> List[str]:
        # return list of strings
        return [t.text for t in self._titles_of_parts().find(f".//{vt_namespace}vector")]

    def _add_titles_of_parts_item(self, title: str):
        titles = self._titles_of_parts()
        vector = titles.find(f".//{vt_namespace}vector")  # new variant appended to vector Element
        new_title = Element(f'{vt_namespace}lpstr', {})
        new_title.text = title
        vector.append(new_title)
        # add one to vector size, as we have added two new variant elements
        vector.attrib['size'] = str(int(vector.attrib.get('size', 0)) + 1)

    def _get_app_xml_value(self, name: str) -> str:
        variants = self._heading_pairs().findall(f".//{vt_namespace}variant")
        # find Pages in headings
        for index in range(len(variants)):
            v = variants[index]
            lpstr = v.find(f".//{vt_namespace}lpstr")
            if type(lpstr) is Element and lpstr.text == name:
                next_v = variants[index+1] if index < (len(variants)-1) else None  # next variant if there is one
                i4 = next_v.find(f".//{vt_namespace}i4") if type(next_v) is Element else None
                if type(i4) is Element:
                    return i4.text

    def _set_app_xml_value(self, name: str, value: str):
        variants = self._heading_pairs().findall(f".//{vt_namespace}variant")
        # find Pages in headings
        for index in range(len(variants)):
            v = variants[index]
            lpstr = v.find(f".//{vt_namespace}lpstr")
            if type(lpstr) is Element and lpstr.text == name:
                next_v = variants[index+1] if index < (len(variants)-1) else None  # next variant if there is one
                i4 = next_v.find(f".//{vt_namespace}i4") if type(next_v) is Element else None
                if type(i4) is Element:
                    i4.text = value
                    return
        # no matching variant found - so create new item and populate it
        vector = self._heading_pairs().find(f".//{vt_namespace}vector")  # new variant appended to vector Element
        name_variant = Element(f'{vt_namespace}variant', {})
        lpstr = Element(f'{vt_namespace}lpstr', {})
        lpstr.text = name
        name_variant.append(lpstr)
        vector.append(name_variant)
        i4_variant = Element(f'{vt_namespace}variant', {})
        i4 = Element(f'{vt_namespace}i4', {})
        i4.text = value
        i4_variant.append(i4)
        vector.append(i4_variant)
        # add two to vector size, as we have added two new variant elements
        vector.attrib['size'] = str(int(vector.attrib.get('size', 0)) + 2)

    def _add_page_to_app_xml(self, new_page_name: str):
        # todo: use _add_titles_of_parts_item()
        HeadingPairs = self._heading_pairs()
        i4 = HeadingPairs.find(f'.//{vt_namespace}i4')
        num_pages = int(i4.text)
        i4.text = str(num_pages+1)  # increment as page added

        TitlesOfParts = self.app_xml.getroot().find(f'{ext_prop_namespace}TitlesOfParts')
        vector = TitlesOfParts.find(f'{vt_namespace}vector')

        lpstr = Element(f'{vt_namespace}lpstr')
        lpstr.text = new_page_name
        vector.append(lpstr)  # add new lpstr element with new page name
        vector_size = int(vector.attrib['size'])
        vector.set('size', str(vector_size+1))  # increment as page added

    def _remove_page_from_app_xml(self, page_name: str):
        HeadingPairs = self.app_xml.getroot().find(f'{ext_prop_namespace}HeadingPairs')
        i4 = HeadingPairs.find(f'.//{vt_namespace}i4')
        num_pages = int(i4.text)
        i4.text = str(num_pages-1)  # decrement as page removed

        TitlesOfParts = self.app_xml.getroot().find(f'{ext_prop_namespace}TitlesOfParts')
        vector = TitlesOfParts.find(f'{vt_namespace}vector')

        for lpstr in vector.findall(f'{vt_namespace}lpstr'):
            if lpstr.text == page_name:
                vector.remove(lpstr)  # remove page from list of names
                break

        vector_size = int(vector.attrib['size'])
        vector.set('size', str(vector_size-1))  # decrement as page removed

    def _create_page(
        self,
        *,
        new_page_xml_str: str,
        page_name: str,
        new_page_element: Element,
        index: int or PagePosition,
        source_page: Optional[VisioFile.Page] = None,
    ) -> VisioFile.Page:
        # Create visio\pages\pageX.xml file
        # Add to visio\pages\_rels\pages.xml.rels
        # Add to visio\pages\pages.xml
        # Add to [Content_Types].xml
        # Add to docProps\app.xml

        page_dir = f'{self.directory}/visio/pages/'  # TODO: better concatenation

        # create pageX.xml
        new_page_xml = ET.ElementTree(ET.fromstring(new_page_xml_str))
        new_page_filename = f'page{len(self.pages) + 1}.xml'
        new_page_path = page_dir+new_page_filename  # TODO: better concatenation

        # update pages.xml.rels - add rel for the new page
        # done by the caller

        # update pages.xml - insert the PageElement Element in it's correct location
        index = self._get_index(index=index, page=source_page)
        self.pages_xml.getroot().insert(index, new_page_element)

        # update [Content_Types].xml - insert reference to the new page
        self._update_content_types_xml(new_page_filename)

        # update app.xml, if it exists
        if self.app_xml:
            self._add_page_to_app_xml(page_name)

        # Update VisioFile object
        new_page = VisioFile.Page(new_page_xml, new_page_path, page_name, self)

        self.pages.insert(index, new_page)  # insert new page at defined index

        return new_page

    def add_page_at(self, index: int, name: Optional[str] = None) -> VisioFile.Page:
        """Add a new page at the specified index of the VisioFile

        :param index: zero-based index where the new page will be placed
        :type index: int

        :param name: The name of the new page
        :type name: str, optional

        :return: :class:`Page` object representing the new page
        """

        # Determine the new page's name
        new_page_name = self._get_new_page_name(name or f'Page-{len(self.pages) + 1}')

        # Determine the new page's filename
        new_page_filename = f'page{len(self.pages) + 1}.xml'

        # Add reference to the new page in pages.xml.rels and get new relid
        new_page_relid = self._update_pages_xml_rels(new_page_filename)

        # Create default empty page xml
        # TODO: figure out the best way to define this default pagesheet XML
        # For example, python-docx has a 'template.docx' file which is copied.
        new_pagesheet_attribs = {
            'FillStyle': '0',
            'LineStyle': '0',
            'TextStyle': '0'
        }
        new_pagesheet_element = Element(f'{namespace}PageSheet', new_pagesheet_attribs)
        new_pagesheet_element.append(Element(f'{namespace}Cell', {'N':'PageWidth', 'V':'8.26771653543307'}))
        new_pagesheet_element.append(Element(f'{namespace}Cell', {'N':'PageHeight', 'V':'11.69291338582677'}))
        new_pagesheet_element.append(Element(f'{namespace}Cell', {'N':'ShdwOffsetX', 'V':'0.1181102362204724'}))
        new_pagesheet_element.append(Element(f'{namespace}Cell', {'N':'ShdwOffsetY', 'V':'-0.1181102362204724'}))
        new_pagesheet_element.append(Element(f'{namespace}Cell', {'N':'PageScale', 'U':'MM', 'V':'0.03937007874015748'}))
        new_pagesheet_element.append(Element(f'{namespace}Cell', {'N':'DrawingScale', 'U':'MM', 'V':'0.03937007874015748'}))
        new_pagesheet_element.append(Element(f'{namespace}Cell', {'N':'DrawingSizeType', 'V':'0'}))
        new_pagesheet_element.append(Element(f'{namespace}Cell', {'N':'DrawingScaleType', 'V':'0'}))
        new_pagesheet_element.append(Element(f'{namespace}Cell', {'N':'InhibitSnap', 'V':'0'}))
        new_pagesheet_element.append(Element(f'{namespace}Cell', {'N':'PageLockReplace', 'U':'BOOL', 'V':'0'}))
        new_pagesheet_element.append(Element(f'{namespace}Cell', {'N':'PageLockDuplicate', 'U':'BOOL', 'V':'0'}))
        new_pagesheet_element.append(Element(f'{namespace}Cell', {'N':'UIVisibility', 'V':'0'}))
        new_pagesheet_element.append(Element(f'{namespace}Cell', {'N':'ShdwType', 'V':'0'}))
        new_pagesheet_element.append(Element(f'{namespace}Cell', {'N':'ShdwObliqueAngle', 'V':'0'}))
        new_pagesheet_element.append(Element(f'{namespace}Cell', {'N':'ShdwScaleFactor', 'V':'1'}))
        new_pagesheet_element.append(Element(f'{namespace}Cell', {'N':'DrawingResizeType', 'V':'1'}))
        new_pagesheet_element.append(Element(f'{namespace}Cell', {'N':'PageShapeSplit', 'V':'1'}))

        new_page_attribs = {
            'ID'   : str(self._get_max_page_id() + 1),
            'NameU': new_page_name,
            'Name' : new_page_name,
        }
        new_page_element = Element(f'{namespace}Page', new_page_attribs)
        new_page_element.append(new_pagesheet_element)

        new_page_rel = {
            '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id' : new_page_relid
        }
        new_page_element.append(Element(f'{namespace}Rel', new_page_rel))

        # create the new page
        new_page = self._create_page(
            new_page_xml_str = f"<?xml version='1.0' encoding='utf-8' ?><PageContents xmlns='{namespace[1:-1]}' xmlns:r='http://schemas.openxmlformats.org/officeDocument/2006/relationships' xml:space='preserve'/>",
            page_name = new_page_name,
            new_page_element = new_page_element,
            index = index
        )

        return new_page

    def add_page(self, name: Optional[str] = None) -> VisioFile.Page:
        """Add a new page at the end of the VisioFile

        :param name: The name of the new page
        :type name: str, optional

        :return: Page object representing the new page
        """

        return self.add_page_at(PagePosition.LAST, name)

    def copy_page(self, page: VisioFile.Page, *, index: Optional[int] = PagePosition.AFTER, name: Optional[str] = None) -> VisioFile.Page:
        """Copy an existing page and insert in VisioFile

        :param page: the page to copy
        :type page: VisioFile.Page
        :param index: the specific int or relation PagePosition location for new page
        :type index: int or PagePosition
        :param name: name of new page (note this may be altered if name already exists)
        :type name: str

        :return: the newly created page
        """
        # Determine the new page's name
        new_page_name = self._get_new_page_name(name or page.name)

        # Determine the new page's filename
        new_page_filename = f'page{len(self.pages) + 1}.xml'

        # Add reference to the new page in pages.xml.rels and get new relid
        new_page_relid = self._update_pages_xml_rels(new_page_filename)

        # Copy the source page and update relevant attributes
        page_element = self.pages_xml.find(f"{namespace}Page[@Name='{page.name}']")
        new_page_element = ET.fromstring(ET.tostring(page_element))

        new_page_element.attrib['ID']    = str(self._get_max_page_id() + 1)
        new_page_element.attrib['NameU'] = new_page_name
        new_page_element.attrib['Name']  = new_page_name
        new_page_element.find(f'{namespace}Rel').attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'] = new_page_relid

        # create the new page
        new_page = self._create_page(
            new_page_xml_str = ET.tostring(page.xml.getroot()),
            page_name = new_page_name,
            new_page_element = new_page_element,
            index = index,
            source_page = page,
        )

        # copy pageX.xml.rels if it exists
        # from testing, this does not actually seem to make a difference
        _, original_filename = os.path.split(page.filename)
        page_xml_rels_file = f'{self.directory}/visio/pages/_rels/{original_filename}.rels'  # TODO: better concatenation
        new_page_xml_rels_file = f'{self.directory}/visio/pages/_rels/{new_page_filename}.rels'  # TODO: better concatenation
        try:
            shutil.copy(page_xml_rels_file, new_page_xml_rels_file)
        except FileNotFoundError:
            pass

        return new_page

    # TODO: dead code - never used
    def get_sub_shapes(self, shape: Element, nth=1):
        for e in shape:
            if 'Shapes' in e.tag:
                nth -= 1
                if not nth:
                    return e

    @staticmethod
    def get_shape_location(shape: Element) -> (float, float):
        x, y = 0.0, 0.0
        cell_PinX = shape.find(f'{namespace}Cell[@N="PinX"]')  # type: Element
        cell_PinY = shape.find(f'{namespace}Cell[@N="PinY"]')
        x = float(cell_PinX.attrib['V'])
        y = float(cell_PinY.attrib['V'])

        return x, y

    @staticmethod
    def set_shape_location(shape: Element, x: float, y: float):
        cell_PinX = shape.find(f'{namespace}Cell[@N="PinX"]')  # type: Element
        cell_PinY = shape.find(f'{namespace}Cell[@N="PinY"]')
        cell_PinX.attrib['V'] = str(x)
        cell_PinY.attrib['V'] = str(y)

    @staticmethod
    # TODO: is this never used?
    def get_shape_text(shape: ET) -> str:
        # technically the below is not an exact replacement of the above...
        text = ""
        text_elem = shape.find(f"{namespace}Text")
        if text_elem is not None:
            text = "".join(text_elem.itertext())
        return text

    @staticmethod
    # TODO: is this never used?
    def set_shape_text(shape: ET, text: str):
        t = shape.find(f"{namespace}Text")  # type: Element
        if t is not None:
            if t.text:
                t.text = text
            else:
                t[0].tail = text

    # context = {'customer_name':'codypy.com', 'year':2020 }
    # example shape text "For {{customer_name}}  (c){{year}}" -> "For codypy.com (c)2020"
    @staticmethod
    def apply_text_context(shapes: Element, context: dict):

        def _replace_shape_text(shape: Element, context: dict):
            text = VisioFile.get_shape_text(shape)

            for key in context.keys():
                r_key = "{{" + key + "}}"
                text = text.replace(r_key, str(context[key]))
            VisioFile.set_shape_text(shape, text)

        for shape in shapes.findall(f"{namespace}Shapes"):
                VisioFile.apply_text_context(shape, context)  # recursive call
                _replace_shape_text(shape, context)

        for shape in shapes.findall(f"{namespace}Shape"):
            _replace_shape_text(shape, context)

    def jinja_render_vsdx(self, context: dict):
        """Transform a template VisioFile object using the Jinja language
        The method updates the VisioFile object loaded from the template file, so does not return any value
        Note: vsdx specific extensions are available such as `{% for item in list %}` statements with no `{% endfor %}`

        :param context: A dictionary containing values that can be accessed by the Jinja processor
        :type context: dict

        :return: None
        """
        # parse each shape in each page as Jinja2 template with context
        pages_to_remove = []  # list of pages to be removed after loop
        for page in self.pages:  # type: VisioFile.Page
            # check if page should be removed
            if VisioFile.jinja_page_showif(page, context):
                loop_shape_ids = list()
                for shapes_by_id in page.shapes:  # type: VisioFile.Shape
                    VisioFile.jinja_render_shape(shape=shapes_by_id, context=context, loop_shape_ids=loop_shape_ids)

                source = ET.tostring(page.xml.getroot(), encoding='unicode')
                source = VisioFile.unescape_jinja_statements(source)  # unescape chars like < and > inside {%...%}
                template = Template(source)
                output = template.render(context)
                page.xml = ET.ElementTree(ET.fromstring(output))  # create ElementTree from Element created from output

                # update loop shape IDs which have been duplicated by Jinja template
                page.set_max_ids()
                for shape_id in loop_shape_ids:
                    shapes_by_id = page._find_shapes_by_id(shape_id)  # type: List[VisioFile.Shape]
                    if shapes_by_id and len(shapes_by_id) > 1:
                        delta = 0
                        for shape in shapes_by_id[1:]:  # from the 2nd onwards - leaving original unchanged
                            # increment each new shape duplicated by the jinja loop
                            self.increment_sub_shape_ids(shape, page)
                            delta += shape.height  # automatically move each duplicate down
                            shape.move(0, -delta)  # move duplicated shapes so they are visible
            else:
                # note page to remove after this loop has completed
                pages_to_remove.append(page)
        # remove pages after processing
        for p in pages_to_remove:
            self.remove_page_by_index(p.index_num)

    @staticmethod
    def jinja_render_shape(shape: VisioFile.Shape, context: dict, loop_shape_ids: list):
        prev_shape = None
        for s in shape.sub_shapes():  # type: VisioFile.Shape
            # manage for loops in template
            loop_shape_id = VisioFile.jinja_create_for_loop_if(s, prev_shape)
            if loop_shape_id:
                loop_shape_ids.append(loop_shape_id)
            prev_shape = s
            # manage 'set self' statements
            VisioFile.jinja_set_selfs(s, context)
            VisioFile.jinja_render_shape(shape=s, context=context, loop_shape_ids=loop_shape_ids)

    @staticmethod
    def jinja_set_selfs(shape: VisioFile.Shape, context: dict):
        # apply any {% self self.xxx = yyy %} statements in shape properties
        jinja_source = shape.text
        matches = re.findall(r'{% set self.(.*?)\s?=\s?(.*?) %}', jinja_source)  # non-greedy search for all {%...%} strings
        for m in matches:  # type: tuple  # expect ('property', 'value') such as ('x', '10') or ('y', 'n*2')
            property_name = m[0]
            value = "{{ "+m[1]+" }}"  # Jinja to be processed
            # todo: replace any self references in value with actual value - i.e. {% set self.x = self.x+1 %}
            self_refs = re.findall(r'self.(.*)[\s+-/*//]?', m[1])  # greedy search for all self.? between +, -, *, or /
            for self_ref in self_refs:  # type: tuple  # expect ('property', 'value') such as ('x', '10') or ('y', 'n*2')
                ref_val = str(shape.__getattribute__(self_ref[0]))
                value = value.replace('self.'+self_ref[0], ref_val)
            # use Jinja template to calculate any self refs found
            template = Template(value)  # value might be '{{ 1.0+2.4*3 }}'
            value = template.render(context)
            if property_name in ['x', 'y']:
                shape.__setattr__(property_name, value)

        # remove any {% set self %} statements, leaving any remaining text
        matches = re.findall('{% set self.*?%}', jinja_source)
        for m in matches:
            jinja_source = jinja_source.replace(m, '')  # remove Jinja 'set self' statement
        shape.text = jinja_source

    @staticmethod
    def unescape_jinja_statements(jinja_source):
        # unescape any text between {% ... %}
        jinja_source_out = jinja_source
        matches = re.findall('{%(.*?)%}', jinja_source)  # non-greedy search for all {%...%} strings
        for m in matches:
            unescaped = m.replace('&gt;', '>').replace('&lt;', '<')
            jinja_source_out = jinja_source_out.replace(m, unescaped)
        return jinja_source_out

    @staticmethod
    def jinja_create_for_loop_if(shape: VisioFile.Shape, previous_shape:VisioFile.Shape or None):
        # update a Shapes tag where text looks like a jinja {% for xxxx %} loop
        # move text to start of Shapes tag and add {% endfor %} at end of tag
        text = shape.text

        # use regex to find all loops
        jinja_loops = re.findall(r"{% for\s(.*?)\s%}", text)

        for loop in jinja_loops:
            jinja_loop_text = f"{{% for {loop} %}}"
            # move the for loop to start of shapes element (just before first Shape element)
            if previous_shape:
                if previous_shape.xml.tail:
                    previous_shape.xml.tail += jinja_loop_text
                else:
                    previous_shape.xml.tail = jinja_loop_text  # add jinja loop text after previous shape, before this element
            else:
                if shape.parent.xml.text:
                    shape.parent.xml.text += jinja_loop_text
                else:
                    shape.parent.xml.text = jinja_loop_text  # add jinja loop at start of parent, just before this element
            shape.text = shape.text.replace(jinja_loop_text, '')  # remove jinja loop from <Text> tag in element

            # add closing 'endfor' to just inside the shapes element, after last shape
            if shape.xml.tail:  # extend or set text at end of Shape element
                shape.xml.tail += "{% endfor %}"
            else:
                shape.xml.tail = '{% endfor %}'

        jinja_show_ifs = re.findall(r"{% showif\s(.*?)\s%}", text)  # find all showif statements
        # jinja_show_if - translate non-standard {% showif statement %} to valid jinja if statement
        for show_if in jinja_show_ifs:
            jinja_show_if = f"{{% if {show_if} %}}"  # translate to actual jinja if statement
            # move the for loop to start of shapes element (just before first Shape element)
            if previous_shape:
                previous_shape.xml.tail = str(previous_shape.xml.tail or '')+jinja_show_if  # add jinja loop text after previous shape, before this element
            else:
                shape.parent.xml.text = str(shape.parent.xml.text or '')+jinja_show_if  # add jinja loop at start of parent, just before this element

            # remove original jinja showif from <Text> tag in element
            shape.text = shape.text.replace(f"{{% showif {show_if} %}}", '')

            # add closing 'endfor' to just inside the shapes element, after last shape
            if shape.xml.tail:  # extend or set text at end of Shape element
                shape.xml.tail += "{% endif %}"
            else:
                shape.xml.tail = '{% endif %}'

        if jinja_loops:
            return shape.ID  # return shape ID if it is a loop, so that duplicate shape IDs can be updated

    @staticmethod
    def jinja_page_showif(page: VisioFile.Page, context: dict):
        text = page.name
        jinja_source = re.findall(r"{% showif\s(.*?)\s%}", text)
        if len(jinja_source):
            # process last matching value
            template_source = "{{ "+jinja_source[-1]+" }}"
            template = Template(template_source)  # value might be '{{ 1.0+2.4*3 }}'
            value = template.render(context)
            # is the value truthy - i.e. not 0, False, or empty string, tuple, list or dict
            print(f"jinja_page_showif(context={context}) statement: {template_source} returns: {type(value)} {value}")
            if value in ['False', '0', '', '()', '[]', '{}']:
                print("value in ['False', '0', '', '()', '[]', '{}']")
                return False  # page should be hidden
            # remove jinja statement from page name
            jinja_statement = re.match("{%.*?%}", page.name)[0]
            page.set_name(page.name.replace(jinja_statement, ''))
            print(f"jinja_statement={jinja_statement} page.name={page.name}")
        return True  # page should be left in

    @staticmethod
    def get_shape_id(shape: ET) -> str:
        return shape.attrib['ID']

    def increment_sub_shape_ids(self, shape: VisioFile.Shape, page, id_map: dict = None):
        id_map = self.increment_shape_ids(shape.xml, page, id_map)
        self.update_ids(shape.xml, id_map)
        for s in shape.sub_shapes():
            id_map = self.increment_shape_ids(s.xml, page, id_map)
            self.update_ids(s.xml, id_map)
            if s.sub_shapes():
                id_map = self.increment_sub_shape_ids(s, page, id_map)
        return id_map

    def copy_shape(self, shape: Element, page: VisioFile.Page) -> ET:
        """Insert shape into first Shapes tag in destination page, and return the copy.

        If destination page does not have a Shapes tag yet, create it.

        Parameters:
            shape (Element): The source shape to be copied. Use Shape.xml
            page (ElementTree): The page where the new Shape will be placed. Use Page.xml
            page_path (str): The filename of the page where the new Shape will be placed. Use Page.filename

        Returns:
            ElementTree: The new shape ElementTree

        """

        new_shape = ET.fromstring(ET.tostring(shape))

        page.set_max_ids()
        # find or create Shapes tag
        shapes_tag = page.xml.find(f"{namespace}Shapes")
        if shapes_tag is None:
            shapes_tag = Element(f"{namespace}Shapes")
            page.xml.getroot().append(shapes_tag)

        id_map = self.increment_shape_ids(new_shape, page) # page_obj)
        self.update_ids(new_shape, id_map)
        shapes_tag.append(new_shape)

        return new_shape

    def insert_shape(self, shape: Element, shapes: Element, page: ET, page_path: str) -> ET:
        # insert shape into shapes tag, and return updated shapes tag
        for page_obj in self.pages:
            if page_obj.filename == page_path:
                break

        id_map = self.increment_shape_ids(shape, page_obj)
        self.update_ids(shape, id_map)
        shapes.append(shape)
        return shapes

    def increment_shape_ids(self, shape: Element, page: VisioFile.Page, id_map: dict=None):
        if id_map is None:
            id_map = dict()
        self.set_new_id(shape, page, id_map)
        for e in shape.findall(f"{namespace}Shapes"):
            self.increment_shape_ids(e, page, id_map)
        for e in shape.findall(f"{namespace}Shape"):
            self.set_new_id(e, page, id_map)

        return id_map

    def set_new_id(self, element: Element, page: VisioFile.Page, id_map: dict):
        page.max_id += 1
        max_id = page.max_id
        if element.attrib.get('ID'):
            current_id = element.attrib['ID']
            id_map[current_id] = max_id  # record mappings
        element.attrib['ID'] = str(max_id)
        return max_id  # return new id for info

    def update_ids(self, shape: Element, id_map: dict):
        # update: <ns0:Cell F="Sheet.15! replacing 15 with new id using prepopulated id_map
        # cycle through shapes looking for Cell tag inside a Shape tag, which may be inside a Shapes tag
        for e in shape.findall(f"{namespace}Shapes"):
            self.update_ids(e, id_map)
        for e in shape.findall(f"{namespace}Shape"):
            # look for Cell elements
            cells = e.findall(f"{namespace}Cell[@F]")
            for cell in cells:
                f = str(cell.attrib['F'])
                if f.startswith("Sheet."):
                    # update sheet refs with new ids
                    shape_id = f.split('!')[0].split('.')[1]
                    new_id = id_map[shape_id]
                    new_f = f.replace(f"Sheet.{shape_id}",f"Sheet.{new_id}")
                    cell.attrib['F'] = new_f
        return shape

    def close_vsdx(self):
        try:
            # Remove extracted folder
            shutil.rmtree(self.directory)
        except (FileNotFoundError, PermissionError):
            pass

    def save_vsdx(self, new_filename=None):
        """save the VisioFile object as new vsdx file

        :param new_filename: path to save vsdx file
        :type new_filename: str

        """
        # write pages.xml.rels
        xml_to_file(self.pages_xml_rels, f'{self.directory}/visio/pages/_rels/pages.xml.rels')

        # write pages.xml file - in case pages added removed
        xml_to_file(self.pages_xml, self._pages_filename())

        # write the master pages to file
        for page in self.master_pages:  # type: VisioFile.Page
            xml_to_file(page.xml, page.filename)

        # write the pages to file
        for page in self.pages:  # type: VisioFile.Page
            xml_to_file(page.xml, page.filename)

        # write [content_Types].xml
        xml_to_file(self.content_types_xml, f'{self.directory}/[Content_Types].xml')

        # write app.xml
        if self.app_xml is not None:
            xml_to_file(self.app_xml, f'{self.directory}/docProps/app.xml')

        # write document.xml
        xml_to_file(self.document_xml, f'{self.directory}/visio/document.xml')

        # write document.xml.rels
        xml_to_file(self.document_xml_rels, f'{self.directory}/visio/_rels/document.xml.rels')

        # wrap up files into zip and rename to vsdx
        base_filename = self.filename[:-5]  # remove ".vsdx" from end
        if new_filename.find(os.sep) > 0:
            directory = new_filename[0:new_filename.rfind(os.sep)]
            if directory:
                if not os.path.exists(directory):
                    os.mkdir(directory)
        shutil.make_archive(base_filename, 'zip', self.directory)
        if not new_filename:
            shutil.move(base_filename + '.zip', base_filename + '_new.vsdx')
        else:
            if new_filename[-5:] != '.vsdx':
                new_filename += '.vsdx'
            shutil.move(base_filename + '.zip', new_filename)
        self.close_vsdx()

    class Cell:
        def __init__(self, xml: Element, shape: VisioFile.Shape):
            self.xml = xml
            self.shape = shape

        @property
        def value(self):
            return self.xml.attrib.get('V')

        @value.setter
        def value(self, value: str):
            self.xml.attrib['V'] = str(value)

        @property
        def formula(self):
            return self.xml.attrib.get('F')

        @formula.setter
        def formula(self, value: str):
            self.xml.attrib['F'] = str(value)

        @property
        def name(self):
            return self.xml.attrib.get('N')

        @property
        def func(self):  # assume F stands for function, i.e. F="Width*0.5"
            return self.xml.attrib.get('F')

        def __repr__(self):
            return f"Cell: name={self.name} val={self.value} func={self.func}"

    class DataProperty:
        def __init__(self, *, xml: Element, shape: VisioFile.Shape):
            """Represents a single Data Property item associated with a Shape object"""
            name = xml.attrib.get('N')
            # get Cell element for each property of DataProperty
            label_cell = xml.find(f'{namespace}Cell[@N="Label"]')
            value_cell = xml.find(f'{namespace}Cell[@N="Value"]')
            value = value_cell.attrib.get('V') if type(value_cell) is Element else None

            if type(label_cell) is Element:
                value_type_cell = xml.find(f'{namespace}Cell[@N="Type"]')
                prompt_cell = xml.find(f'{namespace}Cell[@N="Prompt"]')
                sort_key_cell = xml.find(f'{namespace}Cell[@N="SortKey"]')

                # get values from each Cell Element
                value_type = value_type_cell.attrib.get('V') if type(value_type_cell) is Element else None
                label = label_cell.attrib.get('V') if type(label_cell) is Element else None
                prompt = prompt_cell.attrib.get('V') if type(prompt_cell) is Element else None
                sort_key = sort_key_cell.attrib.get('V') if type(sort_key_cell) is Element else None
            else:
                # over-ridden master shape properties have no label - only a name and value
                master_prop = [p for p in shape.master_shape.data_properties.values() if p.name == name][0]  # type: VisioFile.DataProperty
                label = master_prop.label
                value_type = master_prop.value_type
                prompt = master_prop.prompt
                sort_key = master_prop.sort_key

            # set DataProperty properties from xml
            self.name = name
            self.value = value
            self.value_type = value_type
            self.label = label
            self.prompt = prompt
            self.sort_key = sort_key

            self.shape = shape  # reference back to Shape object
            self.xml = xml  # reference to xml used to create DataProperty

    class Shape:
        """Represents a single shape, or a group shape containing other shapes
        """
        def __init__(self, xml: Element, parent: VisioFile.Page or VisioFile.Shape, page: VisioFile.Page):
            self.xml = xml
            self.parent = parent
            self.tag = xml.tag
            self.ID = xml.attrib.get('ID', None)
            self.master_shape_ID = xml.attrib.get('MasterShape', None)
            self.master_page_ID = xml.attrib.get('Master', None)  # i.e. '2', note: the master_page.name not list index
            if self.master_page_ID is None and isinstance(parent, VisioFile.Shape):  # in case of a sub_shape
                self.master_page_ID = parent.master_page_ID
            self.shape_type = xml.attrib.get('Type', None)
            self.page = page

            # get Cells in Shape
            self.cells = dict()
            self.geometry = None
            for e in self.xml.findall(f"{namespace}Cell"):
                cell = VisioFile.Cell(xml=e, shape=self)
                self.cells[cell.name] = cell
            geometry = self.xml.find(f'{namespace}Section[@N="Geometry"]')
            if type(geometry) is Element:
                #print(f"geometry({type(geometry)}):{geometry}")
                self.geometry = Geometry(xml=geometry, shape=self)
                for r in geometry.findall(f"{namespace}Row"):
                    row_type = r.attrib['T']
                    if row_type:
                        for e in r.findall(f"{namespace}Cell"):
                            cell = VisioFile.Cell(xml=e, shape=self)
                            key = f"Geometry/{row_type}/{cell.name}"
                            self.cells[key] = cell
                            #print(f"added name:['{key}']={cell} {cell.xml}")

            self._data_properties = None  # internal field to hold Shape.data_propertes, set by property

        def __repr__(self):
            return f"<Shape tag={self.tag} ID={self.ID} type={self.shape_type} text='{self.text}' >"

        def __eq__(self, other: VisioFile.Shape) -> bool:
            if not isinstance(other, VisioFile.Shape):
                return False

            return hash(self) == hash(other)

        def __hash__(self):
            return hash((self.ID, self.page.name, self.page.vis.filename))

        def copy(self, page: Optional[VisioFile.Page] = None) -> VisioFile.Shape:
            """Copy this Shape to the specified destination Page, and return the copy.

            If the destination page is not specified, the Shape is copied to its containing Page.

            :param page: The page where the new Shape will be placed.
                If not specified, the copy will be placed in the original shape's page.
            :type page: :class:`Page` (Optional)

            :return: :class:`Shape` the new copy of shape
            """
            dst_page = page or self.page
            new_shape_xml = self.page.vis.copy_shape(self.xml, dst_page)

            # set parent: location for new shape tag to be added
            if page:
                # set parent to first page Shapes tag if destination page passed
                parent = page.shapes
            else:
                # or set parent to source shapes own parent
                parent = self.parent

            return VisioFile.Shape(xml=new_shape_xml, parent=parent, page=dst_page)

        @property
        def master_shape(self) -> VisioFile.Shape:
            """Get this shapes master

            Returns this Shape's master as a Shape object (or None)

            """
            master_page = self.page.vis.get_master_page_by_id(self.master_page_ID)
            if not master_page:
                return   # None if no master page set for this Shape
            master_shape = master_page.shapes[0].sub_shapes()[0]  # there's always a single master shape in a master page

            if self.master_shape_ID is not None:
                master_sub_shape = master_shape.find_shape_by_id(self.master_shape_ID)
                return master_sub_shape

            return master_shape

        @property
        def data_properties(self) -> Dict[str, VisioFile.DataProperty]:
            """
            Get data properties of the shape - which labels, names, and values
            returns a dictionary of DataProperty objects indexed by property label

            :return: Dict[str, VisioFile.DataProperty]
            """
            if self._data_properties:
                # return cached dict if present
                return self._data_properties

            properties = dict()
            if self.master_shape:  # start with master data properties or empty dict
                properties = self.master_shape.data_properties
            properties_xml = self.xml.find(f'{namespace}Section[@N="Property"]')
            if type(properties_xml) is Element:
                property_rows = properties_xml.findall(f'{namespace}Row')
                for prop in property_rows:
                    data_prop = VisioFile.DataProperty(xml=prop, shape=self)
                    # add properties to dict to allow fast lookup by property.label
                    properties[data_prop.label] = data_prop
            self._data_properties = properties  # cache for next call
            return properties

        def cell_value(self, name: str):
            cell = self.cells.get(name)
            if cell:
                return cell.value

            if self.master_page_ID is not None:
                return self.master_shape.cell_value(name)

        def cell_formula(self, name: str):
            cell = self.cells.get(name)
            if cell:
                return cell.formula

            if self.master_page_ID is not None:
                return self.master_shape.cell_formula(name)

        def set_cell_value(self, name: str, value: str):
            cell = self.cells.get(name)
            if cell:  # only set value of existing item
                cell.value = value

            elif self.master_page_ID is not None:
                master_cell_xml = self.master_shape.xml.find(f'{namespace}Cell[@N="{name}"]')
                new_cell = ET.fromstring(ET.tostring(master_cell_xml))

                self.cells[name] = VisioFile.Cell(xml=new_cell, shape=self)
                self.cells[name].value = value

                self.xml.append(self.cells[name].xml)

        # LineStyle="7" FillStyle="7" TextStyle="7"
        @property
        def line_style_id(self):
            return self.xml.attrib.get('LineStyle')

        @line_style_id.setter
        def line_style_id(self, value):
            self.xml.attrib['LineStyle'] = str(value)

        @property
        def fill_style_id(self):
            return self.xml.attrib.get('FillStyle')

        @fill_style_id.setter
        def fill_style_id(self, value):
            self.xml.attrib['FillStyle'] = str(value)

        @property
        def text_style_id(self):
            return self.xml.attrib.get('TextStyle')

        @text_style_id.setter
        def text_style_id(self, value):
            self.xml.attrib['TextStyle'] = str(value)

        @property
        def line_weight(self) -> float:
            val = self.cell_value('LineWeight')
            return to_float(val)

        @line_weight.setter
        def line_weight(self, value: float or str):
            self.set_cell_value('LineWeight', str(value))

        @property
        def line_color(self) -> str:
            return self.cell_value('LineColor')

        @line_color.setter
        def line_color(self, value: str):
            self.set_cell_value('LineColor', str(value))

        @property
        def x(self):
            return to_float(self.cell_value('PinX'))

        @x.setter
        def x(self, value: float or str):
            self.set_cell_value('PinX', str(value))

        @property
        def y(self):
            return to_float(self.cell_value('PinY'))

        @y.setter
        def y(self, value: float or str):
            self.set_cell_value('PinY', str(value))

        @property
        def loc_x(self):
            return to_float(self.cell_value('LocPinX'))

        @loc_x.setter
        def loc_x(self, value: float or str):
            self.set_cell_value('LocPinX', str(value))

        @property
        def loc_y(self):
            return to_float(self.cell_value('LocPinY'))

        @loc_y.setter
        def loc_y(self, value: float or str):
            self.set_cell_value('LocPinY', str(value))

        @property
        def line_to_x(self):
            return to_float(self.cell_value('Geometry/LineTo/X'))

        @line_to_x.setter
        def line_to_x(self, value):
            self.set_cell_value('Geometry/LineTo/X', str(value))

        @property
        def line_to_y(self):
            return to_float(self.cell_value('Geometry/LineTo/Y'))

        @line_to_y.setter
        def line_to_y(self, value):
            self.set_cell_value('Geometry/LineTo/Y', str(value))

        @property
        def begin_x(self):
            return to_float(self.cell_value('BeginX'))

        @begin_x.setter
        def begin_x(self, value: float or str):
            self.set_cell_value('BeginX', str(value))

        @property
        def begin_y(self):
            return to_float(self.cell_value('BeginY'))

        @begin_y.setter
        def begin_y(self, value: float or str):
            self.set_cell_value('BeginY', str(value))

        @property
        def end_x(self):
            return to_float(self.cell_value('EndX'))

        @end_x.setter
        def end_x(self, value: float or str):
            self.set_cell_value('EndX', str(value))

        @property
        def end_y(self):
            return to_float(self.cell_value('EndY'))

        @end_y.setter
        def end_y(self, value: float or str):
            self.set_cell_value('EndY', str(value))

        def move(self, x_delta: float, y_delta: float):
            self.x = self.x + x_delta
            self.y = self.y + y_delta

        @property
        def height(self):
            return to_float(self.cell_value('Height'))

        @height.setter
        def height(self, value: float or str):
            self.set_cell_value('Height', str(value))

        @property
        def width(self):
            return to_float(self.cell_value('Width'))

        @width.setter
        def width(self, value: float or str):
            self.set_cell_value('Width', str(value))

        @property
        def center_x_y(self):
            x = self.x - (self.width/2)
            y = self.y + (self.height/2)
            return x, y

        @staticmethod
        def clear_all_text_from_xml(x: Element):
            x.text = ''
            x.tail = ''
            for i in x:
                VisioFile.Shape.clear_all_text_from_xml(i)

        @property
        def text(self):
            # return contents of Text element, or Master shape (if referenced), or empty string
            text_element = self.xml.find(f"{namespace}Text")

            if isinstance(text_element, Element):
                return "".join(text_element.itertext())  # get all text from <Text> sub elements
            elif self.master_page_ID:
                return self.master_shape.text  # get text from master shape
            return ""

        @text.setter
        def text(self, value):
            text_element = self.xml.find(f"{namespace}Text")
            if isinstance(text_element, Element):  # if there is a Text element then clear out and set contents
                VisioFile.Shape.clear_all_text_from_xml(text_element)
                text_element.text = value
            # todo: create new Text element if not found

        def sub_shapes(self) -> List[VisioFile.Shape]:
            """Get child/sub shapes contained by a VisioFile.Shape

            :returns: list of VisioFile.Shape objects
            :rtype: List[VisioFile.Shape]
            """
            shapes = list()
            # for each shapes tag, look for Shape objects
            # self can be either a Shapes or a Shape
            # a Shapes has a list of Shape
            # a Shape can have 0 or 1 Shapes (1 if type is Group)

            if self.shape_type == 'Group':
                parent_element = self.xml.find(f"{namespace}Shapes")
            else:  # a Shapes
                parent_element = self.xml
            if parent_element:
                shapes = [VisioFile.Shape(xml=shape, parent=self, page=self.page) for shape in parent_element]
            else:
                shapes = []
            return shapes

        def get_max_id(self):
            max_id = int(self.ID)
            if self.shape_type == 'Group':
                for shape in self.sub_shapes():
                    new_max = shape.get_max_id()
                    if new_max > max_id:
                        max_id = new_max
            return max_id

        def find_shape_by_id(self, shape_id: str) -> VisioFile.Shape:  # returns Shape
            """
            Recursively search for a shape, based on a known shape_id, and return a single VisioFile.Shape

            :param shape_id:
            :return: VisooFile.Shape
            """
            # recursively search for shapes by text and return first match
            for shape in self.sub_shapes():  # type: VisioFile.Shape
                if shape.ID == shape_id:
                    return shape
                if shape.shape_type == 'Group':
                    found = shape.find_shape_by_id(shape_id)
                    if found:
                        return found

        def find_shapes_by_id(self, shape_id: str) -> List[VisioFile.Shape]:
            # recursively search for shapes by ID and return all matches
            found = list()
            for shape in self.sub_shapes():  # type: VisioFile.Shape
                if shape.ID == shape_id:
                    found.append(shape)
                if shape.shape_type == 'Group':
                    sub_found = shape.find_shapes_by_id(shape_id)
                    if sub_found:
                        found.extend(sub_found)
            return found  # return list of matching shapes

        def find_shapes_by_master(self, master_page_ID: str, master_shape_ID: str) -> List[VisioFile.Shape]:
            # recursively search for shapes by master ID and return all matches
            found = list()
            for shape in self.sub_shapes():  # type: VisioFile.Shape
                if shape.master_shape_ID == master_shape_ID and shape.master_page_ID == master_page_ID:
                    found.append(shape)
                if shape.shape_type == 'Group':
                    sub_found = shape.find_shapes_by_master(master_shape_ID, master_shape_ID)
                    if sub_found:
                        found.extend(sub_found)
            return found  # return list of matching shapes

        def find_shape_by_text(self, text: str) -> VisioFile.Shape:  # returns Shape
            # recursively search for shapes by text and return first match
            for shape in self.sub_shapes():  # type: VisioFile.Shape
                if text in shape.text:
                    return shape
                if shape.shape_type == 'Group':
                    found = shape.find_shape_by_text(text)
                    if found:
                        return found

        def find_shapes_by_text(self, text: str, shapes: List[VisioFile.Shape] = None) -> List[VisioFile.Shape]:
            # recursively search for shapes by text and return all matches
            if not shapes:
                shapes = list()
            for shape in self.sub_shapes():  # type: VisioFile.Shape
                if text in shape.text:
                    shapes.append(shape)
                if shape.shape_type == 'Group':
                    found = shape.find_shapes_by_text(text)
                    if found:
                        shapes.extend(found)
            return shapes

        def find_shape_by_property_label(self, property_label: str) -> VisioFile.Shape:  # returns Shape
            # recursively search for shapes by property name and return first match
            for shape in self.sub_shapes():  # type: VisioFile.Shape
                if property_label in shape.data_properties.keys():
                    return shape
                if shape.shape_type == 'Group':
                    found = shape.find_shape_by_property_label(property_label)
                    if found:
                        return found

        def find_shapes_by_property_label(self, property_label: str, shapes: List[VisioFile.Shape] = None) -> List[VisioFile.Shape]:
            # recursively search for shapes by property name and return all matches
            if not shapes:
                shapes = list()
            for shape in self.sub_shapes():  # type: VisioFile.Shape
                if property_label in shape.data_properties.keys():
                    shapes.append(shape)
                if shape.shape_type == 'Group':
                    found = shape.find_shapes_by_property_label(property_label)
                    if found:
                        shapes.extend(found)
            return shapes

        def apply_text_filter(self, context: dict):
            # check text against all context keys
            text = self.text
            for key in context.keys():
                r_key = "{{" + key + "}}"
                text = text.replace(r_key, str(context[key]))
            self.text = text

            for s in self.sub_shapes():
                s.apply_text_filter(context)

        def find_replace(self, old: str, new: str):
            # find and replace text in this shape and sub shapes
            text = self.text
            self.text = text.replace(old, new)

            for s in self.sub_shapes():
                s.find_replace(old, new)

        def remove(self):
            self.parent.xml.remove(self.xml)

        def append_shape(self, append_shape: VisioFile.Shape):
            # insert shape into shapes tag, and return updated shapes tag
            id_map = self.page.vis.increment_shape_ids(append_shape.xml, self.page)
            self.page.vis.update_ids(append_shape.xml, id_map)
            self.xml.append(append_shape.xml)

        @property
        def connects(self):
            # get list of connect items linking shapes
            connects = list()
            for c in self.page.connects:
                if self.ID in [c.shape_id, c.connector_shape_id]:
                    connects.append(c)
            return connects

        @property
        def connected_shapes(self):
            # return a list of connected shapes
            shapes = list()
            for c in self.connects:
                if c.connector_shape_id != self.ID:
                    shapes.append(self.page.find_shape_by_id(c.connector_shape_id))
                if c.shape_id != self.ID:
                    shapes.append(self.page.find_shape_by_id(c.shape_id))
            return shapes

    class Connect:
        """Connect class to represent a connection between two `VisioFile.Shape` objects"""
        def __init__(self, xml: Element=None, page: VisioFile.Page=None):
            if page is None:
                return
            if type(xml) is Element:  # create from xml
                self.xml = xml
                self.page = page  # type: VisioFile.Page
                self.from_id = xml.attrib.get('FromSheet')  # ref to the connector shape
                self.to_id = xml.attrib.get('ToSheet')  # ref to the shape where the connector terminates
                self.from_rel = xml.attrib.get('FromCell')  # i.e. EndX / BeginX
                self.to_rel = xml.attrib.get('ToCell')  # i.e. PinX

        @staticmethod
        def create(page: VisioFile.Page=None, from_shape: VisioFile.Shape = None, to_shape: VisioFile.Shape = None) -> VisioFile.Shape:
            """Create a new Connect object between from_shape and to_shape

            :returns: a new Connect object
            :rtype: VisioFile.Shape
            """
            if from_shape and to_shape:  # create new connector shape and connect items between this and the two shapes
                # create new connect shape and get id
                media = Media()
                connector_shape = media.straight_connector.copy(page)  # default to straight connector
                connector_shape.text = ''  # clear text used to find shape
                if not os.path.exists(page.vis._masters_folder):
                    # Add masters folder to directory if not already present
                    shutil.copytree(media._media_vsdx._masters_folder, page.vis._masters_folder)
                    page.vis.load_master_pages()  # load copied master page files into VisioFile object
                    # add new master to document relationship
                    page.vis._add_document_rel(rel_type="http://schemas.microsoft.com/visio/2010/relationships/masters",
                                               target="masters/masters.xml")
                    # create masters/master1 elements in [Content_Types].xml
                    page.vis._add_content_types_override(content_type="application/vnd.ms-visio.masters+xml",
                                                         part_name_path="/visio/masters/masters.xml")
                    page.vis._add_content_types_override(content_type="application/vnd.ms-visio.master+xml",
                                                         part_name_path="/visio/masters/master1.xml")

                # update HeadingPairs and TitlesOfParts in app.xml
                if page.vis._get_app_xml_value('Masters') is None:
                    page.vis._set_app_xml_value('Masters', '1')
                if 'Dynamic connector' not in page.vis._titles_of_parts_list():  # todo: replace static string with name from shape
                    page.vis._add_titles_of_parts_item('Dynamic connector')

                # copy style used by new connector shape
                if not page.vis._get_style_by_id(connector_shape.master_shape.line_style_id):
                    # assume same if is ok, todo: use names for match and increment IDs
                    media_style = media._media_vsdx._get_style_by_id(connector_shape.master_shape.line_style_id)
                    page.vis._style_sheets().append(media_style)
                media._media_vsdx.close_vsdx()

                # set Begin and End Trigger formulae for the new shape - linking to shapes in destination page
                beg_trigger = connector_shape.cells.get('BegTrigger')
                beg_trigger.formula = beg_trigger.formula.replace('Sheet.1!', f'Sheet{from_shape.ID}!')
                end_trigger = connector_shape.cells.get('EndTrigger')
                end_trigger.formula = end_trigger.formula.replace('Sheet.2!', f'Sheet{to_shape.ID}!')
                # create connect relationships
                # todo: FromPart="12" and ToPart="3" represent the part of a shape to connection is from/to
                end_connect_xml = f'<Connect xmlns="http://schemas.microsoft.com/office/visio/2012/main" FromSheet="{connector_shape.ID}" FromCell="EndX" FromPart="12" ToSheet="{to_shape.ID}" ToCell="PinX" ToPart="3"/>'
                beg_connect_xml = f'<Connect xmlns="http://schemas.microsoft.com/office/visio/2012/main" FromSheet="{connector_shape.ID}" FromCell="BeginX" FromPart="9" ToSheet="{from_shape.ID}" ToCell="PinX" ToPart="3"/>'

                # Add these new connection relationships to the page
                page.add_connect(VisioFile.Connect(xml=ET.fromstring(end_connect_xml), page=page))
                page.add_connect(VisioFile.Connect(xml=ET.fromstring(beg_connect_xml), page=page))
                return connector_shape

        @property
        def shape_id(self):
            # ref to the shape where the connector terminates - convenience property
            return self.to_id

        @property
        def shape(self) -> VisioFile.Shape:
            return self.page.find_shape_by_id(self.shape_id)

        @property
        def connector_shape_id(self):
            # ref to the connector shape - convenience property
            return self.from_id

        @property
        def connector_shape(self) -> VisioFile.Shape:
            return self.page.find_shape_by_id(self.connector_shape_id)

        def __repr__(self):
            return f"Connect: from={self.from_id} to={self.to_id} connector_id={self.connector_shape_id} shape_id={self.shape_id}"

    class Page:
        """Represents a page in a vsdx file

        :param vis: the VisioFile object the page belongs to
        :type vis: :class:`VisioFile`
        :param name: the name of the page
        :type name: str
        :param connects: a list of Connect objects in the page
        :type connects: List of :class:`Connect`

        """
        def __init__(self, xml: ET.ElementTree, filename: str, page_name: str, vis: VisioFile):
            self._xml = xml
            self.filename = filename
            self.name = page_name
            self.vis = vis
            self.max_id = 0

        def __repr__(self):
            return f"<Page name={self.name} file={self.filename} >"

        @property
        def connects(self):
            return self.get_connects()

        def set_name(self, value: str):
            # todo: change to name property
            pages_filename = self.vis._pages_filename()  # pages contains Page name, width, height, mapped to Id
            pages = file_to_xml(pages_filename)  # this contains a list of pages with rel_id and filename
            page = pages.getroot().find(f"{namespace}Page[{self.index_num + 1}]")
            #print(f"set_name() page={VisioFile.pretty_print_element(page)}")
            if page:
                page.attrib['Name'] = value
                self.name = value
                self.vis.pages_xml = pages

        @property
        def xml(self):
            return self._xml

        @xml.setter
        def xml(self, value):
            self._xml = value

        @property
        def shapes(self):
            """Return a list of :class:`Shape` objects

            Note: typically returns one :class:`Shape` object which itself contains :class:`Shape` objects

            """
            return [VisioFile.Shape(xml=shapes, parent=self, page=self) for shapes in self.xml.findall(f"{namespace}Shapes")]

        def sub_shapes(self) -> List[VisioFile.Shape]:
            """Return list of Shape objects at top level of VisioFile.Page

            :returns: list of `VisioFile.Shape` objects
            :rtype: List[VisioFile.Shape]
            """
            # note that self.shapes should always return a single shape
            return self.shapes[0].sub_shapes()

        def set_max_ids(self):
            # get maximum shape id from xml in page
            for shapes in self.shapes:
                for shape in shapes.sub_shapes():
                    id = shape.get_max_id()
                    if id > self.max_id:
                        self.max_id = id

            return self.max_id

        @property
        def index_num(self):
            # return zero-based index of this page in parent VisioFile.pages list
            return self.vis.pages.index(self)

        def add_connect(self, connect: VisioFile.Connect):
            connects = self.xml.find(f".//{namespace}Connects")
            if connects is None:
                connects = ET.fromstring(f"<Connects xmlns='{namespace[1:-1]}' xmlns:r='http://schemas.openxmlformats.org/officeDocument/2006/relationships'/>")
                self.xml.getroot().append(connects)
                connects = self.xml.find(f".//{namespace}Connects")

            connects.append(connect.xml)

        def get_connects(self):
            elements = self.xml.findall(f".//{namespace}Connect")  # search recursively
            connects = [VisioFile.Connect(xml=e, page=self) for e in elements]
            return connects

        def get_connectors_between(self, shape_a_id: str='', shape_a_text: str='',
                                  shape_b_id: str='', shape_b_text: str=''):
            shape_a = self.find_shape_by_id(shape_a_id) if shape_a_id else self.find_shape_by_text(shape_a_text)
            shape_b = self.find_shape_by_id(shape_b_id) if shape_b_id else self.find_shape_by_text(shape_b_text)
            connector_ids = set(a.ID for a in shape_a.connected_shapes).intersection(
                set(b.ID for b in shape_b.connected_shapes))

            connectors = set()
            for id in connector_ids:
                connectors.add(self.find_shape_by_id(id))
            return connectors

        def apply_text_context(self, context: dict):
            for s in self.shapes:
                s.apply_text_filter(context)

        def find_replace(self, old: str, new: str):
            for s in self.shapes:
                s.find_replace(old, new)

        def find_shape_by_id(self, shape_id) -> VisioFile.Shape:
            for s in self.shapes:
                found = s.find_shape_by_id(shape_id)
                if found:
                    return found

        def _find_shapes_by_id(self, shape_id) -> List[VisioFile.Shape]:
            # return all shapes by ID - should only be used internally
            found = list()
            for s in self.shapes:
                found = s.find_shapes_by_id(shape_id)
                if found:
                    return found
            return found

        def find_shapes_with_same_master(self, shape: VisioFile.Shape) -> List[VisioFile.Shape]:
            # return all shapes with master
            found = list()
            for s in self.shapes:
                found = s.find_shapes_by_master(master_page_ID=shape.master_page_ID,
                                                master_shape_ID=shape.master_shape_ID)
                if found:
                    return found
            return found

        def find_shape_by_text(self, text: str) -> VisioFile.Shape:
            for s in self.shapes:
                found = s.find_shape_by_text(text)
                if found:
                    return found

        def find_shapes_by_text(self, text: str) -> List[VisioFile.Shape]:
            shapes = list()
            for s in self.shapes:
                found = s.find_shapes_by_text(text)
                if found:
                    shapes.extend(found)
            return shapes

        def find_shape_by_property_label(self, property_label: str) -> VisioFile.Shape:
            # return first matching shape with label
            # note: use label rather than name as label is more easily visible in diagram
            for s in self.shapes:
                found = s.find_shape_by_property_label(property_label)
                if found:
                    return found

        def find_shapes_by_property_label(self, property_label: str) -> List[VisioFile.Shape]:
            # return all matching shapes with property label
            shapes = list()
            for s in self.shapes:
                found = s.find_shapes_by_property_label(property_label)
                if found:
                    shapes.extend(found)
            return shapes


def file_to_xml(filename: str) -> ET.ElementTree:
    """Import a file as an ElementTree"""
    try:
        tree = ET.parse(filename)
        return tree
    except FileNotFoundError:
        pass  # return None


def xml_to_file(xml: ET.ElementTree, filename: str):
    """Save an ElementTree to a file"""
    xml.write(filename, xml_declaration=True, method='xml', encoding='UTF-8')


class Media:
    straight_connector_text = 'STRAIGHT_CONNECTOR'
    curved_connector_text = 'CURVED_CONNECTOR'

    def __init__(self):
        basedir = str(os.path.relpath(__file__))
        file_path = os.sep.join(basedir.split(os.sep)[:-1])
        file_path = os.path.join(file_path, 'media', 'media.vsdx')
        self._media_vsdx = VisioFile(file_path)

    @property
    def straight_connector(self):
        return self._media_vsdx.pages[0].find_shape_by_text(Media.straight_connector_text)

    @property
    def curved_connector(self):
        return self._media_vsdx.pages[0].find_shape_by_text(Media.straight_connector_text)
