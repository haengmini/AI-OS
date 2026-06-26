# DFXISP-R1 Drive Corpus and Theory-Source Inventory

Date: 2026-06-22 UTC
Task: t_b872b08f
Project: dfxisp
Role: researcher

## Summary

Built an evidence inventory for DFX AI-ISP / 머신 비전 설계 work from three tiers:

1. Agent OS Drive local archive: `/opt/data/agent_os_archive/files`
2. DFXISP local cache: `/opt/data/dfxisp_md`
3. External theory/reference sources retrieved by web search/extract

No final architecture decision is made here. This document separates observed facts from researcher interpretation and records confidence / missing-source notes for the analyst.

## Inputs

Local corpus inspected:

- `/opt/data/agent_os_archive/files`
- `/opt/data/dfxisp_md`
- `/opt/data/projects/dfxisp`

External sources retrieved:

- AMD UG947 DFX tutorial: `https://docs.amd.com/r/en-US/ug947-vivado-partial-reconfiguration-tutorial`
- AMD UG909 DFX guide search result: `https://docs.amd.com/r/en-US/ug909-vivado-partial-reconfiguration`
- AMD Vitis Vision Library page: `https://www.amd.com/en/products/software/adaptive-socs-and-fpgas/vitis/vitis-libraries/vitis-vision.html`
- Vitis Vision design examples: `https://xilinx.github.io/Vitis_Libraries/vision/2022.1/design-examples.html`
- COCO official dataset page: `https://cocodataset.org/`
- ExDark official GitHub: `https://github.com/cs-chan/Exclusively-Dark-Image-Dataset`
- Brooks et al. CVPR 2019 unprocessing paper: `https://openaccess.thecvf.com/content_CVPR_2019/html/Brooks_Unprocessing_Images_for_Learned_Raw_Denoising_CVPR_2019_paper.html`
- cocotb docs: `https://docs.cocotb.org/`
- Verilator docs: `https://verilator.org/guide/latest/verilating.html`

NotebookLM / Obsidian / Zotero exports:

- Searched `/opt/data` for filenames containing `Notebook`, `Obsidian`, `Zotero`; no matching local exports were found during this run.

## Output

Local artifact:

- `/opt/data/projects/dfxisp/dfxisp-r1-source-inventory-2026-06-22.md`

Drive artifact:

- Uploaded file ID: `1B2JtafKxGloRT1Gu0yPJ_DePUK0hGc-K`
- Uploaded file URL: `https://drive.google.com/file/d/1B2JtafKxGloRT1Gu0yPJ_DePUK0hGc-K/view?usp=drivesdk`
- Upload target chosen: Agent OS / `05-dashboard/situation-room/docs`, because Agent OS / `06-production` exists but has no direct `DFXISP` project folder at the time of inspection. Existing DFXISP folders found in Drive were outside the Agent OS / `06-production` subtree, so I did not assume they are the requested production destination.

## Decisions

- Inventory-only decision: route this markdown to `05-dashboard/situation-room/docs` unless a direct Agent OS / `06-production/DFXISP` folder appears.
- No design decision is made. The analyst should use this as source evidence for later tradeoff work.

## Verification

- Verified Google Workspace auth using `HERMES_HOME=/opt/data ... setup.py --check` → `AUTHENTICATED: Token valid at /opt/data/google_token.json`.
- Verified Drive folders by `drive search` and `drive get`:
  - Agent OS root: `1xbqGeDdLerv8jd3eeHsR0IS-CHkI7kgz`
  - Agent OS / 06-production: `1OUL1mRG3Re7Ni7eLPLaHhMkHk-kbBPyg`
  - Agent OS / 05-dashboard / situation-room / docs: `1cA0ljwJCm4Mg76Jrk1uQnxZYtkLQhuhd`
- Found no direct child folder named `DFXISP` under Agent OS / `06-production`; only `AI드론` was listed as a direct child at inspection time.
- This inventory includes more than 10 concrete source entries.

## Open Questions

- Whether one of the existing non-`06-production` Drive folders named `DFXISP` should be treated as canonical for this project.
- Whether Zotero / NotebookLM exports exist outside `/opt/data` or under a Drive-only location not present in the local archive.
- Whether current DFXISP local cache should be promoted into Agent OS / `06-production/DFXISP` as a new project folder; this is a Drive/folder organization decision and is not made here.

## Next Agent

analyst — use this source inventory to propose minimal ISP baseline, DPR/adaptive hook points, fixture format, and verification-first tradeoffs.

