from ayto_simulator import AreYouTheOne

ayto = AreYouTheOne(
    men=[
        "Calvin O.", "Calvin S.", "Jimi Blue", "Jonny", "Kevin", "Leandro",
        "Lennert", "Nico", "Olli", "Rob", "Sidar", "Xander"
    ],
    women=[
        "Hati", "Beverly", "Joana", "Henna", "Antonia", "Viki",
        "Sandra", "Ariel", "Nelly", "Elli"
    ]
)

# fixed_assign
ayto.matchbox("Xander", "Elli", True)
ayto.matchbox("Lennert", "Sandra", True)
ayto.matchbox("Jimi Blue", None, True)
ayto.matchbox("Calvin O.", "Nelly", True)

# forbidden (No-Matches)
ayto.matchbox("Calvin S.", "Nelly", False)
ayto.matchbox("Jonny", "Beverly", False)
ayto.matchbox("Jimi Blue", "Nelly", False)
ayto.matchbox("Jimi Blue", "Hati", False)
ayto.matchbox("Sidar", "Henna", False)

# Matching Nights
ayto.add_night(1, [
    ("Calvin O.", "Hati"), ("Calvin S.", "Beverly"), ("Jimi Blue", None), ("Jonny", "Henna"),
    ("Kevin", "Sandra"), ("Leandro", "Viki"), ("Lennert", "Antonia"), ("Nico", "Ariel"),
    ("Olli", None), ("Rob", "Joana"), ("Sidar", "Nelly"), ("Xander", "Elli")
], 2)

ayto.add_night(2, [
    ("Calvin O.", "Hati"), ("Calvin S.", "Joana"), ("Jimi Blue", None), ("Jonny", "Antonia"),
    ("Kevin", "Sandra"), ("Leandro", "Viki"), ("Lennert", None), ("Nico", "Ariel"),
    ("Olli", "Henna"), ("Rob", "Nelly"), ("Sidar", "Beverly"), ("Xander", "Elli")
], 2)

ayto.add_night(3, [
    ("Calvin O.", "Ariel"), ("Calvin S.", "Joana"), ("Jimi Blue", None), ("Jonny", "Viki"),
    ("Kevin", "Sandra"), ("Leandro", "Henna"), ("Lennert", "Nelly"), ("Nico", "Beverly"),
    ("Olli", "Antonia"), ("Rob", "Nelly"), ("Sidar", None), ("Xander", "Elli")
], 2)

ayto.add_night(4, [
    ("Calvin O.", "Nelly"), ("Calvin S.", "Joana"), ("Jimi Blue", None), ("Jonny", None),
    ("Kevin", "Viki"), ("Leandro", "Sandra"), ("Lennert", "Henna"), ("Nico", "Ariel"),
    ("Olli", "Antonia"), ("Rob", "Hati"), ("Sidar", "Beverly"), ("Xander", "Elli")
], 3)

ayto.add_night(5, [
    ("Calvin O.", "Nelly"), ("Calvin S.", "Joana"), ("Jimi Blue", "Henna"), ("Jonny", None),
    ("Kevin", "Viki"), ("Leandro", None), ("Lennert", "Sandra"), ("Nico", "Ariel"),
    ("Olli", "Antonia"), ("Rob", "Hati"), ("Sidar", "Beverly"), ("Xander", "Elli")
], 4)

ayto.add_night(6, [
    ("Calvin O.", "Nelly"), ("Calvin S.", "Antonia"), ("Jimi Blue", "Hati"), ("Jonny", "Viki"),
    ("Kevin", "Ariel"), ("Leandro", "Beverly"), ("Lennert", "Sandra"), ("Nico", None),
    ("Olli", "Henna"), ("Rob", None), ("Sidar", "Joana"), ("Xander", "Elli")
], 4)

ayto.add_night(7, [
    ("Calvin O.", None), ("Calvin S.", "Antonia"), ("Jimi Blue", None), ("Jonny", "Hati"),
    ("Kevin", "Viki"), ("Leandro", "Ariel"), ("Lennert", "Sandra"), ("Nico", "Beverly"),
    ("Olli", "Henna"), ("Rob", "Nelly"), ("Sidar", "Joana"), ("Xander", "Elli")
], 5)

ayto.add_night(8, [
    ("Calvin O.", "Joana"), ("Calvin S.", "Antonia"), ("Jimi Blue", None), ("Jonny", "Hati"),
    ("Kevin", "Ariel"), ("Leandro", "Viki"), ("Lennert", "Sandra"), ("Nico", "Beverly"),
    ("Olli", "Henna"), ("Rob", "Nelly"), ("Sidar", None), ("Xander", "Elli")
], 4)

ayto.add_night(9, [
    ("Calvin O.", "Nelly"), ("Calvin S.", "Joana"), ("Jimi Blue", None), ("Jonny", "Antonia"),
    ("Kevin", "Hati"), ("Leandro", "Ariel"), ("Lennert", "Sandra"), ("Nico", None),
    ("Olli", "Henna"), ("Rob", "Viki"), ("Sidar", "Beverly"), ("Xander", "Elli")
], 4)

ayto.simulate()
ayto.summary()
ayto.showresults(10)