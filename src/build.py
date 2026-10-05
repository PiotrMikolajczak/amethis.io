#!/usr/bin/env python3
"""Render the amethis.io landing page in English (/) and Polish (/pl/) from one template.

Usage: python3 src/build.py   (writes dist/index.html and dist/pl/index.html)
Every claim on the page is taken from the partner briefing deck and the customer brief;
change wording here, never in dist/.
"""
import hashlib
import json
import re
from datetime import date
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = (ROOT / "src" / "template.html").read_text(encoding="utf-8")

EN = {
    "lang": "en", "og_locale": "en_GB", "base": "", "home": "/", "canonical": "https://amethis.io/",
    "href_en": "/", "href_pl": "/pl/", "cur_en": "true", "cur_pl": "false",
    "meta_title": "Amethis – governed AI agents for regulated organisations",
    "meta_desc": "Amethis turns how your organisation works into apps, data and processes up to 30× faster – AI agents do the work, people stay in control. On-prem or your cloud.",
    "skip": "Skip to content", "lang_label": "Language",
    "nav_how": "How it works", "nav_control": "People & agents", "nav_path": "Getting started",
    "nav_trust": "Trust", "nav_partners": "Partners", "nav_cta": "Contact",
    "mail_subject": "Amethis%20%E2%80%93%20introduction", "mail_subject_partner": "Amethis%20%E2%80%93%20partnership",

    "hero_eyebrow": "For regulated organisations",
    "hero_h1": "Your organisation, run by people and AI agents –", "hero_h1_grad": "under your control.",
    "hero_lede": "Describe how your organisation works. Amethis turns it into applications, data, processes and integrations <b>up to 30× faster</b> than building and integrating systems today – and lets AI agents take on the work while your people approve what matters.",
    "hero_cta1": "Talk to us", "hero_cta2": "See how it works",
    "ben1": "Change in weeks, not years", "ben2": "Compliant by design", "ben3": "On-premises or your own Azure, Google Cloud or AWS",
    "scene_alt": "You describe how you work; Amethis builds applications, data, integrations and rules and runs the process: a request arrives, an AI agent checks it, a manager approves, the agent completes it – within permissions, audit trail and compliance, on one golden source with a semantic layer, testable on a digital twin.",
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
    "g_legacy_h": "Your data sources", "g_legacy_p1": "many databases → one golden source,", "g_legacy_p2": "with a semantic layer",
    "g_twin_h": "Digital twin", "g_twin_p1": "compare variants of a change", "g_twin_p2": "before it takes effect",

    "how_label": "How it works",
    "how_h2": "You describe how you work. Amethis builds it – and runs it.",
    "how_sub": "Amethis is a framework in which your applications and AI agents live and work together. You don't commission a software project: you state your requirements, and from them come the applications, data, processing rules and integrations your organisation needs.",
    "st1_h": "Describe", "st1_p": "State your requirements in business language – or simply talk them through with our AI analyst.",
    "st2_h": "Amethis builds", "st2_p": "Applications, data, processing rules and integrations are created from those requirements – up to 30× faster than programming and integrating them today.",
    "st3_h": "People and agents work together", "st3_p": "Everyone works in one shared environment: agents prepare and carry out the work, people decide where it matters, and everything stays in sync in real time.",
    "twin_h": "Digital twin: test before you change",
    "twin_p": "Try every change – a new rule, a new step, an optimisation – on a digital twin of your organisation first. Compare variants, see which one works best, approve it, and roll back at any time.",
    "how_note": "The result is not only speed: <b>one consistent environment</b> for your people, agents and applications – and confidence that everything works exactly as you defined it.",

    "one_label": "One system instead of six",
    "one_h2": "Six kinds of systems you would otherwise buy and connect – in one.",
    "one_sub": "Today a change in how you work touches several separate tools, each with its own supplier, data and project. In Amethis they are one environment, so a change is made once and is consistent everywhere. And in each of the six, the functional depth is comparable to the market leaders of that category.",
    "instead": "instead of",
    "o1_h": "User interfaces", "o1_p": "An integrated, modern UI environment: applications are built from screens (dashboards) made of tiles (widgets), which are assembled from elements – tables, forms, controls, charts, maps – by configuration alone, without programming.", "o1_s": "a separate app-building tool",
    "o2_h": "Processes and approvals", "o2_p": "Workflows, task queues, approvals and deputies – the work that today lives in e-mail and spreadsheets.", "o2_s": "a separate workflow system",
    "o3_h": "Integrations", "o3_p": "Connections with the systems you already have, in real time – even those that only have a screen.", "o3_s": "a separate integration platform",
    "o4_h": "Data and golden source", "o4_p": "One golden source across all your databases, with a semantic layer that describes your organisation – plus reports and analytics on live data.", "o4_s": "a separate data platform",
    "o5_h": "Compliance", "o5_p": "The registers and processes GDPR, NIS2 and the AI Act require, built in.", "o5_s": "separate compliance tools",
    "o6_h": "AI agents", "o6_p": "Agents working on the same data, under the same rules as your people.", "o6_s": "a separate AI platform",

    "ct_label": "People decide · agents do the work",
    "ct_h2": "AI agents take on the work. Your people keep the decisions.",
    "ct_sub": "Agents prepare, check and carry out tasks around the clock. Wherever a decision matters, a person approves it – and every step is recorded.",
    "ap_alt": "Example: an AI agent asks a manager to approve a production re-plan",
    "ap_from": "AI agent · operations planning", "ap_title": "Re-plan 38 orders after a supplier delay", "ap_amount": "saves €214,000",
    "ap_c1": "Data from ERP, the warehouse and 2 supplier portals – one golden source", "ap_c2": "Tested on the digital twin: on-time delivery 91% → 98%",
    "ap_c3": "Notifications for 12 affected customers drafted",
    "ap_ok": "Approve", "ap_no": "Reject", "ap_var": "Compare variants", "ap_c4": "Changes 3 production plans – a manager's approval is required",
    "ap_foot": "Every decision is recorded: who, when and on what basis.",
    "pt1_h": "A human in the loop", "pt1_p": "You decide which steps need a person's approval – and change it as trust grows.",
    "pt2_h": "Advanced user and permission management", "pt2_p": "An agent gets exactly the rights a person in that role would – never more. The same rules apply to everyone.",
    "pt3_h": "A complete audit trail", "pt3_p": "Who did what, when and why – for people and agents alike.",
    "pt4_h": "Stop at any moment", "pt4_p": "Any agent can be paused instantly, without stopping the rest of the organisation.",

    "pa_label": "Getting started",
    "pa_h2": "Become a frontier firm – step by step, starting from what you have.",
    "pa_sub": "You don't replace everything at once. Amethis connects the data you have, builds what is missing and turns your organisation into the best possible place for AI agents to work – and every step delivers value on its own.",
    "ph1_h": "One golden source", "ph1_p": "Amethis connects your databases and sources – however many there are – into one golden source: a single, consistent version of the truth. The systems that hold the data keep running.",
    "ph2_h": "A semantic layer", "ph2_p": "On top of the golden source sits a semantic layer that describes your organisation: what things mean, how they relate and who may see what. People understand it – and so do AI agents.",
    "ph3_h": "Fill the gaps", "ph3_p": "Where data or processes are missing, Amethis builds them: new applications, workflows and rules for the work that today lives in e-mail and spreadsheets. Existing applications move over when it makes sense – even those that offer only a screen.",
    "ph4_h": "Let agents work", "ph4_p": "Complete data, clear meaning and the same rules as for people make the golden source an ideal workplace for AI agents. As trust grows, they take on more – while people keep the decisions.",

    "tr_label": "Trust by design",
    "tr_h2": "Built for organisations that cannot afford to lose control.",
    "tr_sub": "Public administration, finance, defence, healthcare – wherever data is sensitive and the rules are strict.",
    "t1_h": "Your infrastructure", "t1_p": "Runs on your servers, in your own Azure, Google Cloud or AWS account, or in networks cut off from the internet – the AI model included. Your data stays with you.",
    "t2_h": "Regulation built in", "t2_p": "GDPR, NIS2, the AI Act – the registers, processes and records they require are part of the system, not an extra project.",
    "t3_h": "Security for sensitive data", "t3_p": "Advanced user and permission management and data classification, designed for environments up to EU SECRET.",
    "t4_h": "No lock-in", "t4_p": "Your data stays in open, standard formats – you can take it with you at any time, including away from us.",

    "pr_label": "Proof",
    "pr_h2": "A mission-critical public-sector system – three modules in two weeks.",
    "pr_h3": "A real-time situational-awareness application for a public institution, rebuilt from scratch as a working system.",
    "pr_p": "Built from 300 pages of business requirements – functional and non-functional, exactly as they are written for development teams. No custom programming for the project: the same platform that runs every other deployment.",
    "pr_c1": "A live map of the current situation", "pr_c2": "Event reporting with an approval workflow", "pr_c3": "User and access management with an approval queue",
    "pr_n1": "weeks from start to a working system, accepted by the business", "pr_n2": "modules delivered", "pr_n3": "dashboards and views", "pr_n4": "pages of business requirements", "pr_n5": "lines of custom code",
    "f1_h": "Up to 30× faster", "f1_p": "Applications, processes and integrations delivered up to 30× faster than programming them – and changed just as fast.",
    "f2_h": "Extreme efficiency on modest hardware", "f2_p": "Over a million records processed in minutes on a single server, every one of them traceable. To start, the whole platform fits on one machine.",
    "f3_h": "Scales with you", "f3_p": "Built to scale out across servers as data and users grow – from one department to the whole organisation.",

    "pn_label": "For software houses and integrators",
    "pn_h2": "Software houses: your next business model.",
    "pn_sub": "When anyone can generate software with AI, writing code stops being a business. What remains is a sprawl of AI-built silos – inconsistent, non-compliant and with no safe place for agents to work. That is where Amethis comes in: your team stops selling hours of coding and starts delivering compliant, connected systems on one platform.",
    "pn_c1": "Deployment and support stay with you.", "pn_c2": "Source-code escrow protects both you and your client.", "pn_c3": "Start safely: one process, a pilot, or running alongside an existing system.",
    "pn_cta": "Become a partner",

    "cl_label": "European digital sovereignty",
    "cl_h2": "A data- and process-driven organisation – with people augmented by AI agents.",
    "cl_sub": "Tell us about one process you would like to change. We will show you how it looks in Amethis – with your people in control.",
    "cl_cta": "Start a conversation",
    "ft_eu": "Made in the European Union",
    "ft_privacy": "This site sets no cookies and loads nothing from third parties.",
    "gv3_p": "Data model and labels drafted from your requirements and interviews – approved by your people.",
    "gv3_h": "Drafted by an AI analyst",
    "gv2_p": "GDPR, NIS2 and AI Act registers and processes – built in.",
    "gv2_h": "Regulatory registers",
    "gv1_p": "One shared business vocabulary, with data quality measured in the six DAMA dimensions.",
    "gv1_h": "Catalogue, glossary and quality",
    "gv_hl_p": "Full lineage and provenance for every record. A result is always at least as sensitive as its most sensitive input – and its labels cannot be quietly changed.",
    "gv_hl_h": "Classification computed from what was processed – not guessed from the result.",
    "gv_hl_k": "For auditors",
    "gv_sub": "Not documents and a separate catalogue tool: governance built into every operation, following DAMA.",
    "gv_h2": "Governance that runs – not governance on paper.",
    "gv_label": "Data governance and audit",
    "tq_p": "AI makes building cheap. Trusting what was built is the hard part. In Amethis, trust is part of the infrastructure: every result carries where its data came from, which rules produced it, who approved it and how to reverse it. That is why you can rely on what your people and agents produce – not only build it quickly.",
    "tq_h": "Trust in the result – built in, not bolted on.",
    "tq_k": "Two values, not one",
    "tq_date": "August 2026",
    "tq_cite": "Stephanie L. Woerner et al., “AI Value Creation: Five Provocative Propositions”,",
    "tq_tr": "",
    "og_alt": "Amethis: people and AI agents running an organisation under control – a live process with human approval, permissions, audit trail and compliance",
    "c2_card_a": "Agent proposes a re-plan ▸",
    "c2_card_p": "12 orders affected · 2 customers",
    "c2_card_h": "Truck TR-214 · 40 min late",
    "c2_alt": "A live map showing event alerts, a truck on a road, an aircraft, a ship and a drone, with a selected truck and its context",
    "c2_l5": "Drones",
    "c2_l4": "Ships",
    "c2_l3": "Aircraft",
    "c2_l2": "Trucks",
    "c2_l1": "Events and alerts",
    "c2_p": "Events, alerts and moving objects – trucks, aircraft, ships and drones – on one live map, linked to the processes and decisions behind them. Select an object, see its context and act on it, with the same rules and audit trail as everything else.",
    "c2_h": "A live operational picture – built in.",
    "c2_k": "Command and control",
    "nav_pricing": "Pricing",
    "fit_h": "Tailored down to a single workstation – and changed in hours",
    "fit_p": "Every role – even every person – gets a workspace that fits exactly. Complex structures, delegations and deputies, 40+ administration screens – and changes in hours, not release cycles.",
    "pc_label": "Pricing",
    "pc_h2": "You pay for the work your processes actually do.",
    "pc_sub": "Two simple parts: a subscription for the platform, and usage measured in real business operations – not in servers, compute units, environments or the number of things you build.",
    "pc_sub_k": "Subscription",
    "pc_sub_h": "Platform licence",
    "pc_sub_p": "An annual subscription per organisation: the platform, support, security updates and new versions for the whole term – on your servers or in your own cloud.",
    "pc_use_k": "Usage",
    "pc_use_h": "Real business use",
    "pc_m1_h": "Business operations",
    "pc_m1_p": "each completed step of a process – a decision, an inspection, an approval – with its audit trail",
    "pc_m2_h": "Data loads",
    "pc_m2_p": "bulk imports and migrations, priced per record at a fraction of an operation",
    "pc_m3_h": "Data streams",
    "pc_m3_p": "sensors, telemetry and video, priced lower again",
    "pc_m4_h": "Applications and users",
    "pc_m4_p": "the applications you run and the people actively using them",
    "pc_m5_h": "AI assistance",
    "pc_m5_p": "the work AI agents do for you",
    "pc_n1": "No charge for the number of data sets you build",
    "pc_n2": "You pay only for operations that complete",
    "pc_n3": "A fixed annual budget option for the public sector",
}