---

# Source Inventory

Legend:

- Confidence: High = direct local or official source evidence; Medium = source is relevant but version/context mismatch or secondary; Low = weak match / needs original source.
- Fact = claim directly supported by cited source.
- Interpretation = researcher synthesis for DFXISP; not a final decision.

## A. Local Drive / project corpus

### S01 — DFXISP local README

- Type: Local project corpus
- Location: `/opt/data/dfxisp_md/README.md`
- Evidence notes:
  - Lines 3-5 define the project as FPGA-based ISP that changes behavior by lighting environment using DFX, targeting better downstream AI object detection.
  - Lines 9-13 list topic, platform, datasets, output target, and current structure.
  - Lines 52-53 split work into SW track and HW track.
  - Lines 156-161 identify key docs: Architecture, Research Roadmap, Analysis Report, HW/SW Interface.
- Fact:
  - The project is framed as DFX-based adaptive ISP for AI object detection, using ZCU104, Vitis HLS, Vivado, Vitis AI, COCO, and ExDark.
- Interpretation:
  - This should be treated as the local project index and first source for analyst orientation.
- Confidence: High

### S02 — DFXISP Architecture

- Type: Local project corpus
- Location: `/opt/data/dfxisp_md/docs/Architecture.md`
- Evidence notes:
  - Lines 5-9 define three connected axes: pseudo-RAW dataset, Python ISP golden model/evaluation, FPGA DFX adaptive ISP hardware.
  - Lines 17-34 show SW/HW convergence at Python golden model vs HW RGB32 bit comparison plus DPU/CNN evaluation.
  - Lines 62-74 list baseline ISP stages: Bayer16→Bayer8, BLC, Gain, Demosaicing, CCM, Gamma, RGB output.
  - Lines 76-100 list proposal ISP components: checker, binning_gain, pr_controller, isp_proposal.
  - Lines 156-168 warn that current RGB32 mainline and legacy grayscale/YUYV/DFX references are mixed and must be interpreted separately.
- Fact:
  - The repository contains both current RGB32 mainline and historical grayscale/YUYV/DFX material.
- Interpretation:
  - Analyst should explicitly separate current baseline architecture from historical DFX references to avoid wrong interface assumptions.
- Confidence: High

### S03 — DFXISP Research Roadmap

- Type: Local project corpus
- Location: `/opt/data/dfxisp_md/docs/Research_Roadmap.md`
- Evidence notes:
  - Lines 5-8 describe SW and HW tracks converging at golden vectors and DPU integration.
  - Lines 26-35 define RGB32 in/out pipeline and packing `[31:24]=0x00 / [23:16]=B / [15:8]=G / [7:0]=R`.
  - Lines 43-48 list completed items: grayscale DFX build, datasets/eval infrastructure, adaptive ISP gain signals, RGB32 interface decision, HLS RGB32 C-Sim mismatch=0.
  - Lines 74-85 state research purpose/background: DFX-based adaptive ISP to improve CNN object recognition under lighting changes.
  - Lines 139-148 define evaluation conditions A-F and expected relation `C > B > A`, `E ≈ D`.
  - Lines 167-187 provide DynamicSwitch checker simulation logic.
- Fact:
  - Current roadmap asserts RGB32 as interface direction and records several completed simulation/C-Sim milestones.
- Interpretation:
  - Good source for current target flow, but analyst should re-check completion claims against logs before treating them as verified for new work.
- Confidence: High for stated local roadmap; Medium for claims that require raw logs.

### S04 — DFXISP Analysis Report

- Type: Local project corpus / historical + current experiment notes
- Location: `/opt/data/dfxisp_md/docs/Analysis_Report.md`
- Evidence notes:
  - Lines 3-4 warn Part I is historical grayscale RTL simulation, while current mainline is RGB32.
  - Lines 10-18 describe early NORMAL→LOW_LIGHT DFX timing simulation setup.
  - Lines 62-64 claim clean isolation and arithmetic match in the early simulation.
  - Lines 118-123 give a careful conclusion: ISP-in-the-loop helped ExDark relative to none in one setup, but absolute mAP remained lower than raw-trained v2 and JPEG proxy has structural limits.
  - Lines 130-142 motivate pseudo-RAW/unprocessing to avoid double-processing JPEG images.
  - Lines 150-178 summarize three-task simplification and bit-exact proposal ISP validation.
