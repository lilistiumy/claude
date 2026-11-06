#!/usr/bin/env python3
"""Scan English or Indonesian text for common AI-writing tells.

Usage:
    python scan_tells.py draft.txt
    echo "some text" | python scan_tells.py -
    python scan_tells.py draft.txt --lang id     # en | id | both (default: auto)

Prints each hit with its line number, then a summary: counts by category,
connector density and sentence-length spread. It's a flashlight for the
reviewer, not a verdict: a flagged word stays if it's the right word
(field terms, statistical "significant", required proposal headings).
"""
import argparse
import re
import statistics
import sys

EN = {
    "vocabulary": [
        "delve", "delves", "delving", "embark", "embarking", "leverage", "leveraging",
        "harness", "foster", "fostering", "bolster", "underscore", "underscores",
        "showcase", "showcases", "unlock", "unleash", "elevate", "empower", "empowering",
        "streamline", "spearhead", "illuminate", "resonate", "resonates", "transcend",
        "revolutionize", "utilize", "utilizing", "facilitate", "endeavor", "encompass",
        "encompasses", "cultivate", "amplify", "tapestry", "landscape", "realm", "testament",
        "beacon", "symphony", "synergy", "paradigm", "intricacies", "interplay", "cornerstone",
        "linchpin", "treasure trove", "game-changer", "game changer", "pivotal", "crucial",
        "seamless", "seamlessly", "holistic", "vibrant", "bustling", "intricate",
        "meticulous", "meticulously", "profound", "transformative", "cutting-edge",
        "groundbreaking", "ever-evolving", "fast-paced", "unparalleled", "invaluable",
        "noteworthy", "captivating", "furthermore", "moreover", "notably",
        "undeniably", "effortlessly", "in essence", "that being said", "with that in mind",
    ],
    "academic": [
        "shed light", "sheds light", "shedding light", "garnered", "garner", "burgeoning",
        "a growing body", "pave the way", "paving the way", "paves the way",
        "underscores the importance", "highlights the importance", "highlights the need",
        "valuable insights", "nuanced understanding", "intricate interplay", "it is imperative",
        "bridge the gap", "bridging the gap", "comprehensive overview", "multifaceted",
        "thereby", "holistic approach", "future research should", "in recent years",
        "this study aims to", "this paper aims to", "this paper seeks to", "interestingly,",
    ],
    "hedging": [
        "it's important to note", "it is important to note", "it's worth noting",
        "it is worth noting", "it's important to remember", "may potentially",
        "could potentially", "might potentially", "it could be argued", "generally speaking",
        "arguably",
    ],
    "opener/closer": [
        "in today's", "in the realm of", "when it comes to", "in an era", "let's dive",
        "let's explore", "let's break", "hope this email finds you", "i wanted to reach out",
        "i'm reaching out", "in conclusion", "in summary", "to sum up", "ultimately,",
        "at the end of the day", "i hope this helps", "feel free to reach out",
        "don't hesitate to", "the future of", "is bright",
    ],
    "rhetorical": [
        "here's the thing", "here's why", "here's what", "here's the kicker",
        "but there's a catch", "that's where things get", "whether you're a",
        "not only", "take it to the next level", "next level",
    ],
    "sycophancy/residue": [
        "great question", "absolutely!", "certainly!", "you're absolutely right",
        "as an ai", "as of my last", "[your name]", "let me know if you'd like",
        "here is a revised", "here's a revised", "here is the rewritten",
    ],
    "promo/significance": [
        "plays a crucial role", "plays a pivotal role", "plays a vital role",
        "plays a significant role", "plays a key role", "is a testament to", "stands as",
        "profound impact", "drive meaningful", "unlock your", "full potential",
        "experts say", "studies show", "studies have shown",
    ],
}

