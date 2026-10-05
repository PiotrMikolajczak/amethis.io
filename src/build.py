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
    "meta_title": "Amethis — the Executable Operating Model",
    "meta_desc": "Not SaaS. Your operating model, executable. Amethis runs your domain, processes, policies and interfaces as one governed system — where people, AI agents and applications work under the same rules, inside your own perimeter.",
    "skip": "Skip to content", "lang_label": "Language",
    "nav_model": "Operating model", "nav_platform": "Platform", "nav_workspace": "Agents & people",
    "nav_trust": "Trust", "nav_proof": "Proof", "nav_partners": "Partners", "nav_cta": "Contact",
    "mail_subject": "Amethis%20%E2%80%94%20introduction", "mail_subject_partner": "Amethis%20%E2%80%94%20partnership",

    "hero_eyebrow": "Executable Operating Model",
    "hero_h1": "Not SaaS. Your operating model,", "hero_h1_grad": "executable.",
    "hero_lede": "Your consultants drew a target operating model. <b>Amethis runs it.</b> Domain, processes, policies, interfaces and obligations are the running system — versioned, validated, access-governed and audited. People, AI agents and applications work inside it under one set of rules, with a human always in control.",
    "hero_cta1": "Talk to us", "hero_cta2": "What is an EOM?",
    "chip1": "Your perimeter, LLM included", "chip3": "Human-in-the-loop", "chip5": "Made in the EU",
    "scene_alt": "People, AI agents and applications connected only through the Amethis governance core; every flow passes a policy gate, and a direct agent-to-application path is refused.",
    "zone_apps": "APPLICATIONS", "zone_people": "PEOPLE", "zone_agents": "AI AGENTS",
    "denied": "direct path · denied", "ring_label": "POLICY · AUDIT",
    "core_sub1": "EXECUTABLE", "core_sub2": "OPERATING MODEL",
    "n_app1": "Situational picture", "n_app1_s": "live map", "n_app2": "Event register", "n_app2_s": "workflow",
    "n_h1": "Analyst", "n_h1_s": "composes views", "n_h2": "Approver", "n_h2_s": "four-eyes",
    "n_a1": "DQ agent", "n_a1_s": "proposes", "n_a2": "RAG assistant", "n_a2_s": "reads, cites",
    "toast1": "<b>rag-assistant</b> read Events · ABAC allow · 2 fields masked",
    "toast2": "<b>dq-agent</b> proposes 14 corrections · awaiting human approval",
    "toast3": "<b>approver</b> accepted · audit record sealed",

    "s1_v": "up to 30×", "s1_l": "faster build, test and delivery of UI, data pipelines and integrations",
    "s2_v": "1.2M / 8 min", "s2_l": "records processed on a single node, with provenance for every record",
    "s3_l": "lines of bespoke application code in our reference build",
    "s4_l": "written standards — and 1.6M lines of documentation your teams can take over",

    "how_label": "Executable Operating Model",
    "how_h2": "The model is the system.",
    "how_sub": "Domain, processes, policies, interfaces and obligations are not settings layered onto an application that would exist without them. <b>They are the running system</b> — declared, versioned and validated, then executed by the same platform binaries in every deployment. A new application is a new model, not a new codebase.",
    "k_domain": "Domain", "k_process": "Processes", "k_policy": "Policies", "k_iface": "Interfaces", "k_oblig": "Obligations",
    "how_engine_h": "Amethis runtime", "how_engine_p": "executes the model — and governs, audits and measures every action it takes",
    "how_c2": "processes", "how_c5": "governed AI",
    "how_o1": "Applications & dashboards", "how_o1_s": "maps · registers · workflows · drag-and-drop",
    "how_o2": "Pipelines & integrations", "how_o2_s": "near-real-time · stream · batch · video",
    "how_o3": "Machine interfaces",
    "how_o4": "Governed AI agents", "how_o4_s": "same principal, same rules as people",
    "f1_h": "Speed at every level", "f1_p": "Build, test and deploy UI, pipelines and integrations up to <b>30× faster</b> — a scope change is a model change, so late findings cost hours, not re-planning.",
    "f2_h": "Extreme efficiency on modest hardware", "f2_p": "<b>1.2M records in 8 minutes</b> on one node, four parallel streams, provenance for every record. The whole platform fits on a single workstation.",
    "f3_h": "Built for the business, not programmers", "f3_p": "Works directly with <b>analysts, architects and data scientists</b>. Same vocabulary, requirements 1:1, a rapid delivery loop.",

    "ml_label": "The missing layer",
    "ml_h2": "Not another app builder. Not another autonomous agent. The working system in between.",
    "ml_sub": "The market offers either tools to assemble applications or agents that act on their own. Regulated organisations need the middle: <b>full AI assistance across the daily workflow, with humans always in control.</b>",
    "ml_l_k": "First layer", "ml_l_h": "Low-code app builders", "ml_l_p": "Assemble screens fast — while logic, data and governance still live in code somebody has to maintain.",
    "ml_m_h": "Your operating model, running", "ml_m_p": "Runs the organisation's processes through a governed data fabric, UI and machine interfaces — augmented by AI, with approval gates, AI-content labelling, an instant kill-switch and tamper-evident audit.",
    "ml_r_k": "Last layer", "ml_r_h": "Autonomous agent runtimes", "ml_r_p": "Act on their own — with accountability, access control and audit bolted on afterwards, if at all.",

    "ws_label": "People · agents · applications",
    "ws_h2": "One controlled environment. One set of rules for everyone who acts.",
    "ws_sub": "Agents get no side door. They work in the same fabric as your people and your applications — <b>same identity model, same policy decision, same audit trail</b> — on write, read, export, RAG and agent action alike. An agent proposes; a human approves wherever the process says so.",
    "ws_p_h": "People", "ws_p_p": "Analysts, operators and approvers work in role-aware dashboards they compose themselves — and stay the final authority on every gated decision.",
    "ws_a_h": "AI agents", "ws_a_p": "First-class governed principals. They read, propose and act through the platform's own operations, never around them — and the LLM runs on your infrastructure.",
    "ws_s_h": "Applications", "ws_s_p": "Maps, registers, workflows and machine interfaces share one context and one SDK — so what one app learns, the next one can use, under the same policy.",
    "ws_g_h": "Governance as fabric", "ws_g_p": "ABAC + ReBAC, data classification, four-eyes approval and provenance are one architecture — not a separate overlay that watches but cannot enforce.",
    "log_title": "decision-log", "log_note": "Illustrative excerpt of the platform's decision log.",
    "log1": "READ Events · interface view", "log1_p": "2 fields masked",
    "log2": "PROPOSE update · 14 records", "log2_p": "awaiting human approval",
    "log3_who": "human · approver", "log3": "APPROVE proposal P-3381", "log3_p": "four-eyes ok",
    "log4": "change pushed to 23 open sessions", "log4_p": "audited",
    "log5": "EXPORT dataset above its clearance", "log5_p": "deny · classification",
    "log6": "record A-20417 sealed",

    "tr_label": "Trust by design",
    "tr_h2": "Built for highly regulated organisations.",
    "tr_sub": "Security and AI without compromise — compliance is the foundation, not a bolt-on.",
    "t1_h": "Your perimeter only", "t1_p": "The full stack runs on your infrastructure or in your own cloud account — <b>including the LLM</b>. Never a multi-tenant SaaS.",
    "t2_h": "Governance as fabric", "t2_p": "ABAC + ReBAC, audit and human-in-the-loop in one architecture — the same decision on write, read, export, RAG and agents.",
    "t3_h": "Regulation, built in", "t3_p": "GDPR, NIS2, AI Act, Data Act and DAMA — the registries, processes and metadata they require are part of the platform, not separate custom apps.",
    "t4_h": "Classification-native", "t4_p": "Designed for environments up to EU SECRET: classification is a core primitive, not an overlay. Evidence is collected against Common Criteria EAL4+ families.",
    "t5_h": "Sovereign-friendly AI", "t5_p": "Built with models that carry no data-sharing obligation towards foreign agencies; the deployed LLM runs on your own infrastructure.",
    "t6_h": "Open data, no lock-in", "t6_p": "Built on open-source technologies. Your data, lineage and audit stay in open formats — you can take them out at any time, including away from us.",
    "t7_h": "Continuity you can defend", "t7_p": "Source-code escrow and documentation built to be taken over — answers procurement asks for before it asks.",
    "t8_h": "Migration, not big bang", "t8_p": "Strangler fig: legacy systems keep running unchanged while new applications grow around them on governed data.",

    "pr_label": "Proof",
    "pr_h2": "A flagship public-sector system — its three most complex modules in two weeks.",
    "pr_h3": "A mission-critical situational-awareness application, rebuilt from a standing start as a working system.",
    "pr_p": "Same platform binaries as every other deployment. No project-specific application code, no bespoke back end — just the model.",
    "pr_c1": "Live map with near-real-time aircraft positions",
    "pr_c2": "Event reporting with templates and validation history",
    "pr_c3": "Statistics, analytics and an organisational-unit hierarchy",
    "pr_c4": "User, role and access requests with an approval queue",
    "pr_n1": "weeks from start to demo", "pr_n2": "modules delivered", "pr_n3": "dashboards and views",
    "pr_n4": "declarative model files", "pr_n5": "lines of bespoke app code",

    "pa_label": "For delivery partners",
    "pa_h2": "A different business, on the same client base.",
    "pa_sub": "You sell capacity in a market where price per hour only goes one way. Amethis changes what an hour produces — and moves the work from developers to <b>analysts, architects and data people</b>.",
    "pa_quote": "Fixed price stops being a gamble — scope changes are model changes, so late findings cost hours, not re-planning.",
    "pa_quote_s": "What an Executable Operating Model does to a delivery organisation",
    "pa_c1_b": "Deployment and support stay yours.", "pa_c1": "First and second line sit with you; recurring revenue we do not take back.",
    "pa_c2_b": "Escrow works both ways.", "pa_c2": "The client keeps the platform, and you keep the right to maintain what you sold.",
    "pa_c3_b": "Documentation you can take over.", "pa_c3": "63 written standards your people learn from — and your agents work from.",
    "pa_c4_b": "You enter where it is safest.", "pa_c4": "The data layer, a contained PoC, or running in shadow next to the existing system.",
    "pa_cta": "Become a partner",

    "cl_label": "European digital sovereignty",
    "cl_h2": "From policy into product.",
    "cl_sub": "The first working platform where the operating model itself is the system — and every action is constrained, lawful and auditable by design, in an architecture built for NATO-grade accreditation.",
    "cl_cta": "Start a conversation",
    "ft_eu": "Made in the European Union",
    "ft_privacy": "This site sets no cookies and loads nothing from third parties.",
}

