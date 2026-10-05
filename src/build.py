#!/usr/bin/env python3
"""Render the amethis.io landing page in English (/) and Polish (/pl/) from one template.

Usage: python3 src/build.py   (writes dist/index.html and dist/pl/index.html)
Every claim on the page is taken from the partner briefing deck and the customer brief;
change wording here, never in dist/.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = (ROOT / "src" / "template.html").read_text(encoding="utf-8")

EN = {
    "lang": "en", "og_locale": "en_GB", "base": "", "home": "/", "canonical": "https://amethis.io/",
    "href_en": "/", "href_pl": "/pl/", "cur_en": "true", "cur_pl": "false",
    "meta_title": "Amethis — people and AI agents running your organisation, under your control",
    "meta_desc": "Describe how your organisation works and Amethis turns it into applications, data, processes and integrations — up to 30× faster — with AI agents doing the work and people approving what matters. Compliant by design, on your own infrastructure.",
    "skip": "Skip to content", "lang_label": "Language",
    "nav_how": "How it works", "nav_control": "People & agents", "nav_path": "Getting started",
    "nav_trust": "Trust", "nav_partners": "Partners", "nav_cta": "Contact",
    "mail_subject": "Amethis%20%E2%80%94%20introduction", "mail_subject_partner": "Amethis%20%E2%80%94%20partnership",

    "hero_eyebrow": "For regulated organisations",
    "hero_h1": "Your organisation, run by people and AI agents —", "hero_h1_grad": "under your control.",
    "hero_lede": "Describe how your organisation works. Amethis turns it into applications, data, processes and integrations <b>up to 30× faster</b> than building and integrating systems today — and lets AI agents take on the work while your people approve what matters.",
    "hero_cta1": "Talk to us", "hero_cta2": "See how it works",
    "ben1": "Change in weeks, not years", "ben2": "Compliant by design", "ben3": "On your servers or your own cloud",
    "scene_alt": "You describe how you work; Amethis builds applications, data, integrations and rules and runs the process: a request arrives, an AI agent checks it, a manager approves, the agent completes it — all within permissions, audit trail and compliance, connected to existing systems and testable on a digital twin.",
    "g_req_cap": "1 · YOU DESCRIBE HOW YOU WORK",
    "g_req1": "“When a request arrives, check it against our rules.",
    "g_req2": "Above €10,000 a manager approves. Then notify the client.”",
    "g_build_cap": "2 · AMETHIS BUILDS IT AND RUNS IT",
    "g_t1": "Applications", "g_t2": "Data", "g_t3": "Integrations", "g_t4": "Rules",
    "g_live": "LIVE PROCESS",
    "g_s1": "Request", "g_s1s": "arrives", "g_s2": "AI agent", "g_s2s": "checks & prepares",
    "g_s3": "Manager", "g_s3s": "approves", "g_s4": "AI agent", "g_s4s": "completes",
    "g_wait": "awaiting approval",
    "g_p1": "Permissions", "g_p2": "Audit trail", "g_p3": "Compliance",
    "g_legacy_h": "Your existing systems", "g_legacy_p1": "connected and still running —", "g_legacy_p2": "moved over piece by piece",
    "g_twin_h": "Digital twin", "g_twin_p1": "compare variants of a change", "g_twin_p2": "before it takes effect",

    "how_label": "How it works",
    "how_h2": "You describe how you work. Amethis builds it — and runs it.",
    "how_sub": "Amethis is a framework in which your applications and AI agents live and work together. You don't commission a software project: you state your requirements, and from them come the applications, data, processing rules and integrations your organisation needs.",
    "st1_h": "Describe", "st1_p": "State your requirements in business language: what happens, who decides, which rules apply and what information you need.",
    "st2_h": "Amethis builds", "st2_p": "Applications, data, processing rules and integrations are created from those requirements — up to 30× faster than programming and integrating them today.",
    "st3_h": "People and agents work together", "st3_p": "Everyone works in one shared environment: agents prepare and carry out the work, people decide where it matters, and everything stays in sync in real time.",
    "twin_h": "Digital twin: test before you change",
    "twin_p": "Try every change — a new rule, a new step, an optimisation — on a digital twin of your organisation first. Compare variants, see which one works best, approve it, and roll back at any time.",
    "how_note": "The result is not only speed: <b>one consistent environment</b> for your people, agents and applications — and confidence that everything works exactly as you defined it.",

    "one_label": "One system instead of six",
    "one_h2": "Six kinds of systems you would otherwise buy and connect — in one.",
    "one_sub": "Today a change in how you work touches several separate tools, each with its own supplier, data and project. In Amethis they are one environment, so a change is made once and is consistent everywhere.",
    "instead": "instead of",
    "o1_h": "Applications", "o1_p": "Screens, forms, dashboards and workspaces for every role.", "o1_s": "a separate app-building tool",
    "o2_h": "Processes and approvals", "o2_p": "Workflows, task queues, approvals and deputies — the work that today lives in e-mail and spreadsheets.", "o2_s": "a separate workflow system",
    "o3_h": "Integrations", "o3_p": "Connections with the systems you already have, in real time — even those that only have a screen.", "o3_s": "a separate integration platform",
    "o4_h": "Data and analytics", "o4_p": "One version of the truth, with reports and analytics on live data.", "o4_s": "a separate data platform",
    "o5_h": "Compliance", "o5_p": "The registers and processes GDPR, NIS2 and the AI Act require, built in.", "o5_s": "separate compliance tools",
    "o6_h": "AI agents", "o6_p": "Agents working on the same data, under the same rules as your people.", "o6_s": "a separate AI platform",

    "ct_label": "People decide · agents do the work",
    "ct_h2": "AI agents take on the work. Your people keep the decisions.",
    "ct_sub": "Agents prepare, check and carry out tasks around the clock. Wherever a decision matters, a person approves it — and every step is recorded.",
    "ap_alt": "Example: an AI agent asks a person to approve a payment",
    "ap_from": "AI agent · proposal", "ap_title": "Pay invoice FV/2026/0412", "ap_amount": "€12,400",
    "ap_c1": "Matches the purchase order and the delivery", "ap_c2": "Supplier verified",
    "ap_c3": "Above €10,000 — your approval is required",
    "ap_ok": "Approve", "ap_no": "Reject",
    "ap_foot": "Every decision is recorded: who, when and on what basis.",
    "pt1_h": "A human in the loop", "pt1_p": "You decide which steps need a person's approval — and change it as trust grows.",
    "pt2_h": "Advanced user and permission management", "pt2_p": "An agent gets exactly the rights a person in that role would — never more. The same rules apply to everyone.",
    "pt3_h": "A complete audit trail", "pt3_p": "Who did what, when and why — for people and agents alike.",
    "pt4_h": "Stop at any moment", "pt4_p": "Any agent can be paused instantly, without stopping the rest of the organisation.",

    "pa_label": "Getting started",
    "pa_h2": "Become a frontier firm — step by step, without a big bang.",
    "pa_sub": "You don't replace everything at once. Amethis grows alongside the systems you already have, and every step delivers value on its own.",
    "ph1_h": "Start with one process", "ph1_p": "Pick one process — or place Amethis underneath your existing systems as one version of the truth. Nothing else has to change.",
    "ph2_h": "Connect what you have", "ph2_p": "Existing systems keep running. Amethis exchanges data with them in real time — and where a system offers no way in, it works with its screens the way a person does, reading and filling them in.",
    "ph3_h": "Move over piece by piece", "ph3_p": "Applications move module by module, and old screens can be shown inside the new ones in the meantime. There is no switch-over day.",
    "ph4_h": "Let agents take on more", "ph4_p": "As trust grows, agents take on more of the work — while people keep the decisions that matter.",

    "tr_label": "Trust by design",
    "tr_h2": "Built for organisations that cannot afford to lose control.",
    "tr_sub": "Public administration, finance, defence, healthcare — wherever data is sensitive and the rules are strict.",
    "t1_h": "Your infrastructure", "t1_p": "Runs on your servers, in your own cloud account, or in networks cut off from the internet — the AI model included. Your data stays with you.",
    "t2_h": "Regulation built in", "t2_p": "GDPR, NIS2, the AI Act — the registers, processes and records they require are part of the system, not an extra project.",
    "t3_h": "Security for sensitive data", "t3_p": "Advanced user and permission management and data classification, designed for environments up to EU SECRET.",
    "t4_h": "No lock-in", "t4_p": "Your data stays in open, standard formats — you can take it with you at any time, including away from us.",

    "pr_label": "Proof",
    "pr_h2": "A mission-critical public-sector system — three modules in two weeks.",
    "pr_h3": "A real-time situational-awareness application for a public institution, rebuilt from scratch as a working system.",
    "pr_p": "No custom programming for the project — the same platform that runs every other deployment, set up from requirements.",
    "pr_c1": "A live map of the current situation", "pr_c2": "Event reporting with an approval workflow", "pr_c3": "User and access management with an approval queue",
    "pr_n1": "weeks from start to demo", "pr_n2": "modules delivered", "pr_n3": "dashboards and views", "pr_n4": "data sets", "pr_n5": "lines of custom code",
    "f1_h": "Up to 30× faster", "f1_p": "Applications, processes and integrations delivered up to 30× faster than programming them — and changed just as fast.",
    "f2_h": "Extreme efficiency on modest hardware", "f2_p": "Over a million records processed in minutes on a single server, every one of them traceable. To start, the whole platform fits on one machine.",
    "f3_h": "Scales with you", "f3_p": "Built to scale out across servers as data and users grow — from one department to the whole organisation.",

    "pn_label": "For partners",
    "pn_h2": "For delivery partners: a different business with the same clients.",
    "pn_sub": "Your consultants describe, Amethis builds. The work moves from developers to analysts and architects — and a fixed price stops being a gamble.",
    "pn_c1": "Deployment and support stay with you.", "pn_c2": "Source-code escrow protects both you and your client.", "pn_c3": "Start safely: one process, a pilot, or running alongside an existing system.",
    "pn_cta": "Become a partner",

    "cl_label": "European digital sovereignty",
    "cl_h2": "Ready to take the first step?",
    "cl_sub": "Tell us about one process you would like to change. We will show you how it looks in Amethis — with your people in control.",
    "cl_cta": "Start a conversation",
    "ft_eu": "Made in the European Union",
    "ft_privacy": "This site sets no cookies and loads nothing from third parties.",
}

PL = dict(EN)
PL.update({
    "lang": "pl", "og_locale": "pl_PL", "base": "../", "home": "/pl/", "canonical": "https://amethis.io/pl/",
    "cur_en": "false", "cur_pl": "true",
    "meta_title": "Amethis — ludzie i agenci AI prowadzą Twoją organizację, pod Twoją kontrolą",
    "meta_desc": "Opisz, jak działa Twoja organizacja, a Amethis zamieni to w aplikacje, dane, procesy i integracje — nawet 30× szybciej — z agentami AI wykonującymi pracę i ludźmi zatwierdzającymi to, co ważne. Zgodnie z regulacjami, na Twojej infrastrukturze.",
    "skip": "Przejdź do treści", "lang_label": "Język",
    "nav_how": "Jak to działa", "nav_control": "Ludzie i agenci", "nav_path": "Jak zacząć",
    "nav_trust": "Zaufanie", "nav_partners": "Partnerzy", "nav_cta": "Kontakt",
    "mail_subject": "Amethis%20%E2%80%94%20rozmowa", "mail_subject_partner": "Amethis%20%E2%80%94%20partnerstwo",

    "hero_eyebrow": "Dla organizacji regulowanych",
    "hero_h1": "Twoja organizacja, w której ludzie i agenci AI pracują razem —", "hero_h1_grad": "pod Twoją kontrolą.",
    "hero_lede": "Opisz, jak działa Twoja organizacja. Amethis zamieni to w aplikacje, dane, procesy i integracje <b>nawet 30× szybciej</b>, niż dziś trwa budowa i łączenie systemów — a agenci AI przejmą pracę, podczas gdy Twoi ludzie zatwierdzają to, co ważne.",
    "hero_cta1": "Porozmawiajmy", "hero_cta2": "Zobacz, jak to działa",
    "ben1": "Zmiany w tygodnie, nie w lata", "ben2": "Zgodność z regulacjami od początku", "ben3": "Na Twoich serwerach lub w Twojej chmurze",
    "scene_alt": "Opisujesz, jak pracujecie; Amethis buduje aplikacje, dane, integracje i reguły i prowadzi proces: wpływa wniosek, agent AI go sprawdza, kierownik zatwierdza, agent kończy sprawę — w ramach uprawnień, śladu audytu i zgodności, połączony z obecnymi systemami i testowany na cyfrowym bliźniaku.",
    "g_req_cap": "1 · OPISUJESZ, JAK PRACUJECIE",
    "g_req1": "„Gdy wpłynie wniosek, sprawdź go według naszych reguł.",
    "g_req2": "Powyżej 40 000 zł zatwierdza kierownik. Potem powiadom klienta.”",
    "g_build_cap": "2 · AMETHIS TO BUDUJE I URUCHAMIA",
    "g_t1": "Aplikacje", "g_t2": "Dane", "g_t3": "Integracje", "g_t4": "Reguły",
    "g_live": "PROCES NA ŻYWO",
    "g_s1": "Wniosek", "g_s1s": "wpływa", "g_s2": "Agent AI", "g_s2s": "sprawdza, przygotowuje",
    "g_s3": "Kierownik", "g_s3s": "zatwierdza", "g_s4": "Agent AI", "g_s4s": "kończy sprawę",
    "g_wait": "czeka na decyzję",
    "g_p1": "Uprawnienia", "g_p2": "Ślad audytu", "g_p3": "Zgodność",
    "g_legacy_h": "Twoje obecne systemy", "g_legacy_p1": "podłączone i działają dalej —", "g_legacy_p2": "przenoszone kawałek po kawałku",
    "g_twin_h": "Cyfrowy bliźniak", "g_twin_p1": "porównaj warianty zmiany,", "g_twin_p2": "zanim wejdzie w życie",

    "how_label": "Jak to działa",
    "how_h2": "Opisujesz, jak pracujecie. Amethis to buduje — i uruchamia.",
    "how_sub": "Amethis to środowisko, w którym Twoje aplikacje i agenci AI żyją i pracują razem. Nie zamawiasz projektu programistycznego: podajesz wymagania, a z nich powstają aplikacje, dane, reguły przetwarzania i integracje, których potrzebuje Twoja organizacja.",
    "st1_h": "Opisujesz", "st1_p": "Podajesz wymagania językiem biznesu: co się dzieje, kto decyduje, jakie obowiązują reguły i jakich informacji potrzebujesz.",
    "st2_h": "Amethis buduje", "st2_p": "Z tych wymagań powstają aplikacje, dane, reguły przetwarzania i integracje — nawet 30× szybciej niż przy programowaniu i łączeniu ich dzisiaj.",
    "st3_h": "Ludzie i agenci pracują razem", "st3_p": "Wszyscy pracują w jednym wspólnym środowisku: agenci przygotowują i wykonują pracę, ludzie decydują tam, gdzie to ważne, a całość jest zsynchronizowana na bieżąco.",
    "twin_h": "Cyfrowy bliźniak: sprawdź, zanim zmienisz",
    "twin_p": "Każdą zmianę — nową regułę, nowy krok, optymalizację — najpierw wypróbujesz na cyfrowym bliźniaku organizacji. Porównasz warianty, zobaczysz, który działa najlepiej, zatwierdzisz go i w każdej chwili cofniesz.",
    "how_note": "Efektem jest nie tylko szybkość: <b>jedno spójne środowisko</b> dla ludzi, agentów i aplikacji — i pewność, że wszystko działa dokładnie tak, jak to określiliście.",

    "one_label": "Jeden system zamiast sześciu",
    "one_h2": "Sześć rodzajów systemów, które inaczej trzeba kupić i połączyć — w jednym.",
    "one_sub": "Dziś zmiana sposobu pracy dotyka kilku osobnych narzędzi, każde z własnym dostawcą, danymi i projektem. W Amethis to jedno środowisko, więc zmianę robi się raz i jest spójna wszędzie.",
    "instead": "zamiast",
    "o1_h": "Aplikacje", "o1_p": "Ekrany, formularze, pulpity i przestrzenie pracy dla każdej roli.", "o1_s": "osobnego narzędzia do budowy aplikacji",
    "o2_h": "Procesy i akceptacje", "o2_p": "Obieg spraw, kolejki zadań, akceptacje i zastępstwa — praca, która dziś żyje w mailach i arkuszach.", "o2_s": "osobnego systemu obiegu spraw",
    "o3_h": "Integracje", "o3_p": "Połączenia z systemami, które już macie, na bieżąco — nawet z takimi, które mają tylko ekran.", "o3_s": "osobnej platformy integracyjnej",
    "o4_h": "Dane i analityka", "o4_p": "Jedna wersja prawdy, raporty i analizy na aktualnych danych.", "o4_s": "osobnej platformy danych",
    "o5_h": "Zgodność", "o5_p": "Rejestry i procesy wymagane przez RODO, NIS2 i AI Act — wbudowane.", "o5_s": "osobnych narzędzi compliance",
    "o6_h": "Agenci AI", "o6_p": "Agenci pracujący na tych samych danych i według tych samych reguł co Twoi ludzie.", "o6_s": "osobnej platformy AI",

    "ct_label": "Ludzie decydują · agenci wykonują",
    "ct_h2": "Agenci AI przejmują pracę. Decyzje zostają przy Twoich ludziach.",
    "ct_sub": "Agenci przygotowują, sprawdzają i wykonują zadania przez całą dobę. Tam, gdzie decyzja ma znaczenie, zatwierdza ją człowiek — a każdy krok jest zapisany.",
    "ap_alt": "Przykład: agent AI prosi człowieka o zatwierdzenie płatności",
    "ap_from": "Agent AI · propozycja", "ap_title": "Zapłać fakturę FV/2026/0412", "ap_amount": "52 300 zł",
    "ap_c1": "Zgodna z zamówieniem i dostawą", "ap_c2": "Dostawca zweryfikowany",
    "ap_c3": "Powyżej 40 000 zł — wymagana Twoja decyzja",
    "ap_ok": "Zatwierdź", "ap_no": "Odrzuć",
    "ap_foot": "Każda decyzja jest zapisana: kto, kiedy i na jakiej podstawie.",
    "pt1_h": "Człowiek w pętli decyzyjnej", "pt1_p": "Ty decydujesz, które kroki wymagają akceptacji człowieka — i zmieniasz to, gdy rośnie zaufanie.",
    "pt2_h": "Zaawansowane zarządzanie użytkownikami i uprawnieniami", "pt2_p": "Agent dostaje dokładnie te uprawnienia, które miałby człowiek w tej roli — nigdy więcej. Te same reguły obowiązują wszystkich.",
    "pt3_h": "Pełny ślad audytowy", "pt3_p": "Kto, co, kiedy i dlaczego zrobił — tak samo dla ludzi, jak i dla agentów.",
    "pt4_h": "Zatrzymanie w każdej chwili", "pt4_p": "Każdego agenta można natychmiast wstrzymać, nie zatrzymując reszty organizacji.",

    "pa_label": "Jak zacząć",
    "pa_h2": "Stań się „frontier firm” — krok po kroku, bez rewolucji.",
    "pa_sub": "Nie wymieniasz wszystkiego naraz. Amethis rośnie obok systemów, które już macie, a każdy krok daje wartość sam w sobie.",
    "ph1_h": "Zacznij od jednego procesu", "ph1_p": "Wybierz jeden proces — albo umieść Amethis pod obecnymi systemami jako jedną wersję prawdy. Nic więcej nie musi się zmieniać.",
    "ph2_h": "Podłącz to, co masz", "ph2_p": "Obecne systemy działają dalej. Amethis wymienia z nimi dane na bieżąco — a tam, gdzie system nie daje innego dostępu, obsługuje jego ekrany tak jak człowiek: odczytuje je i wypełnia.",
    "ph3_h": "Przenoś kawałek po kawałku", "ph3_p": "Aplikacje przechodzą moduł po module, a stare ekrany mogą w międzyczasie działać wewnątrz nowych. Nie ma dnia przełączenia.",
    "ph4_h": "Daj agentom więcej", "ph4_p": "W miarę wzrostu zaufania agenci przejmują coraz więcej pracy — a ludzie zachowują decyzje, które mają znaczenie.",

    "tr_label": "Zaufanie u podstaw",
    "tr_h2": "Zbudowany dla organizacji, które nie mogą stracić kontroli.",
    "tr_sub": "Administracja publiczna, finanse, obronność, ochrona zdrowia — wszędzie tam, gdzie dane są wrażliwe, a reguły surowe.",
    "t1_h": "Twoja infrastruktura", "t1_p": "Działa na Twoich serwerach, na Twoim koncie w chmurze albo w sieciach odciętych od internetu — razem z modelem AI. Dane zostają u Ciebie.",
    "t2_h": "Regulacje wbudowane", "t2_p": "RODO, NIS2, AI Act — wymagane rejestry, procesy i zapisy są częścią systemu, a nie dodatkowym projektem.",
    "t3_h": "Bezpieczeństwo danych wrażliwych", "t3_p": "Zaawansowane zarządzanie użytkownikami i uprawnieniami oraz klasyfikacja danych, projektowane dla środowisk do EU SECRET włącznie.",
    "t4_h": "Bez uzależnienia od dostawcy", "t4_p": "Dane zostają w otwartych, standardowych formatach — możesz je zabrać w każdej chwili, także od nas.",

    "pr_label": "Dowód",
    "pr_h2": "Krytyczny system sektora publicznego — trzy moduły w dwa tygodnie.",
    "pr_h3": "Aplikacja bieżącej świadomości sytuacyjnej dla instytucji publicznej, odtworzona od zera jako działający system.",
    "pr_p": "Zero programowania pod ten projekt — ta sama platforma, która działa w każdym innym wdrożeniu, ustawiona na podstawie wymagań.",
    "pr_c1": "Mapa bieżącej sytuacji na żywo", "pr_c2": "Zgłaszanie zdarzeń z obiegiem akceptacji", "pr_c3": "Zarządzanie użytkownikami i dostępami z kolejką akceptacji",
    "pr_n1": "tygodnie od startu do dema", "pr_n2": "dostarczone moduły", "pr_n3": "pulpitów i widoków", "pr_n4": "zbiorów danych", "pr_n5": "linii kodu na zamówienie",
    "f1_h": "Nawet 30× szybciej", "f1_p": "Aplikacje, procesy i integracje dostarczane nawet 30× szybciej niż przy programowaniu — i zmieniane równie szybko.",
    "f2_h": "Skrajna wydajność na skromnym sprzęcie", "f2_p": "Ponad milion rekordów przetworzonych w kilka minut na jednym serwerze, każdy z pełnym śladem pochodzenia. Na start cała platforma mieści się na jednej maszynie.",
    "f3_h": "Rośnie razem z Tobą", "f3_p": "Zbudowany tak, by skalować się na kolejne serwery wraz ze wzrostem danych i użytkowników — od jednego działu do całej organizacji.",

    "pn_label": "Dla partnerów",
    "pn_h2": "Dla firm wdrożeniowych: inny biznes z tymi samymi klientami.",
    "pn_sub": "Wasi konsultanci opisują, Amethis buduje. Praca przechodzi od programistów do analityków i architektów — a stała cena przestaje być hazardem.",
    "pn_c1": "Wdrożenie i utrzymanie zostają po waszej stronie.", "pn_c2": "Depozyt kodu źródłowego chroni was i waszego klienta.", "pn_c3": "Bezpieczny start: jeden proces, pilotaż albo praca obok istniejącego systemu.",
    "pn_cta": "Zostań partnerem",

    "cl_label": "Europejska suwerenność cyfrowa",
    "cl_h2": "Gotowi na pierwszy krok?",
    "cl_sub": "Opowiedz nam o jednym procesie, który chcesz zmienić. Pokażemy, jak wygląda w Amethis — z Twoimi ludźmi przy sterach.",
    "cl_cta": "Zacznijmy rozmowę",
    "ft_eu": "Wyprodukowano w Unii Europejskiej",
    "ft_privacy": "Ta strona nie ustawia ciasteczek i niczego nie pobiera od stron trzecich.",
})


# Business identification shown in the footer. Amethis is currently a brand of a sole proprietorship;
# values below come from the Ministry of Finance VAT register (wl-api.mf.gov.pl, NIP 5212106852).
# "address" is optional by design: the register lists only a residence address, published only on request.
COMPANY = {
    "owner": "Piotr Mikołajczak",
    "nip": "5212106852",
    "vat_eu": "PL5212106852",
    "regon": "012640530",
    "address": "",
}

IMPRINT = {
    "en": "Amethis is operated by {owner} · NIP {nip} (EU VAT {vat_eu}) · REGON {regon}",
    "pl": "Markę Amethis prowadzi {owner} · NIP {nip} (VAT UE {vat_eu}) · REGON {regon}",
}


def imprint(lang: str) -> str:
    text = IMPRINT[lang].format(**COMPANY)
    return f"{text} · {COMPANY['address']}" if COMPANY["address"] else text


def render(content: dict) -> str:
    missing = sorted(set(re.findall(r"\{\{(\w+)\}\}", TEMPLATE)) - content.keys())
    if missing:
        sys.exit(f"template keys without content: {missing}")
    return re.sub(r"\{\{(\w+)\}\}", lambda m: content[m.group(1)], TEMPLATE)


def main() -> None:
    dist = ROOT / "dist"
    (dist / "pl").mkdir(parents=True, exist_ok=True)
    EN["imprint"], PL["imprint"] = imprint("en"), imprint("pl")
    (dist / "index.html").write_text(render(EN), encoding="utf-8")
    (dist / "pl" / "index.html").write_text(render(PL), encoding="utf-8")
    print("built dist/index.html and dist/pl/index.html")


if __name__ == "__main__":
    main()