PL = dict(EN)
PL.update({
    "lang": "pl", "og_locale": "pl_PL", "base": "../", "home": "/pl/", "canonical": "https://amethis.io/pl/",
    "cur_en": "false", "cur_pl": "true",
    "meta_title": "Amethis – agenci AI pod kontrolą dla organizacji regulowanych",
    "meta_desc": "Amethis zamienia sposób działania organizacji w aplikacje, dane i procesy nawet 30× szybciej – agenci AI pracują, ludzie decydują. U Ciebie lub w chmurze.",
    "skip": "Przejdź do treści", "lang_label": "Język",
    "nav_how": "Jak to działa", "nav_control": "Ludzie i agenci", "nav_path": "Jak zacząć",
    "nav_trust": "Zaufanie", "nav_partners": "Partnerzy", "nav_cta": "Kontakt",
    "mail_subject": "Amethis%20%E2%80%93%20rozmowa", "mail_subject_partner": "Amethis%20%E2%80%93%20partnerstwo",

    "hero_eyebrow": "Dla organizacji regulowanych",
    "hero_h1": "Twoja organizacja, w której ludzie i agenci AI pracują razem –", "hero_h1_grad": "pod Twoją kontrolą.",
    "hero_lede": "Opisz, jak działa Twoja organizacja. Amethis zamieni to w aplikacje, dane, procesy i integracje <b>nawet 30× szybciej</b>, niż dziś trwa budowa i łączenie systemów – a agenci AI przejmą pracę, podczas gdy Twoi ludzie zatwierdzają to, co ważne.",
    "hero_cta1": "Porozmawiajmy", "hero_cta2": "Zobacz, jak to działa",
    "ben1": "Zmiany w tygodnie, nie w lata", "ben2": "Zgodność z regulacjami od początku", "ben3": "Na Twoich serwerach albo w Twoim Azure, Google Cloud lub AWS",
    "scene_alt": "Opisujesz, jak pracujecie; Amethis buduje aplikacje, dane, integracje i reguły i prowadzi proces: wpływa wniosek, agent AI go sprawdza, kierownik zatwierdza, agent kończy sprawę – w ramach uprawnień, śladu audytu i zgodności, na jednym złotym źródle z warstwą semantyczną, testowany na cyfrowym bliźniaku.",
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
    "g_legacy_h": "Twoje źródła danych", "g_legacy_p1": "wiele baz → jedno źródło prawdy,", "g_legacy_p2": "z warstwą semantyczną",
    "g_twin_h": "Cyfrowy bliźniak", "g_twin_p1": "porównaj warianty zmiany,", "g_twin_p2": "zanim wejdzie w życie",

    "how_label": "Jak to działa",
    "how_h2": "Opisujesz, jak pracujecie. Amethis to buduje – i uruchamia.",
    "how_sub": "Amethis to środowisko, w którym Twoje aplikacje i agenci AI żyją i pracują razem. Nie zamawiasz projektu programistycznego: podajesz wymagania, a z nich powstają aplikacje, dane, reguły przetwarzania i integracje, których potrzebuje Twoja organizacja.",
    "st1_h": "Opisujesz", "st1_p": "Podajesz wymagania językiem biznesu – albo po prostu omawiasz je z naszym agentem analitykiem.",
    "st2_h": "Amethis buduje", "st2_p": "Z tych wymagań powstają aplikacje, dane, reguły przetwarzania i integracje – nawet 30× szybciej niż przy programowaniu i łączeniu ich dzisiaj.",
    "st3_h": "Ludzie i agenci pracują razem", "st3_p": "Wszyscy pracują w jednym wspólnym środowisku: agenci przygotowują i wykonują pracę, ludzie decydują tam, gdzie to ważne, a całość jest zsynchronizowana na bieżąco.",
    "twin_h": "Cyfrowy bliźniak: sprawdź, zanim zmienisz",
    "twin_p": "Każdą zmianę – nową regułę, nowy krok, optymalizację – najpierw wypróbujesz na cyfrowym bliźniaku organizacji. Porównasz warianty, zobaczysz, który działa najlepiej, zatwierdzisz go i w każdej chwili cofniesz.",
    "how_note": "Efektem jest nie tylko szybkość: <b>jedno spójne środowisko</b> dla ludzi, agentów i aplikacji – i pewność, że wszystko działa dokładnie tak, jak to określiliście.",

    "one_label": "Jeden system zamiast sześciu",
    "one_h2": "Sześć rodzajów systemów, które inaczej trzeba kupić i połączyć – w jednym.",
    "one_sub": "Dziś zmiana sposobu pracy dotyka kilku osobnych narzędzi, każde z własnym dostawcą, danymi i projektem. W Amethis to jedno środowisko, więc zmianę robi się raz i jest spójna wszędzie. A w każdej z sześciu kategorii poziom funkcjonalny jest porównywalny z liderami rynku.",
    "instead": "zamiast",
    "o1_h": "Interfejsy użytkownika", "o1_p": "Zintegrowane, nowoczesne środowisko UI: aplikacje powstają z ekranów (pulpitów), na których są kafelki (widżety) złożone z elementów – tabel, formularzy, kontrolek, wykresów, map – wyłącznie konfiguracją, bez programowania.", "o1_s": "osobnego narzędzia do budowy aplikacji",
    "o2_h": "Procesy i akceptacje", "o2_p": "Obieg spraw, kolejki zadań, akceptacje i zastępstwa – praca, która dziś żyje w mailach i arkuszach.", "o2_s": "osobnego systemu obiegu spraw",
    "o3_h": "Integracje", "o3_p": "Połączenia z systemami, które już macie, na bieżąco – nawet z takimi, które mają tylko ekran.", "o3_s": "osobnej platformy integracyjnej",
    "o4_h": "Dane i złote źródło", "o4_p": "Jedno złote źródło danych (golden source) ze wszystkich Twoich baz, z warstwą semantyczną opisującą organizację – oraz raporty i analizy na aktualnych danych.", "o4_s": "osobnej platformy danych",
    "o5_h": "Zgodność", "o5_p": "Rejestry i procesy wymagane przez RODO, NIS2 i AI Act – wbudowane.", "o5_s": "osobnych narzędzi compliance",
    "o6_h": "Agenci AI", "o6_p": "Agenci pracujący na tych samych danych i według tych samych reguł co Twoi ludzie.", "o6_s": "osobnej platformy AI",

    "ct_label": "Ludzie decydują · agenci wykonują",
    "ct_h2": "Agenci AI przejmują pracę. Decyzje zostają przy Twoich ludziach.",
    "ct_sub": "Agenci przygotowują, sprawdzają i wykonują zadania przez całą dobę. Tam, gdzie decyzja ma znaczenie, zatwierdza ją człowiek – a każdy krok jest zapisany.",
    "ap_alt": "Przykład: agent AI prosi kierownika o zatwierdzenie przeplanowania produkcji",
    "ap_from": "Agent AI · planowanie operacji", "ap_title": "Przeplanuj 38 zamówień po opóźnieniu dostawcy", "ap_amount": "oszczędność 890 000 zł",
    "ap_c1": "Dane z ERP, magazynu i 2 portali dostawców – jedno złote źródło", "ap_c2": "Sprawdzone na cyfrowym bliźniaku: terminowość 91% → 98%",
    "ap_c3": "Przygotowane powiadomienia dla 12 klientów, których to dotyczy",
    "ap_ok": "Zatwierdź", "ap_no": "Odrzuć", "ap_var": "Porównaj warianty", "ap_c4": "Zmienia 3 plany produkcji – wymagana decyzja kierownika",
    "ap_foot": "Każda decyzja jest zapisana: kto, kiedy i na jakiej podstawie.",
    "pt1_h": "Człowiek w pętli decyzyjnej", "pt1_p": "Ty decydujesz, które kroki wymagają akceptacji człowieka – i zmieniasz to, gdy rośnie zaufanie.",
    "pt2_h": "Zaawansowane zarządzanie użytkownikami i uprawnieniami", "pt2_p": "Agent dostaje dokładnie te uprawnienia, które miałby człowiek w tej roli – nigdy więcej. Te same reguły obowiązują wszystkich.",
    "pt3_h": "Pełny ślad audytowy", "pt3_p": "Kto, co, kiedy i dlaczego zrobił – tak samo dla ludzi, jak i dla agentów.",
    "pt4_h": "Zatrzymanie w każdej chwili", "pt4_p": "Każdego agenta można natychmiast wstrzymać, nie zatrzymując reszty organizacji.",

    "pa_label": "Jak zacząć",
    "pa_h2": "Stań się „frontier firm” – krok po kroku, zaczynając od tego, co już masz.",
    "pa_sub": "Nie wymieniasz wszystkiego naraz. Amethis łączy dane, które już masz, buduje to, czego brakuje, i zamienia Twoją organizację w najlepsze możliwe miejsce pracy dla agentów AI – a każdy krok daje wartość sam w sobie.",
    "ph1_h": "Jedno złote źródło", "ph1_p": "Amethis łączy Twoje bazy i źródła danych – niezależnie od ich liczby – w jedno złote źródło (golden source): jedną, spójną wersję prawdy. Systemy, które trzymają dane, działają dalej.",
    "ph2_h": "Warstwa semantyczna", "ph2_p": "Na złotym źródle leży warstwa semantyczna, która opisuje Twoją organizację: co znaczą poszczególne pojęcia, jak się ze sobą wiążą i kto co może zobaczyć. Rozumieją ją ludzie – i agenci AI.",
    "ph3_h": "Uzupełnij luki", "ph3_p": "Tam, gdzie brakuje danych albo procesów, Amethis je buduje: nowe aplikacje, obiegi spraw i reguły dla pracy, która dziś żyje w mailach i arkuszach. Istniejące aplikacje przenosisz wtedy, gdy ma to sens – nawet te, które mają tylko ekran.",
    "ph4_h": "Pozwól agentom pracować", "ph4_p": "Kompletne dane, jasne znaczenie i te same reguły co dla ludzi czynią złote źródło idealnym miejscem pracy agentów AI. W miarę wzrostu zaufania przejmują coraz więcej – a decyzje zostają przy ludziach.",

    "tr_label": "Zaufanie u podstaw",
    "tr_h2": "Zbudowany dla organizacji, które nie mogą stracić kontroli.",
    "tr_sub": "Administracja publiczna, finanse, obronność, ochrona zdrowia – wszędzie tam, gdzie dane są wrażliwe, a reguły surowe.",
    "t1_h": "Twoja infrastruktura", "t1_p": "Działa na Twoich serwerach, na Twoim koncie Azure, Google Cloud lub AWS albo w sieciach odciętych od internetu – razem z modelem AI. Dane zostają u Ciebie.",
    "t2_h": "Regulacje wbudowane", "t2_p": "RODO, NIS2, AI Act – wymagane rejestry, procesy i zapisy są częścią systemu, a nie dodatkowym projektem.",
    "t3_h": "Bezpieczeństwo danych wrażliwych", "t3_p": "Zaawansowane zarządzanie użytkownikami i uprawnieniami oraz klasyfikacja danych, projektowane dla środowisk do EU SECRET włącznie.",
    "t4_h": "Bez uzależnienia od dostawcy", "t4_p": "Dane zostają w otwartych, standardowych formatach – możesz je zabrać w każdej chwili, także od nas.",

    "pr_label": "Dowód",
    "pr_h2": "Krytyczny system sektora publicznego – trzy moduły w dwa tygodnie.",
    "pr_h3": "Aplikacja bieżącej świadomości sytuacyjnej dla instytucji publicznej, odtworzona od zera jako działający system.",
    "pr_p": "Zbudowany na podstawie 300 stron wymagań biznesowych – funkcjonalnych i niefunkcjonalnych, takich, jakie pisze się dla zespołów deweloperskich. Zero programowania pod ten projekt: ta sama platforma, która działa w każdym innym wdrożeniu.",
    "pr_c1": "Mapa bieżącej sytuacji na żywo", "pr_c2": "Zgłaszanie zdarzeń z obiegiem akceptacji", "pr_c3": "Zarządzanie użytkownikami i dostępami z kolejką akceptacji",
    "pr_n1": "tygodnie od startu do działającego systemu, odebranego przez biznes", "pr_n2": "dostarczone moduły", "pr_n3": "pulpitów i widoków", "pr_n4": "stron wymagań biznesowych", "pr_n5": "linii kodu na zamówienie",
    "f1_h": "Nawet 30× szybciej", "f1_p": "Aplikacje, procesy i integracje dostarczane nawet 30× szybciej niż przy programowaniu – i zmieniane równie szybko.",
    "f2_h": "Skrajna wydajność na skromnym sprzęcie", "f2_p": "Ponad milion rekordów przetworzonych w kilka minut na jednym serwerze, każdy z pełnym śladem pochodzenia. Na start cała platforma mieści się na jednej maszynie.",
    "f3_h": "Rośnie razem z Tobą", "f3_p": "Zbudowany tak, by skalować się na kolejne serwery wraz ze wzrostem danych i użytkowników – od jednego działu do całej organizacji.",

    "pn_label": "Dla software house'ów i integratorów",
    "pn_h2": "Software house'y: wasz następny model biznesowy.",
    "pn_sub": "Gdy każdy może wygenerować oprogramowanie z pomocą AI, pisanie kodu przestaje być biznesem. Zostaje gąszcz silosów zbudowanych przez AI – niespójnych, niezgodnych z regulacjami i bez bezpiecznego miejsca pracy dla agentów. Tu wchodzi Amethis: wasz zespół przestaje sprzedawać godziny programowania, a zaczyna dostarczać spójne, zgodne z regulacjami systemy na jednej platformie.",
    "pn_c1": "Wdrożenie i utrzymanie zostają po waszej stronie.", "pn_c2": "Depozyt kodu źródłowego chroni was i waszego klienta.", "pn_c3": "Bezpieczny start: jeden proces, pilotaż albo praca obok istniejącego systemu.",
    "pn_cta": "Zostań partnerem",

    "cl_label": "Europejska suwerenność cyfrowa",
    "cl_h2": "Organizacja oparta na danych i procesach – z ludźmi wspieranymi przez agentów AI.",
    "cl_sub": "Opowiedz nam o jednym procesie, który chcesz zmienić. Pokażemy, jak wygląda w Amethis – z Twoimi ludźmi przy sterach.",
    "cl_cta": "Zacznijmy rozmowę",
    "ft_eu": "Wyprodukowano w Unii Europejskiej",
    "ft_privacy": "Ta strona nie ustawia ciasteczek i niczego nie pobiera od stron trzecich.",
    "gv3_p": "Model danych i etykiety przygotowane na podstawie wymagań i rozmów – zatwierdzone przez Twoich ludzi.",
    "gv3_h": "Przygotowane przez agenta analityka",
    "gv2_p": "Rejestry i procesy RODO, NIS2 i AI Act – wbudowane.",
    "gv2_h": "Rejestry regulacyjne",
    "gv1_p": "Jeden wspólny słownik pojęć biznesowych, a jakość danych mierzona w sześciu wymiarach DAMA.",
    "gv1_h": "Katalog, słownik i jakość",
    "gv_hl_p": "Pełny lineage i pochodzenie każdego rekordu. Wynik jest zawsze co najmniej tak wrażliwy jak jego najwrażliwsze wejście – a jego etykiet nie da się po cichu zmienić.",
    "gv_hl_h": "Klasyfikacja liczona z tego, co przetworzono – a nie zgadywana z wyniku.",
    "gv_hl_k": "Dla audytorów",
    "gv_sub": "Nie dokumenty i osobne narzędzie katalogowe: governance wbudowane w każdą operację, zgodnie z DAMA.",
    "gv_h2": "Governance, które działa – a nie leży na papierze.",
    "gv_label": "Zarządzanie danymi i audyt",
    "tq_p": "AI sprawia, że budowanie jest tanie. Trudne jest zaufanie do tego, co powstało. W Amethis zaufanie jest częścią infrastruktury: każdy wynik niesie informację, skąd pochodzą dane, jakie reguły go wytworzyły, kto go zatwierdził i jak go cofnąć. Dlatego możesz polegać na tym, co tworzą Twoi ludzie i agenci – a nie tylko szybko to zbudować.",
    "tq_h": "Zaufanie do wyniku – wbudowane, a nie doklejone.",
    "tq_k": "Dwie wartości, nie jedna",
    "tq_date": "sierpień 2026",
    "tq_cite": "Stephanie L. Woerner i in., „AI Value Creation: Five Provocative Propositions”,",
    "tq_tr": "„To, co wygląda na tanie w budowie, staje się drogie w zaufaniu.”",
    "og_alt": "Amethis: ludzie i agenci AI prowadzą organizację pod kontrolą – proces na żywo z akceptacją człowieka, uprawnieniami, śladem audytu i zgodnością",
    "c2_card_a": "Agent proponuje przeplanowanie ▸",
    "c2_card_p": "12 zamówień · 2 klientów",
    "c2_card_h": "Ciężarówka TR-214 · 40 min opóźnienia",
    "c2_alt": "Mapa na żywo z alertami zdarzeń, ciężarówką na drodze, samolotem, statkiem i dronem oraz wybraną ciężarówką z jej kontekstem",
    "c2_l5": "Drony",
    "c2_l4": "Statki",
    "c2_l3": "Samoloty",
    "c2_l2": "Ciężarówki",
    "c2_l1": "Zdarzenia i alerty",
    "c2_p": "Zdarzenia, alerty i obiekty w ruchu – ciężarówki, samoloty, statki i drony – na jednej mapie na żywo, powiązane z procesami i decyzjami, które za nimi stoją. Wybierasz obiekt, widzisz jego kontekst i działasz – według tych samych reguł i z tym samym śladem audytu co wszystko inne.",
    "c2_h": "Bieżący obraz operacyjny – w standardzie.",
    "c2_k": "Command and control",
    "nav_pricing": "Opłaty",
    "fit_h": "Dopasowane aż do pojedynczego stanowiska – i zmieniane w godziny",
    "fit_p": "Każda rola – a nawet każda osoba – dostaje przestrzeń pracy dopasowaną dokładnie do siebie. Złożone struktury, delegacje i zastępstwa, ponad 40 ekranów administracyjnych – i zmiany w ciągu godzin, a nie cykli wydawniczych.",
    "pc_label": "Model opłat",
    "pc_h2": "Płacisz za pracę, którą faktycznie wykonują Twoje procesy.",
    "pc_sub": "Dwa proste składniki: subskrypcja platformy i użycie mierzone w realnych operacjach biznesowych – a nie w serwerach, jednostkach mocy obliczeniowej, środowiskach czy liczbie rzeczy, które zbudujesz.",
    "pc_sub_k": "Subskrypcja",
    "pc_sub_h": "Licencja platformy",
    "pc_sub_p": "Roczna subskrypcja dla organizacji: platforma, wsparcie, aktualizacje bezpieczeństwa i nowe wersje przez cały okres – na Twoich serwerach albo w Twojej chmurze.",
    "pc_use_k": "Użycie",
    "pc_use_h": "Realne wykorzystanie w biznesie",
    "pc_m1_h": "Operacje biznesowe",
    "pc_m1_p": "każdy zakończony krok procesu – decyzja, kontrola, akceptacja – wraz ze śladem audytu",
    "pc_m2_h": "Paczki danych",
    "pc_m2_p": "masowe ładowania i migracje, rozliczane per rekord za ułamek ceny operacji",
    "pc_m3_h": "Strumienie danych",
    "pc_m3_p": "czujniki, telemetria i wideo – jeszcze taniej",
    "pc_m4_h": "Aplikacje i użytkownicy",
    "pc_m4_p": "aplikacje, które uruchamiasz, i osoby, które aktywnie z nich korzystają",
    "pc_m5_h": "Wsparcie AI",
    "pc_m5_p": "praca, którą wykonują dla Ciebie agenci AI",
    "pc_n1": "Bez opłat za liczbę zbiorów danych, które budujesz",
    "pc_n2": "Płacisz tylko za operacje zakończone",
    "pc_n3": "Wariant ze stałym budżetem rocznym dla sektora publicznego",
})