PL = dict(EN)
PL.update({
    "lang": "pl", "og_locale": "pl_PL", "base": "../", "home": "/pl/", "canonical": "https://amethis.io/pl/",
    "cur_en": "false", "cur_pl": "true",
    "meta_title": "Amethis — Executable Operating Model",
    "meta_desc": "To nie SaaS. Twój model operacyjny — wykonywalny. Amethis uruchamia domenę, procesy, polityki i interfejsy jako jeden rządzony system, w którym ludzie, agenci AI i aplikacje działają według tych samych reguł, wewnątrz Twojego perymetru.",
    "skip": "Przejdź do treści", "lang_label": "Język",
    "nav_model": "Model operacyjny", "nav_platform": "Platforma", "nav_workspace": "Agenci i ludzie",
    "nav_trust": "Zaufanie", "nav_proof": "Dowód", "nav_partners": "Partnerzy", "nav_cta": "Kontakt",
    "mail_subject": "Amethis%20%E2%80%94%20rozmowa", "mail_subject_partner": "Amethis%20%E2%80%94%20partnerstwo",

    "hero_h1": "To nie SaaS. Twój model operacyjny —", "hero_h1_grad": "wykonywalny.",
    "hero_lede": "Konsultanci narysowali wam docelowy model operacyjny. <b>Amethis go uruchamia.</b> Domena, procesy, polityki, interfejsy i obowiązki są działającym systemem — wersjonowanym, walidowanym, objętym kontrolą dostępu i audytem. Ludzie, agenci AI i aplikacje pracują w nim według jednych reguł, a człowiek zawsze trzyma stery.",
    "hero_cta1": "Porozmawiajmy", "hero_cta2": "Czym jest EOM?",
    "chip1": "Twój perymetr, z LLM", "chip3": "Człowiek w pętli", "chip5": "Made in the EU",
    "scene_alt": "Ludzie, agenci AI i aplikacje połączeni wyłącznie przez rdzeń governance Amethis; każdy przepływ przechodzi przez bramkę polityki, a bezpośrednia ścieżka agent–aplikacja jest odrzucona.",
    "zone_apps": "APLIKACJE", "zone_people": "LUDZIE", "zone_agents": "AGENCI AI",
    "denied": "ścieżka bezpośrednia · odmowa", "ring_label": "POLITYKA · AUDYT",
    "core_sub1": "EXECUTABLE", "core_sub2": "OPERATING MODEL",
    "n_app1": "Obraz sytuacyjny", "n_app1_s": "mapa live", "n_app2": "Rejestr zdarzeń", "n_app2_s": "workflow",
    "n_h1": "Analityk", "n_h1_s": "składa widoki", "n_h2": "Zatwierdzający", "n_h2_s": "czworo oczu",
    "n_a1": "Agent DQ", "n_a1_s": "proponuje", "n_a2": "Asystent RAG", "n_a2_s": "czyta, cytuje",
    "toast1": "<b>rag-assistant</b> odczyt Events · ABAC allow · 2 pola zamaskowane",
    "toast2": "<b>dq-agent</b> proponuje 14 poprawek · czeka na akceptację człowieka",
    "toast3": "<b>zatwierdzający</b> zaakceptował · wpis audytu zapieczętowany",

    "s1_v": "do 30×", "s1_l": "szybciej: budowa, testy i wdrożenie UI, potoków danych i integracji",
    "s2_v": "1,2 mln / 8 min", "s2_l": "rekordów na jednym węźle, z pochodzeniem zapisanym dla każdego",
    "s3_l": "linii dedykowanego kodu aplikacji w naszym wdrożeniu referencyjnym",
    "s4_l": "spisane standardy — i 1,6 mln linii dokumentacji do przejęcia przez wasze zespoły",

    "how_h2": "Model jest systemem.",
    "how_sub": "Domena, procesy, polityki, interfejsy i obowiązki nie są ustawieniami nałożonymi na aplikację, która istniałaby bez nich. <b>Są działającym systemem</b> — zadeklarowanym, wersjonowanym i walidowanym, a potem wykonywanym przez te same binaria platformy w każdym wdrożeniu. Nowa aplikacja to nowy model, nie nowa baza kodu.",
    "k_domain": "Domena", "k_process": "Procesy", "k_policy": "Polityki", "k_iface": "Interfejsy", "k_oblig": "Obowiązki",
    "how_engine_h": "Runtime Amethis", "how_engine_p": "wykonuje model — i rządzi, audytuje oraz mierzy każde działanie, które podejmuje",
    "how_c2": "procesy", "how_c5": "rządzone AI",
    "how_o1": "Aplikacje i dashboardy", "how_o1_s": "mapy · rejestry · workflow · drag-and-drop",
    "how_o2": "Potoki i integracje", "how_o2_s": "near-real-time · strumienie · batch · wideo",
    "how_o3": "Interfejsy maszynowe",
    "how_o4": "Rządzeni agenci AI", "how_o4_s": "ten sam pryncypał, te same reguły co ludzie",
    "f1_h": "Szybkość na każdym poziomie", "f1_p": "Budowa, testy i wdrożenie UI, potoków i integracji <b>do 30× szybciej</b> — zmiana zakresu to zmiana modelu, więc późne odkrycia kosztują godziny, a nie przeplanowanie.",
    "f2_h": "Skrajna wydajność na skromnym sprzęcie", "f2_p": "<b>1,2 mln rekordów w 8 minut</b> na jednym węźle, cztery równoległe strumienie, pochodzenie dla każdego rekordu. Cała platforma mieści się na jednej stacji roboczej.",
    "f3_h": "Dla biznesu, nie dla programistów", "f3_p": "Praca wprost z <b>analitykami, architektami i data scientistami</b>. Ten sam język, wymagania 1:1, szybka pętla dostarczania.",

    "ml_label": "Brakująca warstwa",
    "ml_h2": "Nie kolejny kreator aplikacji. Nie kolejny autonomiczny agent. Działający system pomiędzy.",
    "ml_sub": "Rynek oferuje albo narzędzia do składania aplikacji, albo agentów działających na własną rękę. Organizacje regulowane potrzebują środka: <b>pełnego wsparcia AI w codziennej pracy, z człowiekiem zawsze przy sterach.</b>",
    "ml_l_k": "Pierwsza warstwa", "ml_l_h": "Kreatory low-code", "ml_l_p": "Szybko składają ekrany — a logika, dane i governance wciąż żyją w kodzie, który ktoś musi utrzymywać.",
    "ml_m_h": "Twój model operacyjny — działający", "ml_m_p": "Realizuje procesy organizacji przez rządzoną warstwę danych, UI i interfejsy maszynowe — wspierany przez AI, z bramkami akceptacji, oznaczaniem treści AI, natychmiastowym wyłącznikiem i audytem odpornym na manipulację.",
    "ml_r_k": "Ostatnia warstwa", "ml_r_h": "Środowiska autonomicznych agentów", "ml_r_p": "Działają same — a rozliczalność, kontrola dostępu i audyt są doklejane później, o ile w ogóle.",

    "ws_label": "Ludzie · agenci · aplikacje",
    "ws_h2": "Jedno kontrolowane środowisko. Jedne reguły dla każdego, kto działa.",
    "ws_sub": "Agenci nie dostają bocznych drzwi. Pracują w tej samej tkance co wasi ludzie i aplikacje — <b>ten sam model tożsamości, ta sama decyzja polityki, ten sam ślad audytowy</b> — przy zapisie, odczycie, eksporcie, RAG i działaniu agenta. Agent proponuje; człowiek zatwierdza wszędzie tam, gdzie wymaga tego proces.",
    "ws_p_h": "Ludzie", "ws_p_p": "Analitycy, operatorzy i zatwierdzający pracują w dashboardach, które sami składają pod swoją rolę — i pozostają ostatecznym autorytetem przy każdej decyzji z bramką.",
    "ws_a_h": "Agenci AI", "ws_a_p": "Pełnoprawni, rządzeni pryncypałowie. Czytają, proponują i działają przez operacje platformy, nigdy obok nich — a LLM działa na waszej infrastrukturze.",
    "ws_s_h": "Aplikacje", "ws_s_p": "Mapy, rejestry, workflow i interfejsy maszynowe dzielą jeden kontekst i jedno SDK — to, czego nauczy się jedna aplikacja, może użyć następna, pod tą samą polityką.",
    "ws_g_h": "Governance jako tkanka", "ws_g_p": "ABAC + ReBAC, klasyfikacja danych, akceptacja czworga oczu i pochodzenie danych to jedna architektura — nie osobna nakładka, która obserwuje, ale nie egzekwuje.",
    "log_note": "Poglądowy fragment dziennika decyzji platformy.",
    "log1": "READ Events · widok interfejsu", "log1_p": "2 pola zamaskowane",
    "log2": "PROPOSE aktualizacja · 14 rekordów", "log2_p": "czeka na akceptację człowieka",
    "log3_who": "człowiek · zatwierdzający", "log3": "APPROVE propozycja P-3381", "log3_p": "czworo oczu ok",
    "log4": "zmiana wypchnięta do 23 otwartych sesji", "log4_p": "audytowane",
    "log5": "EXPORT zbioru powyżej poświadczenia", "log5_p": "odmowa · klasyfikacja",
    "log6": "wpis A-20417 zapieczętowany",

    "tr_label": "Zaufanie u podstaw",
    "tr_h2": "Zbudowany dla organizacji silnie regulowanych.",
    "tr_sub": "Bezpieczeństwo i AI bez kompromisów — zgodność jest fundamentem, a nie doklejką.",
    "t1_h": "Wyłącznie wasz perymetr", "t1_p": "Cały stos działa na waszej infrastrukturze albo na waszym koncie chmurowym — <b>łącznie z modelem językowym</b>. Nigdy wielodzierżawny SaaS.",
    "t2_h": "Governance jako tkanka", "t2_p": "ABAC + ReBAC, audyt i human-in-the-loop w jednej architekturze — ta sama decyzja przy zapisie, odczycie, eksporcie, RAG i agentach.",
    "t3_h": "Regulacje wbudowane", "t3_p": "RODO, NIS2, AI Act, Data Act i DAMA — wymagane rejestry, procesy i metadane są częścią platformy, a nie osobnymi aplikacjami.",
    "t4_h": "Klasyfikacja w rdzeniu", "t4_p": "Projektowany dla środowisk do EU SECRET włącznie: klasyfikacja jest prymitywem rdzenia, nie nakładką. Dowody zbierane w rodzinach Common Criteria EAL4+.",
    "t5_h": "AI przyjazne suwerenności", "t5_p": "Budowany na modelach bez zobowiązań do dzielenia się danymi z obcymi agencjami; wdrożony LLM działa na waszej infrastrukturze.",
    "t6_h": "Otwarte dane, bez lock-inu", "t6_p": "Zbudowany na technologiach open source. Dane, lineage i audyt zostają w otwartych formatach — możecie je zabrać w każdej chwili, także od nas.",
    "t7_h": "Ciągłość do obrony w przetargu", "t7_p": "Depozyt kodu źródłowego i dokumentacja pisana do przejęcia — odpowiedzi, o które zapyta dział zakupów, zanim zapyta.",
    "t8_h": "Migracja, nie big bang", "t8_p": "Strangler fig: stare systemy pracują bez zmian, a nowe aplikacje rosną wokół nich na rządzonych danych.",

    "pr_label": "Dowód",
    "pr_h2": "Sztandarowy system sektora publicznego — trzy najbardziej złożone moduły w dwa tygodnie.",
    "pr_h3": "Krytyczna aplikacja świadomości sytuacyjnej, odtworzona od zera jako działający system.",
    "pr_p": "Te same binaria platformy co w każdym innym wdrożeniu. Zero kodu aplikacyjnego pod ten projekt, zero dedykowanego backendu — tylko model.",
    "pr_c1": "Mapa live z pozycjami statków powietrznych w near-real-time",
    "pr_c2": "Raportowanie zdarzeń z szablonami i historią walidacji",
    "pr_c3": "Statystyki, analityka i hierarchia jednostek organizacyjnych",
    "pr_c4": "Wnioski o użytkowników, role i dostępy z kolejką akceptacji",
    "pr_n1": "tygodnie od startu do dema", "pr_n2": "dostarczone moduły", "pr_n3": "dashboardów i widoków",
    "pr_n4": "deklaratywnych plików modelu", "pr_n5": "linii dedykowanego kodu",

    "pa_label": "Dla partnerów wdrożeniowych",
    "pa_h2": "Inny biznes na tej samej bazie klientów.",
    "pa_sub": "Sprzedajecie moce w rynku, w którym stawka godzinowa idzie tylko w jedną stronę. Amethis zmienia to, ile powstaje w ciągu godziny — i przesuwa pracę z programistów na <b>analityków, architektów i ludzi od danych</b>.",
    "pa_quote": "Fixed price przestaje być hazardem — zmiana zakresu to zmiana modelu, więc późne odkrycia kosztują godziny, a nie przeplanowanie.",
    "pa_quote_s": "Co Executable Operating Model robi z firmą wdrożeniową",
    "pa_c1_b": "Wdrożenie i utrzymanie są wasze.", "pa_c1": "Pierwsza i druga linia po waszej stronie; powtarzalny przychód, którego nie odbieramy.",
    "pa_c2_b": "Depozyt kodu działa w obie strony.", "pa_c2": "Klient zachowuje platformę, a wy prawo do utrzymywania tego, co sprzedaliście.",
    "pa_c3_b": "Dokumentacja do przejęcia.", "pa_c3": "63 spisane standardy, z których uczą się wasi ludzie — i z których pracują wasze agenty.",
    "pa_c4_b": "Wchodzicie tam, gdzie najbezpieczniej.", "pa_c4": "Warstwa danych, ograniczony PoC albo praca w cieniu istniejącego systemu.",
    "pa_cta": "Zostań partnerem",

    "cl_label": "Europejska suwerenność cyfrowa",
    "cl_h2": "Od polityki do produktu.",
    "cl_sub": "Pierwsza działająca platforma, w której sam model operacyjny jest systemem — a każde działanie jest z założenia ograniczone regułą, zgodne z prawem i rozliczalne, w architekturze budowanej pod akredytację klasy NATO.",
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