ID = {
    "kosakata (id)": [
        "krusial", "esensial", "fundamental", "holistik", "komprehensif", "secara komprehensif",
        "sinergi", "bersinergi", "optimal", "mengoptimalkan", "memaksimalkan", "menavigasi",
        "lanskap", "ekosistem", "menyelami", "mengupas tuntas", "eksplorasi lebih dalam",
        "wawasan berharga", "transformatif", "revolusioner", "paradigma", "multifaset",
        "tonggak", "pilar", "katalisator", "garda terdepan", "membuka peluang",
        "membuka jalan", "memfasilitasi", "mengakselerasi", "mengimplementasikan",
    ],
    "signifikansi kosong (id)": [
        "peran penting", "peran krusial", "peran vital", "peranan penting",
        "peranan yang sangat penting", "memegang peranan", "memainkan peran",
        "dampak yang signifikan", "pengaruh yang signifikan", "memberikan dampak",
        "menjadi kunci", "kunci keberhasilan", "menjadi pilar", "para ahli",
        "berbagai penelitian", "banyak penelitian", "berbagai pihak",
    ],
    "pembuka/penutup (id)": [
        "di era digital", "di era globalisasi", "di era modern", "di era revolusi",
        "dewasa ini", "seiring dengan perkembangan", "seiring perkembangan",
        "perkembangan zaman", "tidak dapat dipungkiri", "tak dapat dipungkiri",
        "tidak bisa dipungkiri", "pada hakikatnya", "dalam dunia yang", "sudah menjadi rahasia umum",
        "mari kita", "kesimpulannya", "secara keseluruhan", "pada akhirnya",
        "dapat disimpulkan bahwa", "semoga bermanfaat", "masa depan yang lebih",
        "demi terwujudnya", "bagi semua pihak", "menambah wawasan",
    ],
    "hedging (id)": [
        "perlu dicatat bahwa", "penting untuk dicatat", "patut dicatat", "perlu diingat bahwa",
        "penting untuk diingat", "dapat dikatakan bahwa", "mungkin dapat", "berpotensi untuk dapat",
        "bisa jadi mungkin",
    ],
    "konektor (id)": [
        "selain itu", "lebih lanjut", "lebih jauh lagi", "tak hanya itu", "tidak hanya itu",
        "di sisi lain", "namun demikian", "oleh karena itu", "dengan demikian",
        "dalam konteks ini", "di samping itu",
    ],
    "tidak baku/kalke (id)": [
        "dimana", "yang mana", "adalah merupakan", "terdiri dari", "berdasarkan pada",
        "dalam rangka untuk", "agar supaya", "demi untuk", "mengambil tempat",
        "dan lain sebagainya", "melakukan analisis", "melakukan pengujian",
        "melakukan peningkatan", "melakukan penelitian terhadap",
    ],
    "klise proposal (id)": [
        "sebagai wadah", "ajang bergengsi", "berdaya saing global", "generasi muda yang",
        "kualitas sumber daya manusia", "kegiatan ini diharapkan", "diharapkan dapat memberikan",
        "kolaborasi lintas sektor", "sinergi dan kolaborasi", "revolusi industri 4.0",
        "society 5.0", "manfaat yang sebesar-besarnya",
    ],
}

PATTERNS_EN = {
    "not-X-but-Y": re.compile(r"\b(?:it'?s|this|that|it is) (?:is )?(?:not|isn'?t) (?:just |only |merely |about )?[^.?!]{1,60}?[,;—–-]+ ?(?:it'?s|but)\b", re.I),
    "question reveal": re.compile(r"(?:^|[.!?]\s+)(?:The|And the) \w+(?: \w+)?\?\s+\w", re.M),
    "-ing tail": re.compile(r",\s(?:thereby\s)?(?:highlighting|underscoring|ensuring|reflecting|showcasing|emphasizing|demonstrating|signaling|marking|paving)\b", re.I),
    "rule of three": re.compile(r"\b\w+(?:\s\w+)?,\s\w+(?:\s\w+)?,?\sand\s\w+", re.I),
    "'significant' (statistical only?)": re.compile(r"(?<!statistically )\bsignificant(?:ly)?\b", re.I),
}

PATTERNS_ID = {
    "tidak hanya X tetapi Y (id)": re.compile(r"\b(?:tidak|tak|bukan)\s(?:hanya|sekadar|cuma|semata(?:-mata)?)\b[^.?!]{1,90}?\b(?:tetapi|tapi|melainkan|namun)\b", re.I),
    "'hal ini' di awal kalimat (id)": re.compile(r"(?:^|[.!?]\s+)Hal (?:ini|tersebut)\b", re.M),
    "', di mana' relatif (id)": re.compile(r",\s+di mana\b", re.I),
    "sangat ... sekali (id)": re.compile(r"\bsangat\s+\w+\s+sekali\b", re.I),
    "rule of three (id)": re.compile(r"\b\w+(?:\s\w+)?,\s\w+(?:\s\w+)?,?\sdan\s\w+", re.I),
    "'signifikan' (statistik?) (id)": re.compile(r"\bsignifikan\b", re.I),
}

