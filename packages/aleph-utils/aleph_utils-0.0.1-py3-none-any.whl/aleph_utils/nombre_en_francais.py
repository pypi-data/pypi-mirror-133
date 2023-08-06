
unites = {'zero': 0, 'un':1, 'deux':2, 'trois': 3, 'quatre': 4, 'cinq': 5, 'six': 6, 'sept': 7, 'huit': 8, 'neuf': 9}

dizaines = {'dix':  10, 'onze': 11, 'douze':12, 'treize':13, 'quatorze':14, 'quinze':15, 'seize':16,
            'vingt':20, 'trente': 30, 'quarante': 40, 'cinquante':50, 'soixante': 60}

autres = {'cent': 100, 'mille': 1000, 'millier': 1000, 'million': 1e6, 'milliard': 1e9}

tout = unites.copy()
tout.update(dizaines)
tout.update(autres)

def lettres_en_nombre(s):
    """Transforme un nombre écrit en toutes lettres en nombre
    Ex: cinq cent milles -> 500000

    USE WITH CAUTION
    """
    split_list = s.lower().replace("-", " ").split(' ')
    current = tout[split_list[0]]
    list_to_add = []
    i = 1
    while i < len(split_list):
        elt = split_list[i]
        # On enleve les et
        if elt == 'et':
            i += 1
            continue
        # On enleve le pluriel
        if elt != "trois" and elt.endswith('s'):
            elt = elt[:-1]
        if elt in autres:
            current *= autres[elt]
            if elt != "cent":
                list_to_add.append(current)
                current = 0
            i += 1
        elif elt in dizaines:
            current += dizaines[elt]
            i += 1
        elif elt in unites:
            if elt == 'quatre' and i < len(split_list)-1 and split_list[i+1].startswith('vingt'):
                current += 80
                i += 2
            else:
                current += unites[elt]
                i += 1
        else:
            raise IndexError("{} not in known number".format(elt))
    final = current + sum(list_to_add)
    print(s, final)
    return final
