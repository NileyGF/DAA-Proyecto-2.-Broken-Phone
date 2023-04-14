
class Graph:
    """ A Graph stores nodes and edges with optional data, or attributes.
        Nodes can be arbitrary (hashable) Python objects with optional
        key/value attributes, except that `None` is not allowed as a node.
        Edges are represented as links between nodes with optional
        key/value attributes.
    """
    def __init__(self):
        self.graph = dict()    # dictionary for graph attributes
        self._node = dict()    # empty node attribute dict
        self._adj = dict()     # empty adjacency dict
    def adj(self):
        """Graph adjacency object holding the neighbors of each node.
        This object is a read-only dict-like structure with node keys
        and neighbor-dict values.  The neighbor-dict is keyed by neighbor
        to the edge-data-dict.  So `G.adj[3][2]['color'] = 'blue'` sets
        the color of the edge `(3, 2)` to `"blue"`.
        """
        return self._adj
    @property
    def name(self):
        """String identifier of the graph.
        This graph attribute appears in the attribute dict G.graph
        keyed by the string `"name"`. as well as an attribute (technically
        a property) `G.name`. This is entirely user controlled.
        """
        return self.graph.get("name", "")
    @name.setter
    def name(self, s):
        self.graph["name"] = s
    def __str__(self):
        """Returns a short summary of the graph"""
        return "".join(
            [
                type(self).__name__,
                f" named {self.name!r}" if self.name else "",
                f" with {self.number_of_nodes()} nodes and {self.number_of_edges()} edges",
            ]
        )
    def __iter__(self):
        """Iterate over the nodes. Use: 'for n in G'"""
        return iter(self._node)
    def __contains__(self, n):
        """Returns True if n is a node, False otherwise. Use: 'n in G'"""
        try:
            return n in self._node
        except TypeError:
            return False
    def __len__(self):
        """Returns the number of nodes in the graph. Use: 'len(G)'"""
        return len(self._node)
    def __getitem__(self, n):
        """Returns a dict of neighbors of node n.  Use: 'G[n]'.
        G[n] is the same as G.adj[n] and similar to G.neighbors(n)
        """
        return self.adj[n]

    def add_node(self, node_for_adding):
        """Add a single node `node_for_adding` and update node attributes  """
        if node_for_adding not in self._node:
            if node_for_adding is None:
                raise ValueError("None cannot be a node")
            self._adj[node_for_adding] = dict()
            self._node[node_for_adding] = dict()

    def remove_node(self, n):
        """Remove node n.
        Removes the node n and all adjacent edges.
        Attempting to remove a non-existent node will raise an exception.
        """
        adj = self._adj
        try:
            nbrs = list(adj[n])  
            del self._node[n]
        except KeyError as err:  
            raise KeyError(f"The node {n} is not in the graph.") from err
        for u in nbrs:
            del adj[u][n]  # remove all edges n-u in graph
        del adj[n]  # now remove node

    def nodes(self):
        """A NodeView of the Graph as G.nodes or G.nodes().
        Can be used as `G.nodes` for data lookup and for set-like operations.
        Can also be used as `G.nodes(data='color', default=None)` to return a
        NodeDataView which reports specific node data but no set operations.
        It presents a dict-like interface as well with `G.nodes.items()`
        iterating over `(node, nodedata)` 2-tuples and `G.nodes[3]['foo']`
        providing the value of the `foo` attribute for node `3`. In addition,
        a view `G.nodes.data('foo')` provides a dict-like interface to the
        `foo` attribute of each node. `G.nodes.data('foo', default=1)`
        provides a default for nodes that do not have attribute `foo`.
        Parameters
        ----------
        data : string or bool, optional (default=False)
            The node attribute returned in 2-tuple (n, ddict[data]).
            If True, return entire node attribute dict as (n, ddict).
            If False, return just the nodes n.
        default : value, optional (default=None)
            Value used for nodes that don't have the requested attribute.
            Only relevant if data is not True or False.
        Returns
        -------
        NodeView
            Allows set-like operations over the nodes as well as node
            attribute dict lookup and calling to get a NodeDataView.
            A NodeDataView iterates over `(n, data)` and has no set operations.
            A NodeView iterates over `n` and includes set operations.
            When called, if data is False, an iterator over nodes.
            Otherwise an iterator of 2-tuples (node, attribute value)
            where the attribute is specified in `data`.
            If data is True then the attribute becomes the
            entire data dictionary.
        Notes
        -----
        If your node data is not needed, it is simpler and equivalent
        to use the expression ``for n in G``, or ``list(G)``.
        Examples
        --------
        There are two simple ways of getting a list of all nodes in the graph:
        >>> G = nx.path_graph(3)
        >>> list(G.nodes)
        [0, 1, 2]
        >>> list(G)
        [0, 1, 2]
        To get the node data along with the nodes:
        >>> G.add_node(1, time="5pm")
        >>> G.nodes[0]["foo"] = "bar"
        >>> list(G.nodes(data=True))
        [(0, {'foo': 'bar'}), (1, {'time': '5pm'}), (2, {})]
        >>> list(G.nodes.data())
        [(0, {'foo': 'bar'}), (1, {'time': '5pm'}), (2, {})]
        >>> list(G.nodes(data="foo"))
        [(0, 'bar'), (1, None), (2, None)]
        >>> list(G.nodes.data("foo"))
        [(0, 'bar'), (1, None), (2, None)]
        >>> list(G.nodes(data="time"))
        [(0, None), (1, '5pm'), (2, None)]
        >>> list(G.nodes.data("time"))
        [(0, None), (1, '5pm'), (2, None)]
        >>> list(G.nodes(data="time", default="Not Available"))
        [(0, 'Not Available'), (1, '5pm'), (2, 'Not Available')]
        >>> list(G.nodes.data("time", default="Not Available"))
        [(0, 'Not Available'), (1, '5pm'), (2, 'Not Available')]
        If some of your nodes have an attribute and the rest are assumed
        to have a default attribute value you can create a dictionary
        from node/attribute pairs using the `default` keyword argument
        to guarantee the value is never None::
            >>> G = nx.Graph()
            >>> G.add_node(0)
            >>> G.add_node(1, weight=2)
            >>> G.add_node(2, weight=3)
            >>> dict(G.nodes(data="weight", default=1))
            {0: 1, 1: 2, 2: 3}
        """
        return NodeView(self)

    def order(self):
        """Returns the number of nodes in the graph."""
        return len(self._node)

    def has_node(self, n):
        """Returns True if the graph contains the node n.
        Identical to `n in G`
        Parameters
        ----------
        n : node
        Examples
        --------
        >>> G = nx.path_graph(3)  # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> G.has_node(0)
        True
        It is more readable and simpler to use
        >>> 0 in G
        True
        """
    def add_edge(self, u_of_edge, v_of_edge):
        """Add an edge between u and v.
        The nodes u and v will be automatically added if they are
        not already in the graph.
        """
        u, v = u_of_edge, v_of_edge
        # add nodes
        self.add_node(u)
        self.add_node(v)

        # add the edge
        datadict = self._adj[u].get(v, dict())
        
        self._adj[u][v] = datadict
        self._adj[v][u] = datadict 
    def remove_edge(self, u, v):
        """Remove the edge between u and v.
        Error if there is not an edge between u and v.
        """
        try:
            del self._adj[u][v]
            del self._adj[v][u]
        except KeyError as err:
            raise KeyError(f"The edge {u}-{v} is not in the graph") from err
    def has_edge(self, u, v):
        """Returns True if the edge (u, v) is in the graph.
        This is the same as `v in G[u]` without KeyError exceptions.
        """
        try:
            return v in self._adj[u]
        except KeyError:
            return False  
    def neighbors(self, n):
        """Returns an iterator over all neighbors of node n.
        This is identical to `iter(G[n])`
        """
        try:
            return iter(self._adj[n])
        except KeyError as err:
            raise KeyError(f"The node {n} is not in the graph.") from err
    def edges(self):
        """An EdgeView of the Graph as G.edges or G.edges().
        edges(self, nbunch=None, data=False, default=None)
        The EdgeView provides set-like operations on the edge-tuples
        as well as edge attribute lookup. When called, it also provides
        an EdgeDataView object which allows control of access to edge
        attributes (but does not provide set-like operations).
        Hence, `G.edges[u, v]['color']` provides the value of the color
        attribute for edge `(u, v)` while
        `for (u, v, c) in G.edges.data('color', default='red'):`
        iterates through all the edges yielding the color attribute
        with default `'red'` if no color attribute exists.
        """
        return EdgeView(self)
    def get_edge_data(self, u, v, default=None):
        """Returns the attribute dictionary associated with edge (u, v).
        This is identical to `G[u][v]` except the default is returned
        instead of an exception if the edge doesn't exist.
        """
        try:
            return self._adj[u][v]
        except KeyError:
            return default
    def adjacency(self):
        """Returns an iterator over (node, adjacency dict) tuples for all nodes """
        return iter(self._adj.items())
     def degree(self):
        """A DegreeView for the Graph as G.degree or G.degree().
        The node degree is the number of edges adjacent to the node.
        The weighted node degree is the sum of the edge weights for
        edges incident to that node.
        This object provides an iterator for (node, degree) as well as
        lookup for the degree for a single node.
        """
        return DegreeView(self)
    def clear(self):
        """Remove all nodes and edges from the graph.
        This also removes the name, and all graph, node, and edge attributes.
        """
        self._adj.clear()
        self._node.clear()
        self.graph.clear()
    def clear_edges(self):
        """Remove all edges from the graph without altering nodes """
        for neighbours_dict in self._adj.values():
            neighbours_dict.clear()
    def copy(self, as_view=False):
        """Returns a copy of the graph"""
        
        G = self.__class__()
        G.graph.update(self.graph)
        G.add_nodes_from((n, d.copy()) for n, d in self._node.items())
        G.add_edges_from(
            (u, v, datadict.copy())
            for u, nbrs in self._adj.items()
            for v, datadict in nbrs.items()
        )
        return G
    def subgraph(self, nodes):
        """Returns a SubGraph view of the subgraph induced on `nodes`.
        The induced subgraph of the graph contains the nodes in `nodes`
        and the edges between those nodes.
        -----
        The graph, edge and node attributes are shared with the original graph.
        Changes to the graph structure is ruled out by the view, but changes
        to attributes are reflected in the original graph.
        To create a subgraph with its own copy of the edge/node attributes use:
        G.subgraph(nodes).copy()
        For an inplace reduction of a graph to a subgraph you can remove nodes:
        G.remove_nodes_from([n for n in G if n not in set(nodes)])
        Subgraph views are sometimes NOT what you want. In most cases where
        you want to do more than simply look at the induced edges, it makes
        more sense to just create the subgraph as its own graph with code like:
        ::
            # Create a subgraph SG based on a (possibly multigraph) G
            SG = G.__class__()
            SG.add_nodes_from((n, G.nodes[n]) for n in largest_wcc)
            if SG.is_multigraph():
                SG.add_edges_from((n, nbr, key, d)
                    for n, nbrs in G.adj.items() if n in largest_wcc
                    for nbr, keydict in nbrs.items() if nbr in largest_wcc
                    for key, d in keydict.items())
            else:
                SG.add_edges_from((n, nbr, d)
                    for n, nbrs in G.adj.items() if n in largest_wcc
                    for nbr, d in nbrs.items() if nbr in largest_wcc)
            SG.graph.update(G.graph)
        Examples
        --------
        >>> G = nx.path_graph(4)  # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> H = G.subgraph([0, 1, 2])
        >>> list(H.edges)
        [(0, 1), (1, 2)]
        """
        induced_nodes = self.nbunch_iter(nodes)
        # if already a subgraph, don't make a chain
        subgraph = nx.graphviews.subgraph_view
        if hasattr(self, "_NODE_OK"):
            return subgraph(self._graph, induced_nodes, self._EDGE_OK)
        return subgraph(self, induced_nodes)

    def edge_subgraph(self, edges):
        """Returns the subgraph induced by the specified edges.
        The induced subgraph contains each edge in `edges` and each
        node incident to any one of those edges.
        -----
        The graph, edge, and node attributes in the returned subgraph
        view are references to the corresponding attributes in the original
        graph. The view is read-only.
        To create a full graph version of the subgraph with its own copy
        of the edge or node attributes, use::
            G.edge_subgraph(edges).copy()
        Examples
        --------
        >>> G = nx.path_graph(5)
        >>> H = G.edge_subgraph([(0, 1), (3, 4)])
        >>> list(H.nodes)
        [0, 1, 3, 4]
        >>> list(H.edges)
        [(0, 1), (3, 4)]
        """
        return nx.edge_subgraph(self, edges)

    def size(self):
        """Returns the number of edges or total of all edge weights 
            G.degree = 2 * size
            Hence size = G.degree // 2
        """
        s = sum(d for v, d in self.degree())
        return s // 2 
    def nbunch_iter(self, nbunch=None):
        """Returns an iterator over nodes contained in nbunch that are
        also in the graph.
        The nodes in nbunch are checked for membership in the graph
        and if not are silently ignored.
        """
        if nbunch is None:  # include all nodes via iterator
            bunch = iter([])
        elif nbunch in self:  # if nbunch is a single node
            bunch = iter([nbunch])
        else:  # if nbunch is a sequence of nodes

            def bunch_iter(nlist, adj):
                try:
                    for n in nlist:
                        if n in adj:
                            yield n
                except TypeError as err:
                    exc, message = err, err.args[0]
                    # capture error for non-sequence/iterator nbunch.
                    if "iter" in message:
                        exc = TypeError(
                            "nbunch is not a node or a sequence of nodes."
                        )
                    # capture error for unhashable node.
                    if "hashable" in message:
                        exc = TypeError(
                            f"Node {n} in sequence nbunch is not a valid node."
                        )
                    raise exc

            bunch = bunch_iter(nbunch, self._adj)
        return bunch