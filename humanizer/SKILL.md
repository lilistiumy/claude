---
name: humanizer
description: Rewrite or write text so it sounds like a real person wrote it, not an AI, in English or Bahasa Indonesia. Tuned for academic writing (skripsi, tesis, journal articles, abstracts, tinjauan pustaka) and proposals/reports (latar belakang, tujuan, event or grant proposals, laporan kegiatan), plus emails and posts. Strips AI tells ("delve", "plays a pivotal role", "Di era digital saat ini", "tidak hanya... tetapi juga", "Selain itu" chains, rule-of-three slogans, em dashes, stacked hedges, summary closers) and keeps every citation, number and term exactly. Use this whenever the user says humanize, de-AI, make it sound human/natural, less robotic, less ChatGPT, sounds too AI, worried Turnitin flags it, or in Indonesian (humanize, parafrase, bikin lebih natural, biar nggak kayak AI, kaku banget, rapikan bahasanya, perbaiki tulisan ini). Also use it by default when drafting any academic paragraph, proposal section or message the user will submit or send as their own work, even if they don't say "humanize".
---

# Humanizer (personal)

The target is text a careful human expert would write: specific, committed to what the evidence supports, with natural rhythm. Not text that has been "disguised". If a sharp supervisor or reviewer would read it as written by someone who knows the material, it's done.

## Defaults for this user

These are settled; don't ask about them again.

- **Languages:** English and Bahasa Indonesia. Reply in the language of the input. Never translate unless asked. Keep English terms the author put in an Indonesian text (e.g. *green finance*, *circular economy*) and keep their formatting.
- **Main use:** academic writing and proposals/reports. Casual messages happen too; use the general rules for those.
- **Output: the rewrite only.** No "Berikut versi yang lebih natural:", no list of changes, no explanation, no scanner output. Keep the original headings, numbering and paragraph order. The one exception: if something truly needs the author's check (a vague claim with no source, a placeholder like `[jumlah peserta]` you had to add), add one short line after the text. Otherwise nothing.

## Workflow

1. **Identify the register.** Academic (EN/ID), proposal/report, or casual. The fixes differ: an abstract keeps its calibrated hedges and has no contractions; a WhatsApp message drops both. Read the matching section below.
2. **Scan.** Know the catalogues:
   - `references/ai-tells.md`: English tells (structure, devices, vocabulary, punctuation).
   - `references/indonesian-tells.md`: Indonesian tells, non-baku/calque patterns, proposal clichés.
   - `references/academic-and-proposals.md`: what to keep, what to cut, and how far to go in formal registers.
   For anything longer than a paragraph or two, run the scanner to catch what the eye skips:
   ```bash
   python scripts/scan_tells.py draft.txt        # or: echo "teks" | python scripts/scan_tells.py -
   ```
   It covers both languages. It is a flashlight, not a judge: a flagged word stays if it's the right word (e.g. *berkelanjutan* in a sustainability paper, *robust* for robust standard errors).
3. **Rewrite, don't patch.** Swapping "crucial" for "important" leaves the AI skeleton. Fix the shape: start with the actual claim or finding, break the rule-of-three, cut the throat-clearing opener and the moral-of-the-story closer, vary sentence length, replace vague significance with what actually happened, according to whom.
4. **Check.** Read it as the examiner, reviewer or panel judge would. Any sentence that sounds like a brochure, a motivational speech or a chatbot? Does every paragraph end with "This highlights the importance of..." / "Hal ini menunjukkan pentingnya..."? Did any number, citation or term change? (It must not.) Re-run the scanner on long pieces.
5. **Deliver** the text only (see Defaults).

## What human writing does (all registers)

AI text is recognisable mostly by its shape, so these matter more than any word list.

