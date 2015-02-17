__author__ = 'hadware'

from svg_render.svg_objects import GridObjectType
from svg_render.network_elements import ElementType


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
                       ElementType.NODE : GridObjectType.CIRCLE,
                       ElementType.SUBNET : GridObjectType.SQUARE}
        return switch_dict[element.type]

    def set_dimension(self, height, width):
        self.height = height
        self.width = width

    def set_offset(self, x_offset, y_offset):
        self.x_offset = x_offset
        self.y_offset = y_offset

    def get_left_side_middle_abs_coord(self):
        return self.x_offset, self.y_offset + self.height / 2

    def get_right_side_middle_abs_coord(self):
        return self.x_offset + self.width, self.y_offset + self.height / 2

class Arrow(GridObject):
    pass

class ConnectorArrow(Arrow):

    def __init__(self, object, from_index, to_index):
        super().__init__(object)
        self.from_index = from_index
        self.to_index = to_index

class HoritontalArrow(GraphObject):
    pass

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

class ArrowColumn(GraphColumn):
    """A column containing arrows pointing to elements"""
    pass

class ElementColumn(GraphColumn):
    """A column of elements, can be any type of svg object (geometrical objects or arrows) """

    def object_reference_index(self, graph_element_reference):
        """Returns the index of the svg object pointing to the graph element in the column,
        or None if it doesn't exist"""
        for i, svg_object in enumerate(self.svg_object_list):
            if svg_object.original_object_ref == graph_element_reference:
                return i

        return None

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
                            new_svg_objects_column.add_svg_object(HoritontalArrow(current_element))

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

    def render_svg(self, graph_height, graph_length):
        """Renders the actual XML """

        #computing dimensions for objects
        column_length = graph_length / len(self.columns)
        min_grid_cell_height = graph_height / max([len(column.svg_object_list) for column in self.columns if isinstance(column, ElementColumn)])
        graph_objects_height = min_cell_height/2

        #telling each cell for each column its dimension and where it should be on the svg layout



