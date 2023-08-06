# /usr/bin/python3
####### PACKAGES
from . import anutils as an
import numpy as np

# Check if we can plot stuff
__IPV__ = False
try:
    import ipyvolume as ipv
    __IPV__ = True
except:
    print("Unable to import Ipyvolume")


### This should definitely be in a yaml file
# No really, how stupid is that !!!!
__N_DIM__= 3

# a generic class for an object set
class Object_set(list):
    """ Object_set
        A class that contains a list of objects plus extra methods and properties
        
    """
    def __init__(self, *args, id=1,
                 config=None, name=None,  build=None, type=None, dim=__N_DIM__, **kwargs):
        list.__init__(self)

        # Filling info
        self.name = name
        self.id = id
        self.type = type
        self.plots = []
        self.dim = dim
        # Reading properties
        self.properties = an.get_prop_dicts(config, type=type, name=name)

        # We allow a custom constructor
        if build is not None:
            build(self, *args, **kwargs)
        else:
            self.build_objects(*args, **kwargs)

    # Stupid builder
    def build_objects(self, *args, **kwargs):
        self.append(Object(None))

    # Generic analyzer
    def analyze(self, obj, analyzer=None, *args, **kwargs):
        #analysis = {'id' : obj.id}
        analysis = {}
        if analyzer is not None:
            for name, func in analyzer.items():
                analysis[name] = func(obj)

        return analysis

    # Plots from Object set, with a possibilty to sort which object to sort
    # Saved ploted items to Object_set.plots
    def plot(self,*args, sorter=None, plotter=None, **kwargs):
        if __IPV__:
            # Do we need to sort which objects to plot ?
            if sorter is not None:
                objs = filter(sorter, self)
            else:
                objs = self

            # Is there a custom plotter ?
            if plotter is not None:
                self.plots.extend( plotter(objs, *args, **kwargs))
                return True
            else:
                self.plots.extend( self.plot_objs(objs, *args, **kwargs) )
                return True
        else:
            return False

    # Plot objs is called by Object_set's plot.
    # A method to plot a list of objects
    def plot_objs(self, objs, *args, **kwargs):
        try:
            positions=np.array([obj.position for obj in objs])
            if self.dim==3:
                s = ipv.scatter(positions[:,0], positions[:,1], positions[:,2], **kwargs)
            elif self.dim==2:
                s = ipv.scatter(positions[:, 0], positions[:, 1], 0, **kwargs)
            return [s]
        except:
            print("Did not manage to plot objects %s. Maybe object.position is not defined" %self.name)
        return []



# A class to contain a single object :
class Object():
    """ Object
        Generic object, not completely useless
        Most objects need id and position
        """

    def __init__(self, *args,  id=1, position=None, **kwargs):
        self.id = id
        self.position = position
