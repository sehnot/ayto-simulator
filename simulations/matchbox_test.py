from ayto_simulator import AreYouTheOne

ayto = AreYouTheOne(
    men=["M1", "M2", "M3"],
    women=["W1", "W2"]
)

ayto.matchbox("M1", "W1", True)
ayto.matchbox("M2", "W2", False)

ayto.simulate()
print(ayto.get_probabilities())