# Ibteshamul Haque
**Resume draft for LFX Mentorship (Fall 2026)** — 1 page · no CGPA  
**Action:** Copy into Word/Google Docs → set margins ~0.6" → export **PDF** → upload to LFX

Replace bracketed fields with your real details.

---

**Ibteshamul Haque**  
[City, Country] · [phone] · [email] · [LinkedIn URL] · [GitHub: github.com/titoatwork — optional if you want profile public without COLIDE]

---

## Summary

Fourth-year CS undergraduate focused on systems-oriented research: end-to-end ML pipelines, performance-critical C/C++ on GPU, controlled Generative AI integration, and reproducible evaluation under faculty mentorship. Seeking LFX Fall 2026 to contribute reviewable artifacts on RISC-V (ISA specifications / architectural parameters, and/or integrity-oriented architecture work). Available **≥30 hours/week** for the term.

---

## Research experience

**Research Attaché (on-site) — IoT intrusion detection systems**  
**Universiti Malaya (FCSIT) · Advisor: Prof. Por Lip Yee** · 2026  
*(On-site: June 2026; design/implementation before visit; residual work and manuscript prep after return)*

- Designed and implemented an end-to-end **IoT intrusion detection** research system: neural detector (CNN-BiLSTM), **custom CUDA C++** fused inference kernels, and **on-device Generative AI** (air-gapped quantized LLM) for alert explainability with measured async dispatch overhead.
- Built **reproducible evaluation** discipline: multi-session latency trials against production frameworks (PyTorch eager/compile, TensorRT, ONNX Runtime), statistical testing, cross-hardware runs (consumer GPU + institutional cluster GPUs), explicit limitations and numerical fidelity checks.
- Applied **knowledge distillation** and focal loss to close most of the accuracy gap to a strong classical teacher while keeping a deployable neural path; documented streaming throughput and energy-oriented metrics for paper readiness.
- Drove work under advisor feedback toward a **submission-ready manuscript** (target: *Future Generation Computer Systems*; under preparation). Implementation largely complete; current focus manuscript preparation with PhD collaborator on writing.

---

## Technical skills

| Area | Skills |
|------|--------|
| **Languages** | Python, C/C++ (incl. CUDA), Shell/bash, SQL (as used) |
| **ML / AI** | PyTorch, scikit-learn, knowledge distillation, imbalanced learning, Generative AI tooling (transformers, quantization, local LLM pipelines) |
| **Systems / GPU** | Custom CUDA kernels, GPU benchmarking, ONNX / ONNX Runtime, TensorRT (as baseline), Linux |
| **Tools** | Git, Docker, YAML/config-driven experiments, Jupyter |
| **Research habits** | Experimental design, multi-session measurement, technical writing, mentor-facing iteration |
| **Growing for LFX** | ISA specifications / RISC-V material, machine-readable architecture parameters, computer architecture & pipeline reasoning; ramping hardware design / RTL (SystemVerilog) as needed |

---

## Education

**B.S. / B.Tech. Computer Science** (4th year)  
[University — or omit name if you prefer; “Computer Science, undergraduate, expected graduation [Year]” is enough]  
Expected graduation: [Month Year]

---

## Selected project (confidential codebase — no public link)

**COLIDE-class research system — CUDA-optimized CNN-BiLSTM + on-device LLM explainability**  
- Four fused CUDA inference blocks (projection/conv, pool path, FP16 BiLSTM, dense head); framework-fair latency comparison with multi-session statistics.  
- Local TinyLlama-class 4-bit explainability path with microsecond-scale p99 dispatch overhead into the detection pipeline.  
- Security-oriented domain (integrity of monitored IoT traffic under attack). Detailed artifacts available to mentors on request under manuscript constraints.

---

## Mentorship availability

- **Term:** LFX Fall 2026 (~mid-Sep to mid-Nov; ≥**30 hours/week**)  
- **Interests:** AI-assisted extraction of architectural parameters from RISC-V ISA specifications; computer architecture / pipeline integrity (CFI/DFI-style systems work)  
- **Strengths for mentors:** ownership of multi-stage work, reproducible evaluation, Generative AI as pipeline infrastructure, clear technical writing

---

## Notes for you (delete before PDF)

1. Keep **one page**. Cut “Selected project” section if Education + Research already fill the page.  
2. **No CGPA** unless a form forces it.  
3. Do **not** put confidential COLIDE GitHub URL if you can’t share it.  
4. LinkedIn/GitHub: public profile OK; keep private repos private.  
5. Filename: `Ibteshamul_Haque_Resume_LFX_Fall2026.pdf`
