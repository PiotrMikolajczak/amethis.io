#!/usr/bin/env python3
"""Render the amethis.io site in English (/) and Polish (/pl/) from one layout and shared section blocks.

Usage: python3 src/build.py   (writes dist/**/index.html for every page in PAGES, both languages)
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
LAYOUT = (ROOT / "src" / "layout.html").read_text(encoding="utf-8")
BLOCKS = ROOT / "src" / "blocks"
SITE = "https://amethis.io"

EN = {
    "lang": "en", "og_locale": "en_GB", "base": "", "home": "/", "canonical": "https://amethis.io/",
    "href_en": "/", "href_pl": "/pl/", "cur_en": "true", "cur_pl": "false",
    "meta_title": "Amethis – governed operations for regulated organisations",
    "meta_desc": "Describe how your organisation works – Amethis runs it, with people and AI agents under your control. An order of magnitude faster, on your own infrastructure.",
    "skip": "Skip to content", "lang_label": "Language",
    "nav_how": "How it works", "nav_control": "People & agents", "nav_path": "Getting started",
    "nav_trust": "Trust", "nav_partners": "Partners", "nav_cta": "Contact",
    "mail_subject": "Amethis%20%E2%80%93%20introduction", "mail_subject_partner": "Amethis%20%E2%80%93%20partnership",

    "hero_eyebrow": "Governed operations platform · for regulated organisations",
    "hero_h1": "Describe how your organisation works. Amethis runs it – with people and AI agents,", "hero_h1_grad": "under your control.",
    "hero_lede": "One governed platform turns your requirements into working applications, data, processes and integrations – in weeks, an order of magnitude faster than building and integrating systems today. AI agents work on the same data and under the same rules as your people, and your people approve what matters.",
    "hero_cta1": "Show us one process", "hero_cta2": "See the proof",
    "ben1": "Working system in weeks, not years", "ben2": "Records and audit trail for regulators", "ben3": "On your servers or in your own Azure, Google Cloud or AWS",
    "scene_alt": "You describe how you work; Amethis builds applications, data, integrations and rules and runs the process: a request arrives, an AI agent checks it, a manager approves, the agent completes it – within permissions, audit trail and compliance, connected to your data sources, with every change rehearsed before it goes live.",
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
    "g_twin_h": "Rehearsal", "g_twin_p1": "replay history on the new rule,", "g_twin_p2": "compare variants before go-live",

    "how_label": "How it works",
    "how_h2": "You describe how you work. Amethis builds it – and runs it.",
    "how_sub": "Amethis is a platform in which your applications and AI agents live and work together. You start from approved requirements, not from a blank development backlog – and from them come the applications, data, rules and integrations your organisation needs.",
    "st1_h": "Describe", "st1_p": "State your requirements in business language – or talk them through with our AI analyst. It drafts the model; your people review and approve it.",
    "st2_h": "Amethis builds and runs", "st2_p": "Applications, data, rules and integrations come from those requirements – in weeks. A change is a change to the description, not a new project.",
    "st3_h": "People and agents work together", "st3_p": "Everyone works in one shared environment: agents prepare and carry out the work, people decide where it matters, and everything stays in sync in real time.",
    "twin_h": "Rehearse before you change",
    "twin_p": "Replay real history against a new rule or step, see the effect, compare variants – then approve, or roll back at any time.",
    "how_note": "Why it is both fast and trustworthy: you configure only the business logic – every other mechanism, from permissions and audit to integrations and scaling, comes with the platform. That configuration is versioned and validated before it runs, and there is no code to write or maintain. <b>You build faster – and every change can be checked.</b>",

    "one_label": "One platform instead of six",
    "one_h2": "Six kinds of systems you would otherwise buy and connect – in one.",
    "one_sub": "Today a change in how you work touches several separate tools, each with its own supplier, data and project. In Amethis they are one environment, so a change is made once and is consistent everywhere.",
    "instead": "instead of",
    "o1_h": "User interfaces", "o1_p": "An integrated, modern UI environment: applications are built from screens (dashboards) made of tiles (widgets), which are assembled from elements – tables, forms, controls, charts, maps – by configuration alone, without programming.", "o1_s": "a separate app-building tool",
    "o2_h": "Processes and approvals", "o2_p": "Workflows, task queues, approvals and deputies – the work that today lives in e-mail and spreadsheets.", "o2_s": "a separate workflow system",
    "o3_h": "Integrations", "o3_p": "Connections with the systems you already have, exchanging data in real time.", "o3_s": "a separate integration platform",
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
    "pt1_h": "A human in the loop", "pt1_p": "You decide which steps need a person's approval – and widen the agent's room as trust grows.",
    "pt2_h": "Same rules for people and agents", "pt2_p": "An agent gets exactly the rights a person in that role would – never more. One set of permissions, enforced on every read and write.",
    "pt3_h": "A complete audit trail", "pt3_p": "Who did what, when, on which data and under which rule – for people and agents alike.",
    "pt4_h": "Pause at any moment", "pt4_p": "Any agent can be paused instantly, its access revoked and its record kept – without stopping the rest of the organisation.",

    "gs_label": "Data and meaning",
    "gs_h2": "One trusted set of data – and a model of your organisation that people and agents understand.",
    "gs_sub": "You don't replace everything at once. Amethis connects the data you have, builds what is missing and turns your organisation into the best possible place for AI agents to work – and every step delivers value on its own.",
    "gs1_h": "One golden source", "gs1_p": "Amethis connects your databases and sources – however many there are – into one golden source: a single, consistent version of the truth. The systems that hold the data keep running.",
    "gs2_h": "A semantic layer", "gs2_p": "On top of the golden source sits a semantic layer that describes your organisation: what things mean, how they relate and who may see what. People understand it – and so do AI agents.",
    "gs3_h": "Fill the gaps", "gs3_p": "Where data or processes are missing, Amethis builds them: new applications, workflows and rules for the work that today lives in e-mail and spreadsheets. Existing applications move over when it makes sense.",
    "gs4_h": "Let agents work", "gs4_p": "Complete data, clear meaning and the same rules as for people make the golden source an ideal workplace for AI agents. As trust grows, they take on more – while people keep the decisions.",

    "tr_label": "Trust and sovereignty",
    "tr_h2": "Built for organisations that cannot afford to lose control.",
    "tr_sub": "Public administration, critical infrastructure, defence, finance, healthcare – wherever data is sensitive and the rules are strict. Made in the European Union.",
    "t1_h": "Your infrastructure", "t1_p": "Runs on your servers, in your own Azure, Google Cloud or AWS account, or in networks cut off from the internet – the AI model included. Never a shared cloud service.",
    "t2_h": "Regulation, operationalised", "t2_p": "The registers, workflows and records that GDPR, NIS2 and the AI Act require are part of the running system – not a separate project.",
    "t3_h": "Security for classified and isolated environments", "t3_p": "Classification labels on every record, permissions computed per row, evidence collected for accreditation. Accreditation is granted per installation by the competent authority.",
    "t4_h": "No lock-in", "t4_p": "Your data and its governance metadata stay in open, standard formats – you can take them with you at any time, including away from us.",

    "pr_label": "Proof",
    "pr_h2": "A mission-critical public-sector system – three modules in two weeks.",
    "pr_h3": "A real-time situational-awareness application for an EU public institution.",
    "pr_p": "Built from 300 pages of functional and non-functional requirements, exactly as written for development teams. No programming for the project – the same platform that runs every other deployment.",
    "pr_c1": "A live map of the current situation", "pr_c2": "Event reporting with an approval workflow", "pr_c3": "User and access management with an approval queue",
    "pr_n1": "weeks to a working, accepted system", "pr_n2": "modules delivered", "pr_n3": "dashboards and views", "pr_n4": "pages of business requirements", "pr_n5": "lines of custom code",
    "f1_h": "Up to 30× faster", "f1_p": "Applications, processes and integrations delivered up to 30× faster than programming them – and changed just as fast.",
    "f2_h": "Extreme efficiency on modest hardware", "f2_p": "Over a million records processed in minutes on a single server, every one of them traceable. To start, the whole platform fits on one machine.",
    "f3_h": "Scales with you", "f3_p": "Built to scale out across servers as data and users grow – from one department to the whole organisation.",

    "pn_label": "For software houses and integrators",
    "pn_h2": "Software houses: your next business model.",
    "pn_sub": "AI makes code cheap to write – and leaves organisations with silos that are hard to govern and give agents no safe place to work. With Amethis your team delivers connected, compliant systems instead: larger programmes with a smaller team, while you keep the delivery, support and recurring revenue.",
    "pn_c1": "Deployment and support stay with you.", "pn_c2": "Source-code escrow protects both you and your client.", "pn_c3": "Start safely: one process, a pilot, or running alongside an existing system.",
    "pn_cta": "Become a partner",

    "cl_label": "European digital sovereignty",
    "cl_h2": "A data- and process-driven organisation – with people augmented by AI agents.",
    "cl_sub": "Tell us about one process you would like to change. In a 45-minute working session we map it with you and show how it looks in Amethis – with your people in control. You leave with a concrete pilot outline.",
    "cl_cta": "Show us one process",
    "ft_eu": "Made in the European Union",
    "ft_privacy": "This site sets no cookies and loads nothing from third parties.",
    "nav_home": "Home",
    "oa_sub": "For public administration, emergency services and critical infrastructure: events, alerts and moving objects on one live map – with the same rules, approvals and audit trail as everything else in Amethis.",
    "oa_h2": "A live operational picture – linked to the decisions behind it.",
    "oa_label": "Solutions · operational awareness",
    "fit_label": "Tailored to every workstation",
    "cl_alt": "Software house or integrator? See the partner programme →",
    "ph3_p": "As trust grows, agents take on more – and your people keep the decisions.",
    "ph3_h": "More processes, more agents",
    "ph2_p": "Connect the systems that hold your data. They keep running; Amethis gives you one trusted view and takes over work piece by piece.",
    "ph2_h": "Pilot on your infrastructure",
    "ph1_p": "Pick a process that lives in e-mail and spreadsheets today. In weeks it runs in Amethis – with your data, your rules and your approvals.",
    "ph1_h": "One process",
    "pa_sub": "You don't replace anything at once. Every step delivers value on its own – and each one makes your organisation a better place for people and AI agents to work.",
    "pa_h2": "Start with one process. Keep everything you have.",
    "pa_label": "Getting started",
    "one_more": "See the platform in detail →",
    "r4_p": "The registers, workflows and evidence your GDPR, NIS2 and AI Act programmes need – kept by the same system that does the work.",
    "r4_h": "Records and evidence for regulators",
    "r3_p": "Your existing systems keep running. Amethis connects them in real time and takes over work piece by piece – no switch-over day.",
    "r3_h": "Integration with what you have",
    "r2_p": "One trusted set of data across your sources, with shared business definitions – and every result traceable to where it came from.",
    "r2_h": "Data you can trust",
    "r1_p": "Screens, forms, task queues, approvals and deputies – built from your requirements, changed in hours.",
    "r1_h": "Applications and processes",
    "oc_sub": "Today a change in how you work touches several tools, each with its own supplier, data and project. In Amethis it is one environment: you make the change once, and it is consistent everywhere – in the screens, the data, the rules and the audit trail.",
    "oc_h2": "Applications, processes, data, integrations, compliance and AI agents – one system, one change.",
    "ap_tag": "Illustrative scenario",
    "pm_sub": "Up to 30× faster – measured on this build, where the back end, data and integration work that normally takes months of programming took days. Analysis and acceptance stay with your experts, so the gain on a whole project depends on the domain.",
    "pm_h2": "Measured, not promised.",
    "pm_label": "Speed and scale",
    "pr_status": "Rebuilt from the institution's own requirements and accepted by the business as working correctly – built the way every Amethis deployment is built, an order of magnitude faster than conventional development.",
    "hero_proofline": "Proven: a mission-critical EU public-sector system – 3 modules from 300 pages of requirements in 2 weeks, 0 lines of custom code →",
    "hero_tag": "Your operating model, running.",
    "ft_nav_label": "Site",
    "nav_opaw": "Operational awareness",
    "nav_governance": "Data governance",
    "nav_proof": "Proof",
    "nav_platform": "Platform",
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
    "meta_title": "Amethis – platforma operacyjna pod kontrolą",
    "meta_desc": "Opisz, jak działa Twoja organizacja – Amethis to uruchomi, z ludźmi i agentami AI pod Twoją kontrolą. O rząd wielkości szybciej, na Twojej infrastrukturze.",
    "skip": "Przejdź do treści", "lang_label": "Język",
    "nav_how": "Jak to działa", "nav_control": "Ludzie i agenci", "nav_path": "Jak zacząć",
    "nav_trust": "Zaufanie", "nav_partners": "Partnerzy", "nav_cta": "Kontakt",
    "mail_subject": "Amethis%20%E2%80%93%20rozmowa", "mail_subject_partner": "Amethis%20%E2%80%93%20partnerstwo",

    "hero_eyebrow": "Platforma operacyjna pod kontrolą · dla organizacji regulowanych",
    "hero_h1": "Opisz, jak działa Twoja organizacja. Amethis to uruchomi – z ludźmi i agentami AI,", "hero_h1_grad": "pod Twoją kontrolą.",
    "hero_lede": "Jedna platforma pod kontrolą zamienia Twoje wymagania w działające aplikacje, dane, procesy i integracje – w tygodnie, o rząd wielkości szybciej niż dzisiejsza budowa i łączenie systemów. Agenci AI pracują na tych samych danych i według tych samych reguł co Twoi ludzie, a ludzie zatwierdzają to, co ważne.",
    "hero_cta1": "Pokaż nam jeden proces", "hero_cta2": "Zobacz dowód",
    "ben1": "Działający system w tygodnie, nie w lata", "ben2": "Rejestry i ślad audytu dla regulatorów", "ben3": "Na Twoich serwerach albo w Twoim Azure, Google Cloud lub AWS",
    "scene_alt": "Opisujesz, jak pracujecie; Amethis buduje aplikacje, dane, integracje i reguły i prowadzi proces: wpływa wniosek, agent AI go sprawdza, kierownik zatwierdza, agent kończy sprawę – w ramach uprawnień, śladu audytu i zgodności, połączony z Twoimi źródłami danych, a każda zmiana jest przećwiczona przed wdrożeniem.",
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
    "g_twin_h": "Próba", "g_twin_p1": "odtwórz historię na nowej regule,", "g_twin_p2": "porównaj warianty przed wdrożeniem",

    "how_label": "Jak to działa",
    "how_h2": "Opisujesz, jak pracujecie. Amethis to buduje – i uruchamia.",
    "how_sub": "Amethis to platforma, w której Twoje aplikacje i agenci AI żyją i pracują razem. Zaczynasz od zatwierdzonych wymagań, a nie od pustego backlogu programistycznego – i z nich powstają aplikacje, dane, reguły i integracje, których potrzebuje organizacja.",
    "st1_h": "Opisujesz", "st1_p": "Podajesz wymagania językiem biznesu – albo omawiasz je z naszym agentem analitykiem. Agent przygotowuje model; Twoi ludzie go sprawdzają i zatwierdzają.",
    "st2_h": "Amethis buduje i uruchamia", "st2_p": "Z wymagań powstają aplikacje, dane, reguły i integracje – w tygodnie. Zmiana to zmiana opisu, nie nowy projekt.",
    "st3_h": "Ludzie i agenci pracują razem", "st3_p": "Wszyscy pracują w jednym wspólnym środowisku: agenci przygotowują i wykonują pracę, ludzie decydują tam, gdzie to ważne, a całość jest zsynchronizowana na bieżąco.",
    "twin_h": "Przećwicz, zanim zmienisz",
    "twin_p": "Odtwórz prawdziwą historię na nowej regule albo kroku, zobacz skutek, porównaj warianty – potem zatwierdź albo w każdej chwili cofnij.",
    "how_note": "Dlaczego to jest jednocześnie szybkie i godne zaufania: konfigurujesz wyłącznie logikę biznesową – wszystkie pozostałe mechanizmy, od uprawnień i audytu po integracje i skalowanie, dostarcza platforma. Ta konfiguracja jest wersjonowana i sprawdzana, zanim zacznie działać, a kodu nie trzeba pisać ani utrzymywać. <b>Budujesz szybciej – i możesz sprawdzić każdą zmianę.</b>",

    "one_label": "Jedna platforma zamiast sześciu",
    "one_h2": "Sześć rodzajów systemów, które inaczej trzeba kupić i połączyć – w jednym.",
    "one_sub": "Dziś zmiana sposobu pracy dotyka kilku osobnych narzędzi, każde z własnym dostawcą, danymi i projektem. W Amethis to jedno środowisko, więc zmianę robi się raz i jest spójna wszędzie.",
    "instead": "zamiast",
    "o1_h": "Interfejsy użytkownika", "o1_p": "Zintegrowane, nowoczesne środowisko UI: aplikacje powstają z ekranów (pulpitów), na których są kafelki (widżety) złożone z elementów – tabel, formularzy, kontrolek, wykresów, map – wyłącznie konfiguracją, bez programowania.", "o1_s": "osobnego narzędzia do budowy aplikacji",
    "o2_h": "Procesy i akceptacje", "o2_p": "Obieg spraw, kolejki zadań, akceptacje i zastępstwa – praca, która dziś żyje w mailach i arkuszach.", "o2_s": "osobnego systemu obiegu spraw",
    "o3_h": "Integracje", "o3_p": "Połączenia z systemami, które już macie, wymieniające dane na bieżąco.", "o3_s": "osobnej platformy integracyjnej",
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
    "pt1_h": "Człowiek w pętli decyzyjnej", "pt1_p": "Ty decydujesz, które kroki wymagają akceptacji człowieka – i poszerzasz pole agenta, gdy rośnie zaufanie.",
    "pt2_h": "Te same reguły dla ludzi i agentów", "pt2_p": "Agent dostaje dokładnie te uprawnienia, które miałby człowiek w tej roli – nigdy więcej. Jeden zestaw uprawnień, egzekwowany przy każdym odczycie i zapisie.",
    "pt3_h": "Pełny ślad audytowy", "pt3_p": "Kto, co, kiedy, na jakich danych i według jakiej reguły – tak samo dla ludzi, jak i dla agentów.",
    "pt4_h": "Wstrzymanie w każdej chwili", "pt4_p": "Każdego agenta można natychmiast wstrzymać, odebrać mu dostęp i zachować jego zapis – nie zatrzymując reszty organizacji.",

    "gs_label": "Dane i znaczenie",
    "gs_h2": "Jeden wiarygodny zbiór danych – i model organizacji zrozumiały dla ludzi i agentów.",
    "gs_sub": "Nie wymieniasz wszystkiego naraz. Amethis łączy dane, które już masz, buduje to, czego brakuje, i zamienia Twoją organizację w najlepsze możliwe miejsce pracy dla agentów AI – a każdy krok daje wartość sam w sobie.",
    "gs1_h": "Jedno złote źródło", "gs1_p": "Amethis łączy Twoje bazy i źródła danych – niezależnie od ich liczby – w jedno złote źródło (golden source): jedną, spójną wersję prawdy. Systemy, które trzymają dane, działają dalej.",
    "gs2_h": "Warstwa semantyczna", "gs2_p": "Na złotym źródle leży warstwa semantyczna, która opisuje Twoją organizację: co znaczą poszczególne pojęcia, jak się ze sobą wiążą i kto co może zobaczyć. Rozumieją ją ludzie – i agenci AI.",
    "gs3_h": "Uzupełnij luki", "gs3_p": "Tam, gdzie brakuje danych albo procesów, Amethis je buduje: nowe aplikacje, obiegi spraw i reguły dla pracy, która dziś żyje w mailach i arkuszach. Istniejące aplikacje przenosisz wtedy, gdy ma to sens.",
    "gs4_h": "Pozwól agentom pracować", "gs4_p": "Kompletne dane, jasne znaczenie i te same reguły co dla ludzi czynią złote źródło idealnym miejscem pracy agentów AI. W miarę wzrostu zaufania przejmują coraz więcej – a decyzje zostają przy ludziach.",

    "tr_label": "Zaufanie i suwerenność",
    "tr_h2": "Zbudowany dla organizacji, które nie mogą stracić kontroli.",
    "tr_sub": "Administracja publiczna, infrastruktura krytyczna, obronność, finanse, ochrona zdrowia – wszędzie tam, gdzie dane są wrażliwe, a reguły surowe. Wyprodukowano w Unii Europejskiej.",
    "t1_h": "Twoja infrastruktura", "t1_p": "Działa na Twoich serwerach, na Twoim koncie Azure, Google Cloud lub AWS albo w sieciach odciętych od internetu – razem z modelem AI. Nigdy jako współdzielona usługa chmurowa.",
    "t2_h": "Regulacje w działaniu", "t2_p": "Rejestry, obiegi i zapisy wymagane przez RODO, NIS2 i AI Act są częścią działającego systemu – nie osobnym projektem.",
    "t3_h": "Bezpieczeństwo dla środowisk niejawnych i odizolowanych", "t3_p": "Etykiety klasyfikacji na każdym rekordzie, uprawnienia liczone per wiersz, dowody zbierane pod akredytację. Akredytację nadaje właściwy organ dla konkretnej instalacji.",
    "t4_h": "Bez uzależnienia od dostawcy", "t4_p": "Dane i ich metadane zarządcze zostają w otwartych, standardowych formatach – możesz je zabrać w każdej chwili, także od nas.",

    "pr_label": "Dowód",
    "pr_h2": "Krytyczny system sektora publicznego – trzy moduły w dwa tygodnie.",
    "pr_h3": "Aplikacja bieżącej świadomości sytuacyjnej dla instytucji publicznej UE.",
    "pr_p": "Zbudowany z 300 stron wymagań funkcjonalnych i niefunkcjonalnych, takich, jakie pisze się dla zespołów deweloperskich. Zero programowania pod projekt – ta sama platforma, która działa w każdym innym wdrożeniu.",
    "pr_c1": "Mapa bieżącej sytuacji na żywo", "pr_c2": "Zgłaszanie zdarzeń z obiegiem akceptacji", "pr_c3": "Zarządzanie użytkownikami i dostępami z kolejką akceptacji",
    "pr_n1": "tygodnie do działającego, odebranego systemu", "pr_n2": "dostarczone moduły", "pr_n3": "pulpitów i widoków", "pr_n4": "stron wymagań biznesowych", "pr_n5": "linii kodu na zamówienie",
    "f1_h": "Nawet 30× szybciej", "f1_p": "Aplikacje, procesy i integracje dostarczane nawet 30× szybciej niż przy programowaniu – i zmieniane równie szybko.",
    "f2_h": "Skrajna wydajność na skromnym sprzęcie", "f2_p": "Ponad milion rekordów przetworzonych w kilka minut na jednym serwerze, każdy z pełnym śladem pochodzenia. Na start cała platforma mieści się na jednej maszynie.",
    "f3_h": "Rośnie razem z Tobą", "f3_p": "Zbudowany tak, by skalować się na kolejne serwery wraz ze wzrostem danych i użytkowników – od jednego działu do całej organizacji.",

    "pn_label": "Dla software house'ów i integratorów",
    "pn_h2": "Software house'y: wasz następny model biznesowy.",
    "pn_sub": "AI sprawia, że kod jest tani w pisaniu – i zostawia organizacje z silosami, którymi trudno zarządzać i w których agenci nie mają bezpiecznego miejsca pracy. Z Amethis Twój zespół dostarcza w zamian spójne, zgodne z regulacjami systemy: większe programy mniejszym zespołem, a wdrożenie, utrzymanie i przychód powtarzalny zostają po Twojej stronie.",
    "pn_c1": "Wdrożenie i utrzymanie zostają po waszej stronie.", "pn_c2": "Depozyt kodu źródłowego chroni was i waszego klienta.", "pn_c3": "Bezpieczny start: jeden proces, pilotaż albo praca obok istniejącego systemu.",
    "pn_cta": "Zostań partnerem",

    "cl_label": "Europejska suwerenność cyfrowa",
    "cl_h2": "Organizacja oparta na danych i procesach – z ludźmi wspieranymi przez agentów AI.",
    "cl_sub": "Opowiedz nam o jednym procesie, który chcesz zmienić. W 45-minutowej sesji roboczej rozpisujemy go razem i pokazujemy, jak wygląda w Amethis – z Twoimi ludźmi przy sterach. Wychodzisz z konkretnym zarysem pilota.",
    "cl_cta": "Pokaż nam jeden proces",
    "ft_eu": "Wyprodukowano w Unii Europejskiej",
    "ft_privacy": "Ta strona nie ustawia ciasteczek i niczego nie pobiera od stron trzecich.",
    "nav_home": "Start",
    "oa_sub": "Dla administracji publicznej, służb i infrastruktury krytycznej: zdarzenia, alerty i obiekty w ruchu na jednej mapie na żywo – według tych samych reguł, akceptacji i śladu audytu co wszystko inne w Amethis.",
    "oa_h2": "Bieżący obraz operacyjny – powiązany z decyzjami, które za nim stoją.",
    "oa_label": "Zastosowania · obraz operacyjny",
    "fit_label": "Dopasowane do każdego stanowiska",
    "cl_alt": "Software house albo integrator? Zobacz program partnerski →",
    "ph3_p": "W miarę wzrostu zaufania agenci przejmują coraz więcej – a decyzje zostają przy ludziach.",
    "ph3_h": "Więcej procesów, więcej agentów",
    "ph2_p": "Podłącz systemy, które trzymają Twoje dane. Działają dalej; Amethis daje jeden wiarygodny obraz i przejmuje pracę kawałek po kawałku.",
    "ph2_h": "Pilot na Twojej infrastrukturze",
    "ph1_p": "Wybierz proces, który dziś żyje w mailach i arkuszach. W tygodnie działa w Amethis – z Twoimi danymi, regułami i akceptacjami.",
    "ph1_h": "Jeden proces",
    "pa_sub": "Nie wymieniasz niczego naraz. Każdy krok daje wartość sam w sobie – i każdy czyni Twoją organizację lepszym miejscem pracy dla ludzi i agentów AI.",
    "pa_h2": "Zacznij od jednego procesu. Zostaw wszystko, co masz.",
    "pa_label": "Jak zacząć",
    "one_more": "Zobacz platformę w szczegółach →",
    "r4_p": "Rejestry, obiegi i dowody, których potrzebują Twoje programy RODO, NIS2 i AI Act – prowadzone przez ten sam system, który wykonuje pracę.",
    "r4_h": "Rejestry i dowody dla regulatorów",
    "r3_p": "Twoje obecne systemy działają dalej. Amethis łączy je na bieżąco i przejmuje pracę kawałek po kawałku – bez dnia przełączenia.",
    "r3_h": "Integracja z tym, co masz",
    "r2_p": "Jeden wiarygodny zbiór danych ze wszystkich źródeł, ze wspólnymi definicjami biznesowymi – i każdy wynik z możliwością prześledzenia, skąd pochodzi.",
    "r2_h": "Dane, którym można ufać",
    "r1_p": "Ekrany, formularze, kolejki zadań, akceptacje i zastępstwa – zbudowane z Twoich wymagań, zmieniane w godziny.",
    "r1_h": "Aplikacje i procesy",
    "oc_sub": "Dziś zmiana sposobu pracy dotyka kilku narzędzi, każde z własnym dostawcą, danymi i projektem. W Amethis to jedno środowisko: zmianę robisz raz i jest spójna wszędzie – na ekranach, w danych, w regułach i w śladzie audytu.",
    "oc_h2": "Aplikacje, procesy, dane, integracje, zgodność i agenci AI – jeden system, jedna zmiana.",
    "ap_tag": "Scenariusz ilustracyjny",
    "pm_sub": "Nawet 30× szybciej – zmierzone przy tej budowie, gdzie prace nad backendem, danymi i integracją, które zwykle zajmują miesiące programowania, zajęły dni. Analiza i odbiór zostają po stronie Twoich ekspertów, więc zysk w całym projekcie zależy od dziedziny.",
    "pm_h2": "Zmierzone, nie obiecane.",
    "pm_label": "Szybkość i skala",
    "pr_status": "Odtworzony z własnych wymagań instytucji i przyjęty przez biznes jako działający poprawnie – zbudowany tak, jak każde wdrożenie Amethis, o rząd wielkości szybciej niż przy klasycznym wytwarzaniu.",
    "hero_proofline": "Sprawdzone: krytyczny system sektora publicznego UE – 3 moduły z 300 stron wymagań w 2 tygodnie, 0 linii kodu na zamówienie →",
    "hero_tag": "Twój model operacyjny – uruchomiony.",
    "ft_nav_label": "Serwis",
    "nav_opaw": "Obraz operacyjny",
    "nav_governance": "Zarządzanie danymi",
    "nav_proof": "Dowód",
    "nav_platform": "Platforma",
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


# Per-page content: titles, descriptions and the links or notes that differ between pages.
def _pages(lp: str, t: dict) -> dict:
    more = lambda href, text: f'<a class="more reveal" href="{lp}{href}">{text}</a>'
    return {
        "home": {"proof_more": more("proof/", t["proof_more"]), "trust_more": more("trust/", t["trust_more"])},
        "platform": {"meta_title": t["platform_title"], "meta_desc": t["platform_desc"],
                     "page_label": t["platform_label"], "page_h1": t["platform_h1"], "page_lede": t["platform_lede"],
                     "six_more": more("solutions/operational-awareness/", t["six_more"])},
        "proof": {"meta_title": t["proof_title"], "meta_desc": t["proof_desc"], "proof_more": ""},
        "trust": {"meta_title": t["trust_title"], "meta_desc": t["trust_desc"],
                  "trust_more": f'<p class="note reveal">{t["assurance"]}</p>'},
        "governance": {"meta_title": t["gov_title"], "meta_desc": t["gov_desc"]},
        "opaw": {"meta_title": t["opaw_title"], "meta_desc": t["opaw_desc"]},
        "pricing": {"meta_title": t["pricing_title"], "meta_desc": t["pricing_desc"]},
        "partners": {"meta_title": t["partners_title"], "meta_desc": t["partners_desc"]},
    }


PAGE_EN = _pages("/", {
    "proof_more": "See the full case and how speed was measured →",
    "trust_more": "Security, assurance and data portability in detail →",
    "six_more": "Operational awareness: a live operational picture →",
    "platform_title": "Platform – your operating model, running | Amethis",
    "platform_desc": "How Amethis runs your operating model: applications built from screens and widgets, one trusted set of data, integrations and workspaces for every role.",
    "platform_label": "Platform · Executable Operating Model", "platform_h1": "Your operating model, running.",
    "platform_lede": "We call it an Executable Operating Model: the way your organisation works – its processes, data, rules, screens and obligations – is defined by configuration and runs as the system itself, instead of being documented next to it. Change the model and the organisation's system changes with it. For analysts: Amethis is a governed operations platform that brings business orchestration and automation, application building, data integration, governance and AI-agent execution into one customer-controlled environment.",
    "proof_title": "Proof – a public-sector system in two weeks | Amethis",
    "proof_desc": "A mission-critical EU public-sector system rebuilt from 300 pages of requirements in two weeks, with zero lines of custom code – and how the speed was measured.",
    "trust_title": "Trust and sovereignty | Amethis",
    "trust_desc": "Where Amethis runs, how people and AI agents are kept under control, how classified environments are handled and how your data stays portable.",
    "assurance": "Assurance: a software bill of materials for every release, security scans on every change and evidence collected for Common Criteria (EAL4+) evaluation. Designed for environments up to EU SECRET – accreditation is granted per installation by the competent security authority.",
    "gov_title": "Data governance and audit | Amethis",
    "gov_desc": "Governance built into every operation: classification computed from inputs, full lineage, a data catalogue, DAMA data quality and regulatory registers.",
    "opaw_title": "Operational awareness – a live operational picture | Amethis",
    "opaw_desc": "A live operational picture for public administration, emergency services and critical infrastructure – events, alerts and moving objects linked to decisions.",
    "pricing_title": "Pricing | Amethis",
    "pricing_desc": "A platform subscription plus usage measured in real business operations – not in servers, compute units, environments or the number of things you build.",
    "partners_title": "Partners – software houses and integrators | Amethis",
    "partners_desc": "For software houses and integrators: deliver larger programmes with a smaller team on Amethis, and keep the delivery, support and recurring revenue.",
})

PAGE_PL = _pages("/pl/", {
    "proof_more": "Zobacz pełny opis i sposób pomiaru szybkości →",
    "trust_more": "Bezpieczeństwo, zapewnienie i przenośność danych w szczegółach →",
    "six_more": "Obraz operacyjny: bieżący obraz sytuacji na mapie →",
    "platform_title": "Platforma – Twój model operacyjny, uruchomiony | Amethis",
    "platform_desc": "Jak Amethis uruchamia model operacyjny: aplikacje z ekranów i widżetów, jeden wiarygodny zbiór danych, integracje i przestrzenie pracy dla każdej roli.",
    "platform_label": "Platforma · Executable Operating Model", "platform_h1": "Twój model operacyjny – uruchomiony.",
    "platform_lede": "Nazywamy to Executable Operating Model – wykonywalnym modelem operacyjnym: sposób działania Twojej organizacji – procesy, dane, reguły, ekrany i obowiązki – jest zdefiniowany konfiguracją i działa jako sam system, zamiast być opisanym obok niego. Zmieniasz model – zmienia się system organizacji. Dla analityków: Amethis to platforma operacyjna pod kontrolą, która łączy orkiestrację i automatyzację procesów biznesowych, budowę aplikacji, integrację danych, zarządzanie danymi i działanie agentów AI w jednym środowisku kontrolowanym przez klienta.",
    "proof_title": "Dowód – system sektora publicznego w dwa tygodnie | Amethis",
    "proof_desc": "Krytyczny system sektora publicznego UE odtworzony z 300 stron wymagań w dwa tygodnie, bez linii kodu na zamówienie – i jak zmierzyliśmy szybkość.",
    "trust_title": "Zaufanie i suwerenność | Amethis",
    "trust_desc": "Gdzie działa Amethis, jak ludzie i agenci AI pozostają pod kontrolą, jak obsługujemy środowiska niejawne i jak Twoje dane pozostają przenośne.",
    "assurance": "Zapewnienie bezpieczeństwa: wykaz składników oprogramowania (SBOM) dla każdego wydania, skany bezpieczeństwa przy każdej zmianie i dowody zbierane pod ocenę Common Criteria (EAL4+). Projektowany dla środowisk do EU SECRET włącznie – akredytację nadaje właściwy organ bezpieczeństwa dla konkretnej instalacji.",
    "gov_title": "Zarządzanie danymi i audyt | Amethis",
    "gov_desc": "Zarządzanie danymi wbudowane w każdą operację: klasyfikacja liczona z wejść, pełny lineage, katalog danych, jakość wg DAMA i rejestry regulacyjne.",
    "opaw_title": "Obraz operacyjny na żywo | Amethis",
    "opaw_desc": "Bieżący obraz operacyjny dla administracji, służb i infrastruktury krytycznej – zdarzenia, alerty i obiekty w ruchu powiązane z decyzjami.",
    "pricing_title": "Opłaty | Amethis",
    "pricing_desc": "Subskrypcja platformy i użycie mierzone w realnych operacjach biznesowych – nie w serwerach, jednostkach mocy, środowiskach ani liczbie rzeczy, które budujesz.",
    "partners_title": "Partnerzy – software house'y i integratorzy | Amethis",
    "partners_desc": "Dla software house'ów i integratorów: większe programy mniejszym zespołem na Amethis, a wdrożenie, utrzymanie i przychód powtarzalny zostają po Twojej stronie.",
})


# Every page: (path under the language prefix, section blocks in order, promote the first h2 to the page h1).
PAGES = {
    "home": ("", ["hero", "proof", "how", "control", "outcomes", "trust", "start", "closing"], False),
    "platform": ("platform/", ["page-head", "six", "fit", "datapath", "closing"], False),
    "proof": ("proof/", ["proof", "proof-metrics", "closing"], True),
    "trust": ("trust/", ["trust", "control", "closing"], True),
    "governance": ("governance/", ["governance", "closing"], True),
    "opaw": ("solutions/operational-awareness/", ["opaw", "closing"], True),
    "pricing": ("pricing/", ["pricing", "closing"], True),
    "partners": ("partners/", ["partners"], True),
}


def structured_data(content: dict, page: str) -> str:
    """Schema.org graph: the organisation and product on the home page, a WebPage elsewhere."""
    org = {"@type": "Organization", "@id": f"{SITE}/#org", "name": "Amethis", "url": f"{SITE}/",
           "logo": f"{SITE}/assets/apple-touch-icon.png", "email": "info@amethis.io",
           "legalName": f"{COMPANY['trade_name']} {COMPANY['owner']}", "vatID": COMPANY["vat_eu"], "areaServed": "EU"}
    site = {"@type": "WebSite", "@id": f"{SITE}/#website", "name": "Amethis", "url": f"{SITE}/",
            "inLanguage": ["en", "pl"], "publisher": {"@id": f"{SITE}/#org"}}
    if page == "home":
        nodes = [org, site, {"@type": "SoftwareApplication", "name": "Amethis", "url": content["canonical"],
                             "applicationCategory": "BusinessApplication",
                             "operatingSystem": "On-premises, Microsoft Azure, Google Cloud, AWS",
                             "description": content["meta_desc"], "inLanguage": content["lang"],
                             "publisher": {"@id": f"{SITE}/#org"}}]
    else:
        nodes = [{"@type": "WebPage", "url": content["canonical"], "name": content["meta_title"],
                  "description": content["meta_desc"], "inLanguage": content["lang"],
                  "isPartOf": {"@id": f"{SITE}/#website"}}]
    graph = {"@context": "https://schema.org", "@graph": nodes}
    return json.dumps(graph, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def write_sitemap(dist: Path) -> None:
    today = date.today().isoformat()
    urls = []
    for slug, _, _ in PAGES.values():
        en, pl = f"{SITE}/{slug}", f"{SITE}/pl/{slug}"
        alt = (f'<xhtml:link rel="alternate" hreflang="en" href="{en}"/>'
               f'<xhtml:link rel="alternate" hreflang="pl" href="{pl}"/>'
               f'<xhtml:link rel="alternate" hreflang="x-default" href="{en}"/>')
        urls += [f"  <url><loc>{u}</loc><lastmod>{today}</lastmod>{alt}</url>\n" for u in (en, pl)]
    (dist / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        f"{''.join(urls)}</urlset>\n", encoding="utf-8")


def page_html(blocks: list, promote_h1: bool) -> str:
    body = "\n".join((BLOCKS / f"{b}.html").read_text(encoding="utf-8") for b in blocks)
    # {{> name}} pulls a shared block into another one (e.g. the operational map card).
    body = re.sub(r"\{\{> ([\w-]+)\}\}", lambda m: (BLOCKS / f"{m.group(1)}.html").read_text(encoding="utf-8"), body)
    if promote_h1:
        # A sub-page without a page head opens with its first section heading as the single h1.
        body = re.sub(r"<h2([^>]*)>(.*?)</h2>", r"<h1\1>\2</h1>", body, count=1, flags=re.S)
    return LAYOUT.replace("{{body}}", body)


def render(html: str, content: dict, where: str) -> str:
    missing = sorted(set(re.findall(r"\{\{(\w+)\}\}", html)) - content.keys())
    if missing:
        sys.exit(f"{where}: keys without content: {missing}")
    return re.sub(r"\{\{(\w+)\}\}", lambda m: content[m.group(1)], html)


def main() -> None:
    dist = ROOT / "dist"
    # Content hash in the stylesheet URL, so a browser never pairs new HTML with a cached old stylesheet.
    css_v = hashlib.sha256((dist / "assets" / "styles.css").read_bytes()).hexdigest()[:10]
    for lang, base, pages in (("en", EN, PAGE_EN), ("pl", PL, PAGE_PL)):
        prefix = "/" if lang == "en" else "/pl/"
        for page, (slug, blocks, promote) in PAGES.items():
            content = {**base, **pages[page]}
            content.update(lp=prefix, css_v=css_v, imprint=imprint(lang),
                           canonical=f"{SITE}{prefix}{slug}", url_en=f"{SITE}/{slug}", url_pl=f"{SITE}/pl/{slug}",
                           href_en=f"/{slug}", href_pl=f"/pl/{slug}")
            content["jsonld"] = structured_data(content, page)
            out = dist / prefix.strip("/") / slug / "index.html"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(render(page_html(blocks, promote), content, f"{lang}/{slug or 'home'}"), encoding="utf-8")
    write_sitemap(dist)
    print(f"built {2 * len(PAGES)} pages")


if __name__ == "__main__":
    main()
