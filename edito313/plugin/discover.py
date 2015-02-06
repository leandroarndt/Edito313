'''
Discovers active plugins and return them (or their URLs or views).

Note that there must be a directory named "plugin" inside the
SITEPATH environment variable (which gets defined by the provided wsgi.py
script if needed). Inside it, all directories listed in the .pth files are
considered installed plugins.
'''

# Imports the module at the plugin directory.

# TODO: DownloadedPlugin.discover()
class DownloadedPlugin(object):
    '''
    Represents a plugin installed on the file system.
    '''
    inited = False
    
    # List of active plugins
    active = []
    
    # List of all plugins
    all = []
    
    # List of active plugins' url modules
    urls = []
    
    @classmethod
    def discover(cls):
        '''
        Discovers modules on PLUGINSPATH and puts them on "active" and "all" lists.
        
        This class method is run on the first time the module is imported.
        '''
        
        cls.inited = True

    def __init__(self, params):
        '''
        Constructor
        '''

if not DownloadedPlugin.inited:
    import plugin # initiate this module
    DownloadedPlugin.discover()