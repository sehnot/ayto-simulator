import time, sys
from collections import Counter, defaultdict


class AreYouTheOne:
    def __init__(self, men, women, time_limit=10.0, solution_cap=100000):
        self.men = men
        self.women = women
        self.time_limit = time_limit
        self.solution_cap = solution_cap

        # central data structures
        self.fixed_assign = {}          # known Perfect Matches
        self.forbidden = set()          # known No-Matches
        self.nights = {}                # Matching Night-Aufstellungen
        self.totals = {}                # Anzahl korrekter Matches pro Nacht
        self.solutions = []             # found valid solutions
        self.tested_total = 0           # Enumerationen (für Statistik)
        self.time_limit_reached = False

        # interne Hilfen
        self.shown_nights = defaultdict(set)
        self.none_left_initial = 0
        self.partial_assign = {}

    # ---------------------------------------------------
    # Public API
    # ---------------------------------------------------

    # process Matchbox result
    def matchbox(self, man, woman, is_match):
        """Process Matchbox result."""
        if is_match:
            self.fixed_assign[man] = woman
        else:
            self.forbidden.add((man, woman))

    # add a Matching Night
    def add_night(self, number, pairs, total_matches):
        """Add a Matching Night."""
        self.nights[number] = pairs
        self.totals[number] = total_matches

    # reset simulation results
    def reset(self):
        """Reset simulation results."""
        self.solutions = []
        self.tested_total = 0
        self.time_limit_reached = False
        self.partial_assign = {}

    # start DFS simulation
    def simulate(self):
        """Start DFS simulation."""
        self.reset()
        self._prepare_data()

        wc = Counter({w: 0 for w in self.women})
        nc = Counter()

        # consider known Perfect Matches
        for m, w in self.fixed_assign.items():
            if w is not None:
                wc[w] += 1
                for n in self.shown_nights.get((m, w), set()):
                    nc[n] += 1

        rem_men = [m for m in self.men if m not in self.fixed_assign]

        start = time.time()
        self._dfs(0, rem_men, wc, nc, self.none_left_initial, start)
        elapsed = time.time() - start

        print(f"\n=== Simulation beendet. Laufzeit: {elapsed:.1f}s | "
              f"Lösungen: {len(self.solutions)} | "
              f"Zeitlimit?: {self.time_limit_reached} | "
              f"Geprüfte Varianten: {self.tested_total} ===")

    # print summary of simulation results
    def summary(self, export = False):
        """Print: (1) known matchbox matches, (2) 100% certain matches, (3) remaining men with possible women sorted by probability."""
        print("\n=== Summary ===\n")
        total = len(self.solutions)
        if total == 0:
            print("Keine Lösungen gefunden — keine Statistiken möglich.")
            return

        # (1) Known Perfect Matches from matchboxes (including None if present)
        fixed_positive = {m: w for m, w in self.fixed_assign.items()}
        if fixed_positive:
            print("Bereits bekannte Perfect Matches (Matchbox):\n")
            for m in self.men:
                if m in fixed_positive:
                    print(f"- {m} -> {fixed_positive[m]}")

        # (2) 100% certain matches across all solutions (excluding already listed)
        certain = {}
        for m in self.men:
            if m in fixed_positive:
                continue
            vals = {sol.get(m) for sol in self.solutions}
            if len(vals) == 1:
                only = next(iter(vals))
                if only is not None:
                    certain[m] = only
        if certain:
            print("\nBerechnete definitive Perfect Matches (100%):\n")
            for m in self.men:
                if m in certain:
                    print(f"- {m} -> {certain[m]}")

        # (3) Remaining men: list possible women sorted by probability desc
        probs = self.get_probabilities()
        remaining_men = [m for m in self.men if m not in fixed_positive and m not in certain]
        if remaining_men:
            print("\nVerbleibende mögliche Zuordnungen (nach Wahrscheinlichkeit):\n")
            for m in remaining_men:
                mp = probs.get(m, {})
                # sort by probability desc, then name asc for stability
                sorted_items = sorted(mp.items(), key=lambda x: (-x[1], x[0]))
                if not sorted_items:
                    print(f"- {m}: (keine Daten)")
                else:
                    items_str = ", ".join(f"{w} ({p}%)" for w, p in sorted_items)
                    print(f"- {m}: {items_str}")

    def showresults(self, limit=10, export=False):
        """Print a table: Männer | Fix | solution columns (up to limit)."""
        print("\n=== Ergebnisse ===\n")
        total = len(self.solutions)
        if total == 0:
            print("Keine Lösungen gefunden — keine Statistiken möglich.")
            return

        # Determine fixed matches: from matchbox positives (including None) or 100% across solutions (including None)
        fixed_positive = {m: w for m, w in self.fixed_assign.items()}
        certain = {}
        for m in self.men:
            if m in fixed_positive:
                continue
            vals = {sol.get(m) for sol in self.solutions}
            if len(vals) == 1:
                only = next(iter(vals))
                # include None as fixed (displayed as 'Niemand')
                certain[m] = only

        # Build table headers
        max_to_show = total if limit is None else max(0, min(int(limit), total))
        sol_subset = self.solutions[:max_to_show]
        headers = ["Männer", "Fix"] + [str(i+1) for i in range(len(sol_subset))]

        name_w = max(len("Männer"), max((len(m) for m in self.men), default=0))
        fix_values = []
        for m in self.men:
            if m in fixed_positive:
                val = fixed_positive[m]
                fix_values.append("Niemand" if val is None else val)
            elif m in certain:
                val = certain[m]
                fix_values.append("Niemand" if val is None else val)
            else:
                fix_values.append("---")
        fix_w = max(len("Fix"), max((len(v) for v in fix_values), default=3))
        # solution columns width: based on woman names and '-'
        woman_max = max([len(w) for w in self.women] + [1]) if self.women else 1
        col_w = max(5, woman_max)

        # Print header
        header = headers[0].ljust(name_w) + " | " + headers[1].ljust(fix_w)
        if sol_subset:
            header += " | " + " | ".join(h.rjust(col_w) for h in headers[2:])
        print(header)
        print("-" * len(header))

        # Print rows
        for idx, m in enumerate(self.men):
            # Fix column value
            if m in fixed_positive:
                fix_raw = fixed_positive[m]
                fix_val = "Niemand" if fix_raw is None else fix_raw
            elif m in certain:
                fix_raw = certain[m]
                fix_val = "Niemand" if fix_raw is None else fix_raw
            else:
                fix_val = "---"

            row = m.ljust(name_w) + " | " + fix_val.ljust(fix_w)
            if sol_subset:
                cells = []
                for sol in sol_subset:
                    if fix_val != "---":
                        # leave empty cells for fixed men
                        cells.append("".rjust(col_w))
                    else:
                        w = sol.get(m)
                        cells.append(((w if w is not None else "-")).rjust(col_w))
                row += " | " + " | ".join(cells)
            print(row)

    # calculate the percentage probability of each pairing
    def get_probabilities(self):
        """Calculate the percentage probability of each pairing."""
        if not self.solutions:
            print("No solutions found — no statistics possible.")
            return {}

        freq = {m: Counter() for m in self.men}
        for sol in self.solutions:
            for m in self.men:
                w = sol.get(m)
                # count even when w is None (meaning unmatched)
                freq[m][w] += 1

        probabilities = {}
        for m in self.men:
            total = sum(freq[m].values())
            if total == 0:
                probabilities[m] = {}
                continue
            # map None to 'Niemand' label for user-friendly output and stable sorting
            probabilities[m] = {
                ("Niemand" if w is None else w): round(100 * c / total, 2)
                for w, c in freq[m].items()
            }

        return probabilities

    # ---------------------------------------------------
    # Internal logic
    # ---------------------------------------------------

    # prepare helper structures for DFS
    def _prepare_data(self):
        """Prepare helper structures for DFS."""
        self.shown_nights.clear()
        for n, pairs in self.nights.items():
            for man, woman in pairs:
                if woman is not None:
                    self.shown_nights[(man, woman)].add(n)

        # None capacity: how often can None occur?
        self.none_left_initial = max(0, len(self.men) - len(self.women))
        self.none_left_initial -= sum(1 for m, w in self.fixed_assign.items() if w is None)
        if self.none_left_initial < 0:
            self.none_left_initial = 0

    # recursive search algorithm
    def _dfs(self, idx, rem_men, wc_local, nc_local, none_left, start):
        """Recursive search algorithm."""
        self.tested_total += 1

        # Time limit
        if time.time() - start > self.time_limit:
            self.time_limit_reached = True
            return
        if len(self.solutions) >= self.solution_cap:
            return

        if idx >= len(rem_men):
            # check night-light totals
            for n, total in self.totals.items():
                if nc_local.get(n, 0) != total:
                    return
            sol = dict(self.fixed_assign)
            sol.update(self.partial_assign)
            self.solutions.append(sol)
            return

        m = rem_men[idx]
        candidate_women = [w for w in self.women if wc_local[w] == 0]
        if none_left > 0:
            candidate_women.append(None)

        for w in candidate_women:
            if (m, w) in self.forbidden:
                continue
            self.partial_assign[m] = w
            used_real = False
            if w is not None:
                wc_local[w] += 1
                used_real = True

            nc2 = nc_local.copy()
            if w is not None:
                for n in self.shown_nights.get((m, w), set()):
                    nc2[n] += 1
            # prune: no night-light may be exceeded
            if any(nc2[n] > self.totals[n] for n in self.totals):
                if used_real:
                    wc_local[w] -= 1
                del self.partial_assign[m]
                continue

            self._dfs(idx + 1, rem_men, wc_local, nc2, none_left - (1 if w is None else 0), start)
            if used_real:
                wc_local[w] -= 1
            del self.partial_assign[m]

            if self.time_limit_reached or len(self.solutions) >= self.solution_cap:
                return

    # print progress bar
    def _print_progress(self, current, total, start_time):
        pct = current / total
        elapsed = time.time() - start_time
        bar_len = 30
        filled = int(bar_len * pct)
        bar = "#" * filled + "-" * (bar_len - filled)
        sys.stdout.write(f"\r[{bar}] {pct*100:5.1f}% | {elapsed:6.1f}s elapsed")
        sys.stdout.flush()
