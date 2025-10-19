# AYTO Simulator

Ein leichtgewichtiges Python-Skript zur Simulation und Analyse des TV-Formats „Are You The One?“  
Der Simulator durchsucht mittels Tiefensuche (DFS) alle gültigen Paarungen unter gegebenen Randbedingungen, berechnet Wahrscheinlichkeiten und liefert kompakte Ausgaben zu bekannten, sicheren und verbleibenden Zuordnungen.

## Features
- **Flexible Datenbasis**: Beliebige Listen von `men` und `women`.
- **Matchbox-Ergebnisse**: Positive (Perfect Match) und negative (No-Match).
- **Matching Nights**: Aufstellungen pro Nacht inkl. Anzahl korrekter Lichter.
- **None-Zuordnungen**: Überzählige Personen können `None` zugeordnet werden.
- **Limit für None**: `None` ist nur so oft erlaubt, wie das eine Geschlecht überzählig ist (fest gesetzte `None`-Zuordnungen zählen in dieses Limit).
- **Statistiken**: Wahrscheinlichkeiten je Mann/Frau, sichere 100%-Matches, Ergebnis-Tabellen.

## Projektstruktur
- `ayto_simulator/` – Paket mit der Kernlogik
  - [core.py]
   – Klasse [AreYouTheOne]
- `simulations/` – Beispielskripte zur Nutzung

## Installation und Ausführung
- Python 3.9+ empfohlen.
- Projektverzeichnis in Ihre Umgebung kopieren/klonen.
- Aus der Projektwurzel ausführen (wichtig für den Modul-Import):
```bash
python -m simulations.ayto-vip-2025
```
Oder ein eigenes Skript unter `simulations/` anlegen und ebenfalls als Modul starten.

## Datenmodell und Formate
- **Men/Women**: einfache Listen von Namen, z. B. `["Adam", "Bernd", ...]`.
- **Matchbox**: [AreYouTheOne.matchbox(man, woman, is_match)]
  - `is_match=True` → Perfect Match (auch `woman=None` möglich).
  - `is_match=False` → No-Match.
- **Matching Nights**: [AreYouTheOne.add_night(number, pairs, total_matches)]
  - `pairs`: Liste von `(man, woman)` mit `woman` ggf. `None`.
  - `total_matches`: Anzahl korrekter Lichter (Integer).
- **None-Regel**: `None` darf nur so oft vorkommen, wie das eine Geschlecht überzählig ist. Bereits feste `None`-Zuordnungen reduzieren diese Kapazität. `None` trägt nicht zu Lichter-Zählungen bei.

## Schnellstart (Beispiel)
```python
from ayto_simulator import AreYouTheOne

ayto = AreYouTheOne(
    men=["Adam", "Bernd", "Calvin"],
    women=["Anna", "Berta"]
)

# Matchbox: Adam–Anna ist Perfect Match, Bernd–Berta ist No-Match
ayto.matchbox("Adam", "Anna", True)
ayto.matchbox("Bernd", "Berta", False)

# Matching Night 1 mit 2 korrekten Lichtern
ayto.add_night(1, [
    ("Adam", "Anna"), ("Bernd", "Berta"), ("Calvin", None)
], 2)

ayto.simulate()
ayto.summary()          # Übersicht: bekannte/sichere Matches + Rest mit Wahrscheinlichkeiten
ayto.showresults(10)    # Tabelle: Männer | Fix | bis zu 10 Lösungen als Spalten
print(ayto.get_probabilities())
```

## API-Referenz: Klasse [AreYouTheOne] (in [ayto_simulator/core.py]
- **Konstruktor**
  - [AreYouTheOne(men, women, time_limit=120.0, solution_cap=100000)]
  - `time_limit`: Abbruch nach Sekunden.
  - `solution_cap`: max. Anzahl der zu speichernden Lösungen.
- **matchbox(man, woman, is_match)**
  - Speichert Perfect Match (True) bzw. No-Match (False).
  - `woman` darf `None` sein (z. B. aus Matchbox oder als feste Regel).
- **add_night(number, pairs, total_matches)**
  - Fügt eine Matching Night hinzu.
  - `pairs` ist eine Liste von `(man, woman)`, `woman` kann `None` sein.
  - `total_matches` ist ein Integer (auch als dritter Positionsparameter möglich).
- **simulate()**
  - Startet die DFS-Suche. Beachtet Zeitlimit, `solution_cap`, die Night-Totals sowie die `None`-Kapazität.
- **summary()**
  - Gibt aus:
    - Bereits bekannte Perfect Matches (aus Matchbox, inkl. `None`).
    - Berechnete definitive Perfect Matches (100% über alle Lösungen).
    - Verbleibende Männer mit möglichen Frauen nach absteigender Wahrscheinlichkeit (inkl. „Niemand“ für `None`).
- **showresults(limit=10)**
  - Tabellarische Ausgabe:
    - Spalten: `Männer | Fix | 1 | 2 | ...` (bis zu `limit` Lösungen).
    - `Fix` zeigt Perfect Matches (Matchbox), berechnete 100%-Matches oder „Niemand“ bei 100% `None`; sonst `---`.
    - Für Männer mit Fix-Zuordnung bleiben die Lösungsspalten leer.
    - Für andere Männer steht je Lösung die zugeordnete Frau (oder `-` für `None`).
- **get_probabilities() -> dict[str, dict[str, float]]**
  - Liefert pro Mann eine Map Frau→Prozentsatz. `None` wird als Schlüssel „Niemand“ ausgegeben.

## Tipps und Hinweise
- **Einschränkungen nutzen**: Jede zusätzliche Information (Matchbox, Nights, No-Matches) reduziert den Suchraum und beschleunigt die Simulation.
- **Zeitlimit anpassen**: Bei großen Instanzen ggf. `time_limit` erhöhen.
- **solution_cap**: Senken, wenn nur Wahrscheinlichkeiten benötigt werden.
- **Ausführung als Modul**: Vermeidet Import-Probleme (`python -m simulations.dein_script`).
