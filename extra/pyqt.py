
from PyQt4 import QtGui


# settings are stored in a dictionary named std_settings, they are 
#  {'Get Setting Exec ({n})', 'Set Setting Exec({n})') : 
#         ('GetInput', 'SetInput')}
#  Where {0} should be formatted with the value given by the settings dict
#  A default setting == None indicates that something special has to be
#  done
#   Everything put into settings MUST BE PICKLEABLE
#   Also keep in mind that everything has to be it's representation, as
#   Readable by a python interpreter. So SetInput should not be "hello world"
#   but rather '"hello world"' or repr("hello world")

class StdWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(StdWidget, self).__init__(parent)

    def save_settings(self, application_settings):
        '''Puts own settings into the application_settings dict
        
        This function is to-be extended by the parent class.
        It retuturns a dict of settings that still need to be gotten.
        
        All upper level functions should return the same thing -- the highest
        level function does error checking by ensuring that bool(need_settings)
            == False
        '''
        assert(self._NAME_ not in application_settings)
        settings = {}

        need_settings = {}
        # save settings that can be proccessed.
        for key, value in self.std_settings.iteritems():
            getexec, setexec = key
            getval, setval = value
            if getval == None:
                need_settings[key] = getval, setval
            else:
                try:
                    gotval = eval(getexec)(*getval)
                    # TODO: have an Args return type that doesn't
                    # convert to single element tuple
                    settings[key] = getval, (gotval,)
                except Exception as E:
                    print "ERROR: Failure to save settings!"
                    print 'Class name:', self._NAME_
                    print 'Error:', E                    
                    print "SYNTAX:", getexec, getval
#                    import pdb; pdb.set_trace()
                    
        application_settings[self._NAME_] = settings
        return need_settings
        
    def load_settings(self, application_settings):
        '''Load settings given the previous settings from the 
        application settings
        
        Returns the settings that still need to be loaded. All
        implementations of this function should do the same (for error
            checking at top level)
        '''
        std_settings = self.std_settings        
        try:
            settings = application_settings[self._NAME_]
        except KeyError:
            settings = std_settings
        # remove unrecognized settings
        for key in tuple(settings.keys()):
            if key not in std_settings:
                del settings[key]
            
        # add settings not specified
        for key in std_settings.iterkeys():
            if key not in settings:
                settings[key] = std_settings[key]
        
        need_settings = {}
        # process settings that can be processed+?expect(.*?)(t+?expect(.*?)(t
        for key, item in settings.iteritems():
            getexec, setexec = key
            getval, setval = item

            if setval == None:
                need_settings[key] = getval, setval
            else:
                try:
                    eval(setexec)(*setval)
                except Exception as E:
                    print "ERROR: Failure to load settings!"
                    print 'Name', self._NAME_
                    print 'Error:', E                    
                    print "SYNTAX:", setexec, setval
                    print '\n', 'Loading default setting'
#                    import pdb; pdb.set_trace()
                    eval(key[1])(*std_settings[key][1])
        # return settings that still need to be loaded in -- 
        #  to be used in parent
        return need_settings