- Fact:
  - The document explicitly labels historical vs current portions and records both positive results and limitations.
- Interpretation:
  - Use this as evidence for risk and methodology, not as a single final performance claim.
- Confidence: High for local report contents; Medium for unverified experiment reproducibility.

### S05 — HW/SW Interface Specification

- Type: Local project corpus
- Location: `/opt/data/dfxisp_md/docs/HW_SW_Interface.md`
- Evidence notes:
  - Lines 5-14 state that current RGB32 interface and older ZCU104 DFX AXI/DDR records coexist.
  - Lines 20-31 define RGB32 packing.
  - Lines 33-40 define pseudo-RAW Bayer format and dataset locations.
  - Lines 41-50 define Python golden model as HW verification reference.
  - Lines 83-88 list low-light core operations: 2x2 binning, gain, gamma 강화.
  - Lines 121-129 warn legacy DMA width/YUYV values are not current mainline.
  - Lines 165-177 classify current-trust vs historical-reference information.
- Fact:
  - Current reliable interface facts are RGB32 packing, pseudo-RAW format, Python golden model, proposal pipeline concept.
- Interpretation:
  - This should be an analyst guardrail document for interface assumptions.
- Confidence: High

### S06 — Proposal ISP README

- Type: Local project corpus / implementation note
- Location: `/opt/data/dfxisp_md/isppipeline/proposal/README.md`
- Evidence notes:
  - Lines 1-4 identify proposal ISP as baseline plus checker and DFX-target partial module.
  - Lines 7-20 show pipeline: Bayer16→static frontend→checker→Partial Module with normal gamma or low-light binning+gain+gamma.
  - Lines 24-30 list files: `checker`, `binning_gain`, `pr_controller`, `prep_and_check.py`, `build.sh`.
  - Lines 32-50 show intended build/verification and example mismatch=0 PASS for bright and dark cases.
- Fact:
  - Proposal README provides a concrete HLS-level structure and local verification harness names.
- Interpretation:
  - Analyst can map DPR/adaptive hook to `Partial Module`, but should decide whether the current milestone uses real DFX or a static-mode abstraction first.
- Confidence: High for local structure; Medium for PASS examples until rerun.

### S07 — Baseline ISP README

- Type: Local project corpus / implementation note
- Location: `/opt/data/dfxisp_md/isppipeline/baseline/README.md`
- Evidence notes:
  - Lines 1-5 define baseline ISP using Vitis Vision L1 functions and no adaptive processing.
  - Lines 9-17 list pipeline: Bayer16 → scale → BLC → gaincontrol → demosaicing → CCM → gamma → RGB8.
  - Lines 20-22 warn about WB gain and channel packing/CCM identity to avoid channel mixing.
  - Lines 47-52 claim host g++ C-Sim OK and note csynth/cosim are follow-up via `run_hls.tcl`.
- Fact:
  - Baseline is a concrete non-adaptive comparison pipeline using Vitis Vision functions.
- Interpretation:
  - Baseline should be the first minimal pipeline candidate, because adaptive logic can be evaluated as a delta.
- Confidence: High for local structure; Medium for PASS until rerun.

### S08 — DFX ISP Pipeline Tutorial

- Type: Local project reference / tutorial
- Location: `/opt/data/dfxisp_md/docs/reference/DFX_ISPPIPELINE_Tutorial.md`
- Evidence notes:
  - Lines 3-7 cite Vivado/Vitis 2024.1, ZCU104, AMD UG947 and UG909.
  - Lines 31-49 define DFX use case: runtime replacement of Binning/Gain modules and resource sharing via static region plus RP.
  - Lines 73-79 state DFX core principles: RM changes via partial bitstream, static routing lock, `pr_verify` compatibility.
  - Lines 95-152 list reference project structure including static HDL, RP wrappers, Tcl, pblocks, implementation outputs, bitstreams.
  - Lines 166-167 warn DFX license requirement for implementation; simulations can run without DFX license.
- Fact:
  - Local DFX tutorial aligns the project with AMD DFX terminology and flow artifacts.
- Interpretation:
  - Good theory-to-project bridge; analyst should cross-check with official AMD docs for current version differences.
- Confidence: High as local reference; Medium for official compatibility because it is a derived tutorial.

### S09 — HW inspection workflow plan

