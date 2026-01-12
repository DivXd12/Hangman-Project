import argparse
import csv
import unicodedata
from collections import Counter
from pathlib import Path


def normalize_word(w):
    if not w:
        return ""
    return unicodedata.normalize("NFC", w.strip().lower())


def matches_pattern(word, pattern):
    if len(word) != len(pattern):
        return False
    for wc, pc in zip(word, pattern):
        if pc == "*":
            continue
        if wc != pc:
            return False
    return True


def best_letter_by_freq(candidates, guessed):
    cnt = Counter()
    for w in candidates:
        for ch in set(w):
            if ch not in guessed:
                cnt[ch] += 1
    return cnt.most_common(1)[0][0] if cnt else None

 
def solve_instance(pattern, target, words):
    guessed_letters = set()
    attempts = 0
    seq = []
    pattern = normalize_word(pattern)
    target = normalize_word(target)
    L = len(pattern)
    candidates = [w for w in words if len(w) == L and matches_pattern(w, pattern)]

    while len(candidates) > 1:
        letter = best_letter_by_freq(candidates, guessed_letters)
        if not letter:
            break
        seq.append(letter)
        guessed_letters.add(letter)
        attempts += 1

    
        new_pattern = "".join(
            [letter if target[i] == letter or pattern[i] != "*" else pattern[i] for i in range(L)]
        )
        pattern = new_pattern
        candidates = [w for w in candidates if matches_pattern(w, pattern)]

    if len(candidates) == 1:
        seq.append(candidates[0])
        attempts += 1
        return attempts, candidates[0], "OK", " ".join(seq)

    return attempts, "", "FAIL", " ".join(seq)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", "-i", required=True)
    ap.add_argument("--output", "-o", required=True)
    args = ap.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    with open(input_path, encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        rows = list(reader)

    results = []
    for row in rows:
        if len(row) < 3:
            continue
        game_id, pattern, target = row[0], row[1].lower(), row[2].lower()
        dict_words = [r[2].lower() for r in rows if len(r) >= 3]
        attempts, found, status, seq = solve_instance(pattern, target, dict_words)
        results.append([game_id, attempts, found, status, seq])

    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["game_id", "total_incercari", "cuvant_gasit", "status", "secventa_incercari"])
        writer.writerows(results)

    print(f"Rezultate scrise în: {output_path}")


if __name__ == "__main__":
    main()
