from subprocess import call

seeds = [str(x+1) for x in xrange(10)]
instances = [str(x+1) for x in xrange(53)]
types = ['SMOOTH','NONDIFF','WILD3','NOISY3']
algos = {'g':'GPS','m':'MADS'}
strategies = ['n','ol','os','om']
i=0
total=strategies.__len__()*algos.__len__()*seeds.__len__()*instances.__len__()*types.__len__()

for instance in instances:
    for type in types:
        # exename = instance+'_'+type+"/bb.exe"
        # cppname = instance + '_' + type + "/bb.cpp"
        # call(["g++", "-o", exename, cppname])
        for algo in algos:
            for strategy in strategies:
                foldername = instance+'_'+type+'/'+algo+strategy
                for seed in seeds:
                    param_file=foldername+'/'+seed+'_param.txt'
                    call(['$NOMAD_HOME/bin/nomad ' + param_file],shell=True)
                    i=i+1
                    print (str(i)+'/'+str(total)+' run de NOMAD de fait')