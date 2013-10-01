import shelve
import cProfile, profile, pstats

def import_path(fullpath, do_reload = False):
    """ 
    Import a file with full path specification. Allows one to
    import from anywhere, something __import__ does not do. 
    """
    path, filename = os.path.split(fullpath)
    filename, ext = os.path.splitext(filename)
    sys.path.insert(0, path)
    module = __import__(filename)
    if do_reload:
        reload(module)
    del sys.path[0]
    return module

def set_priority(pid=None,priority=1):
    """ Set The Priority of a Windows Process.  Priority is a value between 0-5 where
        2 is normal priority.  Default sets the priority of the current
        python process to "below normal" but can take any valid process ID and priority. 
        http://code.activestate.com/recipes/496767-set-process-priority-in-windows/
        """
        
    import win32api,win32process,win32con
    
    priorityclasses = [win32process.IDLE_PRIORITY_CLASS,
                       win32process.BELOW_NORMAL_PRIORITY_CLASS,
                       win32process.NORMAL_PRIORITY_CLASS,
                       win32process.ABOVE_NORMAL_PRIORITY_CLASS,
                       win32process.HIGH_PRIORITY_CLASS,
                       win32process.REALTIME_PRIORITY_CLASS]
    if pid == None:
        pid = win32api.GetCurrentProcessId()
    handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
    win32process.SetPriorityClass(handle, priorityclasses[priority])

class print_twice(object):
    '''replaces std_out to print to both a file object and the standard
    print location'''
    def __init__(self, fname):
        self.stdout = sys.stdout
        sys.stdout = self
        self.file = open(fname, 'w')
    
    def write(self, text):
        self.stdout.write(text)
        self.file.write(text)
        
if os.name in ("nt", "dos"):
     exefile = ".exe"
else:
     exefile = ""

def win_run(program, *args, **kw):
    '''For running stuff on Windows. Used in spawn'''
     mode = kw.get("mode", os.P_WAIT)
     for path in os.environ["PATH"].split(os.pathsep):
          file = os.path.join(path, program) + ".exe"
          try:
                return os.spawnv(mode, file, (file,) + args)
          except os.error:
                pass
     raise os.error, "cannot find executable"
 
def spawn(program, *args):
    '''Forgot for sure what this does but I think it spawns a new process
    that is not dependent on the python one'''
     try:
          # check if the os module provides a shortcut
          return os.spawnvp(program, (program,) + args)
     except AttributeError:
          pass
     try:
          spawnv = os.spawnv
     except AttributeError:
          # assume it's unix
          pid = os.fork()
          if not pid:
                os.execvp(program, (program,) + args)
          return os.wait()[0]
     else:
          # got spawnv but no spawnp: go look for an executable
          for path in os.environ["PATH"].split(os.pathsep):
                file = os.path.join(path, program) + exefile
                try:
                     return spawnv(os.P_WAIT, file, (file,) + args)
                except os.error:
                     pass
          raise IOError, "cannot find executable"

def module_path(local_function):
    ''' returns the module path without the use of __file__.  Requires a function defined 
    locally in the module.  This is necessary for some applications like IDLE.
    from http://stackoverflow.com/questions/729583/getting-file-path-of-imported-module'''
    return os.path.abspath(inspect.getsourcefile(local_function))