PATTERNS_ALL = {
    "em dash": re.compile(r"—|\s–\s|\s--\s"),
    "emoji": re.compile("[\U0001F300-\U0001FAFF✅✨❤]"),
}

ID_MARKERS = {"yang", "dan", "di", "ini", "dengan", "untuk", "dari", "dalam", "tidak",
              "adalah", "pada", "akan", "juga", "atau", "itu", "karena", "oleh", "sebagai"}
EN_MARKERS = {"the", "and", "of", "to", "is", "in", "that", "for", "with", "this",
              "are", "on", "as", "be", "by", "it", "was", "which"}


def detect_lang(text):
    toks = re.findall(r"[a-zA-Z]+", text.lower())
    i = sum(t in ID_MARKERS for t in toks)
    e = sum(t in EN_MARKERS for t in toks)
    if i == e == 0:
        return "both"
    if i > 2 * e:
        return "id"
    if e > 2 * i:
        return "en"
    return "both"


def term_regex(t):
    return re.compile(r"(?<![\w-])" + re.escape(t) + (r"(?![\w-])" if t[-1].isalnum() else ""))


def scan(text, lang):
    words, patterns = {}, dict(PATTERNS_ALL)
    if lang in ("en", "both"):
        words.update(EN)
        patterns.update(PATTERNS_EN)
    if lang in ("id", "both"):
        words.update(ID)
        patterns.update(PATTERNS_ID)
    compiled = [(cat, t, term_regex(t)) for cat, terms in words.items() for t in terms]
    hits = []
    for n, line in enumerate(text.splitlines() or [text], 1):
        low = line.lower()
        found = [(m.start(), m.end(), cat, t) for cat, t, rx in compiled for m in rx.finditer(low)]
        for s, e, cat, t in found:
            # skip a term that sits inside a longer flagged phrase ("komprehensif" in "secara komprehensif")
            if not any(s2 <= s and e <= e2 and (e2 - s2) > (e - s) for s2, e2, _, _ in found):
                hits.append((n, cat, t))
        for name, rx in patterns.items():
            for m in rx.finditer(line):
                hits.append((n, name, m.group(0).strip()[:60]))
    return hits


def sentence_lengths(text):
    sents = [s for s in re.split(r"(?<=[.!?])\s+", text.strip()) if len(s.split()) > 1]
    return [len(s.split()) for s in sents]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src", help="file path, or - for stdin")
    ap.add_argument("--lang", choices=["auto", "en", "id", "both"], default="auto")
    a = ap.parse_args()
    text = sys.stdin.read() if a.src == "-" else open(a.src, encoding="utf-8").read()
    lang = detect_lang(text) if a.lang == "auto" else a.lang

    hits = scan(text, lang)
    for n, cat, t in hits:
        print(f"line {n:>3}  [{cat}]  {t}")

    words = max(len(text.split()), 1)
    print("\n--- summary ---")
    print(f"language checked: {lang}")
    print(f"{len(hits)} flags in {words} words ({len(hits) / words * 100:.1f} per 100 words)")
    counts = {}
    for _, cat, _ in hits:
        counts[cat] = counts.get(cat, 0) + 1
    for cat, c in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {c}")
    lens = sentence_lengths(text)
    if len(lens) >= 3:
        mean, sd = statistics.mean(lens), statistics.pstdev(lens)
        note = "  <- very even rhythm, vary sentence length" if len(lens) >= 6 and sd < 0.35 * mean else ""
        print(f"sentences: {len(lens)}, avg {mean:.1f} words, spread {sd:.1f}{note}")
        conn = counts.get("konektor (id)", 0) + sum(
            1 for _, cat, t in hits if cat == "vocabulary" and t in ("furthermore", "moreover", "notably"))
        if conn / len(lens) > 0.3:
            print(f"connectors: {conn} in {len(lens)} sentences  <- connector chain, cut most of them")
    if not hits:
        print("No common tells found. Still read it out loud.")


if __name__ == "__main__":
    main()
