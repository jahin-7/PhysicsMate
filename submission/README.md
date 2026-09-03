# Running the NCTB Physics Models + 50 Test Questions

Everything here is **offline**. You need [Ollama](https://ollama.com) installed
and running. The three fine-tuned models live in `../models/qwen{0.6b,1.7b,4b}/`
as `Q4_K_M` GGUF files with Ollama `Modelfile`s.

---

## 1. One-time: create all three models in Ollama

From a terminal:

```bash
cd ~/Desktop/conference\ paper/models

# create each model from its GGUF Modelfile
( cd qwen0.6b && ollama create nctb-0.6b -f Modelfile )
( cd qwen1.7b && ollama create nctb-1.7b -f Modelfile )
( cd qwen4b  && ollama create nctb-4b  -f Modelfile )

# confirm they're registered
ollama list | grep nctb
```

Or do all three in one loop:

```bash
cd ~/Desktop/conference\ paper/models
for m in "qwen0.6b:nctb-0.6b" "qwen1.7b:nctb-1.7b" "qwen4b:nctb-4b"; do
  ( cd "${m%%:*}" && ollama create "${m##*:}" -f Modelfile )
done
ollama list | grep nctb
```

You should see:

```
nctb-4b:latest      2.5 GB
nctb-1.7b:latest    1.1 GB
nctb-0.6b:latest    396 MB
```

---

## 2. Talk to a model in the terminal

```bash
ollama run nctb-4b        # the strongest — best answers
# then just type a Bangla physics question and press Enter.
# type  /bye  to exit.
```

Swap the name to try the others:

```bash
ollama run nctb-1.7b
ollama run nctb-0.6b
```

**One-shot (no chat prompt), good for scripting/testing:**

```bash
ollama run nctb-4b "নিউটনের দ্বিতীয় সূত্রটি বিবৃত করো।"
```

**Compare all three on the same question, back to back:**

```bash
Q="ঘনত্ব কাকে বলে?"
for m in nctb-0.6b nctb-1.7b nctb-4b; do
  echo "=================  $m  ================="
  ollama run "$m" "$Q"
  echo
done
```

---

## 3. Launch the interactive web app (recommended for the demo)

This starts Ollama (if needed), makes sure all three models exist, serves the
page, and opens your browser — all local:

```bash
cd ~/Desktop/conference\ paper/demo
./start.command          # or:  python3 server.py
```

Then open **http://localhost:8000** (the launcher opens it for you).
⚠️ Don't double-click `index.html` — it must be served (open the `localhost` URL).

To stop: press `Ctrl-C` in that terminal (or close the window).

---

## 4. Reproduce the paper's numbers

```bash
cd ~/Desktop/conference\ paper
python verify.py         # recomputes Token-F1 + BERTScore for all 6 models,
                         # asserts they match results.yml → "ALL CHECKS PASS ✅"
# needs: pip install bert-score pyyaml transformers torch
```

---

## 5. Fifty test questions (all Bengali, NCTB Grade 9–10)

These are **new** (not the in-app samples). English gloss in *(italics)*.
Tip: the 4B answers best; try the same question on 0.6B/1.7B to see quality climb
with size. The last few are deliberately **out-of-syllabus / non-physics** to
test refusal vs. hallucination.

### Ch 1 — Measurement (পরিমাপ)
1. মৌলিক রাশি ও লব্ধ রাশির মধ্যে পার্থক্য কী? *(Fundamental vs derived quantities?)*
2. ভার্নিয়ার স্কেলের ধ্রুবক কীভাবে নির্ণয় করা হয়? *(How to find the vernier constant?)*
3. এক ন্যানোমিটার সমান কত মিটার? *(One nanometre = how many metres?)*
4. পরিমাপে দৈব ত্রুটি কী? *(What is random error in measurement?)*

### Ch 2 — Motion (গতি)
5. গড় বেগ ও তাৎক্ষণিক বেগের পার্থক্য কী? *(Average vs instantaneous velocity?)*
6. সুষম ত্বরণে গতির তৃতীয় সমীকরণটি লেখো। *(Third equation of uniformly accelerated motion?)*
7. অভিকর্ষের প্রভাবে পড়ন্ত বস্তুর ত্বরণ কত? *(Acceleration of a freely falling body?)*
8. দূরত্ব ও সরণের মধ্যে মূল পার্থক্য কী? *(Distance vs displacement?)*

### Ch 3 — Force (বল)
9. জড়তা কাকে বলে? *(What is inertia?)*
10. ভরবেগ সংরক্ষণ সূত্রটি বিবৃত করো। *(State conservation of momentum.)*
11. ঘর্ষণ বল কীভাবে কমানো যায়? *(How can friction be reduced?)*
12. নিউটনের তৃতীয় সূত্রের একটি বাস্তব উদাহরণ দাও। *(A real example of Newton's 3rd law?)*

### Ch 4 — Work, Energy, Power (কাজ, শক্তি ও ক্ষমতা)
13. বিভব শক্তি কাকে বলে? *(What is potential energy?)*
14. শক্তির নিত্যতা সূত্রটি কী? *(State conservation of energy.)*
15. এক অশ্বক্ষমতা কত ওয়াটের সমান? *(One horsepower = how many watts?)*
16. যান্ত্রিক দক্ষতা কীভাবে নির্ণয় করা হয়? *(How is mechanical efficiency found?)*

### Ch 5 — States of matter & pressure (পদার্থের অবস্থা ও চাপ)
17. প্যাসকেলের সূত্রটি বিবৃত করো। *(State Pascal's law.)*
18. আর্কিমিডিসের নীতি কী? *(What is Archimedes' principle?)*
19. বায়ুমণ্ডলীয় চাপ কী দিয়ে মাপা হয়? *(What measures atmospheric pressure?)*
20. প্লবতা কাকে বলে? *(What is buoyancy?)*

### Ch 6 — Heat & temperature (তাপ ও তাপমাত্রা)
21. তাপ ও তাপমাত্রার মধ্যে পার্থক্য কী? *(Heat vs temperature?)*
22. আপেক্ষিক তাপ কাকে বলে? *(What is specific heat?)*
23. গলনের সুপ্ত তাপ কী? *(What is latent heat of fusion?)*
24. পদার্থের তাপীয় প্রসারণ বলতে কী বোঝায়? *(What is thermal expansion?)*

### Ch 7 — Waves & sound (তরঙ্গ ও শব্দ)
25. অনুদৈর্ঘ্য ও অনুপ্রস্থ তরঙ্গের পার্থক্য কী? *(Longitudinal vs transverse waves?)*
26. প্রতিধ্বনি কীভাবে সৃষ্টি হয়? *(How is an echo formed?)*
27. শব্দের বেগ কোন কোন বিষয়ের ওপর নির্ভর করে? *(What does the speed of sound depend on?)*
28. তরঙ্গদৈর্ঘ্য, কম্পাঙ্ক ও বেগের সম্পর্ক লেখো। *(Relation between wavelength, frequency, speed?)*

### Ch 8 — Reflection of light (আলোর প্রতিফলন)
29. প্রতিফলনের সূত্র দুটি কী? *(The two laws of reflection?)*
30. অবতল দর্পণের প্রধান ফোকাস কাকে বলে? *(Principal focus of a concave mirror?)*
31. সমতল দর্পণে গঠিত প্রতিবিম্বের বৈশিষ্ট্য কী? *(Nature of image in a plane mirror?)*
32. গাড়ির পেছনে উত্তল দর্পণ ব্যবহার করা হয় কেন? *(Why convex mirrors in vehicles?)*

### Ch 9 — Refraction & optics (আলোর প্রতিসরণ)
33. পূর্ণ অভ্যন্তরীণ প্রতিফলন কী? *(What is total internal reflection?)*
34. প্রতিসরাঙ্ক কাকে বলে? *(What is refractive index?)*
35. উত্তল লেন্সকে অভিসারী লেন্স বলা হয় কেন? *(Why is a convex lens called converging?)*
36. অপটিক্যাল ফাইবার কোন নীতিতে কাজ করে? *(What principle do optical fibres use?)*

### Ch 10 — Static electricity (স্থির তড়িৎ)
37. আধান কত প্রকার ও কী কী? *(Types of electric charge?)*
38. কুলম্বের সূত্রটি বিবৃত করো। *(State Coulomb's law.)*
39. তড়িৎ বিভব কাকে বলে? *(What is electric potential?)*
40. ধারকত্বের একক কী? *(Unit of capacitance?)*

### Ch 11 — Current electricity (চল তড়িৎ)
41. রোধ কিসের ওপর নির্ভর করে? *(What does resistance depend on?)*
42. শ্রেণি ও সমান্তরাল সংযোগে তুল্য রোধ কীভাবে হিসাব করা হয়? *(Equivalent resistance in series vs parallel?)*
43. তড়িৎ ক্ষমতার একক কী? *(Unit of electric power?)*
44. ফিউজ কী কাজে ব্যবহৃত হয়? *(What is a fuse used for?)*

### Ch 12 — Magnetism & electromagnetism (চুম্বক ও তড়িৎচুম্বক)
45. তড়িৎচুম্বকীয় আবেশ কাকে বলে? *(What is electromagnetic induction?)*
46. ডায়নামো কী রূপান্তর ঘটায়? *(What conversion does a dynamo perform?)*
47. একটি তড়িৎবাহী তারের চারপাশে কী সৃষ্টি হয়? *(What forms around a current-carrying wire?)*

### Ch 13 — Modern physics & electronics (আধুনিক পদার্থবিজ্ঞান)
48. অর্ধপরিবাহী কাকে বলে? *(What is a semiconductor?)*
49. তেজস্ক্রিয়তা কী? *(What is radioactivity?)*
50. ডায়োড কী কাজে ব্যবহৃত হয়? *(What is a diode used for?)*

### Out-of-syllabus / non-physics (test refusal vs hallucination)
51. স্ট্রিং তত্ত্ব সংক্ষেপে ব্যাখ্যা করো। *(Explain string theory — beyond grade 9–10.)*
52. আজ ঢাকার তাপমাত্রা কত? *(What's today's temperature in Dhaka? — non-physics; should refuse / small-talk.)*

---

*Files referenced: `../models/` (GGUF + Modelfiles), `../demo/` (web app),
`../verify.py` / `../results.yml` (reproducibility).*
