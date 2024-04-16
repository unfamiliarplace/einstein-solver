from thing import Thing

P_Leon = Thing('Leon')
P_Yvette = Thing('Yvette')
P_Isac = Thing('Isac')
P_Eric = Thing('Eric')
t1s = {P_Isac, P_Eric, P_Leon, P_Yvette}

R_Greg = Thing('Greg\'s')
R_Irene = Thing('Irene\'s')
R_Charlie = Thing('Charlie\'s')
R_Lyon = Thing('Lyon\'s')
t2s = {R_Greg, R_Irene, R_Charlie, R_Lyon}

F_Ham = Thing('Ham')
F_Turkey = Thing('Turkey')
F_Chicken = Thing('Chicken')
F_Pork = Thing('Pork')
t3s = {F_Chicken, F_Ham, F_Pork, F_Turkey}

C_14 = Thing('14.99')
C_15 = Thing('15.99')
C_16 = Thing('16.99')
C_17 = Thing('17.99')
t4s = {C_14, C_15, C_16, C_17}

things = t1s.union(t2s).union(t3s).union(t4s)

def clue_1() -> bool:
    return not any((
        Thing.is_pair(P_Yvette, R_Lyon),
        Thing.is_pair(P_Yvette, C_14),
    ))

def clue_2() -> bool:
    return not any((
        Thing.is_pair(C_16, R_Irene),
        Thing.is_pair(C_16, R_Lyon)
    ))

def clue_3() -> bool:
    if any((
        Thing.is_pair(R_Lyon, C_17), Thing.is_pair(P_Leon, F_Pork)
    )):
        return False
    
    a = Thing.is_pair(P_Leon, C_17) and Thing.is_pair(F_Pork, R_Lyon)
    b = Thing.is_pair(P_Leon, R_Lyon) and Thing.is_pair(F_Pork, C_17)

    return (a + b) == 1

def clue_4() -> bool:
    return (R_Charlie.t4, F_Chicken.t4) in (
        (C_14, C_15),
        (C_15, C_16),
        (C_16, C_17)
    )

def clue_5() -> bool:
    if Thing.is_pair(P_Yvette, R_Irene):
        return False
    
    return any((
        Thing.is_pair(F_Pork, P_Yvette),
        Thing.is_pair(F_Pork, R_Irene)
    ))

def clue_6() -> bool:
    return Thing.is_pair(P_Isac, F_Chicken)

clues = [
    clue_1,
    clue_2,
    clue_3,
    clue_4,
    clue_5,
    clue_6
]