# Business identification shown in the footer. Amethis is currently a brand of a sole proprietorship;
# values below come from the Ministry of Finance VAT register (wl-api.mf.gov.pl, NIP 5212106852).
# "address" is optional by design: the register lists only a residence address, published only on request.
COMPANY = {
    "trade_name": "QuickUp",
    "owner": "Piotr Mikołajczak",
    "nip": "5212106852",
    "vat_eu": "PL5212106852",
    "regon": "012640530",
    "address": "",
}

IMPRINT = {
    "en": "{trade_name}, {owner} · EU VAT {vat_eu}",
    "pl": "{trade_name}, {owner} · VAT UE {vat_eu}",
}


def imprint(lang: str) -> str:
    text = IMPRINT[lang].format(**COMPANY)
    return f"{text} · {COMPANY['address']}" if COMPANY["address"] else text


def structured_data(content: dict) -> str:
    """Schema.org graph (Organization, WebSite, SoftwareApplication) for search engines."""
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Organization", "@id": "https://amethis.io/#org", "name": "Amethis", "url": "https://amethis.io/",
             "logo": "https://amethis.io/assets/apple-touch-icon.png", "email": "info@amethis.io",
             "legalName": f"{COMPANY['trade_name']} {COMPANY['owner']}", "vatID": COMPANY["vat_eu"], "areaServed": "EU"},
            {"@type": "WebSite", "@id": "https://amethis.io/#website", "name": "Amethis", "url": "https://amethis.io/",
             "inLanguage": ["en", "pl"], "publisher": {"@id": "https://amethis.io/#org"}},
            {"@type": "SoftwareApplication", "name": "Amethis", "url": content["canonical"],
             "applicationCategory": "BusinessApplication",
             "operatingSystem": "On-premises, Microsoft Azure, Google Cloud, AWS",
             "description": content["meta_desc"], "inLanguage": content["lang"],
             "publisher": {"@id": "https://amethis.io/#org"}},
        ],
    }
    return json.dumps(graph, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def write_sitemap(dist: Path) -> None:
    today = date.today().isoformat()
    alt = ('<xhtml:link rel="alternate" hreflang="en" href="https://amethis.io/"/>'
           '<xhtml:link rel="alternate" hreflang="pl" href="https://amethis.io/pl/"/>'
           '<xhtml:link rel="alternate" hreflang="x-default" href="https://amethis.io/"/>')
    urls = "".join(f"  <url><loc>{u}</loc><lastmod>{today}</lastmod>{alt}</url>\n"
                   for u in ("https://amethis.io/", "https://amethis.io/pl/"))
    (dist / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        f"{urls}</urlset>\n", encoding="utf-8")


def render(content: dict) -> str:
    missing = sorted(set(re.findall(r"\{\{(\w+)\}\}", TEMPLATE)) - content.keys())
    if missing:
        sys.exit(f"template keys without content: {missing}")
    return re.sub(r"\{\{(\w+)\}\}", lambda m: content[m.group(1)], TEMPLATE)


def main() -> None:
    dist = ROOT / "dist"
    (dist / "pl").mkdir(parents=True, exist_ok=True)
    EN["imprint"], PL["imprint"] = imprint("en"), imprint("pl")
    # Content hash in the stylesheet URL, so a browser never pairs new HTML with a cached old stylesheet.
    css_v = hashlib.sha256((dist / "assets" / "styles.css").read_bytes()).hexdigest()[:10]
    EN["css_v"] = PL["css_v"] = css_v
    EN["jsonld"], PL["jsonld"] = structured_data(EN), structured_data(PL)
    write_sitemap(dist)
    (dist / "index.html").write_text(render(EN), encoding="utf-8")
    (dist / "pl" / "index.html").write_text(render(PL), encoding="utf-8")
    print("built dist/index.html and dist/pl/index.html")


if __name__ == "__main__":
    main()
