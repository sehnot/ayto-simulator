from ayto_simulator import AreYouTheOne

ayto = AreYouTheOne(
    men=["Adam", "Bernd", "Calvin", "Dennis", "Erik"],
    women=["Anna", "Berta", "Calma", "Diana"]
)

ayto.matchbox("Adam", "Anna", True)
ayto.matchbox("Bernd", "Berta", False)

ayto.add_night(1, [
    ("Adam", "Anna"),
    ("Bernd", "Berta"),
    ("Calvin", "Calma"),
    ("Dennis", "Diana"),
    ("Erik", None)
], total_matches=3)

ayto.simulate()
ayto.summary()

print("\nWahrscheinlichkeiten:")
for man, probs in ayto.get_probabilities().items():
    print(f"{man:10s}: {probs}")