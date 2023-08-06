from pyes.utils import *
# File Interface Class
class FileInterface():

    _default_value = {
            "info": {"contacts": [], "requests_arch": [], "requests_made":0, "requests_exec": 0},
            "active_req": {"road": "", "trac": "", "seed": [], "crop": ""}
    }

    @classmethod
    def _default_schema():
        #list, positive int, path
        listt = lambda c: c if (type(c) == list) else []
        pintt = lambda n: n if (type(n) == int and n>0) else 0
        pathh = lambda p: p if os.path.exists(p) else ""

        return Schema({

            "info":
            {
                "contacts": Use(listt),
                "requests_arch": Use(listt),
                "requests_made": Use(pintt),
                "requests_exec": Use(pintt)
            },
            
            "active_req":
            {
                "road": Use(pathh),
                "trac": Use(str),
                "seed": Use(listt),
                "crop": Use(lambda s:s)
            }
        }, ignore_extra_keys=True, description= "File Interface Schema")
    
    def __init__(self, intf_path = "C:/Users/{0}/AppData/Roaming/PYJSX/INTFS/".format(Utils.get_user())):

        self.value = self._default_value
        self.path = intf_path

        #if pulled is invalid: recover remains/push
        self.pull(auto_repair=True)
    
    # [VALIDATORS]
    def validate(self, oo):
        return self._default_schema().is_valid(oo)

    def recover(self, oo):
        return self._default_schema().validate(oo)

    # [GRABBERS]
    def grab_raw(self):
            with open(self.path, 'r') as f: c = f.read()
            return c

    def grab_proper(self):

        if(os.path.exists(pp)): return None
        with open(pp ,'r') as f: 
            try:    v = self.recover(json.loads(f.read() or ""))
            except: v = None

        return v

    def pull(self, auto_repair = False):
        proper_pulled = self.grab_proper(self.path) 
        if(proper_pulled is not None): 
            self.value = proper_pulled
            if(auto_repair):
                self.push(new_value= proper_pulled)
            return True
        
        return False

    def grab_signal(self):

        return '{dir_name}/executed_{intf_name}.tmp'.format(
                            dir_name  = os.path.dirname(self.path),
                            intf_name = os.path.basename(self.path)
                    )

    # [SETTERS/MODIFIERS]
    def push(self, new_value = None):
        return Utils.make_file(self.path, cc = json.dumps(
            new_value if self.validate(new_value) else self.value,
            ensure_ascii= False, indent=4  
        ))