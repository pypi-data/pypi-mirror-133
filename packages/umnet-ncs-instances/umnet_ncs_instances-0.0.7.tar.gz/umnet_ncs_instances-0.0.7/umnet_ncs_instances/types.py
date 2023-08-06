from lxml import etree
import logging
import re
import inspect


logging.getLogger(__name__)

class Node:
    '''
    Class that generically represents an xml/yang node
    '''
    _ns = None

    def set_ns(self, value):
        self._ns = value

    @property
    def nsmap(self):
        if self._ns:
            return {None:self._ns}
        else:
            return None



class Container(Node):

    '''
    Class meant to represent a Yang container.
    Basically this is a 'Node' class that can have children.
    Only instance initializer classes are allowed to set children
    '''
    def __setattr__(self, name, value):
        '''
        Limiting who can set container children and how.
        '''
        # private attributes can be set with no restriction,
        # otherwise we'd be stepping on ourselves
        if name.startswith("_"):
            self.__dict__[name] = value
            return

        # if the attribute exists already and we're setting it as the right
        # type, that is fine too
        if name in self.__dict__ and type(self.__dict__[name]) == type(value):
            self.__dict__[name] = value
            return

        # Only the initializer or node functions can create new attribues.
        # looking up who is trying to set an attribute
        caller = inspect.currentframe().f_back
        caller_info = inspect.getframeinfo(caller)
        calling_func = caller_info[2]

        # only the special ncs_instance function 'initialize_model' can set
        # children on containers
        if(calling_func == 'initialize_model'):

            # any assigned value must of one of our special 'yang' types
            if isinstance(value, (Container, LeafList, List, Leaf)):
                self.__dict__[name] = value
            else:
                raise TypeError(f'Can only initialize attributes as Leafs or Nodes')


        # a user can call the 'choice' function on a choice child
        elif(calling_func == 'choose'):
            self.__dict__[name] = value

        # the user can also directly assign a value to a leaf child
        elif(isinstance(self.__dict__[name], Leaf)):
            self.__dict__[name].value = value

        # or they can directly assign a list to a leaflist
        elif isinstance(self.__dict__[name], LeafList) and type(value) == list:
                self.__dict__[name]._values = []

                # assigning each entry in our list individually
                # so that the type is checked
                for v in value:
                    self.__dict__[name].append(v)

    def __getattribute__(self, name):

        '''
        Overloading 'getattribute' so that if someone wants to read
        a Leaf or LeafList attribute they'll get the value
        of the Node
        '''

        obj = super().__getattribute__(name)

        if(isinstance(obj, Leaf)):
            return self.__dict__[name].value
        if(isinstance(obj, LeafList)):
            return self.__dict__[name].values

        return obj
    

    def get_child_nodes(self):
        children = {}
        for name, obj in self.__dict__.items():
            if isinstance(obj,(Leaf, LeafList, List, Container)):
                children[name] = obj
        return children


class Leaf(Node):
    '''
    Leaf class that takes a type in its constructor.
    '''
    def __init__(self, leaf_type:type, value=None):
        self._value = value
        self._type = leaf_type

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if type(value) != self._type:
            raise TypeError(f'Invalid type for {value}, must be {self._type}')
   
        self._value = value


class LeafList(Node):
    '''
    LeafList class that takes a type in its constructor.
    Newly appended items must be of that type
    '''
    def __init__(self, leaf_type:type):
        self._values = []
        self._type = leaf_type

    def append(self, value):
        if isinstance(value, self._type):
            self._values.append(value)
        else:
            raise TypeError(f'Invalid type for {value}, must be {self._type}')

    def extend(self, values:list):
        for v in values:
            self.append(v)

    def remove(self, value):
        self._values.remove(value)

    def __iter__(self):
        return(iter(self._values))

    @property
    def values(self):
        return self._values


class List(Node):
    '''
    Dict class that takes a class type in its constructor.
    Newly-appended items must be of that class.
    '''
    def __init__(self, list_type:'Container', keyattr:str='name'):
        self._class = list_type()
        self._class.initialize_model()
        self._values = {}
        self._keyattr = keyattr

        if keyattr not in self._class.__dict__:
            raise ValueError(f'{keyattr} not an attribute in {self._class}') 

    def __getitem__(self, key):
        return self._values[key]

    def __setitem__(self, key, value):

        # item must be of the right class type
        if(not(isinstance(value, self._class.__class__))):
            raise TypeError(f'Invalid value type, must be {self._class}')

        # set the key value in the object's attribute
        # as well as adding it to our list
        value.__dict__[self._keyattr] = Leaf(type(key))
        setattr(value, self._keyattr, key)
        self._values[key] = value


    def items(self):
        return self._values.items()
    def keys(self):
        return self._values.keys()
    def values(self):
        return self._values.values()
    def pop(self, key):
        return self._values.pop(key)
    
    def __iter__(self):
        return(iter(self._values))

