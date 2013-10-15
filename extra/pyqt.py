
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

    def save_settings(self):
        '''returns the name and current settings dict to be saved
        by the application
        
        This function is to-be extended by the parent class. It returns
        a dict of settings that have been gotten and a dict of
        settings that still need to be gotten.
        
        All upper level functions should return the same thing -- the highest
        level function does error checking by ensuring that bool(need_settings)
            == False
        '''
        return_settings = {}
        need_settings = {}
        # save settings that can be proccessed.
        for key, value in self.std_settings.iteritems():
            getexec, setexec = key
            getval, setval = value
            if getval == None:
                need_settings[getexec] = getval
            else:
                return_settings[getexec] = eval(getexec.format('self'))
        return return_settings, need_settings
        
    def load_settings(self, application_settings):
        '''Load settings given the previous settings from the 
        application settings
        
        Returns the settings that still need to be loaded. All
        implementations of this function should do the same (for error
            checking at top level)
        '''
        try:
            settings = application_settings[self._NAME_]
        except KeyError:
            settings = self.std_settings
        std_settings = self.std_settings
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
                need_settings[setexec] = setval
            else:
                try:
                    exec(setexec.format(n=setval))
                except SyntaxError as E:
                    error = ("Syntax Error in loading: ", 
                        setexec.format(n=setval))
                    log(ERROR, error)
                    raise E
            
        # return settings that still need to be loaded in -- 
        #  to be used in parent
        return need_settings