__author__ = 'hadware'

from enum import Enum
class GridObjectType(Enum):
    CIRCLE = 1
    SQUARE = 2
    ELLIPSE = 3
    RHOMBUS = 4

class SvgTag:

    def __init__(self):
        self.name = None
        self.inner_tags = []

    def add_internal_tag(self, tag):
        if isinstance(tag, list):
            self.inner_tags += tag
        else:
            self.inner_tags.append(tag)

    def _print_header(self):
        pass

    def to_string(self):
        inner_tags_render = "\n".join([tag.to_string() for tag in self.inner_tags])

        return """<%s %s>
        %s
        </%s>""" % (self.name, self._print_header(), inner_tags_render, self.name)

class GroupTag(SvgTag):

    def __init__(self, translate_coord = None):
        super().__init__()
        self.name = "g"
        self.translate_coord = translate_coord

class ShapeTag(SvgTag):
    def __init__(self, width, height, coordinate = None, type = None):
        super().__init__()
        self.coordinate = coordinate
        self.width = width
        self.height = height
        self.type = type

class SvgFile:
    """Stores all of what should be printed on the SVG file in a list of objects"""

    def __init__(self):
        self.header_tag_list = []
        self.body_tag_list = []


