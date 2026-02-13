# Humanoid Robotics
*Gardener Technical Analysis | 2026-02-13*

*This report analyzes 88 curated items with technical depth.*

---

## Executive Synthesis

Analysis of 88 sources reveals several technical developments in humanoid robot.

### Language Models & Architecture

**[AINews] Z.ai GLM-5: New SOTA Open Weights LLM**
*Latent.Space*
Building on yesterday's [Reddit](/?date=2026-02-12&category=reddit#item-caa559351de6) coverage, Z.ai launched GLM-5, a new state-of-the-art open-weights LLM with 744B parameters (40B active) trained o...
[Source](https://www.latent.space/p/ainews-zai-glm-5-new-sota-open-weights)

**Scaling Verification Can Be More Effective than Scaling Policy Learning for Vision-Language-Action Alignment**
*arXiv (Artificial Intelligence)*
This paper investigates test-time verification as a way to close the gap between intended instructions and generated actions in Vision-Language-Action (VLA) models for robotics. They characterize test...
[Source](http://arxiv.org/abs/2602.12281)

**Gaia2: Benchmarking LLM Agents on Dynamic and Asynchronous Environments**
*arXiv (Artificial Intelligence)*
Introduces Gaia2, a benchmark for evaluating LLM agents in dynamic, asynchronous environments where environments evolve independently of agent actions. Includes write-action verifiers for RL training....
[Source](http://arxiv.org/abs/2602.11964)

**VLAW: Iterative Co-Improvement of Vision-Language-Action Policy and World Model**
*arXiv (Robotics)*
VLAW proposes iterative co-improvement of VLA policies and world models through online interaction, using action-conditioned video generation models as learned simulators. Addresses the key challenge...
[Source](http://arxiv.org/abs/2602.12063)

**JEPA-VLA: Video Predictive Embedding is Needed for VLA Models**
*arXiv (Computer Vision)*
Proposes JEPA-VLA, arguing that video predictive embeddings (JEPA-style) are superior visual representations for VLA models compared to contrastive or reconstruction-based approaches. Shows improved s...
[Source](http://arxiv.org/abs/2602.11832)

### Robotics & Control

**MolmoSpaces: A Large-Scale Open Ecosystem for Robot Navigation and Manipulation**
*arXiv (Artificial Intelligence)*
MolmoSpaces is a large-scale open ecosystem for robot navigation and manipulation with 230k+ diverse indoor environments and 130k annotated object assets, from the Allen AI / UW / Georgia Tech team.
[Source](http://arxiv.org/abs/2602.11337)

**Ctrl&Shift: High-Quality Geometry-Aware Object Manipulation in Visual Generation**
*arXiv (Computer Vision)*
Presents Ctrl&Shift, a diffusion framework for geometry-consistent object manipulation in images/videos without explicit 3D reconstruction. Decomposes manipulation into two stages for background prese...
[Source](http://arxiv.org/abs/2602.11440)

**Learning to Manipulate Anything: Revealing Data Scaling Laws in Bounding-Box Guided Policies**
*arXiv (Robotics)*
Investigates data scaling laws in semantic manipulation by using bounding-box instructions to specify target objects. Introduces Label-UMI, a handheld segmentation device with automated annotation pip...
[Source](http://arxiv.org/abs/2602.11885)

**Accelerating Robotic Reinforcement Learning with Agent Guidance**
*arXiv (Artificial Intelligence)*
Introduces Agent-guided Policy Search (AGPS) that replaces human supervisors with a multimodal agent for real-world robotic RL training, addressing the scalability bottleneck of human-in-the-loop meth...
[Source](http://arxiv.org/abs/2602.11978)

**General Humanoid Whole-Body Control via Pretraining and Fast Adaptation**
*arXiv (Robotics)*
FAST introduces a general humanoid whole-body control framework using Parseval-Guided Residual Policy Adaptation for fast adaptation to out-of-distribution motions while mitigating catastrophic forget...
[Source](http://arxiv.org/abs/2602.11929)

### Other

**The modern age has richly rewarded people with a combination of high intelligence and high agency. N...**
*Twitter*
John Carmack argues that AI automation of intelligence will empower people with high agency but lower intelligence, if they trust AI advice. Uses provocative example of a 'ruthless criminal' with alwa...
[Source](https://twitter.com/ID_AA_Carmack/status/2022019443547660304)

**We let Chrome's Auto Browse agent surf the web for us—here's what happened**
*Ars Technica - All content*
Google launched Auto Browse, a Chrome-based AI agent in preview for AI Pro and AI Ultra subscribers, capable of navigating the web autonomously to complete tasks. The agent's integration into Chrome g...
[Source](https://arstechnica.com/google/2026/02/tested-how-chromes-auto-browse-agent-handles-common-web-tasks/)

**On the Adoption of AI Coding Agents in Open-source Android and iOS Development**
*arXiv (Artificial Intelligence)*
First empirical study of AI coding agent contributions in open-source mobile (Android/iOS) development, analyzing 2,901 AI-authored pull requests across 193 repositories.
[Source](http://arxiv.org/abs/2602.12144)

**# A 150-year-old passage from Marx basically describes AGI — and a short story called “Manna” shows both possible outcomes**
*r/singularity*
Discussion connecting a Marx passage from Capital Vol. III to AGI's potential societal impact, referencing the short story 'Manna' as illustrating two possible outcomes of labor displacement by techno...
[Source](https://reddit.com/r/singularity/comments/1r2pqcm/a_150yearold_passage_from_marx_basically/)

**AI agents for B2B. Please suggest any masterminds, communities etc**
*r/LocalLLaMA*
Discussion about whether large context windows are being overused as storage instead of improving retrieval quality, arguing attention is a finite computational budget.
[Source](https://reddit.com/r/LocalLLaMA/comments/1r30kyj/ai_agents_for_b2b_please_suggest_any_masterminds/)

### Learning & Training

**Adaptive Milestone Reward for GUI Agents**
*arXiv (Artificial Intelligence)*
ADMIRE proposes adaptive milestone rewards for training GUI agents via RL, dynamically distilling milestones from successful explorations and using asymmetric credit assignment to resolve the reward f...
[Source](http://arxiv.org/abs/2602.11524)

**Adaptive-Horizon Conflict-Based Search for Closed-Loop Multi-Agent Path Finding**
*arXiv (Robotics)*
ACCBS is a closed-loop multi-agent path finding algorithm built on finite-horizon CBS with a dynamic horizon-changing mechanism inspired by iterative deepening in MPC. It reuses constraint trees acros...
[Source](http://arxiv.org/abs/2602.12024)

**Ｋｅｙ  Ｉｎｓｉｇｈｔｓ：**
*Twitter*
(𝙉𝙤𝙩𝙚 𝙚𝙨𝙥𝙚𝙘𝙞𝙖𝙡𝙡𝙮 𝙩𝙝𝙚 𝙡𝙖𝙨𝙩 𝙤𝙣𝙚.) • Why driverless train operations require more than ... Kirk Borne shares key insights on driverless train operations, discussing digital twins, predictive availability...
[Source](https://twitter.com/KirkDBorne/status/2021985526413242853)

**Stroke of Surprise: Progressive Semantic Illusions in Vector Sketching**
*arXiv (Computer Vision)*
Introduces 'Progressive Semantic Illusions' — a novel vector sketching task where adding strokes transforms the perceived semantic meaning of a sketch. The framework optimizes strokes under dual const...
[Source](http://arxiv.org/abs/2602.12280)

### Code Generation & Synthesis

**Robot-DIFT: Distilling Diffusion Features for Geometrically Consistent Visuomotor Control**
*arXiv (Robotics)*
Robot-DIFT argues that a key bottleneck in generalizable manipulation is the structural mismatch between visual encoders (optimized for semantic invariance) and the geometric sensitivity needed for cl...
[Source](http://arxiv.org/abs/2602.11934)

**I made Cursor work for 44mins at a time, running new automation test cases 👀 https://t.co/GQn1vH41zr**
*Twitter*
tdinh_me reports making Cursor run automated test cases for 44 minutes continuously, showcasing extended AI coding agent sessions.
[Source](https://twitter.com/tdinh_me/status/2021788077400977731)

### Safety & Alignment

**You don't need a Mac Mini to run @OpenClaw.**
*Twitter*
Use https://t.co/jeP0nebHIv instead. With it you can sa... Scobleizer promotes a cloud hosting service for OpenClaw, an AI agent with full system access. Pitches it as solving setup complexity and sec...
[Source](https://twitter.com/Scobleizer/status/2021862295421559158)

**It’s AI-fornication**
*r/ChatGPT*
AI-generated parody song 'AI-fornication' in the style of Red Hot Chili Peppers about AI risks.
[Source](https://reddit.com/r/ChatGPT/comments/1r33bpl/its_aifornication/)

## Critical Assessment

Key observations:

- 88 items analyzed from news, research, social, and reddit sources
- Themes identified: Language Models & Architecture, Robotics & Control, Other, Learning & Training, Code Generation & Synthesis, Safety & Alignment
- See individual sources for detailed methodology and results

## References

1. [The modern age has richly rewarded people with a combination of high intelligence and high agency. N...](https://twitter.com/ID_AA_Carmack/status/2022019443547660304)
2. [[AINews] Z.ai GLM-5: New SOTA Open Weights LLM](https://www.latent.space/p/ainews-zai-glm-5-new-sota-open-weights)
3. [Scaling Verification Can Be More Effective than Scaling Policy Learning for Vision-Language-Action Alignment](http://arxiv.org/abs/2602.12281)
4. [Gaia2: Benchmarking LLM Agents on Dynamic and Asynchronous Environments](http://arxiv.org/abs/2602.11964)
5. [MolmoSpaces: A Large-Scale Open Ecosystem for Robot Navigation and Manipulation](http://arxiv.org/abs/2602.11337)
6. [VLAW: Iterative Co-Improvement of Vision-Language-Action Policy and World Model](http://arxiv.org/abs/2602.12063)
7. [We let Chrome's Auto Browse agent surf the web for us—here's what happened](https://arstechnica.com/google/2026/02/tested-how-chromes-auto-browse-agent-handles-common-web-tasks/)
8. [JEPA-VLA: Video Predictive Embedding is Needed for VLA Models](http://arxiv.org/abs/2602.11832)
9. [GigaBrain-0.5M*: a VLA That Learns From World Model-Based Reinforcement Learning](http://arxiv.org/abs/2602.12099)
10. [ABot-M0: VLA Foundation Model for Robotic Manipulation with Action Manifold Learning](http://arxiv.org/abs/2602.11236)
11. [🔬Beyond AlphaFold: How Boltz is Open-Sourcing the Future of Drug Discovery](https://www.latent.space/p/boltz)
12. [Owning the AI Pareto Frontier — Jeff Dean](https://www.latent.space/p/jeffdean)
13. [Existing AI agents are largely short-horizon (e.g. chat) or constrained (e.g. agentic process automa...](https://twitter.com/jerryjliu0/status/2022001467851411776)
14. [HoloBrain-0 Technical Report](http://arxiv.org/abs/2602.12062)
15. [Robot-DIFT: Distilling Diffusion Features for Geometrically Consistent Visuomotor Control](http://arxiv.org/abs/2602.11934)
16. [Adaptive Milestone Reward for GUI Agents](http://arxiv.org/abs/2602.11524)
17. [Ctrl&Shift: High-Quality Geometry-Aware Object Manipulation in Visual Generation](http://arxiv.org/abs/2602.11440)
18. [Learning to Manipulate Anything: Revealing Data Scaling Laws in Bounding-Box Guided Policies](http://arxiv.org/abs/2602.11885)
19. [You don't need a Mac Mini to run @OpenClaw.](https://twitter.com/Scobleizer/status/2021862295421559158)
20. [HAIC: Humanoid Agile Object Interaction Control via Dynamics-Aware World Model](http://arxiv.org/abs/2602.11758)