- Type: Local project planning / verification note
- Location: `/opt/data/dfxisp_md/docs/reference/demo_plan_hw_inspection_workflow.md`
- Evidence notes:
  - Lines 1-13 state the purpose: color end-to-end rewrite, SW golden bit-exact comparison, RGB32 in/out decision.
  - Lines 37-42 mark Phase A golden contract complete and list golden artifacts.
  - Lines 44-61 mark C-Sim and kernel rewrite outcomes, including mismatch=0 for three datapath kernels and checker PASS.
  - Lines 63-90 define phases D-J: C-Synth, Co-Sim, RTL sim, PR verify, implementation/timing, bitstream, ICAP/DDR.
  - Lines 108-113 list risks: timing, interface width, DDR bandwidth, demo vs real ISP.
- Fact:
  - This is the clearest local verification-first workflow from golden model to bitstream.
- Interpretation:
  - Analyst should reuse phase gates as acceptance criteria but not assume D-J are complete.
- Confidence: High for plan/status text; Medium for completed claims unless logs are rerun.

### S10 — Agent OS DFXISP project framing

- Type: Agent OS project workspace
- Location: `/opt/data/projects/dfxisp/PROJECT.md` and `/opt/data/projects/dfxisp/spec.md`
- Evidence notes:
  - PROJECT lines 10-16 define mission and principle: FPGA reconfigurable hardware + adaptive ISP, accuracy/reproducibility/verification priority.
  - PROJECT lines 25-41 define Phase 0 focus and milestone output.
  - PROJECT lines 45-46 scope research, baseline, fixture/flow, and excludes unverified implementation/board bring-up.
  - spec lines 5-8 define the current core problem.
  - spec lines 13-19 list desired spec package and Kanban handoff flow.
  - spec lines 53-60 define first milestone acceptance criteria.
- Fact:
  - Current Agent OS framing is verification-first and explicitly pre-implementation.
- Interpretation:
  - This task should feed analyst architecture/spec rather than start implementation.
- Confidence: High

### S11 — Agent OS legacy masterplan references

- Type: Agent OS archive / historical project context
- Location: `/opt/data/agent_os_archive/files/_archive/legacy-plans/AI_Native_Agent_Ecosystem_마스터플랜.md`
- Evidence notes from search results:
  - Lines 20-21 mention RTL verification chain and Python/NumPy golden model replacing MATLAB for cocotb bit-exact comparison.
  - Lines 173-175 record user research context: FPGA adaptive image processing, DPR replacing ISP modules by lighting, Histogram Checker → PR Controller → ICAP → DPU.
  - Lines 925-926 mention Zotero → NotebookLM workflow for DPR/ISP paper PDFs.
- Fact:
  - Legacy Agent OS context already contains the same research theme and verification discipline.
- Interpretation:
  - Useful for continuity, but should not override current `/opt/data/projects/dfxisp` spec.
- Confidence: Medium, because it is archived/legacy.

## B. External theory / reference sources

### S12 — AMD UG947 Dynamic Function eXchange tutorial

- Type: Official AMD documentation
- URL: `https://docs.amd.com/r/en-US/ug947-vivado-partial-reconfiguration-tutorial`
- Evidence notes from web extraction:
  - AMD UG947 teaches DFX from RTL/IP design through synthesis, implementation, verification, bitstream/PDI generation, and hardware reconfiguration.
  - It describes static region, Reconfigurable Partitions, Reconfigurable Modules, pblocks, locked static checkpoints, `pr_verify`, full/partial bitstreams, and runtime partial images.
- Fact:
  - Official DFX flow requires separation of static region/RP/RM and verification of static compatibility.
- Interpretation:
  - DFXISP should keep checker/pr_controller/static ISP boundary explicit if real DFX remains in scope.
- Confidence: High
- Caveat:
  - Extracted UG947 version was 2025.2 while project constraints say Vivado/Vitis 2024.1. Use concepts, but check 2024.1 docs/tool behavior before exact commands.

### S13 — AMD UG909 Dynamic Function eXchange guide

- Type: Official AMD documentation search result
- URL: `https://docs.amd.com/r/en-US/ug909-vivado-partial-reconfiguration`
- Evidence notes:
  - Web search result identifies UG909 as AMD Vivado Design Suite User Guide for Dynamic Function eXchange, describing how to use DFX to reconfigure modules.
  - Direct extraction timed out during this run.
- Fact:
  - UG909 is the canonical AMD guide for DFX methodology.
- Interpretation:
  - Analyst should retrieve/use UG909 directly before making detailed DFX implementation decisions.