- **Specific over general.** "Ekspor CPO turun [X]% pada 2023 ([sumber])" beats "menghadapi berbagai tantangan". Pull the specifics from the author's own text and sources. Never invent facts, sources or numbers to get there.
- **Uneven rhythm.** Mix short and long sentences and paragraphs of different lengths. AI writes medium sentences in medium paragraphs, all alike. (In academic text, vary within reason: no fragments.)
- **Commit to what the evidence supports.** One precise hedge where uncertainty is real ("suggests", "cenderung"), not stacked hedges ("may potentially suggest").
- **Plain words.** "use" not "utilize", "menggunakan" not "mengutilisasi", "start" not "embark", "berperan" not "memainkan peran yang sangat krusial".
- **Connectors that state the real relation, or none.** Replace "Furthermore / Moreover / Selain itu / Lebih lanjut" chains with the actual link ("This contrasts with...", "Temuan ini sejalan dengan..."), or let two sentences sit side by side.
- **Let it end.** Stop when the point is made. No "In conclusion, it is evident that...", "Secara keseluruhan...", "Semoga bermanfaat", "masa depan yang lebih cerah".
- **Fewer devices.** No "not just X, but Y" / "tidak hanya X, tetapi juga Y" by reflex, no "The result? ...", no rhetorical question answered in the next line.
- **Punctuation like a person.** Commas, periods, parentheses. Em dashes (—): none by default. Indonesian writing almost never uses them.
- **Formatting only when earned.** Prose stays prose. Keep headings and lists a template requires (proposal sections, RAB tables); don't add bold mini-headers or bullets of your own.

## Register: academic (EN and ID)

Details and examples in `references/academic-and-proposals.md`. The essentials:

- **Sacred, never touched:** citations and their order, numbers, statistics, p-values, quotes, variable names, equations, table and figure references, defined terms, and the author's field terminology. Never add a citation or source.
- **Formal stays formal:** no contractions, slang, fragments, exclamation marks or rhetorical questions. Humanising here means precise and direct, not casual.
- **Calibrate hedges, don't delete them.** Correlational result → "is associated with" / "berhubungan dengan", not "proves" / "membuktikan". Remove only the redundant layer.
- **"Significant" / "signifikan" only for statistical significance.** Otherwise say "large", "substantial", "cukup besar", or give the number.
- **Lead with the finding, not the field.** Not "In recent years, X has garnered significant attention" / "Dewasa ini, X menjadi perhatian banyak pihak", but the claim plus citation.
- **Indonesian academic:** follow KBBI/EYD V (*terdiri atas*, *berdasarkan*, no relative *di mana* / *yang mana*, no *adalah merupakan*). Keep the author's choice of *peneliti* / *penulis* / passive voice; don't switch to *kita* or *Anda*.

## Register: proposals and reports

- **Concrete beats aspirational.** Replace "diharapkan dapat meningkatkan kualitas SDM yang unggul, kreatif, dan inovatif" with what will actually happen: who, how many, when, what output. If a needed number isn't in the source, use a placeholder like `[jumlah peserta]` and mention it in the one trailing line.
- **Keep the required structure** (Latar Belakang, Tujuan, Sasaran, Waktu dan Tempat, RAB...) and every number in budgets and timelines exactly.
- **Start the background with the problem and its data**, not "Di era globalisasi yang semakin pesat".
- **Active, with a real subject:** "Panitia menyeleksi 40 tim" over "Akan dilakukan proses seleksi oleh pihak panitia".
- **Kill slogan triplets and stacked buzzwords** (*sinergi, kolaborasi, inovasi*; *wadah*; *ajang bergengsi*; *berdaya saing global*) unless the funder's call literally uses that term.

## Register: casual and messages

Use `references/ai-tells.md` and `references/examples-general.md`. Contractions, short messages, plain sign-offs. In Indonesian chats, keep the author's own informal style (*nggak*, *udah*, *aja*, mixed English) instead of turning it into baku.

## Keep the author

- Preserve meaning, facts, and any phrase they clearly chose on purpose.
- Keep their spelling and variety (British/American English, baku or informal Indonesian, code-mixing).
- Match length roughly. Humanising usually makes text shorter; in academic writing, don't cut content or arguments, cut padding.
- No fake typos, random lowercase or slang they wouldn't use. That reads as a costume.
- Files: for a .docx, extract the text, rewrite, and write it back with the docx skill if they want a file; otherwise return the text.

## About AI detectors (Turnitin, GPTZero...)

They are unreliable in both directions and flag human text too. Don't promise anything will "pass" or quote a score. Writing that is specific and grounded in the author's own data and sources is what reads as human to examiners, and it's the best bet with detectors too. If the user asks, say this in one or two sentences, then do the rewrite.

## My voice

Personal rules. These override the generic defaults above.

- Bilingual: English and Bahasa Indonesia; mostly academic papers and proposals (sustainability / green economy topics, student event and competition proposals with RAB).
- Wants only the rewritten text back, never a report of changes.
- _(Add more as you learn them. When the user corrects a rewrite, e.g. "jangan ganti istilah itu" or "I always write 'this study' not 'this paper'", offer once to save the rule here.)_
