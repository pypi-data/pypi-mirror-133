
def run():
    
    # steps:
    #     modify the interface obj
    #     dump it into interface file
    #     create signal file to signal end of execution

    intff['info']['reqs_exec']  = intff['info']['reqs_exec'] + 1
    intff['active_req']['crop'] = result
    
    # dump new interface with crop result
    with open(intf_path, 'w', encoding='utf8') as f:
        f.write(json.dumps(intff, indent =4))

    # write signal file
    with open(exec_signal, 'w') as ef: ef.write('')

if __name__ == "__main__": run()