- Confidence: Medium due to extraction timeout; source identity is strong, content not fully captured here.

### S14 — AMD Vitis Vision Library

- Type: Official AMD product/reference page
- URL: `https://www.amd.com/en/products/software/adaptive-socs-and-fpgas/vitis/vitis-libraries/vitis-vision.html`
- Evidence notes from extraction:
  - Vitis Vision Library provides accelerated computer vision and image processing for AMD adaptive platforms.
  - Page positions it for edge/data center, real-time throughput, efficient vision pipelines, color conversion, bit-depth conversion, pixel arithmetic, filters, statistics, classifiers, and AI-powered vision pipelines.
- Fact:
  - Vitis Vision is an official AMD library suitable for accelerated vision/image processing on AMD platforms.
- Interpretation:
  - Supports using Vitis Vision L1 functions as baseline ISP building blocks, consistent with local baseline README.
- Confidence: High

### S15 — Vitis Vision design examples / ISP examples

- Type: AMD/Xilinx documentation site
- URL: `https://xilinx.github.io/Vitis_Libraries/vision/2022.1/design-examples.html`
- Evidence notes from extraction:
  - Design examples include multiple Image Sensor Processing pipelines: Basic ISP, ISP 2020.2, ISP 2021.1, ISP with HDR, ISP with GTM, Mono ISP, RGB-IR ISP, and ISP multistream.
  - It notes most functions are implemented in streaming model except a few memory-mapped functions.
- Fact:
  - Vitis Vision provides reference ISP pipelines and streaming image-processing examples.
- Interpretation:
  - Baseline/adaptive DFXISP should borrow streaming/dataflow assumptions from Vitis Vision rather than inventing a full ISP from scratch.
- Confidence: High, with version caveat (2022.1 docs vs project 2024.1 constraint).

### S16 — COCO dataset

- Type: Official dataset site
- URL: `https://cocodataset.org/`
- Evidence notes from extraction:
  - COCO is a large-scale object detection, segmentation, and captioning dataset.
  - It lists 330K images, more than 200K labeled, 1.5M object instances, 80 object categories, 91 stuff categories, captions, and keypoints.
- Fact:
  - COCO is appropriate as a general-light object detection benchmark source.
- Interpretation:
  - DFXISP use of COCO should remain a proxy for ordinary-light image distribution, not a raw sensor dataset.
- Confidence: High

### S17 — ExDark dataset

- Type: Official dataset GitHub / publication record
- URL: `https://github.com/cs-chan/Exclusively-Dark-Image-Dataset`
- Evidence notes from extraction:
  - ExDark has 7,363 low-light images, 10 illumination conditions, 12 object classes, image-level and bounding-box annotations.
  - Published as “Getting to Know Low-light Images with The Exclusively Dark Dataset,” CVIU 2019.
  - Repository notes BSD-3-Clause license and commercial-use contact.
- Fact:
  - ExDark is directly relevant to low-light object detection evaluation.
- Interpretation:
  - Strong dataset match for DFXISP’s low-light goal, but because images are already processed JPEG-like outputs, raw-ISP claims need pseudo-RAW or sensor capture caveats.
- Confidence: High

### S18 — Brooks et al. “Unprocessing Images for Learned Raw Denoising”

- Type: Peer-reviewed CVPR paper
- URL: `https://openaccess.thecvf.com/content_CVPR_2019/html/Brooks_Unprocessing_Images_for_Learned_Raw_Denoising_CVPR_2019_paper.html`
- Evidence notes from extraction:
  - Paper presents a technique to “unprocess” images by inverting each step of an image-processing pipeline to synthesize realistic raw sensor measurements from Internet photos.
  - Abstract emphasizes that pipeline stages such as gain, color correction, and tone mapping affect finished images and should be modeled.
- Fact:
  - Unprocessing is a recognized method for generating raw-like data from processed images.
- Interpretation:
  - This is the strongest theory source for DFXISP pseudo-RAW generation and for explaining why COCO/ExDark JPEGs are an imperfect ISP input.
- Confidence: High

### S19 — cocotb documentation

- Type: Official tool documentation
- URL: `https://docs.cocotb.org/`
- Evidence notes from extraction:
  - cocotb is a coroutine-based cosimulation testbench environment for verifying VHDL/SystemVerilog RTL using Python.
  - It requires an HDL simulator and lets Python be used for testbenches.
- Fact:
  - cocotb can support Python-based RTL verification where the DUT is already defined in HDL.
