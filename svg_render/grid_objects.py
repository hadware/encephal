
__author__ = 'hadware'

from svg_render.network_elements import ElementType
from enum import Enum
from svg_render.cdata_patch import ET
from math import sqrt

DEFAULT_CSS_PATH = "graph_style.css"

class GridObjectType(Enum):
    RECT = 1
    ELLIPSE = 2
    RHOMBUS = 3

class GridObject:

    def __init__(self, object):
        self.original_object_ref = object

    def svg_tag(self):
        """returns a string containing the svg markup of this shape"""
        pass

class GraphObject(GridObject):

    def __init__(self, object):
        super().__init__(object)
        self.type = GraphObject.translate_element_to_shape(object)

    @classmethod
    def translate_element_to_shape(cls, element):
        switch_dict = {ElementType.CONNEXION : GridObjectType.RHOMBUS,
                       ElementType.NODE : GridObjectType.ELLIPSE,
                       ElementType.SUBNET : GridObjectType.RECT}
        return switch_dict[element.type]

    def set_dimensions(self, height, width):
        self.height = height
        self.width = width

    def set_offset(self, y_offset):
        self.y_offset = y_offset

    def calc_inner_shape_offset(self, graph_objects_height):
        self.inner_shape_offset = self.height / 2 - graph_objects_height / 2

    def insert_into_svg_tree(self, tree):
        grid_cell = ET.SubElement(tree, "g", transform="translate(0,%d)" % self.y_offset)

        switch_dict = {GridObjectType.RHOMBUS : "node_rhombus",
                       GridObjectType.ELLIPSE : "node_ellipse",
                       GridObjectType.RECT : "node_rect"}

        graphical_symbol = ET.SubElement(grid_cell, "use", y=str(self.inner_shape_offset))
        graphical_symbol.set("xlink:href", "#" + switch_dict[self.type])


class HorizontalArrow(GraphObject):

    def insert_into_svg_tree(self, tree):
        grid_cell = ET.SubElement(tree, "g", transform="translate(0,%d)" % self.y_offset)
        graphical_symbol = ET.SubElement(grid_cell, "use", y=str(self.inner_shape_offset))
        graphical_symbol.set("xlink:href", "#horizontal_arrow")

class Arrow(GridObject):
    pass

class ConnectorArrow(Arrow):

    def __init__(self, object, from_index, to_index):
        super().__init__(object)
        self.from_index = from_index
        self.to_index = to_index

    def set_start_and_end(self, start_coord, end_coord):
        self.start_coord = start_coord
        self.end_coord = end_coord

    def insert_into_svg_tree(self, tree):
        arrow_tag = ET.SubElement(tree, "line",
                                  x1=str(self.start_coord[0]),
                                  y1=str(self.start_coord[1]),
                                  x2=str(self.end_coord[0]),
                                  y2=str(self.end_coord[1]))



class GraphColumn:
    """A column in a graph, mainly a list of SvgObjects"""

    def __init__(self, element_list = None):
        if element_list is not None:
            self.svg_object_list = element_list
        else:
            self.svg_object_list = []

    def add_svg_object(self, svg_object):
        """Adds an SVG object to the column"""
        self.svg_object_list.append(svg_object)

    def insert_into_svg_tree(self, tree):
        pass


class ArrowColumn(GraphColumn):
    """A column containing arrows pointing to elements"""

    def set_elements_property(self, right_hand_column, left_hand_column):
        for element in self.svg_object_list:
            start_coord = list(right_hand_column.middle_coordinates_of_cell_right_side(element.from_index))
            end_coord = list(left_hand_column.middle_coordinates_of_cell_left_side(element.to_index))
            element.set_start_and_end(start_coord, end_coord)

    def insert_into_svg_tree(self, tree):
        for arrow in self.svg_object_list:
            arrow.insert_into_svg_tree(tree)


