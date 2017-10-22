from collections import namedtuple


Task = namedtuple('Task', [
    'task_id',
    'name',
    'solution'
    # ,
    # 'test'
])

tasks = (
    Task(task_id='id: 1980', name='Double', solution='def dvojnasobek(n):    print ("Dvojnasobek cisla", n, "je", 2*n)\n'),
    Task(task_id='id: 2004', name='Sudá čísla', solution='    for i in range(n+1):\\n        if i%2 == 0: print i\\n\n'),
    Task(task_id='id: 2005', name='Dělitelé', solution='    for i in range(1,n+1):\\n        if n % i == 0:\\n            print i\\n\n'),
    Task(task_id='id: 2006', name='Faktoriál', solution='    f = 1\\n    for i in range(1,n+1):\\n        f = f * i\\n    return f\\n\n'),
    Task(task_id='id: 2007', name='Ciferný součet', solution='    soucet = 0\\n    while n > 0:\\n        soucet += n % 10\\n        n = n // 10\\n    return soucet\\n\n'),
    Task(task_id='id: 2008', name='Fibonacciho posloupnost', solution='    a, b = 1, 1\\n    for i in range(n):\\n        print a,\\n        a, b = b, a+b\\n\n'),
    Task(task_id='id: 2009', name='Největší společný dělitel', solution='    # Eucliduv algoritmus\\n    while b != 0:\\n        t = b\\n        b = a % b\\n        a = t\\n    return a\\n\n'),
    Task(task_id='id: 2010', name='Binární zápis', solution='    vystup = \\"\\"\\n    while n > 0:\\n        if n % 2 == 0: vystup = \\"0\\" + vystup\\n        else: vystup = \\"1\\" + vystup\\n        n = n // 2\\n    print vystup\\n\n'),
    Task(task_id='id: 2011', name='Šachovnice', solution='    for y in range(n):\\n        for x in range(n):\\n            if (x + y) % 2 == 0: print \\"X\\",\\n            else: print \\".\\",\\n        print\\n\n'),
    Task(task_id='id: 2012', name='Výpis prvočísel', solution='    i = 1\\n    while n > 0:\\n        if pocet_delitelu(i) == 2:\\n            print i,\\n            n = n - 1\\n        i = i + 1\\n\\ndef pocet_delitelu(n):\\n    pocet = 0\\n    for i in range(1, n+1):\\n        if n % i == 0:\\n            pocet = pocet + 1\\n    return pocet    \\n\n'),
    Task(task_id='id: 2013', name='Pascalův trojúhelník', solution='    for n in range(pocet_radku):\\n        for k in range(0, n + 1):\\n            print kombinacni_cislo(n,k),\\n        print\\n  \\ndef faktorial(n):\\n    f = 1\\n    for i in range(1,n+1):\\n        f = f * i\\n    return f\\n\\ndef kombinacni_cislo(n,k):\\n    return faktorial(n)/(faktorial(n-k) * faktorial(k))\\n\n'),
    Task(task_id='id: 2014', name='Mocniny dvojky', solution='    x = 1\\n    for i in range(n):\\n        print x,\\n        x = x * 2\\n\n'),
    Task(task_id='id: 2015', name='Tajná posloupnost', solution='    aktualni = 1\\n    strop = 1\\n    for i in range(n):\\n        print aktualni,\\n        aktualni += 1\\n        if aktualni > strop:\\n            aktualni = 1\\n            strop += 1\\n\n'),
    Task(task_id='id: 2016', name='Součet', solution='    return sum(range(n+1))\\n\n'),
    Task(task_id='id: 2017', name='Čtverec', solution='    \\n    print \\"*\\"*n+\\"\\\\n\\"+(\\"*\\"+\\"+\\"*(n-2)+\\"*\\"+\\"\\\\n\\")*(n-2)+\\"*\\"*n\\n\n'),
    Task(task_id='id: 2018', name='Trojúhelník', solution='    for i in range(n):\\n        for j in range(n-i):\\n            print \\"#\\",\\n        print\\n\n'),
    Task(task_id='id: 2019', name='Počet dělitelů', solution='   \\n    return len([ x for x in range(1,n+1) if n % x == 0 ])\\n\n'),
    Task(task_id='id: 2020', name='Diamant', solution='    for x in range(-n,n+1):\\n        for y in range(-n,n+1):\\n            if abs(x)+abs(y) <= n:\\n                print \\"#\\",\\n            else:\\n                print \'.\',\\n        print\\n\n'),
    Task(task_id='id: 2021', name='Cik-cak', solution="    radek(text,0)\\n    radek(text,1)\\n    \\ndef radek(text, parita):\\n    for i in range(len(text)):\\n        if i % 2 == parita:\\n            print text[i],\\n        else:\\n            print '.',\\n    print    \\n\n"),
    Task(task_id='id: 2022', name='Palindrom', solution='    for i in range(len(text)):\\n        if text[i] != text[len(text)-i-1]:\\n            return False\\n    return True\\n'),
    Task(task_id='id: 2023', name='Přesmyčky', solution="    s1 = list(slovo1)\\n    s1.sort()\\n    s2 = list(slovo2)\\n    s2.sort()\\n    print slovo1, 'a', slovo2,\\n    if s1 == s2:\\n        print 'jsou',\\n    else:\\n        print 'nejsou',\\n    print 'vzajemne presmycky'\\n\n"),
    Task(task_id='id: 2024', name='Binární číslo', solution='    h = 0\\n    for i in range(len(retezec)):\\n        if retezec[-i-1] == \\"1\\":\\n            h += 2**i\\n    return h\\n\n'),
    Task(task_id='id: 2025', name='Podmnožiny', solution='    podmn = []\\n    for i in range(2**n):\\n        mnozina = []\\n        for j in range(n):\\n            if i & (2**j):\\n                mnozina.append(j+1)\\n        if len(mnozina) == k:        \\n            podmn.append(mnozina)\\n    podmn.sort()\\n    for mnozina in podmn:\\n        for x in mnozina: print x,\\n        print\\n\n'),
    Task(task_id='id: 2026', name='Caesarova šifra', solution='    vystup = \\"\\"\\n    for i in range(len(text)):\\n        if text[i] == \' \': vystup = vystup + \' \'\\n        else:\\n            c = ord(text[i]) + n\\n            while (c > ord(\'z\')): c = c - 26\\n            vystup = vystup + chr(c)\\n    return vystup\\n\n'),
    Task(task_id='id: 2027', name='Velké X', solution="    for x in range(n):\\n        for y in range(n):\\n            if x == y or x == n - 1 - y: print '#',\\n            else: print '.',\\n        print\\n\n"),
    Task(task_id='id: 2028', name='Transpoziční šifra', solution='    zacatek = \\"\\"\\n    konec = \\"\\"\\n    for i in range(len(text)):\\n        if i % 2 == 0:\\n            zacatek = zacatek + text[i]\\n        else:\\n            konec = text[i] + konec\\n    return zacatek + konec                            \\n\n'),
    Task(task_id='id: 2029', name='První písmena', solution='    vystup = \\"\\"\\n    for i in range(len(text)):\\n        if i == 0 or text[i-1] == \\" \\":\\n            vystup += text[i]\\n    return vystup\\n\n'),
    Task(task_id='id: 2030', name='Všechny přesmyčky', solution='    presmycky = permutace(slovo)\\n    presmycky.sort()\\n    posledni = None\\n    for presmycka in presmycky:\\n        if presmycka != posledni:\\n            print presmycka\\n        posledni = presmycka\\n\t\\ndef permutace(slovo):\\n    if len(slovo) == 1: return [ slovo ]\\n    vystup = []\\n    for i in range(len(slovo)):\\n        nove_slovo = slovo[:i] + slovo[i+1:]\\n        for per in permutace(nove_slovo):\\n            vystup.append(slovo[i] + per)\\n    return vystup\\n\n'),
    Task(task_id='id: 2031', name='Frekvenční analýza', solution="    frekvence = [ 0 for i in range(26) ]\\n    for pismeno in text:\\n        if ord(pismeno) >= ord('a') and ord(pismeno) <= ord('z'):\\n            frekvence[ord(pismeno) - ord('a')] += 1\\n    for i in range(26):\\n        if frekvence[i] != 0:\\n            print chr(ord('a')+i), frekvence[i]\\n\n"),
)
