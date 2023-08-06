# PYJSX
class PYJSX():

    @classmethod
    def jspy_args(self, ss):
        
        #boolean
        if(ss in ['true', 'false']): return ss.title()
        #string
        if(type(ss) is str):         return '"{0}"'.format(ss)
        
        #any
        return str(ss)
    
    @classmethod
    def process_intf(self, intf):

        pp = intf['active_req']['road']
        if(not os.path.exsits(pp)): raise ValueError("Python:PYJSX:process_intf: Invalid Road")

        return dotdict({

            path: pp,
            name: Utils.file_name(pp),
            func: intf['active_req']['trac'],
            args: ','.join(self.jspy_args(arg) for arg in args) 
        })
    
    @classmethod
    def execute_request(self, request):

        # append to sys path
        sys.path.append(os.path.dirname(request.path))

        n = request.name
        n_as = n.replace('.', '_')
        f = request.func
        a = request.args
        # execute and harvest
        try:
            exec('import {0} as {1}'.format(n, n_as))
            result = eval('{name_as}.{func}({args})'.format(
                        name_as = n_as,
                        func = f, args = a )
                    )

        except Exception as e:
            result = 'Python:PYJSX:execute_request:{err}'.format(err = str(e).replace('\'', '\\\''))
        
        return result