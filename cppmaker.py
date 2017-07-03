import os
import subprocess
import shutil
import copy
import shlex


class  marde:
    def __init__(self,a):
        self.value = a
    def __str__(self):
        return str(self.value)


prob_type_list = ['SMOOTH','NONDIFF','WILD3','NOISY3']

with open('prob_style.txt', 'r') as f:
    # Ouvrir le parameters.txt
    iniFile = f.readlines()
    f.close()

# element = [instance, nprob, n, m, ns]
for place, element in enumerate(iniFile):
    element = [element.split()[1][:-1],element.split()[4][:-1],element.split()[7][:-1],element.split()[10][:-1],element.split()[13][:-1]]
    iniFile[place]=element
    for idx, num in enumerate(element):
        num = int(num)
        element[idx]=num

make_directories = True
generate_bbcpp = True
generate_nesgtcpp = True
generate_x0files = True
generate_paramfiles = True
compile_bbcpp = True
compile_omsgt = True
compile_nesgt = True
compile_rdsgt = False


for type in prob_type_list:
    for object in iniFile:

        #On creer la liste des probleme
        num_inst=int(object[0])
        prob_type=marde(type)
        instance = marde(iniFile[num_inst-1][0])
        nprob = marde(iniFile[num_inst-1][1])
        n = marde(iniFile[num_inst-1][2])
        m = marde(iniFile[num_inst-1][3])
        ns = marde(iniFile[num_inst-1][4])
        dir_name = str(instance.value)+ "_" + str(prob_type.value)

        if make_directories:
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)

        if generate_bbcpp:
            with open("bb.cpp", 'r') as file:
                # Ouvrir le history.txt
                bbcpp = file.readlines()
                file.close()

            instance_line = list(bbcpp[688])
            type_line= list(bbcpp[689])
            nprob_line = list(bbcpp[690])
            n_line = list(bbcpp[691])
            m_line = list(bbcpp[692])
            i=1

            ## on cree un dict pour iterer sur les variable a modifier
            line_dict={instance:instance_line,prob_type:type_line,nprob:nprob_line,n:n_line,m:m_line}

            for obj in line_dict:
                idx = 33
                for el in list(str(obj)):
                    line_dict[obj][idx]= el
                    idx = idx + 1
                line_dict[obj][:]=line_dict[obj][0:idx]
                line_dict[obj].append(' ')
                line_dict[obj].append(';')
                line_dict[obj].append('\n')

            bbcpp[688] = ''.join(instance_line)
            bbcpp[689] = ''.join(type_line)
            bbcpp[690] = ''.join(nprob_line)
            bbcpp[691] = ''.join(n_line)
            bbcpp[692] = ''.join(m_line)

            #thefile = open(dir_name+"\ bb.cpp", 'w')
            thefile = open(dir_name+"/bb.cpp", 'w')
            for item in bbcpp:
                    thefile.write('%s ' % item)
            thefile.close()

        if generate_nesgtcpp:
            with open("bb.cpp", 'r') as file:
                # Ouvrir le history.txt
                bbcpp = file.readlines()
                file.close()

            instance_line = list(bbcpp[688])
            type_line= list(bbcpp[689])
            nprob_line = list(bbcpp[690])
            n_line = list(bbcpp[691])
            m_line = list(bbcpp[692])
            f_line = list(bbcpp[734])
            f_line[12:]="-f;\n"
            i=1

            ## on cree un dict pour iterer sur les variable a modifier
            line_dict={instance:instance_line,prob_type:type_line,nprob:nprob_line,n:n_line,m:m_line}

            for obj in line_dict:
                idx = 33
                for el in list(str(obj)):
                    line_dict[obj][idx]= el
                    idx = idx + 1
                line_dict[obj][:]=line_dict[obj][0:idx]
                line_dict[obj].append(' ')
                line_dict[obj].append(';')
                line_dict[obj].append('\n')

            bbcpp[688] = ''.join(instance_line)
            bbcpp[689] = ''.join(type_line)
            bbcpp[690] = ''.join(nprob_line)
            bbcpp[691] = ''.join(n_line)
            bbcpp[692] = ''.join(m_line)
            bbcpp[734] = ''.join(f_line)

            #thefile = open(dir_name+"\ bb.cpp", 'w')
            thefile = open(dir_name+"/nesgt.cpp", 'w')
            for item in bbcpp:
                    thefile.write('%s ' % item)
            thefile.close()

        if generate_x0files:
            generation = "./generate_x0.exe " + str(instance.value)
            args = shlex.split(generation)
            result = subprocess.Popen(args,stdout=subprocess.PIPE).communicate()[0][:-2]
            #result = subprocess.run(generation,stdout=subprocess.PIPE).stdout.decode('utf-8')[:-3]
            #os.rename("path/to/current/file.foo", "path/to/new/desination/for/file.foo")

            x0file = open(dir_name+"/x0.txt", 'w')
            x0file.write('%s\n' % result)
            x0file.close()


        # for item in table:
        #     for subItem in item:
        #         thefile.write('%s ' % subItem)
        #     thefile.write('\n')
        # thefile.close()

        if generate_paramfiles:
            seeds = ['1','2','3','4','5','6','7','8','9','10']
            direction_types = {'c':'CS','g':'GPS','m' : 'ORTHO'}
            ordering_strategies = ['n','ol','os','om','or','oo','no']
            with open("param.txt", 'r') as file:
                # Ouvrir le param.txt
                param_base = file.readlines()
                file.close()

            table = []  # initialisation de la liste qui contient chaque ligne du fichier
            for x in param_base:
                # Pour chaque ligne de mon history je dois
                # creer une liste
                # appender la liste a l indice x du array
                ligne = list(map(str, (x.split())))  # creer la ligne de float
                table.append(ligne)  # ajoute a la table
            param_base = table
            ext='.txt'

            for seed in seeds:
                for direction in direction_types:
                    for strat in ordering_strategies:
                        param=copy.deepcopy(param_base)
                        for ligne in param:
                            if ligne and ligne[0] == 'DIMENSION':
                                ligne[1]=str(object[2])
                            if ligne and ligne[0] == 'SOLUTION_FILE':
                                typeOfFile = 'solution'
                                ligne[1] = str(instance.value)+ "_" + str(prob_type.value)+'_'+typeOfFile + '_'+seed+'_'+direction+strat + ext
                            if ligne and ligne[0] == 'HISTORY_FILE':
                                typeOfFile = 'history'
                                ligne[1] = str(instance.value)+ "_" + str(prob_type.value)+'_'+typeOfFile + '_'+seed+'_'+direction+strat + ext
                            if ligne and ligne[0] == 'SOLUTION_FILE':
                                typeOfFile = 'solution'
                                ligne[1] = str(instance.value)+ "_" + str(prob_type.value)+'_'+typeOfFile + '_'+seed+'_'+direction+strat + ext
                            if ligne and ligne[0] == 'STATS_FILE':
                                typeOfFile = 'stats'
                                ligne[1] = str(instance.value) + "_" + str(prob_type.value) + '_' + typeOfFile + '_' + seed + '_' + direction + strat + ext
                            if ligne and ligne[0] == 'SEED':
                                ligne[1] = seed
                            if ligne and ligne[0] == 'DIRECTION_TYPE':
                                ligne[1] = direction_types[direction]
                            if ligne and ligne[0] == 'OPPORTUNISTIC_EVAL':
                                if strat == 'n':
                                    ligne[1] = 'no'
                                else:
                                    ligne[1]='yes'
                            if ligne and ligne[0] == '#DISABLE':
                                if strat == 'ol':
                                    ligne[0]='DISABLE'
                                else:
                                    ligne[0]='#DISABLE'
                            if ligne and ligne[0] == 'MODEL_EVAL_SORT':
                                if strat == 'om':
                                    ligne[1] = 'yes'
                                else:
                                    ligne[1]='no'

                            #lors quon a fini les modif de param

                        newFileName = dir_name + "/" + direction+strat+'/'+seed+"_"+"param.txt"
                        # if os.path.exists(dir_name + "/" + direction+strat): delete dirs
                        #     shutil.rmtree(dir_name + "/" + direction+strat)

                        if not os.path.exists(dir_name + "/" + direction + strat):
                            os.mkdir(dir_name + "/" + direction + strat)

                        if os.path.exists(dir_name + "/" + direction + strat + '/'+"param.txt"):
                            os.remove(dir_name + "/" + direction + strat + '/'+"param.txt")

                        thefile = open(newFileName, 'w')
                        for item in param:
                            for subItem in item:
                                thefile.write('%s ' % subItem)
                            thefile.write('\n')
                        thefile.close()
                        print (str(num_inst) + type + direction + strat + seed)

        if compile_bbcpp == True:
            exename = str(instance.value)+'_'+type+"/bb.exe"
            cppname = str(instance.value) + '_' + type + "/bb.cpp"
            args=shlex.split("g++ -o " + exename +" "+ cppname)
            subprocess.Popen(args)

        if compile_omsgt == True:
            exename = str(instance.value)+'_'+type+"/omsgt.exe"
            cppname = str(instance.value) + '_' + type + "/bb.cpp"
            args=shlex.split("g++ -o " + exename +" "+ cppname)
            subprocess.Popen(args)

        if compile_nesgt == True:
            exename = str(instance.value)+'_'+type+"/nesgt.exe"
            cppname = str(instance.value) + '_' + type + "/nesgt.cpp"
            args=shlex.split("g++ -o " + exename +" "+ cppname)
            subprocess.Popen(args)

if compile_rdsgt == True:
    exename = "rd.exe"
    cppname = "/rd.cpp"
    args=shlex.split("g++ -o " + exename +" "+ cppname)
    subprocess.Popen(args)
    
# n_instance
# n
# m
# prob type
