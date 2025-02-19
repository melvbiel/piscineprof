import os
 
commande = ''

#default values
param = {'bdd': [(1,3,10, "2024-06-08"),(2,1,13, "2024-06-09"),(3,2,6, "2024-06-10"), (3,1,8, "2024-06-11") ],
         'nages': [(1, "Brasse"), (2, "Dos"), (3, "Crawl")],
         'nageurs': [(1, "Pierre"), (2, "Paul"), (3, "Léa")]
        }


def reset(param):
    '''réinitialise la bdd'''
    param.clear()
    param['bdd'] = []
    param['nages'] = []
    param['nageurs'] = []


def get_str_from_num_in_list(num, liste):
    """Return str from num into liste"""
    for elt in liste:
        if elt[0]==num:
            return elt[1]
    #la ligne suivante ne devrait jamais être exécutée
    return "unknown"


def cmd_individu(param):
    """Ajoute un nouveau najeur"""
    prénom = input("Prénom du nouveau nageur ? ")
    id = len(param['nageurs'])+1
    param['nageurs'].append( (id,prénom ))
    print(param['nageurs'])


def cmd_nouvelle_nage(param):
    """Ajoute une nouvelle nage au logiciel"""
    nage = input("Quelle nage enregistrer ? ")
    id = len(param['nages'])+1
    param['nages'].append( (id,nage ))
    print(param['nages'])


def cmd_ajout(param):
    """Ajoute un évènement à la liste"""
    for elt in param['nageurs']:
        print(f"{elt[0]:5} : {elt[1]}")
    a = int(input("Nageur n° ? "))
    for elt in param['nages']:
        print(f"{elt[0]:5} : {elt[1]}")
    b = int(input("Nage n° ? "))
    c = int(input("combien de longueur ? "))
    d = input("Date de la performance (yyyy-mm-dd) ? ")
    param['bdd'].append((a, b, c, d))


def cmd_liste(param):
    """Affiche toutes les performances des nageurs"""
    print("Prénom       |   Nage    |   Longueur   |   Date")
    print("-----------------------------------------------")
    for elt in param['bdd']:
        nageur = get_str_from_num_in_list(elt[0], param['nageurs'])
        nage = get_str_from_num_in_list(elt[1], param['nages'])
        print(f" {nageur:12}| {nage:10}| {elt[2]:10} | {elt[3]}")

def cmd_nageur(param):
    """Affiche toutes les performances d'un nageur"""
    while True:
        try:
            for elt in param['nageurs']:
                print(f"{elt[0]:5} : {elt[1]}")

            tmp = int(input("Quel numéro de nageur ? "))

            if tmp not in [elt[0] for elt in param['nageurs']]:
                print("Erreur : Ce numéro de nageur n'existe pas. Veuillez réessayer.")
                continue  

            print(f"Performances de {get_str_from_num_in_list(tmp, param['nageurs'])}")
            print("  nage   |  longueur   |  date")
            print("-------------------------------")
            for elt in param['bdd']:
                if elt[0] == tmp:
                    nage = get_str_from_num_in_list(elt[1], param['nages'])
                    print(f" {nage:8}|  {elt[2]}|  {elt[3]}") 
                    somme=0
                    indice=0
                    moyenne=0
                    max_longueur=0
                    min_longueur=100
                    for elt in param['bdd']:
                        if max_longueur<elt[2]:
                            max_longueur=elt[2]
                        
                    for elt in param['bdd']:
                        if min_longueur>elt[2]:
                            min_longueur=elt[2]
                        
                    for elt in param['bdd']:
                        somme += elt[2]
                        indice += 1
                        moyenne = somme/indice
                
                    print(f'maximum:', max_longueur)
                    print(f'minimum:', min_longueur)
                    print('la moyenne est:', moyenne)
        
            break

        except ValueError:
            print("Erreur : Veuillez entrer un nombre valide.")


def cmd_nage(param):
    """Affiche toutes les performances suivant une nage donnée"""
    for elt in param['nages']:
        print(f"{elt[0]:5} : {elt[1]}")
    tmp = int(input("Quel numéro de nage ? "))
    print("Nage ", tmp)
    print(" Nageur     |  longueur")
    print("------------------------")
    for elt in param['bdd']:
        if elt[1]== tmp:
            nageur = get_str_from_num_in_list(elt[0], param['nageurs'])
            print(f" {nageur:11}|  {elt[2]}")


def cmd_exit(param):
    tmp = input("En êtes-vous sûr ? (o)ui/(n)on ")
    if tmp == 'o':
        cmd_save(param, 'save.backup')
        return False
    else:
        return True


def cmd_save(param, filename = 'save.csv'):
    '''sauvegarde complète de la BDD'''
    fichier = open(filename, 'w')
    # sauvegarde des nageurs
    fichier.write('@ nageurs\n')
    for elt in param['nageurs']:
        fichier.write(str(elt[0])+','+str(elt[1])+"\n")
    # sauvegarde des nages
    fichier.write('@ nages\n')
    for elt in param['nages']:
        fichier.write(str(elt[0])+','+str(elt[1])+"\n")
    # sauvegarde des données
    fichier.write('@ bdd\n')
    for elt in param['bdd']:
        fichier.write(str(elt[0])+','+str(elt[1])+','+str(elt[2])+"\n")
    fichier.close()


def cmd_load(param, filename = 'save.csv'):
    '''chargement complet la BDD avec réinitialisation'''
    reset(param)
    key = ''
    fichier = open(filename, 'r')
    for line in fichier:
        line.strip()
        if line[-1] == '\n':
            line = line[:-1]
        if line[0]=='#':
            continue
        if line[0]=='@':
            key = line[2:]
            continue
        if key =='':
            continue
        tmp = line.split(',')
        # convertion en int de ce qui doit l'être
        if key == 'bdd':
            for i in range(len(tmp)):
                tmp[i] = int(tmp[i])
        if key == 'nages' or key == 'nageurs':
            tmp[0] = int(tmp[0])
        param[key].append(tuple(tmp))
    fichier.close()

    '''Traitement de la commande d'entrée'''

def get_cmd():
    while True:
        try:
            msg = int(input("Que faut-il faire ? (Ajout: 1, Individu: 2, Nouvelle nage: 3, Liste: 4, Nageur: 5, Nage: 6, Save: 7, Load: 8, Exit: 0)"))
            return msg
        except:
            print("Indiquez bien une valeur numérique")

#
#   Programme principal
#
isAlive = True

if os.path.exists('save.backup'):
    cmd_load(param, 'save.backup')

while isAlive:
    
    commande = get_cmd()
    
    if commande == 1:
        cmd_ajout(param)

    elif commande == 2:
        cmd_individu(param)

    elif commande == 3:
        cmd_nouvelle_nage(param)

    elif commande == 4:
        cmd_liste(param)

    elif commande == 5:
        cmd_nageur(param)

    elif commande == 6:
        cmd_nage(param)

    elif commande == 7:
        cmd_save(param)

    elif commande == 8:
        cmd_load(param)

    elif commande == 0:
        isAlive = cmd_exit(param)

    else:
        print(f"Commande {commande} inconnue")