class Choice(Container):
    '''
    Yang 'choice' object model. Basically a specialized container where
    only some of the children are valid.

    Practically speaking, you can set attributes for any/all choices, no 
    matter what you 'choose' w/the choose method. NCSInstance.gen_xml
    does validate that you have chosen which path is valid (by that we mean
    you set the choice attribute) so it knows what to output.
    '''
    def __init__(self, choices:list, choice=None):
        self._choices = [self._pythonify(c) for c in choices]

        if choice:
            self.choose(choice)
        else:
            self._choice = None

    def choose(self, choice:str):
        choice = self._pythonify(choice)

        if choice not in self._choices:
            raise ValueError(f'Invalid choice {choice} for {self}')

        self._choice = choice

    @property
    def choice(self):
        return self._choice

    @property
    def choices(self):
        return self._choices

    def _pythonify(self, value:str):
        return value.replace("-","_")

class NCSInstance(Container):
    '''
    Class that represents a service or device instance.

    The component class must have two static variables:
        '_path' and '_nsmap'. These define where the instance
        lives in the tree and maps xml namespaces to points along
        that path.

    Note that you CANNOT create an NCSInstance along a '_path':
        that indexes into a list. To do that you must define an NCSInstance
    with the List as an attribute, then define a bunch of sub-attributes
    accordingly.

    The initializer of the class should define the structure of
    the instance - once initialized, attributes cannot be added or modified
    at runtime (you can just set values).

       
    '''

    _path = "/config"
    _nsmap = {
            "config":"http://tail-f.com/ns/config/1.0",
            }
    def __init__(self):
        self.initialize_model()



    def _get_path(self):
        '''
        Parses the static _path and _nsmap attributes into a
        list of dicts mapping each node on the path to an
        xml namespace (or none if there was none.)
        '''
        if not(self._path.startswith("/")):
            raise ValueError('_path attribute must be a full path')

        path = self._path[1::].split("/")
        if not(path):
            raise ValueError('Need at least one hop in _path!')

        fq_path = []
        for p in path:
            ns = self._nsmap.get(p, False)
            if ns:
                fq_path.append((p,{None:ns}))
            else:
                fq_path.append((p,None))

        return(fq_path)

    def __eq__(self, other):
        if isinstance(other, NCSInstance):
            return self.gen_xml() == other.gen_xml()
        return False

    def gen_xml(self):
        '''
        Generate xml data based on our NCS instance object.
        '''

        # first lets start our tree based on the "path" attribute
        path = self._get_path()
        
        # root of our tree is the first path element
        first_hop = path.pop(0)
        root = etree.Element(first_hop[0],nsmap=first_hop[1])
        tree = root
        # next nodes on the tree are what's left on the path
        for node, ns in path:
            tree = etree.SubElement(tree, node, nsmap=ns)

        # now we need to add the child attributes of this object
        children = self.get_child_nodes()
        for node_name, node_obj in self.get_child_nodes().items():
            self._walk_tree(tree, node_name, node_obj)

        # convert to string
        xml_str = etree.tostring(root, pretty_print=True)
        xml_str = xml_str.decode('utf-8')

        # if we've got some string munging, apply it here.
        if(hasattr(self,'_xml_munge')):
            for pattern, repl in self._xml_munge.items():
                xml_str = re.sub(pattern, repl, xml_str)

        return xml_str

    def _walk_tree(self, tree:etree.Element, node_name:str, node_obj):

        logging.debug(f'processing node {node_name}, type {type(node_obj)}')
       
        # un-pythonify node names
        node_name = node_name.replace("_","-")

        # skip empty and 'ns' nodes
        if not(node_obj) or node_name=='ns':
            return

        # Leaf processing - just need to extract leaf value and set as text
        if isinstance(node_obj, Leaf):
            logging.debug(f'saving leaf value {node_obj.value}')
            if node_obj.value != None:
                xml_node = etree.SubElement(tree, node_name, nsmap=node_obj.nsmap)
                xml_node.text = str(node_obj.value)
            return
        
        # LeafList - extract leaf values for all items in list
        if isinstance(node_obj, LeafList):
            logging.debug(f'saving leaflist values {list(node_obj)}')
            for n in node_obj:
                xml_node = etree.SubElement(tree, node_name, nsmap=node_obj.nsmap)
                xml_node.text = str(n)
            return

        # List - a dictionary of containers
        if isinstance(node_obj, List):

            for entry_name, entry_data in node_obj.items():
                logging.debug(f'processing list object {entry_name}')
                xml_list_entry = etree.SubElement(tree, node_name, nsmap=node_obj.nsmap)
                children = entry_data.get_child_nodes()
                for name, obj in children.items():
                    self._walk_tree(xml_list_entry, name, obj)

        # a choice node is a container where we follow the 'chosen'
        # path only
        elif isinstance(node_obj, Choice):

            # need to follow the chosen path
            if(node_obj.choice==None):
                raise ValueError(f'Need to set {node_name} choice!')

            child_name = node_obj.choice
            child_obj = node_obj.__dict__[child_name]
            logging.debug(f'choice is {child_name} {type(child_obj)}')
            self._walk_tree(tree, child_name, child_obj)

        # container is a container
        elif isinstance(node_obj, Container):
            xml_container = etree.SubElement(tree, node_name, nsmap=node_obj.nsmap)
            children = node_obj.get_child_nodes()
            for name, obj in children.items():
                self._walk_tree(xml_container, name, obj)