class ElementColumn(GraphColumn):
    """A column of elements, can be any type of svg object (geometrical objects or arrows) """

    def object_reference_index(self, graph_element_reference):
        """Returns the index of the svg object pointing to the graph element in the column,
        or None if it doesn't exist"""
        for i, svg_object in enumerate(self.svg_object_list):
            if svg_object.original_object_ref == graph_element_reference:
                return i

        return None

    def calc_cell_dimensions(self, graph_dimensions):
        self.cell_height = graph_dimensions.graph_height / len(self.svg_object_list)
        self.width = graph_dimensions.column_width

    def set_column_offset(self, x_offset):
        """Sets the x-offset for the whole column"""
        self.x_offset = x_offset

    def set_elements_property(self, graph_dimensions):
        """Asks the column to set its element's positional properties (size and offset)"""
        for i, element in enumerate(self.svg_object_list):
            element.set_offset(self.cell_height * i)
            element.set_dimensions(self.cell_height, self.width)
            element.calc_inner_shape_offset(graph_dimensions.graph_objects_height)

    def middle_coordinates_of_cell_left_side(self, cell_index):
        return self.x_offset, self.svg_object_list[cell_index].y_offset + self.cell_height / 2

    def middle_coordinates_of_cell_right_side(self, cell_index):
        return self.x_offset + self.width, self.svg_object_list[cell_index].y_offset + self.cell_height / 2

    def insert_into_svg_tree(self, tree):
        column_group = ET.SubElement(tree, "g", transform="translate(%d,0)" % self.x_offset)
        column_group.set("class", "element_column column")

        for element in self.svg_object_list:
            element.insert_into_svg_tree(column_group)


class GridDimensions:
    """Computes and stores most of the dimensions needed to render the graph svg file"""

    def __init__(self, graph_width, graph_height, column_count, elements_per_column_max):
        self.graph_height = graph_height
        self.graph_width = graph_width
        self.column_width = int(graph_width / column_count)
        self.min_grid_cell_height = graph_height / elements_per_column_max
        self.graph_objects_height = self.min_grid_cell_height/2
        self.border = 30

class SvgTree:
    """Takes care of building the XML tree and rendering the actual file"""

    def __init__(self, grid_dimensions):
        self.grid_dimensions = grid_dimensions
        self.root = ET.Element("svg",
                               width=str(grid_dimensions.graph_width + grid_dimensions.border * 2),
                               height=str(grid_dimensions.graph_height + grid_dimensions.border*2))
        self.inner_svg = ET.SubElement(self.root, "svg",
                                       width=str(grid_dimensions.graph_width),
                                       heigh=str(grid_dimensions.graph_height),
                                       x=str(grid_dimensions.border),
                                       y=str(grid_dimensions.border))

        self._add_style()
        self._add_defs()

    def _add_style(self):
        """Adds the css style from an external css file directly intro the tree"""
        style = ET.SubElement(self.inner_svg, "style", type="text/css")
        cdata = ET.SubElement(style, '![CDATA[')
        with open(DEFAULT_CSS_PATH, "r") as css_file:
            cdata.text = css_file.read()

    def _add_defs(self):
        """Adds graphical element references in the tree for later 'use' by the GraphObject classes"""
        defs = ET.SubElement(self.inner_svg, "defs")

        #adding shape refs
        def_ellipse = ET.SubElement(defs, "ellipse", id="node_ellipse",
                                    cx=str(self.grid_dimensions.column_width/2),
                                    cy=str(self.grid_dimensions.graph_objects_height/2),
                                    rx=str(self.grid_dimensions.column_width/2),
                                    ry=str(self.grid_dimensions.graph_objects_height/2))

        def_rect = ET.SubElement(defs, "rect", id="node_rect",
                                 width=str(self.grid_dimensions.column_width),
                                 height=str(self.grid_dimensions.graph_objects_height))

        def_rhombus= ET.SubElement(defs, "polygon", id="node_rhombus",
                                   points="%f, %f  %f,%f %f,%f %f,%f"
                                          % (0, self.grid_dimensions.graph_objects_height/2,
                                             self.grid_dimensions.column_width / 2, 0,
                                             self.grid_dimensions.column_width, self.grid_dimensions.graph_objects_height / 2,
                                             self.grid_dimensions.column_width /2, self.grid_dimensions.graph_objects_height))

        horizontal_arrow = ET.SubElement(defs, "g", id="horizontal_arrow")
        inner_line = ET.SubElement(horizontal_arrow, "line",
                                   x1=str(0),
                                   y1=str(self.grid_dimensions.graph_objects_height/2),
                                   x2=str(self.grid_dimensions.column_width),
                                   y2=str(self.grid_dimensions.graph_objects_height/2))


    def get_grid_root(self):
        """Returns the tree's node in which the grid elements will be inserted"""
        return self.inner_svg

    def write_svg_file(self, filename):
        """Writes the SVG file"""
        tree = ET.ElementTree(self.root)
        tree.write(filename)

