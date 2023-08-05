from copy import deepcopy
from typing import Any, List, Optional, Union

from fedot.core.dag.graph_node import GraphNode
from fedot.core.pipelines.convert import graph_structure_as_nx_graph


class GraphOperator:
    def __init__(self, graph=None):
        self._graph = graph

    def delete_node(self, node: GraphNode):
        def make_secondary_node_as_primary(node_child, new_type):
            # TODO move classes definition to additional methods
            new_primary_node = new_type(content=node_child.content)
            this_node_children = self.node_children(node_child)
            for node in this_node_children:
                index = node.nodes_from.index(node_child)
                node.nodes_from.remove(node_child)
                node.nodes_from.insert(index, new_primary_node)

        node_children_cached = self.node_children(node)
        self_root_node_cached = self._graph.root_node

        for node_child in self.node_children(node):
            node_child.nodes_from.remove(node)

        if node.nodes_from and len(node_children_cached) == 1:
            for node_from in node.nodes_from:
                node_children_cached[0].nodes_from.append(node_from)
        elif not node.nodes_from:
            for node_child in node_children_cached:
                if not node_child.nodes_from:
                    make_secondary_node_as_primary(node_child, type(node))
        self._graph.nodes.clear()
        self.add_node(self_root_node_cached)

    def delete_subtree(self, node: GraphNode):
        """Delete node with all the parents it has"""
        for node_child in self.node_children(node):
            node_child.nodes_from.remove(node)
        for subtree_node in node.ordered_subnodes_hierarchy():
            self._graph.nodes.remove(subtree_node)

    def update_node(self, old_node: GraphNode, new_node: GraphNode):
        self.actualise_old_node_children(old_node, new_node)
        if ((new_node.nodes_from is None and old_node.nodes_from is None) or
                (new_node.nodes_from is not None and old_node.nodes_from is not None)):
            new_node.nodes_from = old_node.nodes_from
        self._graph.nodes.remove(old_node)
        self._graph.nodes.append(new_node)
        self.sort_nodes()

    def update_subtree(self, old_node: GraphNode, new_node: GraphNode):
        """Exchange subtrees with old and new nodes as roots of subtrees"""
        new_node = deepcopy(new_node)
        self.actualise_old_node_children(old_node, new_node)
        self.delete_subtree(old_node)
        self.add_node(new_node)
        self.sort_nodes()

    def add_node(self, node: GraphNode):
        """
        Add new node to the Pipeline

        :param node: new Node object
        """
        if node not in self._graph.nodes:
            self._graph.nodes.append(node)
            if node.nodes_from:
                for new_parent_node in node.nodes_from:
                    self.add_node(new_parent_node)

    def distance_to_root_level(self, node: GraphNode):
        def recursive_child_height(parent_node: GraphNode) -> int:
            node_child = self.node_children(parent_node)
            if node_child:
                height = recursive_child_height(node_child[0]) + 1
                return height
            else:
                return 0

        height = recursive_child_height(node)
        return height

    def nodes_from_layer(self, layer_number: int) -> List[Any]:
        def get_nodes(node: Any, current_height):
            nodes = []
            if current_height == layer_number:
                nodes.append(node)
            else:
                if node.nodes_from:
                    for child in node.nodes_from:
                        nodes.extend(get_nodes(child, current_height + 1))
            return nodes

        nodes = get_nodes(self._graph.root_node, current_height=0)
        return nodes

    def actualise_old_node_children(self, old_node: GraphNode, new_node: GraphNode):
        old_node_offspring = self.node_children(old_node)
        for old_node_child in old_node_offspring:
            index_of_old_node_in_child_nodes_from = old_node_child.nodes_from.index(old_node)
            old_node_child.nodes_from[index_of_old_node_in_child_nodes_from] = new_node

    def sort_nodes(self):
        """layer by layer sorting"""
        if not isinstance(self._graph.root_node, list):
            nodes = self._graph.root_node.ordered_subnodes_hierarchy()
        else:
            nodes = self._graph.nodes
        self._graph.nodes = nodes

    def node_children(self, node) -> List[Optional[GraphNode]]:
        return [other_node for other_node in self._graph.nodes
                if other_node.nodes_from and
                node in other_node.nodes_from]

    def connect_nodes(self, parent: GraphNode, child: GraphNode):
        if child.descriptive_id not in [p.descriptive_id for p in parent.ordered_subnodes_hierarchy()]:
            if child.nodes_from:
                # if not already connected
                child.nodes_from.append(parent)
            else:
                # add parent to initial node
                new_child = GraphNode(nodes_from=[], content=child.content)
                new_child.nodes_from.append(parent)
                self.update_node(child, new_child)

    def root_node(self) -> Union[GraphNode, List[GraphNode]]:
        if len(self._graph.nodes) == 0:
            return []
        roots = [node for node in self._graph.nodes
                 if not any(self._graph.operator.node_children(node))]
        if len(roots) == 1:
            return roots[0]
        return roots

    def is_graph_equal(self, other_graph: 'Graph') -> bool:
        if isinstance(self._graph.root_node, list):
            if isinstance(other_graph.root_node, list):
                return set([rn.descriptive_id for rn in self._graph.root_node]) == \
                       set([rn.descriptive_id for rn in other_graph.root_node])
            else:
                return False
        elif isinstance(other_graph.root_node, list):
            return False
        else:
            return self._graph.root_node.descriptive_id == other_graph.root_node.descriptive_id

    def graph_description(self) -> str:
        return str({
            'depth': self._graph.depth,
            'length': self._graph.length,
            'nodes': self._graph.nodes,
        })

    def graph_depth(self) -> int:
        if len(self._graph.nodes) == 0:
            return 0

        def _depth_recursive(node: GraphNode):
            if node is None:
                return 0
            if node.nodes_from is None or len(node.nodes_from) == 0:
                return 1
            else:
                return 1 + max([_depth_recursive(next_node) for next_node in node.nodes_from])

        root = self.root_node()
        if isinstance(root, list):
            return max([_depth_recursive(n) for n in root])
        else:
            return _depth_recursive(root)

    def get_nodes_degrees(self):
        """ Nodes degree as the number of edges the node has:
         k = k(in) + k(out)"""
        graph, _ = graph_structure_as_nx_graph(self._graph)
        index_degree_pairs = graph.degree
        node_degrees = [node_degree[1] for node_degree in index_degree_pairs]
        return node_degrees
