# File Interface Class
class FileInterface():

    def __init__(self, intf_path = "C:/Users/{0}/AppData/Roaming/PYJSX/INTFS/".format(Utils.get_user())):

        self.value = {
            "info": {"contacts": [], "requests_arch": [], "requests_made":0, "requests_exec": 0},
            "active_req": {"road": "", "trac": "", "seed": [], "crop": ""}
        }
        self.path = intf_path
        self.update_from_source()

    def update_from_source(self):
        self.value = self.grab_interface(self.path) or self.value
    
    def update_source(self, new_value = self.value):
        pp = self.path
        with open(pp, 'w') as f:
            json.dump(new_value, f, ensure_ascii= False, indent=4)

    # static props:
    #   structure (FileInterface basic structure)
    intf_struct = {

        "MAJ": ('info', 'active_req'), # major
        "INF": ('contacts', 'requests_arch', 'requests_exec', 'requests_made'), # info
        "ACR": ('road', 'trac', 'seed', 'crop') # active request
    }

    @classmethod
    def validate_structure(self, oo):

        S = self.intf_struct
        if(
                all(k in oo               for k in S['MAJ'])
            and all(k in oo['info']       for k in S['INF'])
            and all(k in oo['active_req'] for k in S['ACR'])
        ): return True

        return False

    @classmethod
    def grab_interface(self, pp):
        
        if(not os.path.exists(pp)): return None
        
        with open(pp ,'r') as f:
            c = f.read()
        
        c = json.loads(c)
        if(not self.validate_structure(c)): return None

        return c
    
    @classmethod
    def grab_signal(self, pp):

        return '{dir_name}/executed_{intf_name}.tmp'.format(
                            dir_name  = os.path.dirname(pp),
                            intf_name = os.path.basename(pp)
                    )

    @classmethod
    def load_interfaces(self, user_name = "bouda"):

        loaded = []

        path = "C:/Users/{0}/AppData/Roaming/PYJSX/interfaces.json".format(user_name)
        with open(path, 'r') as f: 
            interfaces = json.loads(f.read())
        
        for i in interfaces:
            i = self.grab_interface(i)
            if(not i): continue
            loaded.append(i)

        return loaded