class GraphGrid:
    """Stores the actual geometrical objects in a grid"""

    def __init__(self, hierarchy_tree):
        """Builds the grid using the hierarchy tree"""
        self.max_vertical_subdivison_number = max([len(node_list) for node_list in hierarchy_tree])
        self.hierarchy_tree_height = len(hierarchy_tree)
        self.column_number = self.hierarchy_tree_height * 2 - 1

        # building a grid of the graphical elements, using the tree.
        # The grid is pretty close to what will actually be displayed on the SVG document
        self.columns =[ElementColumn([ GraphObject(element) for element in hierarchy_tree[0]])]
        # iterating through all the tree's layers, building the grid using both the last layer printed on the grid,
        # and the
        for i, element_list in enumerate(hierarchy_tree[:-1]):
            new_arrow_column = ArrowColumn()
            new_svg_objects_column = ElementColumn()

            for element_index_in_column, svg_object in enumerate(self._previous_element_column().svg_object_list):

                for current_element in svg_object.original_object_ref.connected_to:
                    # if a svg_object (arrow or else) has already been added to the next colmun, we'll just to add the arrow
                    # it points to
                    svg_object_index_in_next_column = new_svg_objects_column.object_reference_index(current_element)

                    if svg_object_index_in_next_column is None:
                        # the index is none, so we actually have to add something

                        # if the current_element is in the next row of the hierarchy tree it should be added to
                        # the new column, else we just add an arrow
                        if current_element in hierarchy_tree[i+1]:
                            new_svg_objects_column.add_svg_object(GraphObject(current_element))
                        else:
                            new_svg_objects_column.add_svg_object(HorizontalArrow(current_element))

                        #now the column index shouldn't be none, since we've added the elemnt to the column
                        svg_object_index_in_next_column = new_svg_objects_column.object_reference_index(current_element)

                    # adding the arrow pointing to the new element in the intermediate "arrow" column
                    new_arrow_column.add_svg_object(ConnectorArrow(object=current_element,
                                                                   from_index=element_index_in_column,
                                                                   to_index=svg_object_index_in_next_column))
            self.columns += [new_arrow_column, new_svg_objects_column]

    def _previous_element_column(self):
        for column in reversed(self.columns):
            if isinstance(column, ElementColumn):
                return column

        return None

    def _get_elements_columns(self):
        return [column for column in self.columns if isinstance(column, ElementColumn)]

    def render_svg(self, filename, graph_height, graph_length):
        """Renders the actual XML """

        graph_dimensions = GridDimensions(graph_height=graph_height,
                                          graph_width=graph_length,
                                          column_count=len(self.columns),
                                          elements_per_column_max=max([len(column.svg_object_list) for column in self.columns if isinstance(column, ElementColumn)]))


        #telling each cell for each column its dimension and where it should be on the svg layout
        for i, column in enumerate(self._get_elements_columns()):
            column.calc_cell_dimensions(graph_dimensions)
            column.set_column_offset(i * graph_dimensions.column_width * 2)
            column.set_elements_property(graph_dimensions)

        for i, column in enumerate(self.columns):
            if isinstance(column, ArrowColumn):
                column.set_elements_property(self.columns[i-1], self.columns[i+1])


        # making the XML tree corresponding to the SVG file
        svg_file = SvgTree(grid_dimensions=graph_dimensions)

        #asks each column element to add itself to the svg tree
        for column in self.columns:
            column.insert_into_svg_tree(svg_file.get_grid_root())

        svg_file.write_svg_file(filename)

