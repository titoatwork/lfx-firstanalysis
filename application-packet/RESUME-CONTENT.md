# Resume content — LFX Fall 2026 (Part II primary)

**Status:** Content ready; **personal fields still need your values**  
**Export:** 1 page PDF · filename `Ibteshamul_Haque_Resume_LFX_Fall2026.pdf`  
**Rules:** No CGPA · no confidential COLIDE URL · no friend email · no Spring authorship claims

---

## Header (fill brackets)

**Ibteshamul Haque**  
[City, Country] · [phone] · [display email] · [LinkedIn if desired] · github.com/titoatwork

---

## Summary

Fourth-year CS undergraduate with systems-oriented research experience and measurable open-source prework on RISC-V architectural parameter extraction. Reproduced public Spring LFX evaluation baselines, built a schema-valid UDB draft export path, and ran controlled multi-model ablations with honest negative results. Seeking LFX Fall 2026 Part II; available **≥30 hours/week**.

---

## Education

**B.Tech / B.S. Computer Science** (4th year)  
[University name — e.g. UPES, Dehradun]  
Expected graduation: [Month Year]

---

## Selected technical project

**AI-assisted RISC-V architectural parameter extraction (pre-apply)**  
Public: github.com/titoatwork/lfx-firstanalysis · path `riscv-param-extraction/`  
*(Reproduces and extends public Spring Part I work; credit @ishaan-arora-1 / UDB PRs #1765–#1832)*

- Reproduced the public RISC-V architectural-parameter extraction pipeline against pinned **185**-parameter and live **223**-parameter gold sets, measuring **72.9%** and **64.2%** adjusted recall respectively (classification accuracy ~**88%**; WARL-class recall **50%** on the Part I freeze).
- Built a reviewed-output-to-UDB draft exporter producing **schema-valid** YAML for **83** existing named parameters and **20** candidate parameters (structural validation only; not unsolicited merges).
- Ran a controlled **60**-chunk cross-model experiment: **gpt-4o-mini** **32.2%** adjusted recall versus the public Claude-sonnet-4 baseline **72.9%**, with **3.8%** parameter-name Jaccard; documented high-confidence dual-model “new” names as **review candidates**.
- Evaluated a prompt-only WARL intervention and reported the **negative** result: matched WARL recall decreased from **3/24** to **2/24**.

---

## Research experience

**Research Attaché (on-site) — IoT intrusion detection**  
**Universiti Malaya (FCSIT) · Advisor: Prof. Por Lip Yee** · 2026  
*(On-site June 2026; design/implementation before visit; manuscript prep after)*

- Owned an end-to-end IoT IDS research system: neural detection, custom CUDA C++ inference path, and on-device Generative AI explainability with measured pipeline overhead.
- Built reproducible evaluation: multi-session latency trials, baselines across frameworks, cross-hardware runs, explicit limitations.
- Manuscript in preparation (target FGCS); implementation largely complete.

---

## Skills

| Area | Skills |
|------|--------|
| Languages | Python, C/C++ (CUDA), Shell, SQL |
| ML / AI | PyTorch, evaluation pipelines, controlled LLM stages, structured outputs |
| Systems | Linux, Git, GPU benchmarking, YAML/config-driven experiments |
| Domain (LFX) | RISC-V ISA specs, architectural parameters, WARL/taxonomy literacy, UDB-oriented YAML, run manifests |
| Research habits | Baselines, ablations, honest limitations, mentor-facing writing |

---

## Mentorship availability

- **Term:** LFX Fall 2026 (~mid-Sep to mid-Nov) · **≥30 h/week**  
- **Primary interest:** AI-assisted extraction of architectural parameters (Part II)  
- **Timezone:** India (IST); flexible for US-Pacific meetings  

---

## Your action items before PDF

1. Fill city, phone, email, LinkedIn (optional), university, graduation date.  
2. Confirm GitHub `titoatwork` is what you want public.  
3. One page only; cut skills table detail if needed.  
4. Delete any confidential COLIDE links.  
5. Export PDF and re-upload to LFX profile if numbers change.  