- Interpretation:
  - Good candidate for connecting Python golden fixtures to RTL simulation in DFXISP, but it is not the simulator itself.
- Confidence: High

### S20 — Verilator documentation

- Type: Official tool documentation
- URL: `https://verilator.org/guide/latest/verilating.html`
- Evidence notes from extraction:
  - Verilator supports modes including `--binary`, `--cc`, `--sc`, `--lint-only`, `--json-only`, and preprocessing.
  - `--lint-only` checks the design for warnings without producing normal generated output.
  - `--cc` translates SystemVerilog design into C++.
- Fact:
  - Verilator is useful for lint and fast compiled simulation flows for supported SystemVerilog subsets.
- Interpretation:
  - Fits Agent OS legacy verification chain as an early static/lint gate before simulator/Vivado gates, but Vivado remains necessary for HLS/DFX synthesis/timing.
- Confidence: High

---

# Evidence Synthesis for Analyst

## Facts supported by multiple sources

1. DFXISP is an adaptive ISP research project aiming to improve downstream object detection under lighting changes using FPGA/DFX.
   - Evidence: S01, S02, S03, S10, S11.
2. Current local direction favors RGB32 in/out and Python golden model bit comparison.
   - Evidence: S03, S05, S09.
3. Baseline ISP and proposal ISP are already sketched as separate local structures.
   - Evidence: S06, S07.
4. Low-light adaptation currently centers on checker-driven mode selection plus 2x2 binning, gain, and gamma changes.
   - Evidence: S03, S05, S06, S08.
5. Local corpus mixes current RGB32 direction with older grayscale/YUYV/DFX artifacts.
   - Evidence: S02, S04, S05.
6. Official AMD DFX flow requires static/RP/RM partitioning and compatibility verification, not just a mode signal.
   - Evidence: S08, S12, S13.
7. COCO and ExDark are relevant object-detection datasets, but processed-image datasets are not raw sensor inputs.
   - Evidence: S16, S17, S18 plus S04 limitations.

## Researcher interpretations / not final decisions

1. Minimal baseline candidate:
   - Bayer/pseudo-RAW → BLC → gain/WB → demosaic → CCM → gamma → RGB fixture.
   - Reason: locally documented baseline (S07) and Vitis Vision support (S14/S15).
2. Adaptive hook candidates:
   - checker threshold, gamma LUT/parameter table, binning/gain module, stage bypass, or true RP replacement.
   - Reason: local proposal (S06), DFX tutorial (S08), official DFX model (S12).
3. Verification-first fixture should prioritize Python golden model and small RGB32/pseudo-RAW fixtures before board integration.
   - Reason: S05/S09 and project framing S10.
4. For claims about “AI object detection improvement,” analyst should distinguish:
   - proxy JPEG/COCO/ExDark experiments;
   - pseudo-RAW/unprocessed experiments;
   - real Bayer sensor/board experiments.
   - Reason: S04 and S18.

## Missing sources / uncertainty list

| Missing / uncertain source | Why it matters | Confidence impact | Recommended next action |
|---|---|---:|---|
| Direct Agent OS / `06-production/DFXISP` Drive folder | Required target path if canonical project folder exists | Medium | Ask operator or create/choose folder only after Drive organization decision |
| Zotero DPR/ISP paper PDFs | Needed for formal literature review beyond local docs | Medium | Locate Zotero export or Drive folder; do not infer paper list |
| NotebookLM export notes | Could contain synthesized prior research | Medium | Locate export or ask operator |
| Original Vivado/Vitis logs for mismatch=0, pr_verify, WNS | Needed to verify local PASS claims | Medium | Analyst/coder should rerun or inspect logs before implementation decisions |
| UG909 full extracted content for Vivado 2024.1 | DFX methodology details and exact constraints | Medium | Fetch official 2024.1 UG909 PDF/page if available |
| Exact board/sensor input assumptions | Demosaic bypass vs real Bayer path affects architecture | High | Analyst should mark this as a design fork |

## Source priority recommendation

For the next analyst pass, use the sources in this order:

1. S10 project framing/spec — defines current task scope.
2. S02/S05/S09 — current architecture/interface/verification guardrails.
3. S06/S07 — concrete local baseline/proposal candidates.
4. S12/S14/S15 — official AMD DFX/Vitis Vision grounding.
5. S16/S17/S18 — dataset/methodology grounding for AI/object-detection claims.
6. S04/S11 — use for historical context and caveats, not as final truth.
