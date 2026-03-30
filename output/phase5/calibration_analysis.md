# PWC Pipeline — Phase 5 Calibration Analysis

Scored pairs: 2409 | Official: 1208 | Non-official: 1201

Current thresholds: STRONG ≥ 0.75 | MEDIUM ≥ 0.45


---

## 1. Score Distribution

```
Score range      All  Official  Non-off  Histogram (all)
-----------------------------------------------------------------
[0.00–0.05)       27         0       27  ░░░░░░░░░░░░░░░░░░░░░░░░░
[0.05–0.10)       38         0       38  ░░░░░░░░░░░░░░░░░░░░░░░░░
[0.10–0.15)      198         0      198  ██░░░░░░░░░░░░░░░░░░░░░░░
[0.15–0.20)        0         0        0  ░░░░░░░░░░░░░░░░░░░░░░░░░
[0.20–0.25)      230         7      223  ██░░░░░░░░░░░░░░░░░░░░░░░
[0.25–0.30)      416        19      397  ████░░░░░░░░░░░░░░░░░░░░░
[0.30–0.35)       67        24       43  █░░░░░░░░░░░░░░░░░░░░░░░░
[0.35–0.40)        0         0        0  ░░░░░░░░░░░░░░░░░░░░░░░░░
[0.40–0.45)       75        25       50  █░░░░░░░░░░░░░░░░░░░░░░░░
[0.45–0.50)      162        50      112  ██░░░░░░░░░░░░░░░░░░░░░░░ ◄ MEDIUM threshold
[0.50–0.55)      127        49       78  █░░░░░░░░░░░░░░░░░░░░░░░░
[0.55–0.60)      372       342       30  ████░░░░░░░░░░░░░░░░░░░░░
[0.60–0.65)        0         0        0  ░░░░░░░░░░░░░░░░░░░░░░░░░
[0.65–0.70)      466       462        4  █████░░░░░░░░░░░░░░░░░░░░
[0.70–0.75)        0         0        0  ░░░░░░░░░░░░░░░░░░░░░░░░░
[0.75–0.80)      201       200        1  ██░░░░░░░░░░░░░░░░░░░░░░░ ◄ STRONG threshold
[0.80–0.85)       19        19        0  ░░░░░░░░░░░░░░░░░░░░░░░░░
[0.85–0.90)        9         9        0  ░░░░░░░░░░░░░░░░░░░░░░░░░
[0.90–0.95)        2         2        0  ░░░░░░░░░░░░░░░░░░░░░░░░░
[0.95–1.00)        0         0        0  ░░░░░░░░░░░░░░░░░░░░░░░░░
```

**Summary statistics:**

| Metric | All | Official | Non-official |
|---|---|---|---|
| Min | 0.0 | 0.2 | 0.0 |
| Max | 0.9 | 0.9 | 0.75 |
| Mean | 0.45 | 0.628 | 0.271 |
| Median | 0.45 | 0.65 | 0.25 |


---

## 2. Official vs Non-official Breakdown

| Level | Official | Non-official |
|---|---|---|
| STRONG | 230 / 1208 | 1 / 1201 |
| MEDIUM | 903 / 1208 | 224 / 1201 |
| WEAK | 75 / 1208 | 976 / 1201 |

> **Key finding:** All 1201 non-official repos are WEAK at current thresholds.  
> Max non-official score: `0.750` — threshold for MEDIUM is `0.45`.  
> Gap: `-0.300` — non-official repos would need this score increase to reach MEDIUM.


---

## 3. Threshold Sensitivity

How STRONG/MEDIUM/WEAK counts change as thresholds vary (all scored pairs).

```
STRONG≥   MEDIUM≥    STRONG  MEDIUM    WEAK
---------------------------------------------
0.60      0.35          921     579     909
0.60      0.40          921     512     976
0.60      0.45          921     437    1051
0.60      0.50          921     275    1213
0.65      0.35          697     803     909
0.65      0.40          697     736     976
0.65      0.45          697     661    1051
0.65      0.50          697     499    1213
0.70      0.35          483    1017     909
0.70      0.40          483     950     976
0.70      0.45          483     875    1051
0.70      0.50          483     713    1213
0.75      0.35          231    1269     909
0.75      0.40          231    1202     976
0.75      0.45          231    1127    1051 ◄ current
0.75      0.50          231     965    1213
0.80      0.35           30    1470     909
0.80      0.40           30    1403     976
0.80      0.45           30    1328    1051
0.80      0.50           30    1166    1213
```


---

## 4. Borderline Pairs

Pairs within ±0.05 of a threshold (most sensitive to recalibration).

### Near STRONG threshold (0.75 ± 0.05): 201 pairs

| Score | Level | Official | LLM | Title |
|---|---|---|---|---|
| `0.75` | STRONG | Y | STRONG | QLoRA: Efficient Finetuning of Quantized LLMs |
| `0.75` | STRONG | Y | MEDIUM | On the limits of cross-domain generalization in automated X- |
| `0.75` | STRONG | Y | STRONG | Levenshtein Training for Word-level Quality Estimation |
| `0.75` | STRONG | Y | STRONG | On Sparsifying Encoder Outputs in Sequence-to-Sequence Model |
| `0.75` | STRONG | Y | STRONG | Kannada-MNIST: A new handwritten digits dataset for the Kann |
| `0.75` | STRONG | Y | STRONG | UUKG: Unified Urban Knowledge Graph Dataset for Urban Spatio |
| `0.75` | STRONG | Y | STRONG | A Strong Gravitational Lens Is Worth a Thousand Dark Matter  |
| `0.75` | STRONG | Y | STRONG | A Feasibility Study on Image Inpainting for Non-cleft Lip Ge |
| `0.75` | STRONG | Y | STRONG | An Adaptive and Altruistic PSO-based Deep Feature Selection  |
| `0.75` | STRONG | Y | STRONG | MiNet: Mixed Interest Network for Cross-Domain Click-Through |
| `0.75` | STRONG | Y | STRONG | Self-Calibrated Efficient Transformer for Lightweight Super- |
| `0.75` | STRONG | Y | STRONG | Using Speech Synthesis to Train End-to-End Spoken Language U |
| `0.75` | STRONG | Y | STRONG | Deep Spatial-angular Regularization for Compressive Light Fi |
| `0.75` | STRONG | Y | STRONG | Visual Analytics for Understanding Draco's Knowledge Base |
| `0.75` | STRONG | Y | STRONG | Echoes from Alexandria: A Large Resource for Multilingual Bo |
| `0.75` | STRONG | Y | STRONG | Global Robustness Evaluation of Deep Neural Networks with Pr |
| `0.75` | STRONG | Y | STRONG | A 3D Reactive Navigation Algorithm for Mobile Robots by Usin |
| `0.75` | STRONG | Y | STRONG | WRENCH: A Comprehensive Benchmark for Weak Supervision |
| `0.75` | STRONG | Y | STRONG | BSNet: Box-Supervised Simulation-assisted Mean Teacher for 3 |
| `0.75` | STRONG | Y | STRONG | Performance of Hyperbolic Geometry Models on Top-N Recommend |
| `0.75` | STRONG | N | STRONG | ResUNet-a: a deep learning framework for semantic segmentati |
| `0.75` | STRONG | Y | STRONG | Global Structure Knowledge-Guided Relation Extraction Method |
| `0.75` | STRONG | Y | STRONG | ALPHA: AnomaLous Physiological Health Assessment Using Large |
| `0.75` | STRONG | Y | — | Learning Latent Super-Events to Detect Multiple Activities i |
| `0.75` | STRONG | Y | STRONG | Bidirectional Attentive Memory Networks for Question Answeri |
| `0.75` | STRONG | Y | — | Generating Hard-Negative Out-of-Scope Data with ChatGPT for  |
| `0.75` | STRONG | Y | STRONG | Graph Transformer Networks: Learning Meta-path Graphs to Imp |
| `0.75` | STRONG | Y | STRONG | Robust Target Training for Multi-Source Domain Adaptation |
| `0.75` | STRONG | Y | STRONG | A Unified Framework for Masked and Mask-Free Face Recognitio |
| `0.75` | STRONG | Y | — | Teach CLIP to Develop a Number Sense for Ordinal Regression |
| `0.75` | STRONG | Y | STRONG | MiranDa: Mimicking the Learning Processes of Human Doctors t |
| `0.75` | STRONG | Y | STRONG | Boosting Few-Shot Visual Learning with Self-Supervision |
| `0.75` | STRONG | Y | STRONG | Immiscible Color Flows in Optimal Transport Networks for Ima |
| `0.75` | STRONG | Y | STRONG | BINet: Multi-perspective Business Process Anomaly Classifica |
| `0.75` | STRONG | Y | — | DeVLBert: Learning Deconfounded Visio-Linguistic Representat |
| `0.75` | STRONG | Y | STRONG | Overcoming Recency Bias of Normalization Statistics in Conti |
| `0.75` | STRONG | Y | STRONG | Deformable VisTR: Spatio temporal deformable attention for v |
| `0.75` | STRONG | Y | STRONG | Derivative Delay Embedding: Online Modeling of Streaming Tim |
| `0.75` | STRONG | Y | — | Inducing Systematicity in Transformers by Attending to Struc |
| `0.75` | STRONG | Y | STRONG | High Probability Complexity Bounds for Non-Smooth Stochastic |
| `0.75` | STRONG | Y | STRONG | "Zero-Shot" Point Cloud Upsampling |
| `0.75` | STRONG | Y | STRONG | Semi-supervised Domain Adaptation via Sample-to-Sample Self- |
| `0.75` | STRONG | Y | STRONG | Edge Representation Learning with Hypergraphs |
| `0.75` | STRONG | Y | STRONG | Intent Factored Generation: Unleashing the Diversity in Your |
| `0.75` | STRONG | Y | STRONG | MGNN: Graph Neural Networks Inspired by Distance Geometry Pr |
| `0.75` | STRONG | Y | STRONG | Surface-SOS: Self-Supervised Object Segmentation via Neural  |
| `0.75` | STRONG | Y | STRONG | Real-Time Drone Detection and Tracking With Visible, Thermal |
| `0.75` | STRONG | Y | STRONG | RDA: An Accelerated Collision Free Motion Planner for Autono |
| `0.75` | STRONG | Y | STRONG | Solving ARC visual analogies with neural embeddings and vect |
| `0.75` | STRONG | Y | STRONG | Progressive Confident Masking Attention Network for Audio-Vi |
| `0.75` | STRONG | Y | — | ZEBRA: Zero-Shot Example-Based Retrieval Augmentation for Co |
| `0.75` | STRONG | Y | — | NLPineers@ NLU of Devanagari Script Languages 2025: Hate Spe |
| `0.75` | STRONG | Y | — | Transfer-Prompting: Enhancing Cross-Task Adaptation in Large |
| `0.75` | STRONG | Y | STRONG | An Informative Path Planning Framework for Active Learning i |
| `0.75` | STRONG | Y | — | OPIRL: Sample Efficient Off-Policy Inverse Reinforcement Lea |
| `0.75` | STRONG | Y | STRONG | Sparse maximal update parameterization: A holistic approach  |
| `0.75` | STRONG | Y | STRONG | USCORE: An Effective Approach to Fully Unsupervised Evaluati |
| `0.75` | STRONG | Y | — | MFA-Conformer: Multi-scale Feature Aggregation Conformer for |
| `0.75` | STRONG | Y | STRONG | Importance of Aligning Training Strategy with Evaluation for |
| `0.75` | STRONG | Y | — | SAT: Improving Semi-Supervised Text Classification with Simp |
| `0.75` | STRONG | Y | STRONG | EPSILON: An Efficient Planning System for Automated Vehicles |
| `0.75` | STRONG | Y | STRONG | Aneumo: A Large-Scale Comprehensive Synthetic Dataset of Ane |
| `0.75` | STRONG | Y | STRONG | MSC: A Dataset for Macro-Management in StarCraft II |
| `0.75` | STRONG | Y | STRONG | Learning Vector-Quantized Item Representation for Transferab |
| `0.75` | STRONG | Y | STRONG | Video Self-Stitching Graph Network for Temporal Action Local |
| `0.75` | STRONG | Y | STRONG | Dynamical Mechanism of Sampling-based Stochastic Inference u |
| `0.75` | STRONG | Y | STRONG | CondLaneNet: a Top-to-down Lane Detection Framework Based on |
| `0.75` | STRONG | Y | — | The Devil is in the Prompts: De-Identification Traces Enhanc |
| `0.75` | STRONG | Y | — | Interpretable Image Recognition with Hierarchical Prototypes |
| `0.75` | STRONG | Y | STRONG | The AiiDA-KKR plugin and its application to high-throughput  |
| `0.75` | STRONG | Y | STRONG | Analyzing the Performance of Large Language Models on Code S |
| `0.75` | STRONG | Y | STRONG | Efficient Temporal Sentence Grounding in Videos with Multi-T |
| `0.75` | STRONG | Y | STRONG | Cross-Sensor Adversarial Domain Adaptation of Landsat-8 and  |
| `0.75` | STRONG | Y | STRONG | SPIN: Spacecraft Imagery for Navigation |
| `0.75` | STRONG | Y | STRONG | Input Normalized Stochastic Gradient Descent Training of Dee |
| `0.75` | STRONG | Y | STRONG | DDD20 End-to-End Event Camera Driving Dataset: Fusing Frames |
| `0.75` | STRONG | Y | STRONG | Automatic selection of clustering algorithms using supervise |
| `0.75` | STRONG | Y | — | Non-Autoregressive Dialog State Tracking |
| `0.75` | STRONG | Y | STRONG | Revisiting, Benchmarking and Understanding Unsupervised Grap |
| `0.75` | STRONG | Y | STRONG | PBench: Workload Synthesizer with Real Statistics for Cloud  |
| `0.75` | STRONG | Y | STRONG | OmniGlue: Generalizable Feature Matching with Foundation Mod |
| `0.75` | STRONG | Y | STRONG | Brain-like Flexible Visual Inference by Harnessing Feedback  |
| `0.75` | STRONG | Y | STRONG | Domain-Specific Denoising Diffusion Probabilistic Models for |
| `0.75` | STRONG | Y | STRONG | LLM-PQ: Serving LLM on Heterogeneous Clusters with Phase-Awa |
| `0.75` | STRONG | Y | STRONG | Refining Diffusion Planner for Reliable Behavior Synthesis b |
| `0.75` | STRONG | Y | STRONG | PiCANet: Pixel-wise Contextual Attention Learning for Accura |
| `0.75` | STRONG | Y | STRONG | Escape with Your Self: A Solution to the Avoidance Problem w |
| `0.75` | STRONG | Y | STRONG | Energy-Based Models for Continual Learning |
| `0.75` | STRONG | Y | STRONG | GAP: A Graph-aware Language Model Framework for Knowledge Gr |
| `0.75` | STRONG | Y | STRONG | CAPRI-FAIR: Integration of Multi-sided Fairness in Contextua |
| `0.75` | STRONG | Y | STRONG | Hallucinated but Factual! Inspecting the Factuality of Hallu |
| `0.75` | STRONG | Y | STRONG | Restore Anything Model via Efficient Degradation Adaptation |
| `0.75` | STRONG | Y | STRONG | Domain-Generalizable Multiple-Domain Clustering |
| `0.75` | STRONG | Y | — | A Lightweight Inception Boosted U-Net Neural Network for Rou |
| `0.75` | STRONG | Y | STRONG | LightX3ECG: A Lightweight and eXplainable Deep Learning Syst |
| `0.75` | STRONG | Y | — | Information-Theoretic Probing for Linguistic Structure |
| `0.75` | STRONG | Y | STRONG | LiDAR Snowfall Simulation for Robust 3D Object Detection |
| `0.75` | STRONG | Y | STRONG | A probability theoretic approach to drifting data in continu |
| `0.75` | STRONG | Y | STRONG | MILE: A Multi-Level Framework for Scalable Graph Embedding |
| `0.75` | STRONG | Y | — | Leveraging Transfer Learning and Multiple Instance Learning  |
| `0.75` | STRONG | Y | — | OwLore: Outlier-weighed Layerwise Sampled Low-Rank Projectio |
| `0.75` | STRONG | Y | STRONG | SpectralNet: Spectral Clustering using Deep Neural Networks |
| `0.75` | STRONG | Y | STRONG | Model and Data Agreement for Learning with Noisy Labels |
| `0.75` | STRONG | Y | STRONG | Understanding normalization in contrastive representation le |
| `0.75` | STRONG | Y | STRONG | TACCL: Guiding Collective Algorithm Synthesis using Communic |
| `0.75` | STRONG | Y | STRONG | MedCPT: Contrastive Pre-trained Transformers with Large-scal |
| `0.75` | STRONG | Y | STRONG | Label-Efficient Self-Supervised Speaker Verification With In |
| `0.75` | STRONG | Y | STRONG | CEEBERT: Cross-Domain Inference in Early Exit BERT |
| `0.75` | STRONG | Y | STRONG | Street-View Image Generation from a Bird's-Eye View Layout |
| `0.75` | STRONG | Y | STRONG | Graph Neural Networks Exponentially Lose Expressive Power fo |
| `0.75` | STRONG | Y | STRONG | SAFRAN: An interpretable, rule-based link prediction method  |
| `0.75` | STRONG | Y | STRONG | The Larger They Are, the Harder They Fail: Language Models d |
| `0.75` | STRONG | Y | STRONG | Unveiling Deep Shadows: A Survey and Benchmark on Image and  |
| `0.75` | STRONG | Y | — | Single Layer Predictive Normalized Maximum Likelihood for Ou |
| `0.75` | STRONG | Y | STRONG | Masked Diffusion Models Are Fast Distribution Learners |
| `0.75` | STRONG | Y | STRONG | Generative Data Augmentation for Commonsense Reasoning |
| `0.75` | STRONG | Y | STRONG | The matter density PDF for modified gravity and dark energy  |
| `0.75` | STRONG | Y | STRONG | Assessment of Deep Learning Segmentation for Real-Time Free- |
| `0.75` | STRONG | Y | — | UPop: Unified and Progressive Pruning for Compressing Vision |
| `0.75` | STRONG | Y | STRONG | Learning to Adversarially Blur Visual Object Tracking |
| `0.75` | STRONG | Y | STRONG | ConsInstancy: Learning Instance Representations for Semi-Sup |
| `0.75` | STRONG | Y | STRONG | FairSync: Ensuring Amortized Group Exposure in Distributed R |
| `0.75` | STRONG | Y | STRONG | Reliable Fidelity and Diversity Metrics for Generative Model |
| `0.75` | STRONG | Y | STRONG | End-to-End Label Uncertainty Modeling in Speech Emotion Reco |
| `0.75` | STRONG | Y | STRONG | Improving Query Representations for Dense Retrieval with Pse |
| `0.75` | STRONG | Y | STRONG | Enhancing Feature Diversity Boosts Channel-Adaptive Vision T |
| `0.75` | STRONG | Y | STRONG | Adaptive Topological Feature via Persistent Homology: Filtra |
| `0.75` | STRONG | Y | STRONG | Environmental Sound Classification on the Edge: A Pipeline f |
| `0.75` | STRONG | Y | STRONG | Robust Outlier Detection Method Based on Local Entropy and G |
| `0.75` | STRONG | Y | STRONG | Tree Prompting: Efficient Task Adaptation without Fine-Tunin |
| `0.75` | STRONG | Y | STRONG | Permutationally Invariant Networks for Enhanced Sampling (PI |
| `0.75` | STRONG | Y | — | Harmony: A Joint Self-Supervised and Weakly-Supervised Frame |
| `0.75` | STRONG | Y | STRONG | Multi-News: a Large-Scale Multi-Document Summarization Datas |
| `0.75` | STRONG | Y | STRONG | NTK-Guided Few-Shot Class Incremental Learning |
| `0.75` | STRONG | Y | STRONG | Improving AMR Parsing with Sequence-to-Sequence Pre-training |
| `0.75` | STRONG | Y | STRONG | Reservoir computing approaches for representation and classi |
| `0.75` | STRONG | Y | STRONG | ChemCrow: Augmenting large-language models with chemistry to |
| `0.75` | STRONG | Y | — | Noisy Boundaries: Lemon or Lemonade for Semi-supervised Inst |
| `0.75` | STRONG | Y | — | End-to-End Supermask Pruning: Learning to Prune Image Captio |
| `0.75` | STRONG | Y | STRONG | BraTS orchestrator : Democratizing and Disseminating state-o |
| `0.75` | STRONG | Y | — | Spatio-Temporal Wind Speed Forecasting using Graph Networks  |
| `0.75` | STRONG | Y | STRONG | PAD: Phase-Amplitude Decoupling Fusion for Multi-Modal Land  |
| `0.75` | STRONG | Y | STRONG | A Missing Data Imputation GAN for Character Sprite Generatio |
| `0.75` | STRONG | Y | STRONG | Neural Relational Inference with Fast Modular Meta-learning |
| `0.75` | STRONG | Y | STRONG | TRIDENT: Tri-modal Real-time Intrusion Detection Engine for  |
| `0.75` | STRONG | Y | STRONG | Lightplane: Highly-Scalable Components for Neural 3D Fields |
| `0.75` | STRONG | Y | STRONG | Learning discrete Lagrangians for variational PDEs from data |
| `0.75` | STRONG | Y | — | A Keypoint-based Global Association Network for Lane Detecti |
| `0.75` | STRONG | Y | STRONG | ConceptLab: Creative Concept Generation using VLM-Guided Dif |
| `0.75` | STRONG | Y | STRONG | MARS-Gym: A Gym framework to model, train, and evaluate Reco |
| `0.75` | STRONG | Y | STRONG | Set You Straight: Auto-Steering Denoising Trajectories to Si |
| `0.75` | STRONG | Y | STRONG | Mapping Supervised Bilingual Word Embeddings from English to |
| `0.75` | STRONG | Y | STRONG | Modality Distillation with Multiple Stream Networks for Acti |
| `0.75` | STRONG | Y | STRONG | Richer Convolutional Features for Edge Detection |
| `0.75` | STRONG | Y | STRONG | LIONs: An Empirically Optimized Approach to Align Language M |
| `0.75` | STRONG | Y | STRONG | FunASR: A Fundamental End-to-End Speech Recognition Toolkit |
| `0.75` | STRONG | Y | STRONG | Tracking Fringe and Coordinated Activity on Twitter Leading  |
| `0.75` | STRONG | Y | STRONG | TAPER: Time-Aware Patient EHR Representation |
| `0.75` | STRONG | Y | STRONG | Beyond Correlation: A Path-Invariant Measure for Seismogram  |
| `0.75` | STRONG | Y | STRONG | Contrastive Self-Supervised Learning Based Approach for Pati |
| `0.75` | STRONG | Y | STRONG | Audio-based AI classifiers show no evidence of improved COVI |
| `0.75` | STRONG | Y | — | Assessing Phrasal Representation and Composition in Transfor |
| `0.75` | STRONG | Y | STRONG | Multiscale Quantile Regression with Local Error Control |
| `0.75` | STRONG | Y | — | Improving Rare Word Translation With Dictionaries and Attent |
| `0.75` | STRONG | Y | STRONG | Dual Adaptive Representation Alignment for Cross-domain Few- |
| `0.75` | STRONG | Y | STRONG | Neural Architecture Search for Compressed Sensing Magnetic R |
| `0.75` | STRONG | Y | STRONG | A Data-Driven Aggressive Autonomous Racing Framework Utilizi |
| `0.75` | STRONG | Y | STRONG | Dodrio: Exploring Transformer Models with Interactive Visual |
| `0.75` | STRONG | Y | STRONG | Visual Grounding Methods for VQA are Working for the Wrong R |
| `0.75` | STRONG | Y | STRONG | Three approaches to facilitate DNN generalization to objects |
| `0.75` | STRONG | Y | STRONG | Actor-Critic Instance Segmentation |
| `0.75` | STRONG | Y | STRONG | Bending the Future: Autoregressive Modeling of Temporal Know |
| `0.75` | STRONG | Y | STRONG | RSANet: Recurrent Slice-wise Attention Network for Multiple  |
| `0.75` | STRONG | Y | STRONG | Benchmarking and Understanding Compositional Relational Reas |
| `0.75` | STRONG | Y | STRONG | Elevating Skeleton-Based Action Recognition with Efficient M |
| `0.75` | STRONG | Y | STRONG | Descriptor-based Foundation Models for Molecular Property Pr |
| `0.75` | STRONG | Y | STRONG | BanditSum: Extractive Summarization as a Contextual Bandit |
| `0.75` | STRONG | Y | STRONG | AV-CrossNet: an Audiovisual Complex Spectral Mapping Network |
| `0.75` | STRONG | Y | STRONG | Closing the Curious Case of Neural Text Degeneration |
| `0.75` | STRONG | Y | STRONG | DyRRen: A Dynamic Retriever-Reranker-Generator Model for Num |
| `0.75` | STRONG | Y | STRONG | Simple multi-dataset detection |
| `0.75` | STRONG | Y | — | OneNet: Enhancing Time Series Forecasting Models under Conce |
| `0.75` | STRONG | Y | STRONG | Dual Learning for Semi-Supervised Natural Language Understan |
| `0.75` | STRONG | Y | STRONG | CosmiXs: Improved spectra for dark matter indirect detection |
| `0.75` | STRONG | Y | STRONG | Speaker Anonymization with Phonetic Intermediate Representat |
| `0.75` | STRONG | Y | — | LFZip: Lossy compression of multivariate floating-point time |
| `0.75` | STRONG | Y | STRONG | Computing Multiple Image Reconstructions with a Single Hyper |
| `0.75` | STRONG | Y | — | LEEETs-Dial: Linguistic Entrainment in End-to-End Task-orien |
| `0.75` | STRONG | Y | STRONG | CDGP: Automatic Cloze Distractor Generation based on Pre-tra |
| `0.75` | STRONG | Y | STRONG | Semi-Supervised Panoptic Narrative Grounding |
| `0.75` | STRONG | Y | STRONG | EMORL: Ensemble Multi-Objective Reinforcement Learning for E |
| `0.75` | STRONG | Y | STRONG | NeRP: Implicit Neural Representation Learning with Prior Emb |
| `0.75` | STRONG | Y | STRONG | Decision-centric fairness: Evaluation and optimization for r |
| `0.75` | STRONG | Y | — | UniNet: A Unified Scene Understanding Network and Exploring  |
| `0.75` | STRONG | Y | STRONG | SPATL: Salient Parameter Aggregation and Transfer Learning f |
| `0.75` | STRONG | Y | STRONG | P$^2$-ViT: Power-of-Two Post-Training Quantization and Accel |
| `0.75` | STRONG | Y | STRONG | OpenDelta: A Plug-and-play Library for Parameter-efficient A |
| `0.75` | STRONG | Y | STRONG | ViPNAS: Efficient Video Pose Estimation via Neural Architect |
| `0.75` | STRONG | Y | STRONG | PRO-V: An Efficient Program Generation Multi-Agent System fo |
| `0.75` | STRONG | Y | STRONG | HADES: Homologous Automated Document Exploration and Summari |
| `0.75` | STRONG | Y | STRONG | Cross-domain Detection via Graph-induced Prototype Alignment |

### Near MEDIUM threshold (0.45 ± 0.05): 364 pairs

| Score | Level | Official | LLM | Title |
|---|---|---|---|---|
| `0.5` | MEDIUM | Y | STRONG | Ensemble Kalman Methods: A Mean Field Perspective |
| `0.5` | MEDIUM | N | STRONG | Towards Cross-Tokenizer Distillation: the Universal Logit Di |
| `0.5` | MEDIUM | N | STRONG | An End-to-End Architecture for Keyword Spotting and Voice Ac |
| `0.5` | MEDIUM | Y | STRONG | Aligning Query Representation with Rewritten Query and Relev |
| `0.5` | MEDIUM | N | STRONG | EESEN: End-to-End Speech Recognition using Deep RNN Models a |
| `0.5` | MEDIUM | N | WEAK | Conditional Image Synthesis With Auxiliary Classifier GANs |
| `0.5` | MEDIUM | N | STRONG | HigherHRNet: Scale-Aware Representation Learning for Bottom- |
| `0.5` | MEDIUM | N | STRONG | Vitruvion: A Generative Model of Parametric CAD Sketches |
| `0.5` | MEDIUM | Y | STRONG | Interpretable Concept Bottlenecks to Align Reinforcement Lea |
| `0.5` | MEDIUM | Y | STRONG | CritiPrefill: A Segment-wise Criticality-based Approach for  |
| `0.5` | MEDIUM | N | STRONG | Automatic Speech Recognition Benchmark for Air-Traffic Commu |
| `0.5` | MEDIUM | N | STRONG | Link Prediction Based on Graph Neural Networks |
| `0.5` | MEDIUM | N | STRONG | Ridiculously Fast Shot Boundary Detection with Fully Convolu |
| `0.5` | MEDIUM | N | STRONG | PointNet: Deep Learning on Point Sets for 3D Classification  |
| `0.5` | MEDIUM | N | STRONG | Map3D: Registration Based Multi-Object Tracking on 3D Serial |
| `0.5` | MEDIUM | Y | STRONG | Targeting SARS-CoV-2 with AI- and HPC-enabled Lead Generatio |
| `0.5` | MEDIUM | Y | STRONG | Garden optimization problems for benchmarking quantum anneal |
| `0.5` | MEDIUM | Y | STRONG | Efficient Monte Carlo Tree Search via On-the-Fly State-Condi |
| `0.5` | MEDIUM | Y | STRONG | Weighted asymmetric least squares regression with fixed-effe |
| `0.5` | MEDIUM | N | STRONG | SegNet: A Deep Convolutional Encoder-Decoder Architecture fo |
| `0.5` | MEDIUM | N | STRONG | YOLACT++: Better Real-time Instance Segmentation |
| `0.5` | MEDIUM | Y | WEAK | A two-dimensional stabilized discontinuous Galerkin method o |
| `0.5` | MEDIUM | N | STRONG | Deep Preset: Blending and Retouching Photos with Color Style |
| `0.5` | MEDIUM | N | STRONG | HierVL: Learning Hierarchical Video-Language Embeddings |
| `0.5` | MEDIUM | N | STRONG | DeepTraffic: Crowdsourced Hyperparameter Tuning of Deep Rein |
| `0.5` | MEDIUM | Y | MEDIUM | StrongSORT: Make DeepSORT Great Again |
| `0.5` | MEDIUM | Y | STRONG | DTDN: Dual-task De-raining Network |
| `0.5` | MEDIUM | N | STRONG | Logic Tensor Networks for Semantic Image Interpretation |
| `0.5` | MEDIUM | N | STRONG | StyleTTS 2: Towards Human-Level Text-to-Speech through Style |
| `0.5` | MEDIUM | N | STRONG | Sentence-BERT: Sentence Embeddings using Siamese BERT-Networ |
| `0.5` | MEDIUM | N | STRONG | Real Time Pear Fruit Detection and Counting Using YOLOv4 Mod |
| `0.5` | MEDIUM | Y | WEAK | SeqGenSQL -- A Robust Sequence Generation Model for Structur |
| `0.5` | MEDIUM | N | STRONG | A Novel Use of Discrete Wavelet Transform Features in the Pr |
| `0.5` | MEDIUM | Y | STRONG | Visualisation and 'diagnostic classifiers' reveal how recurr |
| `0.5` | MEDIUM | N | STRONG | Deep High-Resolution Representation Learning for Human Pose  |
| `0.5` | MEDIUM | Y | MEDIUM | Solving the Resource Constrained Project Scheduling Problem  |
| `0.5` | MEDIUM | Y | STRONG | An Event-Driven Approach for Studying Gene Block Evolution i |
| `0.5` | MEDIUM | N | WEAK | Diffusion Models Beat GANs on Image Synthesis |
| `0.5` | MEDIUM | Y | STRONG | Transformer Architecture for NetsDB |
| `0.5` | MEDIUM | N | STRONG | Adaptive Network Sparsification with Dependent Variational B |
| `0.5` | MEDIUM | Y | WEAK | Three things everyone should know about Vision Transformers |
| `0.5` | MEDIUM | N | STRONG | Learning Spatiotemporal Occupancy Grid Maps for Lifelong Nav |
| `0.5` | MEDIUM | Y | STRONG | Experimental Shake Gesture Detection API for Apple Watch |
| `0.5` | MEDIUM | Y | STRONG | Aligning Knowledge Concepts to Whole Slide Images for Precis |
| `0.5` | MEDIUM | N | STRONG | FedCD: Improving Performance in non-IID Federated Learning |
| `0.5` | MEDIUM | Y | WEAK | Max-Margin Token Selection in Attention Mechanism |
| `0.5` | MEDIUM | Y | WEAK | MatrixNet: Learning over symmetry groups using learned group |
| `0.5` | MEDIUM | N | STRONG | Object-driven Text-to-Image Synthesis via Adversarial Traini |
| `0.5` | MEDIUM | N | STRONG | K-Adapter: Infusing Knowledge into Pre-Trained Models with A |
| `0.5` | MEDIUM | Y | MEDIUM | PHEMEPlus: Enriching Social Media Rumour Verification with E |
| `0.5` | MEDIUM | N | STRONG | SPLICE: A Synthetic Paid Loss and Incurred Cost Experience S |
| `0.5` | MEDIUM | N | STRONG | FitNets: Hints for Thin Deep Nets |
| `0.5` | MEDIUM | N | STRONG | PCN: Point Completion Network |
| `0.5` | MEDIUM | N | STRONG | ReconNet: Non-Iterative Reconstruction of Images from Compre |
| `0.5` | MEDIUM | N | STRONG | Aggregated Residual Transformations for Deep Neural Networks |
| `0.5` | MEDIUM | N | STRONG | Relation Networks for Object Detection |
| `0.5` | MEDIUM | N | STRONG | Towards 3D Human Pose Estimation in the Wild: a Weakly-super |
| `0.5` | MEDIUM | Y | WEAK | Few-shot Personalized Scanpath Prediction |
| `0.5` | MEDIUM | N | STRONG | From Planes to Corners: Multi-Purpose Primitive Detection in |
| `0.5` | MEDIUM | Y | STRONG | Energetic closure of the spatially resolved global food syst |
| `0.5` | MEDIUM | Y | STRONG | Downstream Transformer Generation of Question-Answer Pairs w |
| `0.5` | MEDIUM | N | STRONG | Stacked Cross Attention for Image-Text Matching |
| `0.5` | MEDIUM | Y | STRONG | Intra-video Positive Pairs in Self-Supervised Learning for U |
| `0.5` | MEDIUM | N | MEDIUM | Visual Compositional Learning for Human-Object Interaction D |
| `0.5` | MEDIUM | N | STRONG | QaNER: Prompting Question Answering Models for Few-shot Name |
| `0.5` | MEDIUM | N | STRONG | PrObeD: Proactive Object Detection Wrapper |
| `0.5` | MEDIUM | N | MEDIUM | HarDNet: A Low Memory Traffic Network |
| `0.5` | MEDIUM | N | STRONG | Social NCE: Contrastive Learning of Socially-aware Motion Re |
| `0.5` | MEDIUM | Y | STRONG | Multi-View Picking: Next-best-view Reaching for Improved Gra |
| `0.5` | MEDIUM | Y | WEAK | Do LLMs Implicitly Determine the Suitable Text Difficulty fo |
| `0.5` | MEDIUM | N | STRONG | MolGAN: An implicit generative model for small molecular gra |
| `0.5` | MEDIUM | N | STRONG | ChemDFM: A Large Language Foundation Model for Chemistry |
| `0.5` | MEDIUM | N | STRONG | Multi-level Attention Model for Weakly Supervised Audio Clas |
| `0.5` | MEDIUM | N | STRONG | Where are the Masks: Instance Segmentation with Image-level  |
| `0.5` | MEDIUM | N | STRONG | CoupleNet: Coupling Global Structure with Local Parts for Ob |
| `0.5` | MEDIUM | N | MEDIUM | WizardMath: Empowering Mathematical Reasoning for Large Lang |
| `0.5` | MEDIUM | N | MEDIUM | MULAN: Multitask Universal Lesion Analysis Network for Joint |
| `0.5` | MEDIUM | Y | STRONG | MERTech: Instrument Playing Technique Detection Using Self-S |
| `0.5` | MEDIUM | N | STRONG | HoroPCA: Hyperbolic Dimensionality Reduction via Horospheric |
| `0.5` | MEDIUM | N | STRONG | Synchronous Bidirectional Neural Machine Translation |
| `0.5` | MEDIUM | N | STRONG | ODDN: Addressing Unpaired Data Challenges in Open-World Deep |
| `0.5` | MEDIUM | Y | MEDIUM | Optimization of Non-Equilibrium Self-Assembly Protocols Usin |
| `0.5` | MEDIUM | N | STRONG | HunyuanVideo: A Systematic Framework For Large Video Generat |
| `0.5` | MEDIUM | N | STRONG | On Embeddings for Numerical Features in Tabular Deep Learnin |
| `0.5` | MEDIUM | Y | MEDIUM | Revising the stochastic iterative ensemble smoother |
| `0.5` | MEDIUM | N | STRONG | Boosting Soft Actor-Critic: Emphasizing Recent Experience wi |
| `0.5` | MEDIUM | N | STRONG | COCO-Stuff: Thing and Stuff Classes in Context |
| `0.5` | MEDIUM | Y | MEDIUM | Learning Zero-Sum Linear Quadratic Games with Improved Sampl |
| `0.5` | MEDIUM | N | STRONG | Simple Contrastive Representation Learning for Time Series F |
| `0.5` | MEDIUM | N | MEDIUM | Social GAN: Socially Acceptable Trajectories with Generative |
| `0.5` | MEDIUM | N | STRONG | When Being Unseen from mBERT is just the Beginning: Handling |
| `0.5` | MEDIUM | Y | STRONG | Automated Performance Testing Based on Active Deep Learning |
| `0.5` | MEDIUM | N | STRONG | Tracklet-Switch Adversarial Attack against Pedestrian Multi- |
| `0.5` | MEDIUM | Y | MEDIUM | The Photo-Astrometric Vertical Tracer Density of the Milky W |
| `0.5` | MEDIUM | N | STRONG | The First Few Tokens Are All You Need: An Efficient and Effe |
| `0.5` | MEDIUM | Y | STRONG | Towards Effective Discrimination Testing for Generative AI |
| `0.5` | MEDIUM | N | STRONG | The completed SDSS-IV extended Baryon Oscillation Spectrosco |
| `0.5` | MEDIUM | N | STRONG | Data Distributional Properties Drive Emergent In-Context Lea |
| `0.5` | MEDIUM | Y | MEDIUM | Damage and recovery of flagella in soil bacteria exposed to  |
| `0.5` | MEDIUM | Y | WEAK | BigDL 2.0: Seamless Scaling of AI Pipelines from Laptops to  |
| `0.5` | MEDIUM | Y | STRONG | ContactOpt: Optimizing Contact to Improve Grasps |
| `0.5` | MEDIUM | N | STRONG | PCT: Point cloud transformer |
| `0.5` | MEDIUM | Y | STRONG | Efficient Compression of Overparameterized Deep Models throu |
| `0.5` | MEDIUM | Y | STRONG | One Law, Many Languages: Benchmarking Multilingual Legal Rea |
| `0.5` | MEDIUM | N | STRONG | Knowledge-aware Graph Neural Networks with Label Smoothness  |
| `0.5` | MEDIUM | N | MEDIUM | Pix2seq: A Language Modeling Framework for Object Detection |
| `0.5` | MEDIUM | Y | WEAK | LSRFormer: Efficient Transformer Supply Convolutional Neural |
| `0.5` | MEDIUM | Y | STRONG | Language-Grounded Dynamic Scene Graphs for Interactive Objec |
| `0.5` | MEDIUM | Y | STRONG | Closing the Generalization Gap of Adaptive Gradient Methods  |
| `0.5` | MEDIUM | Y | STRONG | Sample Selection via Contrastive Fragmentation for Noisy Lab |
| `0.5` | MEDIUM | Y | MEDIUM | Weakly supervised cross-modal learning in high-content scree |
| `0.5` | MEDIUM | N | STRONG | 360SD-Net: 360° Stereo Depth Estimation with Learnable Cost  |
| `0.5` | MEDIUM | N | STRONG | OpenBox: A Generalized Black-box Optimization Service |
| `0.5` | MEDIUM | N | STRONG | Distance-IoU Loss: Faster and Better Learning for Bounding B |
| `0.5` | MEDIUM | N | STRONG | Robot Navigation with Map-Based Deep Reinforcement Learning |
| `0.5` | MEDIUM | N | STRONG | FSSD: Feature Fusion Single Shot Multibox Detector |
| `0.5` | MEDIUM | N | STRONG | Efficient Ladder-style DenseNets for Semantic Segmentation o |
| `0.5` | MEDIUM | N | STRONG | Instant-Teaching: An End-to-End Semi-Supervised Object Detec |
| `0.5` | MEDIUM | Y | MEDIUM | Hate Speech Detection: A Solved Problem? The Challenging Cas |
| `0.5` | MEDIUM | Y | STRONG | Clustering of Big Data with Mixed Features |
| `0.5` | MEDIUM | N | STRONG | A Note on Connecting Barlow Twins with Negative-Sample-Free  |
| `0.5` | MEDIUM | N | STRONG | Bayesian Batch Active Learning as Sparse Subset Approximatio |
| `0.5` | MEDIUM | N | MEDIUM | Defense for Black-box Attacks on Anti-spoofing Models by Sel |
| `0.5` | MEDIUM | Y | STRONG | Nested Sampling with Normalising Flows for Gravitational-Wav |
| `0.5` | MEDIUM | N | STRONG | Few-Shot Learning with Graph Neural Networks |
| `0.5` | MEDIUM | N | STRONG | Unsupervised Multiple Choices Question Answering: Start Lear |
| `0.5` | MEDIUM | Y | MEDIUM | RD-VIO: Robust Visual-Inertial Odometry for Mobile Augmented |
| `0.45` | MEDIUM | Y | STRONG | One-shot World Models Using a Transformer Trained on a Synth |
| `0.45` | MEDIUM | Y | STRONG | Sample Condensation in Online Continual Learning |
| `0.45` | MEDIUM | N | WEAK | Feature Pyramid Networks for Object Detection |
| `0.45` | MEDIUM | N | MEDIUM | Improving Nighttime Driving-Scene Segmentation via Dual Imag |
| `0.45` | MEDIUM | Y | STRONG | Exploring the Determinants of Pedestrian Crash Severity Usin |
| `0.45` | MEDIUM | Y | WEAK | A chemo-dynamical link between the Gj\"oll stream and NGC 32 |
| `0.45` | MEDIUM | Y | STRONG | FaceX: Understanding Face Attribute Classifiers through Summ |
| `0.45` | MEDIUM | N | STRONG | SinGAN: Learning a Generative Model from a Single Natural Im |
| `0.45` | MEDIUM | Y | WEAK | DG-Trans: Dual-level Graph Transformer for Spatiotemporal In |
| `0.45` | MEDIUM | N | STRONG | Deep learning methods allow fully automated segmentation of  |
| `0.45` | MEDIUM | Y | STRONG | The language of mental health problems in social media |
| `0.45` | MEDIUM | N | STRONG | MIST: A Simple and Scalable End-To-End 3D Medical Imaging Se |
| `0.45` | MEDIUM | Y | STRONG | A Blackbox Yield Estimation Workflow with Gaussian Process R |
| `0.45` | MEDIUM | N | STRONG | G-Retriever: Retrieval-Augmented Generation for Textual Grap |
| `0.45` | MEDIUM | N | STRONG | Hybrid Deep Network for Anomaly Detection |
| `0.45` | MEDIUM | N | STRONG | Adaptive-Halting Policy Network for Early Classification |
| `0.45` | MEDIUM | Y | WEAK | SEENN: Towards Temporal Spiking Early Exit Neural Networks |
| `0.45` | MEDIUM | Y | STRONG | Differential Privacy Has Disparate Impact on Model Accuracy |
| `0.45` | MEDIUM | N | STRONG | A Large-scale Dataset for Hate Speech Detection on Vietnames |
| `0.45` | MEDIUM | N | STRONG | NeRF-Supervised Deep Stereo |
| `0.45` | MEDIUM | N | STRONG | A C-LSTM Neural Network for Text Classification |
| `0.45` | MEDIUM | N | MEDIUM | BanditPAM: Almost Linear Time $k$-Medoids Clustering via Mul |
| `0.45` | MEDIUM | N | MEDIUM | ParetoQ: Scaling Laws in Extremely Low-bit LLM Quantization |
| `0.45` | MEDIUM | Y | MEDIUM | The Rhythms of the Night: increase in online night activity  |
| `0.45` | MEDIUM | Y | STRONG | MuJoCo MPC for Humanoid Control: Evaluation on HumanoidBench |
| `0.45` | MEDIUM | N | STRONG | Semi-Supervised Learning with Ladder Networks |
| `0.45` | MEDIUM | N | STRONG | node2vec: Scalable Feature Learning for Networks |
| `0.45` | MEDIUM | Y | MEDIUM | PDFA Distillation via String Probability Queries |
| `0.45` | MEDIUM | Y | STRONG | Linear Causal Bandits: Unknown Graph and Soft Interventions |
| `0.45` | MEDIUM | N | STRONG | Residual Correlation in Graph Neural Network Regression |
| `0.45` | MEDIUM | N | STRONG | DeepBlindness: Fast Blindness Map Estimation and Blindness T |
| `0.45` | MEDIUM | N | STRONG | Convolutional Neural Networks with Alternately Updated Cliqu |
| `0.45` | MEDIUM | N | STRONG | Attention Is All You Need |
| `0.45` | MEDIUM | N | STRONG | A Style-Aware Content Loss for Real-time HD Style Transfer |
| `0.45` | MEDIUM | Y | STRONG | Split-PU: Hardness-aware Training Strategy for Positive-Unla |
| `0.45` | MEDIUM | Y | STRONG | Secure Safety Filter: Towards Safe Flight Control under Sens |
| `0.45` | MEDIUM | N | STRONG | Deformable ConvNets v2: More Deformable, Better Results |
| `0.45` | MEDIUM | N | MEDIUM | FOSTER: Feature Boosting and Compression for Class-Increment |
| `0.45` | MEDIUM | N | STRONG | A Novel Benchmark and Dataset for Efficient 3D Gaussian Spla |
| `0.45` | MEDIUM | N | STRONG | Searching for Exoplanets Using Artificial Intelligence |
| `0.45` | MEDIUM | N | STRONG | No Reason for No Supervision: Improved Generalization in Sup |
| `0.45` | MEDIUM | N | STRONG | Free as in Free Word Order: An Energy Based Model for Word S |
| `0.45` | MEDIUM | N | STRONG | Generalized Focal Loss: Learning Qualified and Distributed B |
| `0.45` | MEDIUM | N | STRONG | Reverse Attention for Salient Object Detection |
| `0.45` | MEDIUM | N | STRONG | Modeling Tabular data using Conditional GAN |
| `0.45` | MEDIUM | N | STRONG | Low-effort place recognition with WiFi fingerprints using de |
| `0.45` | MEDIUM | Y | STRONG | Topological Embedding of Human Brain Networks with Applicati |
| `0.45` | MEDIUM | N | STRONG | Forget-free Continual Learning with Winning Subnetworks |
| `0.45` | MEDIUM | N | MEDIUM | AdaSpeech: Adaptive Text to Speech for Custom Voice |
| `0.45` | MEDIUM | Y | STRONG | Modeling chemistry during star formation: Water deuteration  |
| `0.45` | MEDIUM | N | STRONG | FCOS: Fully Convolutional One-Stage Object Detection |
| `0.45` | MEDIUM | N | STRONG | Hybrid Search for Efficient Planning with Completeness Guara |
| `0.45` | MEDIUM | N | STRONG | Joint Face Detection and Alignment using Multi-task Cascaded |
| `0.45` | MEDIUM | Y | MEDIUM | APIA: An Architecture for Policy-Aware Intentional Agents |
| `0.45` | MEDIUM | N | STRONG | Letter-Based Speech Recognition with Gated ConvNets |
| `0.45` | MEDIUM | N | STRONG | Cascade Cost Volume for High-Resolution Multi-View Stereo an |
| `0.45` | MEDIUM | N | STRONG | Learning K-way D-dimensional Discrete Codes for Compact Embe |
| `0.45` | MEDIUM | N | STRONG | PPF-FoldNet: Unsupervised Learning of Rotation Invariant 3D  |
| `0.45` | MEDIUM | N | STRONG | Character-level Convolutional Networks for Text Classificati |
| `0.45` | MEDIUM | N | STRONG | Controlled abstention neural networks for identifying skillf |
| `0.45` | MEDIUM | Y | MEDIUM | MuS2: A Real-World Benchmark for Sentinel-2 Multi-Image Supe |
| `0.45` | MEDIUM | N | STRONG | Drawing Early-Bird Tickets: Towards More Efficient Training  |
| `0.45` | MEDIUM | N | STRONG | Holistically-Nested Edge Detection |
| `0.45` | MEDIUM | N | STRONG | Colorful Image Colorization |
| `0.45` | MEDIUM | N | WEAK | Road Extraction by Deep Residual U-Net |
| `0.45` | MEDIUM | N | STRONG | The Design and Implementation of a Real Time Visual Search S |
| `0.45` | MEDIUM | Y | STRONG | Natural Reference Frames within Video Analysis |
| `0.45` | MEDIUM | Y | STRONG | Towards Exact Computation of Inductive Bias |
| `0.45` | MEDIUM | N | STRONG | A joint separation-classification model for sound event dete |
| `0.45` | MEDIUM | N | STRONG | AixBench: A Code Generation Benchmark Dataset |
| `0.45` | MEDIUM | N | STRONG | Unsupervised Deep Learning for Structured Shape Matching |
| `0.45` | MEDIUM | Y | WEAK | Bi-Sparse Unsupervised Feature Selection |
| `0.45` | MEDIUM | Y | STRONG | The dynamics and outcome of star formation with jets, radiat |
| `0.45` | MEDIUM | N | WEAK | StackGAN: Text to Photo-realistic Image Synthesis with Stack |
| `0.45` | MEDIUM | Y | STRONG | Towards gaze-independent c-VEP BCI: A pilot study |
| `0.45` | MEDIUM | Y | WEAK | Schema2QA: High-Quality and Low-Cost Q&A Agents for the Stru |
| `0.45` | MEDIUM | Y | WEAK | The Role of Publicly Available Data in MICCAI Papers from 20 |
| `0.45` | MEDIUM | N | STRONG | PaLM-E: An Embodied Multimodal Language Model |
| `0.45` | MEDIUM | Y | STRONG | MVTec AD -- A Comprehensive Real-World Dataset for Unsupervi |
| `0.45` | MEDIUM | Y | STRONG | Cluster-guided Asymmetric Contrastive Learning for Unsupervi |
| `0.45` | MEDIUM | Y | MEDIUM | FeynCalc 9 |
| `0.45` | MEDIUM | Y | MEDIUM | Enhancing Sequence-to-Sequence Neural Lemmatization with Ext |
| `0.45` | MEDIUM | Y | WEAK | Theoretical analysis and computation of the sample Frechet m |
| `0.45` | MEDIUM | N | STRONG | Simple BERT Models for Relation Extraction and Semantic Role |
| `0.45` | MEDIUM | Y | WEAK | UCC: Uncertainty guided Cross-head Co-training for Semi-Supe |
| `0.45` | MEDIUM | N | STRONG | Potential Gap: Using Reactive Policies to Guarantee Safe Nav |
| `0.45` | MEDIUM | Y | MEDIUM | LLMs' morphological analyses of complex FST-generated Finnis |
| `0.45` | MEDIUM | N | STRONG | Speaking the Same Language: Matching Machine to Human Captio |
| `0.45` | MEDIUM | N | STRONG | Robust Burned Area Delineation through Multitask Learning |
| `0.45` | MEDIUM | N | STRONG | YOLO9000: Better, Faster, Stronger |
| `0.45` | MEDIUM | Y | STRONG | Instantaneous PSD Estimation for Speech Enhancement based on |
| `0.45` | MEDIUM | Y | WEAK | Quantum Error Mitigation |
| `0.45` | MEDIUM | Y | WEAK | Bilevel Coreset Selection in Continual Learning: A New Formu |
| `0.45` | MEDIUM | N | STRONG | Community-based Outlier Detection for Edge-attributed Graphs |
| `0.45` | MEDIUM | N | STRONG | Single Shot Scene Text Retrieval |
| `0.45` | MEDIUM | N | STRONG | Enhancing the Protein Tertiary Structure Prediction by Multi |
| `0.45` | MEDIUM | N | STRONG | ns3-gym: Extending OpenAI Gym for Networking Research |
| `0.45` | MEDIUM | Y | STRONG | The integration of angular velocity |
| `0.45` | MEDIUM | N | MEDIUM | Multi-layer Representation Fusion for Neural Machine Transla |
| `0.45` | MEDIUM | N | STRONG | CodeGeeX: A Pre-Trained Model for Code Generation with Multi |
| `0.45` | MEDIUM | N | STRONG | A large annotated medical image dataset for the development  |
| `0.45` | MEDIUM | N | STRONG | Zero-Shot Learning -- A Comprehensive Evaluation of the Good |
| `0.45` | MEDIUM | N | MEDIUM | EfficientDet: Scalable and Efficient Object Detection |
| `0.45` | MEDIUM | N | STRONG | GAMA: A Large Audio-Language Model with Advanced Audio Under |
| `0.45` | MEDIUM | N | STRONG | Sound Event Localization and Detection of Overlapping Source |
| `0.45` | MEDIUM | Y | WEAK | Rejuvenated accretors have less bound envelopes: Impact of R |
| `0.45` | MEDIUM | N | STRONG | Framing U-Net via Deep Convolutional Framelets: Application  |
| `0.45` | MEDIUM | N | MEDIUM | Decoupling Representation and Classifier for Long-Tailed Rec |
| `0.45` | MEDIUM | Y | STRONG | Toward Aligning Human and Robot Actions via Multi-Modal Demo |
| `0.45` | MEDIUM | N | MEDIUM | Wide Residual Networks |
| `0.45` | MEDIUM | N | STRONG | SimCSE: Simple Contrastive Learning of Sentence Embeddings |
| `0.45` | MEDIUM | N | MEDIUM | SRFlow: Learning the Super-Resolution Space with Normalizing |
| `0.45` | MEDIUM | N | STRONG | Multi-Anchor Active Domain Adaptation for Semantic Segmentat |
| `0.45` | MEDIUM | Y | STRONG | Supercomputing tensor networks for U(1) symmetric quantum ma |
| `0.45` | MEDIUM | N | STRONG | SIDA: Social Media Image Deepfake Detection, Localization an |
| `0.45` | MEDIUM | N | STRONG | R$^2$-Gaussian: Rectifying Radiative Gaussian Splatting for  |
| `0.45` | MEDIUM | N | STRONG | ChamNet: Towards Efficient Network Design through Platform-A |
| `0.45` | MEDIUM | N | STRONG | RobustTP: End-to-End Trajectory Prediction for Heterogeneous |
| `0.45` | MEDIUM | Y | MEDIUM | A new Linear Time Bi-level $\ell_{1,\infty}$ projection ; Ap |
| `0.45` | MEDIUM | N | STRONG | Hierarchical Graph Representation Learning with Differentiab |
| `0.45` | MEDIUM | Y | WEAK | Redistributing Low-Frequency Words: Making the Most of Monol |
| `0.45` | MEDIUM | N | STRONG | Sparse eigenbasis approximation: multiple feature extraction |
| `0.45` | MEDIUM | N | STRONG | High-Resolution Image Inpainting with Iterative Confidence F |
| `0.45` | MEDIUM | N | STRONG | GloDyNE: Global Topology Preserving Dynamic Network Embeddin |
| `0.45` | MEDIUM | N | STRONG | Physical Attack on Monocular Depth Estimation with Optimal A |
| `0.45` | MEDIUM | N | STRONG | Fast unfolding of communities in large networks |
| `0.45` | MEDIUM | N | STRONG | Multi-Object Representation Learning with Iterative Variatio |
| `0.45` | MEDIUM | N | STRONG | Panther: Fast Top-k Similarity Search in Large Networks |
| `0.45` | MEDIUM | N | STRONG | Aerial Map-Based Navigation Using Semantic Segmentation and  |
| `0.45` | MEDIUM | N | WEAK | HGRN2: Gated Linear RNNs with State Expansion |
| `0.45` | MEDIUM | N | STRONG | GroupCDL: Interpretable Denoising and Compressed Sensing MRI |
| `0.45` | MEDIUM | Y | STRONG | Winner-takes-all learners are geometry-aware conditional den |
| `0.45` | MEDIUM | N | STRONG | Neural AMR: Sequence-to-Sequence Models for Parsing and Gene |
| `0.45` | MEDIUM | Y | STRONG | Probabilistic Decomposed Linear Dynamical Systems for Robust |
| `0.45` | MEDIUM | N | STRONG | A Sensitivity Analysis of (and Practitioners' Guide to) Conv |
| `0.45` | MEDIUM | N | STRONG | HOME: Heatmap Output for future Motion Estimation |
| `0.45` | MEDIUM | Y | STRONG | Graph Anomaly Detection with Unsupervised GNNs |
| `0.45` | MEDIUM | Y | STRONG | AI Expands Scientists' Impact but Contracts Science's Focus |
| `0.45` | MEDIUM | N | STRONG | Spatiotemporal Emotion Recognition using Deep CNN Based on E |
| `0.45` | MEDIUM | N | STRONG | Chain-of-Thought Reasoning Without Prompting |
| `0.45` | MEDIUM | N | STRONG | Reconstructive Visual Instruction Tuning |
| `0.45` | MEDIUM | N | STRONG | HUSE: Hierarchical Universal Semantic Embeddings |
| `0.45` | MEDIUM | N | STRONG | The CLRS-Text Algorithmic Reasoning Language Benchmark |
| `0.45` | MEDIUM | N | STRONG | Towards AI-Complete Question Answering: A Set of Prerequisit |
| `0.45` | MEDIUM | N | STRONG | Singularity-free Guiding Vector Field for Robot Navigation |
| `0.45` | MEDIUM | Y | WEAK | Computing intersections of closed geodesics on the modular c |
| `0.45` | MEDIUM | Y | WEAK | A Structured Syntax-Semantics Interface for English-AMR Alig |
| `0.45` | MEDIUM | N | STRONG | Blind Adversarial Pruning: Balance Accuracy, Efficiency and  |
| `0.45` | MEDIUM | N | STRONG | FaceNet: A Unified Embedding for Face Recognition and Cluste |
| `0.45` | MEDIUM | N | STRONG | Learning Dynamic Routing for Semantic Segmentation |
| `0.45` | MEDIUM | N | STRONG | A Multi-Objective Anytime Rule Mining System to Ease Iterati |
| `0.45` | MEDIUM | N | STRONG | FaceNet: A Unified Embedding for Face Recognition and Cluste |
| `0.45` | MEDIUM | N | STRONG | StateSpaceModels.jl: a Julia Package for Time-Series Analysi |
| `0.45` | MEDIUM | N | STRONG | Representation Tradeoffs for Hyperbolic Embeddings |
| `0.45` | MEDIUM | N | WEAK | A Fixed-Point Model for Pancreas Segmentation in Abdominal C |
| `0.45` | MEDIUM | N | STRONG | Temporally smooth online action detection using cycle-consis |
| `0.45` | MEDIUM | Y | STRONG | Spectral Regularization: an Inductive Bias for Sequence Mode |
| `0.45` | MEDIUM | N | STRONG | Augmented CycleGAN: Learning Many-to-Many Mappings from Unpa |
| `0.45` | MEDIUM | N | STRONG | Reasoning in complex environments with the SelectScript decl |
| `0.45` | MEDIUM | N | STRONG | ORB-SLAM3: An Accurate Open-Source Library for Visual, Visua |
| `0.45` | MEDIUM | N | STRONG | Investigating Self-Attention Network for Chinese Word Segmen |
| `0.45` | MEDIUM | N | STRONG | pyBART: Evidence-based Syntactic Transformations for IE |
| `0.4` | WEAK | N | STRONG | Learning to Cluster Faces on an Affinity Graph |
| `0.4` | WEAK | N | WEAK | NAFSSR: Stereo Image Super-Resolution Using NAFNet |
| `0.4` | WEAK | N | WEAK | Frustum PointNets for 3D Object Detection from RGB-D Data |
| `0.4` | WEAK | N | STRONG | Towards Universal Backward-Compatible Representation Learnin |
| `0.4` | WEAK | N | MEDIUM | BlazeFace: Sub-millisecond Neural Face Detection on Mobile G |
| `0.4` | WEAK | N | STRONG | DialogueGCN: A Graph Convolutional Neural Network for Emotio |
| `0.4` | WEAK | N | MEDIUM | A Modular and Robust Physics-Based Approach for Lensless Ima |
| `0.4` | WEAK | N | STRONG | DeblurGAN-v2: Deblurring (Orders-of-Magnitude) Faster and Be |
| `0.4` | WEAK | N | STRONG | Logram: Efficient Log Parsing Using n-Gram Dictionaries |
| `0.4` | WEAK | N | STRONG | Temporal superimposed crossover module for effective continu |
| `0.4` | WEAK | Y | STRONG | Model-independent constraints on the hydrogen-ionizing emiss |
| `0.4` | WEAK | Y | STRONG | Geometric Mean Metric Learning |
| `0.4` | WEAK | N | WEAK | Effective LSTMs for Target-Dependent Sentiment Classificatio |
| `0.4` | WEAK | Y | STRONG | Forced Exploration in Bandit Problems |
| `0.4` | WEAK | N | MEDIUM | Associative Embedding: End-to-End Learning for Joint Detecti |
| `0.4` | WEAK | N | WEAK | The Lottery Ticket Hypothesis: Finding Sparse, Trainable Neu |
| `0.4` | WEAK | N | WEAK | Qwen2.5-VL Technical Report |
| `0.4` | WEAK | N | WEAK | Deep Residual Learning for Image Recognition |
| `0.4` | WEAK | Y | WEAK | Healing Unsafe Dialogue Responses with Weak Supervision Sign |
| `0.4` | WEAK | N | MEDIUM | Improved Training of Wasserstein GANs |
| `0.4` | WEAK | N | MEDIUM | Adaptive Online Replanning with Diffusion Models |
| `0.4` | WEAK | N | WEAK | Faster R-CNN: Towards Real-Time Object Detection with Region |
| `0.4` | WEAK | N | WEAK | Text-Only Training for Image Captioning using Noise-Injected |
| `0.4` | WEAK | N | MEDIUM | Kernelized Capsule Networks |
| `0.4` | WEAK | N | MEDIUM | SCUT-FBP5500: A Diverse Benchmark Dataset for Multi-Paradigm |
| `0.4` | WEAK | N | MEDIUM | Deep Face Recognition: A Survey |
| `0.4` | WEAK | N | MEDIUM | Position Interpolation Improves ALiBi Extrapolation |
| `0.4` | WEAK | Y | WEAK | DSig: Breaking the Barrier of Signatures in Data Centers |
| `0.4` | WEAK | Y | WEAK | Doubly-Robust Self-Training |
| `0.4` | WEAK | Y | WEAK | PPT: Token Pruning and Pooling for Efficient Vision Transfor |
| `0.4` | WEAK | Y | WEAK | NNoculation: Catching BadNets in the Wild |
| `0.4` | WEAK | Y | WEAK | Exploring Pre-Trained Transformers and Bilingual Transfer Le |
| `0.4` | WEAK | N | WEAK | AIM: An Adaptive and Iterative Mechanism for Differentially  |
| `0.4` | WEAK | Y | WEAK | PPO-Based Vehicle Control for Ramp Merging Scheme Assisted b |
| `0.4` | WEAK | N | WEAK | Fast R-CNN |
| `0.4` | WEAK | Y | WEAK | Scalable simulation-based inference for implicitly defined m |
| `0.4` | WEAK | Y | WEAK | IP102: A Large-Scale Benchmark Dataset for Insect Pest Recog |
| `0.4` | WEAK | Y | WEAK | Anonymisation Models for Text Data: State of the art, Challe |
| `0.4` | WEAK | N | MEDIUM | A Retrospective Analysis of the Fake News Challenge Stance D |
| `0.4` | WEAK | N | WEAK | VoxelNet: End-to-End Learning for Point Cloud Based 3D Objec |
| `0.4` | WEAK | Y | WEAK | Four Things Everyone Should Know to Improve Batch Normalizat |
| `0.4` | WEAK | N | MEDIUM | Personalizing Dialogue Agents: I have a dog, do you have pet |
| `0.4` | WEAK | N | WEAK | Learning Filter Basis for Convolutional Neural Network Compr |
| `0.4` | WEAK | Y | WEAK | Variational Monte Carlo on a Budget — Fine-tuning pre-traine |
| `0.4` | WEAK | N | WEAK | WaveGlow: A Flow-based Generative Network for Speech Synthes |
| `0.4` | WEAK | N | WEAK | HumanSD: A Native Skeleton-Guided Diffusion Model for Human  |
| `0.4` | WEAK | N | MEDIUM | Joint Bilateral Learning for Real-time Universal Photorealis |
| `0.4` | WEAK | N | WEAK | Free-Form Image Inpainting with Gated Convolution |
| `0.4` | WEAK | N | WEAK | Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena |
| `0.4` | WEAK | Y | MEDIUM | On Devon Allen's Disqualification at the 2022 World Track an |
| `0.4` | WEAK | N | MEDIUM | The Medical Segmentation Decathlon |
| `0.4` | WEAK | Y | WEAK | Sentiment analysis in Bengali via transfer learning using mu |
| `0.4` | WEAK | N | WEAK | Layer-compensated Pruning for Resource-constrained Convoluti |
| `0.4` | WEAK | N | WEAK | How Do Vision Transformers Work? |
| `0.4` | WEAK | N | MEDIUM | Reflexion: Language Agents with Verbal Reinforcement Learnin |
| `0.4` | WEAK | N | WEAK | Understanding Black-box Predictions via Influence Functions |
| `0.4` | WEAK | N | MEDIUM | Posterior Control of Blackbox Generation |
| `0.4` | WEAK | N | MEDIUM | Two-Stream Convolutional Networks for Action Recognition in  |
| `0.4` | WEAK | N | WEAK | Towards Robust Monocular Depth Estimation: Mixing Datasets f |
| `0.4` | WEAK | N | MEDIUM | Diffusion Models for Multi-target Adversarial Tracking |
| `0.4` | WEAK | Y | WEAK | SGNet: A Super-class Guided Network for Image Classification |
| `0.4` | WEAK | N | WEAK | GraphGAN: Graph Representation Learning with Generative Adve |
| `0.4` | WEAK | Y | WEAK | Deep Geometry-Aware Camera Self-Calibration from Video |
| `0.4` | WEAK | Y | WEAK | JointCL: A Joint Contrastive Learning Framework for Zero-Sho |
| `0.4` | WEAK | N | WEAK | GAN-QP: A Novel GAN Framework without Gradient Vanishing and |
| `0.4` | WEAK | Y | WEAK | Multi-Stage Prompting for Knowledgeable Dialogue Generation |
| `0.4` | WEAK | N | WEAK | Semantic Understanding of Scenes through the ADE20K Dataset |
| `0.4` | WEAK | Y | WEAK | Depth-Aware Concealed Crop Detection in Dense Agricultural S |
| `0.4` | WEAK | N | WEAK | Making Monolingual Sentence Embeddings Multilingual using Kn |
| `0.4` | WEAK | Y | WEAK | SDRSAC: Semidefinite-Based Randomized Approach for Robust Po |
| `0.4` | WEAK | N | WEAK | Learning Face Representation from Scratch |
| `0.4` | WEAK | N | MEDIUM | Learning and Planning in Average-Reward Markov Decision Proc |
| `0.4` | WEAK | N | WEAK | Esophageal Tumor Segmentation in CT Images using Dilated Den |
| `0.4` | WEAK | Y | MEDIUM | DES Y3 + KiDS-1000: Consistent cosmology combining cosmic sh |
| `0.4` | WEAK | Y | WEAK | Estimating Linguistic Complexity for Science Texts |


---

## 5. LLM vs Rule-based Disagreements

Cases where LLM judgment diverges from rule-based level (before LLM was added).

**415 pairs changed level after LLM signal was added.**

| Pre-LLM | Post-LLM | LLM | Official | Pre-score | Title |
|---|---|---|---|---|---|
| MEDIUM | STRONG | STRONG | Y | `0.7` | Why are Visually-Grounded Language Models Bad at Image Class |
| MEDIUM | STRONG | MEDIUM | Y | `0.7` | On the limits of cross-domain generalization in automated X- |
| MEDIUM | STRONG | STRONG | Y | `0.7` | Any-to-Any Style Transfer: Making Picasso and Da Vinci Colla |
| MEDIUM | STRONG | STRONG | Y | `0.7` | Model Patching: Closing the Subgroup Performance Gap with Da |
| MEDIUM | STRONG | STRONG | Y | `0.7` | BRSR-OpGAN: Blind Radar Signal Restoration using Operational |
| MEDIUM | STRONG | STRONG | Y | `0.65` | QLoRA: Efficient Finetuning of Quantized LLMs |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Levenshtein Training for Word-level Quality Estimation |
| MEDIUM | STRONG | STRONG | Y | `0.65` | On Sparsifying Encoder Outputs in Sequence-to-Sequence Model |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Kannada-MNIST: A new handwritten digits dataset for the Kann |
| MEDIUM | STRONG | STRONG | Y | `0.65` | UUKG: Unified Urban Knowledge Graph Dataset for Urban Spatio |
| MEDIUM | STRONG | STRONG | Y | `0.65` | A Strong Gravitational Lens Is Worth a Thousand Dark Matter  |
| MEDIUM | STRONG | STRONG | Y | `0.65` | A Feasibility Study on Image Inpainting for Non-cleft Lip Ge |
| MEDIUM | STRONG | STRONG | Y | `0.65` | An Adaptive and Altruistic PSO-based Deep Feature Selection  |
| MEDIUM | STRONG | STRONG | Y | `0.65` | MiNet: Mixed Interest Network for Cross-Domain Click-Through |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Self-Calibrated Efficient Transformer for Lightweight Super- |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Using Speech Synthesis to Train End-to-End Spoken Language U |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Deep Spatial-angular Regularization for Compressive Light Fi |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Visual Analytics for Understanding Draco's Knowledge Base |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Echoes from Alexandria: A Large Resource for Multilingual Bo |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Global Robustness Evaluation of Deep Neural Networks with Pr |
| MEDIUM | STRONG | STRONG | Y | `0.65` | A 3D Reactive Navigation Algorithm for Mobile Robots by Usin |
| MEDIUM | STRONG | STRONG | Y | `0.65` | WRENCH: A Comprehensive Benchmark for Weak Supervision |
| MEDIUM | STRONG | STRONG | Y | `0.65` | BSNet: Box-Supervised Simulation-assisted Mean Teacher for 3 |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Performance of Hyperbolic Geometry Models on Top-N Recommend |
| MEDIUM | STRONG | STRONG | N | `0.65` | ResUNet-a: a deep learning framework for semantic segmentati |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Global Structure Knowledge-Guided Relation Extraction Method |
| MEDIUM | STRONG | STRONG | Y | `0.65` | ALPHA: AnomaLous Physiological Health Assessment Using Large |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Bidirectional Attentive Memory Networks for Question Answeri |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Graph Transformer Networks: Learning Meta-path Graphs to Imp |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Robust Target Training for Multi-Source Domain Adaptation |
| MEDIUM | STRONG | STRONG | Y | `0.65` | A Unified Framework for Masked and Mask-Free Face Recognitio |
| MEDIUM | STRONG | STRONG | Y | `0.65` | MiranDa: Mimicking the Learning Processes of Human Doctors t |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Boosting Few-Shot Visual Learning with Self-Supervision |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Immiscible Color Flows in Optimal Transport Networks for Ima |
| MEDIUM | STRONG | STRONG | Y | `0.65` | BINet: Multi-perspective Business Process Anomaly Classifica |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Overcoming Recency Bias of Normalization Statistics in Conti |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Deformable VisTR: Spatio temporal deformable attention for v |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Derivative Delay Embedding: Online Modeling of Streaming Tim |
| MEDIUM | STRONG | STRONG | Y | `0.65` | High Probability Complexity Bounds for Non-Smooth Stochastic |
| MEDIUM | STRONG | STRONG | Y | `0.65` | "Zero-Shot" Point Cloud Upsampling |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Semi-supervised Domain Adaptation via Sample-to-Sample Self- |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Edge Representation Learning with Hypergraphs |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Intent Factored Generation: Unleashing the Diversity in Your |
| MEDIUM | STRONG | STRONG | Y | `0.65` | MGNN: Graph Neural Networks Inspired by Distance Geometry Pr |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Surface-SOS: Self-Supervised Object Segmentation via Neural  |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Real-Time Drone Detection and Tracking With Visible, Thermal |
| MEDIUM | STRONG | STRONG | Y | `0.65` | RDA: An Accelerated Collision Free Motion Planner for Autono |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Solving ARC visual analogies with neural embeddings and vect |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Progressive Confident Masking Attention Network for Audio-Vi |
| MEDIUM | STRONG | STRONG | Y | `0.65` | An Informative Path Planning Framework for Active Learning i |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Sparse maximal update parameterization: A holistic approach  |
| MEDIUM | STRONG | STRONG | Y | `0.65` | USCORE: An Effective Approach to Fully Unsupervised Evaluati |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Importance of Aligning Training Strategy with Evaluation for |
| MEDIUM | STRONG | STRONG | Y | `0.65` | EPSILON: An Efficient Planning System for Automated Vehicles |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Aneumo: A Large-Scale Comprehensive Synthetic Dataset of Ane |
| MEDIUM | STRONG | STRONG | Y | `0.65` | MSC: A Dataset for Macro-Management in StarCraft II |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Learning Vector-Quantized Item Representation for Transferab |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Video Self-Stitching Graph Network for Temporal Action Local |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Dynamical Mechanism of Sampling-based Stochastic Inference u |
| MEDIUM | STRONG | STRONG | Y | `0.65` | CondLaneNet: a Top-to-down Lane Detection Framework Based on |
| MEDIUM | STRONG | STRONG | Y | `0.65` | The AiiDA-KKR plugin and its application to high-throughput  |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Analyzing the Performance of Large Language Models on Code S |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Efficient Temporal Sentence Grounding in Videos with Multi-T |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Cross-Sensor Adversarial Domain Adaptation of Landsat-8 and  |
| MEDIUM | STRONG | STRONG | Y | `0.65` | SPIN: Spacecraft Imagery for Navigation |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Input Normalized Stochastic Gradient Descent Training of Dee |
| MEDIUM | STRONG | STRONG | Y | `0.65` | DDD20 End-to-End Event Camera Driving Dataset: Fusing Frames |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Automatic selection of clustering algorithms using supervise |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Revisiting, Benchmarking and Understanding Unsupervised Grap |
| MEDIUM | STRONG | STRONG | Y | `0.65` | PBench: Workload Synthesizer with Real Statistics for Cloud  |
| MEDIUM | STRONG | STRONG | Y | `0.65` | OmniGlue: Generalizable Feature Matching with Foundation Mod |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Brain-like Flexible Visual Inference by Harnessing Feedback  |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Domain-Specific Denoising Diffusion Probabilistic Models for |
| MEDIUM | STRONG | STRONG | Y | `0.65` | LLM-PQ: Serving LLM on Heterogeneous Clusters with Phase-Awa |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Refining Diffusion Planner for Reliable Behavior Synthesis b |
| MEDIUM | STRONG | STRONG | Y | `0.65` | PiCANet: Pixel-wise Contextual Attention Learning for Accura |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Escape with Your Self: A Solution to the Avoidance Problem w |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Energy-Based Models for Continual Learning |
| MEDIUM | STRONG | STRONG | Y | `0.65` | GAP: A Graph-aware Language Model Framework for Knowledge Gr |
| MEDIUM | STRONG | STRONG | Y | `0.65` | CAPRI-FAIR: Integration of Multi-sided Fairness in Contextua |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Hallucinated but Factual! Inspecting the Factuality of Hallu |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Restore Anything Model via Efficient Degradation Adaptation |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Domain-Generalizable Multiple-Domain Clustering |
| MEDIUM | STRONG | STRONG | Y | `0.65` | LightX3ECG: A Lightweight and eXplainable Deep Learning Syst |
| MEDIUM | STRONG | STRONG | Y | `0.65` | LiDAR Snowfall Simulation for Robust 3D Object Detection |
| MEDIUM | STRONG | STRONG | Y | `0.65` | A probability theoretic approach to drifting data in continu |
| MEDIUM | STRONG | STRONG | Y | `0.65` | MILE: A Multi-Level Framework for Scalable Graph Embedding |
| MEDIUM | STRONG | STRONG | Y | `0.65` | SpectralNet: Spectral Clustering using Deep Neural Networks |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Model and Data Agreement for Learning with Noisy Labels |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Understanding normalization in contrastive representation le |
| MEDIUM | STRONG | STRONG | Y | `0.65` | TACCL: Guiding Collective Algorithm Synthesis using Communic |
| MEDIUM | STRONG | STRONG | Y | `0.65` | MedCPT: Contrastive Pre-trained Transformers with Large-scal |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Label-Efficient Self-Supervised Speaker Verification With In |
| MEDIUM | STRONG | STRONG | Y | `0.65` | CEEBERT: Cross-Domain Inference in Early Exit BERT |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Street-View Image Generation from a Bird's-Eye View Layout |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Graph Neural Networks Exponentially Lose Expressive Power fo |
| MEDIUM | STRONG | STRONG | Y | `0.65` | SAFRAN: An interpretable, rule-based link prediction method  |
| MEDIUM | STRONG | STRONG | Y | `0.65` | The Larger They Are, the Harder They Fail: Language Models d |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Unveiling Deep Shadows: A Survey and Benchmark on Image and  |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Masked Diffusion Models Are Fast Distribution Learners |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Generative Data Augmentation for Commonsense Reasoning |
| MEDIUM | STRONG | STRONG | Y | `0.65` | The matter density PDF for modified gravity and dark energy  |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Assessment of Deep Learning Segmentation for Real-Time Free- |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Learning to Adversarially Blur Visual Object Tracking |
| MEDIUM | STRONG | STRONG | Y | `0.65` | ConsInstancy: Learning Instance Representations for Semi-Sup |
| MEDIUM | STRONG | STRONG | Y | `0.65` | FairSync: Ensuring Amortized Group Exposure in Distributed R |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Reliable Fidelity and Diversity Metrics for Generative Model |
| MEDIUM | STRONG | STRONG | Y | `0.65` | End-to-End Label Uncertainty Modeling in Speech Emotion Reco |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Improving Query Representations for Dense Retrieval with Pse |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Enhancing Feature Diversity Boosts Channel-Adaptive Vision T |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Adaptive Topological Feature via Persistent Homology: Filtra |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Environmental Sound Classification on the Edge: A Pipeline f |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Robust Outlier Detection Method Based on Local Entropy and G |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Tree Prompting: Efficient Task Adaptation without Fine-Tunin |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Permutationally Invariant Networks for Enhanced Sampling (PI |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Multi-News: a Large-Scale Multi-Document Summarization Datas |
| MEDIUM | STRONG | STRONG | Y | `0.65` | NTK-Guided Few-Shot Class Incremental Learning |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Improving AMR Parsing with Sequence-to-Sequence Pre-training |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Reservoir computing approaches for representation and classi |
| MEDIUM | STRONG | STRONG | Y | `0.65` | ChemCrow: Augmenting large-language models with chemistry to |
| MEDIUM | STRONG | STRONG | Y | `0.65` | BraTS orchestrator : Democratizing and Disseminating state-o |
| MEDIUM | STRONG | STRONG | Y | `0.65` | PAD: Phase-Amplitude Decoupling Fusion for Multi-Modal Land  |
| MEDIUM | STRONG | STRONG | Y | `0.65` | A Missing Data Imputation GAN for Character Sprite Generatio |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Neural Relational Inference with Fast Modular Meta-learning |
| MEDIUM | STRONG | STRONG | Y | `0.65` | TRIDENT: Tri-modal Real-time Intrusion Detection Engine for  |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Lightplane: Highly-Scalable Components for Neural 3D Fields |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Learning discrete Lagrangians for variational PDEs from data |
| MEDIUM | STRONG | STRONG | Y | `0.65` | ConceptLab: Creative Concept Generation using VLM-Guided Dif |
| MEDIUM | STRONG | STRONG | Y | `0.65` | MARS-Gym: A Gym framework to model, train, and evaluate Reco |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Set You Straight: Auto-Steering Denoising Trajectories to Si |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Mapping Supervised Bilingual Word Embeddings from English to |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Modality Distillation with Multiple Stream Networks for Acti |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Richer Convolutional Features for Edge Detection |
| MEDIUM | STRONG | STRONG | Y | `0.65` | LIONs: An Empirically Optimized Approach to Align Language M |
| MEDIUM | STRONG | STRONG | Y | `0.65` | FunASR: A Fundamental End-to-End Speech Recognition Toolkit |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Tracking Fringe and Coordinated Activity on Twitter Leading  |
| MEDIUM | STRONG | STRONG | Y | `0.65` | TAPER: Time-Aware Patient EHR Representation |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Beyond Correlation: A Path-Invariant Measure for Seismogram  |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Contrastive Self-Supervised Learning Based Approach for Pati |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Audio-based AI classifiers show no evidence of improved COVI |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Multiscale Quantile Regression with Local Error Control |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Dual Adaptive Representation Alignment for Cross-domain Few- |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Neural Architecture Search for Compressed Sensing Magnetic R |
| MEDIUM | STRONG | STRONG | Y | `0.65` | A Data-Driven Aggressive Autonomous Racing Framework Utilizi |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Dodrio: Exploring Transformer Models with Interactive Visual |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Visual Grounding Methods for VQA are Working for the Wrong R |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Three approaches to facilitate DNN generalization to objects |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Actor-Critic Instance Segmentation |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Bending the Future: Autoregressive Modeling of Temporal Know |
| MEDIUM | STRONG | STRONG | Y | `0.65` | RSANet: Recurrent Slice-wise Attention Network for Multiple  |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Benchmarking and Understanding Compositional Relational Reas |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Elevating Skeleton-Based Action Recognition with Efficient M |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Descriptor-based Foundation Models for Molecular Property Pr |
| MEDIUM | STRONG | STRONG | Y | `0.65` | BanditSum: Extractive Summarization as a Contextual Bandit |
| MEDIUM | STRONG | STRONG | Y | `0.65` | AV-CrossNet: an Audiovisual Complex Spectral Mapping Network |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Closing the Curious Case of Neural Text Degeneration |
| MEDIUM | STRONG | STRONG | Y | `0.65` | DyRRen: A Dynamic Retriever-Reranker-Generator Model for Num |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Simple multi-dataset detection |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Dual Learning for Semi-Supervised Natural Language Understan |
| MEDIUM | STRONG | STRONG | Y | `0.65` | CosmiXs: Improved spectra for dark matter indirect detection |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Speaker Anonymization with Phonetic Intermediate Representat |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Computing Multiple Image Reconstructions with a Single Hyper |
| MEDIUM | STRONG | STRONG | Y | `0.65` | CDGP: Automatic Cloze Distractor Generation based on Pre-tra |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Semi-Supervised Panoptic Narrative Grounding |
| MEDIUM | STRONG | STRONG | Y | `0.65` | EMORL: Ensemble Multi-Objective Reinforcement Learning for E |
| MEDIUM | STRONG | STRONG | Y | `0.65` | NeRP: Implicit Neural Representation Learning with Prior Emb |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Decision-centric fairness: Evaluation and optimization for r |
| MEDIUM | STRONG | STRONG | Y | `0.65` | SPATL: Salient Parameter Aggregation and Transfer Learning f |
| MEDIUM | STRONG | STRONG | Y | `0.65` | P$^2$-ViT: Power-of-Two Post-Training Quantization and Accel |
| MEDIUM | STRONG | STRONG | Y | `0.65` | OpenDelta: A Plug-and-play Library for Parameter-efficient A |
| MEDIUM | STRONG | STRONG | Y | `0.65` | ViPNAS: Efficient Video Pose Estimation via Neural Architect |
| MEDIUM | STRONG | STRONG | Y | `0.65` | PRO-V: An Efficient Program Generation Multi-Agent System fo |
| MEDIUM | STRONG | STRONG | Y | `0.65` | HADES: Homologous Automated Document Exploration and Summari |
| MEDIUM | STRONG | STRONG | Y | `0.65` | Cross-domain Detection via Graph-induced Prototype Alignment |
| WEAK | MEDIUM | MEDIUM | N | `0.4` | Improving Nighttime Driving-Scene Segmentation via Dual Imag |
| WEAK | MEDIUM | STRONG | Y | `0.4` | Ensemble Kalman Methods: A Mean Field Perspective |
| WEAK | MEDIUM | STRONG | N | `0.4` | Towards Cross-Tokenizer Distillation: the Universal Logit Di |
| WEAK | MEDIUM | STRONG | N | `0.4` | An End-to-End Architecture for Keyword Spotting and Voice Ac |
| WEAK | MEDIUM | STRONG | Y | `0.4` | Aligning Query Representation with Rewritten Query and Relev |
| WEAK | MEDIUM | STRONG | N | `0.4` | EESEN: End-to-End Speech Recognition using Deep RNN Models a |
| WEAK | MEDIUM | STRONG | N | `0.4` | HigherHRNet: Scale-Aware Representation Learning for Bottom- |
| WEAK | MEDIUM | STRONG | N | `0.4` | Vitruvion: A Generative Model of Parametric CAD Sketches |
| WEAK | MEDIUM | STRONG | Y | `0.4` | Interpretable Concept Bottlenecks to Align Reinforcement Lea |
| WEAK | MEDIUM | STRONG | Y | `0.4` | CritiPrefill: A Segment-wise Criticality-based Approach for  |
| WEAK | MEDIUM | STRONG | N | `0.4` | Automatic Speech Recognition Benchmark for Air-Traffic Commu |
| WEAK | MEDIUM | STRONG | N | `0.4` | Link Prediction Based on Graph Neural Networks |
| WEAK | MEDIUM | STRONG | N | `0.4` | Ridiculously Fast Shot Boundary Detection with Fully Convolu |
| WEAK | MEDIUM | STRONG | N | `0.4` | PointNet: Deep Learning on Point Sets for 3D Classification  |
| WEAK | MEDIUM | STRONG | N | `0.4` | Map3D: Registration Based Multi-Object Tracking on 3D Serial |
| WEAK | MEDIUM | STRONG | Y | `0.4` | Targeting SARS-CoV-2 with AI- and HPC-enabled Lead Generatio |
| WEAK | MEDIUM | STRONG | Y | `0.4` | Garden optimization problems for benchmarking quantum anneal |
| WEAK | MEDIUM | STRONG | Y | `0.4` | Efficient Monte Carlo Tree Search via On-the-Fly State-Condi |
| WEAK | MEDIUM | STRONG | Y | `0.4` | Weighted asymmetric least squares regression with fixed-effe |
| WEAK | MEDIUM | STRONG | N | `0.4` | SegNet: A Deep Convolutional Encoder-Decoder Architecture fo |
| WEAK | MEDIUM | STRONG | N | `0.4` | YOLACT++: Better Real-time Instance Segmentation |
| WEAK | MEDIUM | STRONG | N | `0.4` | Deep Preset: Blending and Retouching Photos with Color Style |
| WEAK | MEDIUM | STRONG | N | `0.4` | HierVL: Learning Hierarchical Video-Language Embeddings |
| WEAK | MEDIUM | STRONG | N | `0.4` | DeepTraffic: Crowdsourced Hyperparameter Tuning of Deep Rein |
| WEAK | MEDIUM | MEDIUM | N | `0.4` | BanditPAM: Almost Linear Time $k$-Medoids Clustering via Mul |
| WEAK | MEDIUM | MEDIUM | N | `0.4` | ParetoQ: Scaling Laws in Extremely Low-bit LLM Quantization |
| WEAK | MEDIUM | MEDIUM | Y | `0.4` | The Rhythms of the Night: increase in online night activity  |
| WEAK | MEDIUM | STRONG | Y | `0.4` | DTDN: Dual-task De-raining Network |
| WEAK | MEDIUM | STRONG | N | `0.4` | Logic Tensor Networks for Semantic Image Interpretation |
| WEAK | MEDIUM | MEDIUM | Y | `0.4` | PDFA Distillation via String Probability Queries |
| WEAK | MEDIUM | STRONG | N | `0.4` | StyleTTS 2: Towards Human-Level Text-to-Speech through Style |
| WEAK | MEDIUM | STRONG | N | `0.4` | Sentence-BERT: Sentence Embeddings using Siamese BERT-Networ |
| WEAK | MEDIUM | STRONG | N | `0.4` | Real Time Pear Fruit Detection and Counting Using YOLOv4 Mod |
| WEAK | MEDIUM | STRONG | N | `0.4` | A Novel Use of Discrete Wavelet Transform Features in the Pr |
| WEAK | MEDIUM | STRONG | Y | `0.4` | Visualisation and 'diagnostic classifiers' reveal how recurr |
| WEAK | MEDIUM | STRONG | N | `0.4` | Deep High-Resolution Representation Learning for Human Pose  |
| WEAK | MEDIUM | MEDIUM | N | `0.4` | FOSTER: Feature Boosting and Compression for Class-Increment |
| WEAK | MEDIUM | STRONG | Y | `0.4` | An Event-Driven Approach for Studying Gene Block Evolution i |
| WEAK | MEDIUM | STRONG | Y | `0.4` | Transformer Architecture for NetsDB |
| WEAK | MEDIUM | STRONG | N | `0.4` | Adaptive Network Sparsification with Dependent Variational B |
| WEAK | MEDIUM | MEDIUM | N | `0.4` | AdaSpeech: Adaptive Text to Speech for Custom Voice |
| WEAK | MEDIUM | MEDIUM | Y | `0.4` | APIA: An Architecture for Policy-Aware Intentional Agents |
| WEAK | MEDIUM | STRONG | N | `0.4` | Learning Spatiotemporal Occupancy Grid Maps for Lifelong Nav |
| WEAK | MEDIUM | STRONG | Y | `0.4` | Experimental Shake Gesture Detection API for Apple Watch |
| WEAK | MEDIUM | STRONG | Y | `0.4` | Aligning Knowledge Concepts to Whole Slide Images for Precis |
| WEAK | MEDIUM | STRONG | N | `0.4` | FedCD: Improving Performance in non-IID Federated Learning |
| WEAK | MEDIUM | STRONG | N | `0.4` | Object-driven Text-to-Image Synthesis via Adversarial Traini |
| WEAK | MEDIUM | STRONG | N | `0.4` | K-Adapter: Infusing Knowledge into Pre-Trained Models with A |
| WEAK | MEDIUM | STRONG | N | `0.4` | SPLICE: A Synthetic Paid Loss and Incurred Cost Experience S |
| WEAK | MEDIUM | STRONG | N | `0.4` | FitNets: Hints for Thin Deep Nets |
| WEAK | MEDIUM | STRONG | N | `0.4` | PCN: Point Completion Network |
| WEAK | MEDIUM | STRONG | N | `0.4` | ReconNet: Non-Iterative Reconstruction of Images from Compre |
| WEAK | MEDIUM | STRONG | N | `0.4` | Aggregated Residual Transformations for Deep Neural Networks |
| WEAK | MEDIUM | STRONG | N | `0.4` | Relation Networks for Object Detection |
| WEAK | MEDIUM | MEDIUM | Y | `0.4` | MuS2: A Real-World Benchmark for Sentinel-2 Multi-Image Supe |
| WEAK | MEDIUM | STRONG | N | `0.4` | Towards 3D Human Pose Estimation in the Wild: a Weakly-super |
| WEAK | MEDIUM | STRONG | N | `0.4` | From Planes to Corners: Multi-Purpose Primitive Detection in |
| WEAK | MEDIUM | STRONG | Y | `0.4` | Energetic closure of the spatially resolved global food syst |
| WEAK | MEDIUM | STRONG | Y | `0.4` | Downstream Transformer Generation of Question-Answer Pairs w |
| WEAK | MEDIUM | STRONG | N | `0.4` | Stacked Cross Attention for Image-Text Matching |
| WEAK | MEDIUM | STRONG | Y | `0.4` | Intra-video Positive Pairs in Self-Supervised Learning for U |
| WEAK | MEDIUM | STRONG | N | `0.4` | QaNER: Prompting Question Answering Models for Few-shot Name |
| WEAK | MEDIUM | STRONG | N | `0.4` | PrObeD: Proactive Object Detection Wrapper |
| WEAK | MEDIUM | STRONG | N | `0.4` | Social NCE: Contrastive Learning of Socially-aware Motion Re |
| WEAK | MEDIUM | STRONG | Y | `0.4` | Multi-View Picking: Next-best-view Reaching for Improved Gra |
| WEAK | MEDIUM | STRONG | N | `0.4` | MolGAN: An implicit generative model for small molecular gra |
| WEAK | MEDIUM | STRONG | N | `0.4` | ChemDFM: A Large Language Foundation Model for Chemistry |
| WEAK | MEDIUM | STRONG | N | `0.4` | Multi-level Attention Model for Weakly Supervised Audio Clas |
| WEAK | MEDIUM | STRONG | N | `0.4` | Where are the Masks: Instance Segmentation with Image-level  |
| WEAK | MEDIUM | MEDIUM | Y | `0.4` | FeynCalc 9 |
| WEAK | MEDIUM | STRONG | N | `0.4` | CoupleNet: Coupling Global Structure with Local Parts for Ob |
| WEAK | MEDIUM | MEDIUM | Y | `0.4` | Enhancing Sequence-to-Sequence Neural Lemmatization with Ext |
| WEAK | MEDIUM | STRONG | Y | `0.4` | MERTech: Instrument Playing Technique Detection Using Self-S |
| WEAK | MEDIUM | STRONG | N | `0.4` | HoroPCA: Hyperbolic Dimensionality Reduction via Horospheric |
| WEAK | MEDIUM | STRONG | N | `0.4` | Synchronous Bidirectional Neural Machine Translation |
| WEAK | MEDIUM | STRONG | N | `0.4` | ODDN: Addressing Unpaired Data Challenges in Open-World Deep |
| WEAK | MEDIUM | STRONG | N | `0.4` | HunyuanVideo: A Systematic Framework For Large Video Generat |
| WEAK | MEDIUM | MEDIUM | Y | `0.4` | LLMs' morphological analyses of complex FST-generated Finnis |
| WEAK | MEDIUM | STRONG | N | `0.4` | On Embeddings for Numerical Features in Tabular Deep Learnin |
| WEAK | MEDIUM | STRONG | N | `0.4` | Boosting Soft Actor-Critic: Emphasizing Recent Experience wi |
| WEAK | MEDIUM | STRONG | N | `0.4` | COCO-Stuff: Thing and Stuff Classes in Context |
| WEAK | MEDIUM | MEDIUM | N | `0.4` | Multi-layer Representation Fusion for Neural Machine Transla |
| WEAK | MEDIUM | STRONG | N | `0.4` | Simple Contrastive Representation Learning for Time Series F |
| WEAK | MEDIUM | MEDIUM | N | `0.4` | EfficientDet: Scalable and Efficient Object Detection |
| WEAK | MEDIUM | STRONG | N | `0.4` | When Being Unseen from mBERT is just the Beginning: Handling |
| WEAK | MEDIUM | STRONG | Y | `0.4` | Automated Performance Testing Based on Active Deep Learning |
| WEAK | MEDIUM | STRONG | N | `0.4` | Tracklet-Switch Adversarial Attack against Pedestrian Multi- |
| WEAK | MEDIUM | STRONG | N | `0.4` | The First Few Tokens Are All You Need: An Efficient and Effe |
| WEAK | MEDIUM | MEDIUM | N | `0.4` | Decoupling Representation and Classifier for Long-Tailed Rec |
| WEAK | MEDIUM | STRONG | Y | `0.4` | Towards Effective Discrimination Testing for Generative AI |
| WEAK | MEDIUM | MEDIUM | N | `0.4` | Wide Residual Networks |
| WEAK | MEDIUM | STRONG | N | `0.4` | The completed SDSS-IV extended Baryon Oscillation Spectrosco |
| WEAK | MEDIUM | MEDIUM | N | `0.4` | SRFlow: Learning the Super-Resolution Space with Normalizing |
| WEAK | MEDIUM | STRONG | N | `0.4` | Data Distributional Properties Drive Emergent In-Context Lea |
| WEAK | MEDIUM | MEDIUM | Y | `0.4` | A new Linear Time Bi-level $\ell_{1,\infty}$ projection ; Ap |
| WEAK | MEDIUM | STRONG | Y | `0.4` | ContactOpt: Optimizing Contact to Improve Grasps |
| WEAK | MEDIUM | STRONG | N | `0.4` | PCT: Point cloud transformer |
| WEAK | MEDIUM | STRONG | Y | `0.4` | Efficient Compression of Overparameterized Deep Models throu |
| WEAK | MEDIUM | STRONG | Y | `0.4` | One Law, Many Languages: Benchmarking Multilingual Legal Rea |
| WEAK | MEDIUM | STRONG | N | `0.4` | Knowledge-aware Graph Neural Networks with Label Smoothness  |
| WEAK | MEDIUM | STRONG | Y | `0.4` | Language-Grounded Dynamic Scene Graphs for Interactive Objec |
| WEAK | MEDIUM | STRONG | Y | `0.4` | Closing the Generalization Gap of Adaptive Gradient Methods  |
| WEAK | MEDIUM | STRONG | Y | `0.4` | Sample Selection via Contrastive Fragmentation for Noisy Lab |
| WEAK | MEDIUM | STRONG | N | `0.4` | 360SD-Net: 360° Stereo Depth Estimation with Learnable Cost  |
| WEAK | MEDIUM | STRONG | N | `0.4` | OpenBox: A Generalized Black-box Optimization Service |
| WEAK | MEDIUM | STRONG | N | `0.4` | Distance-IoU Loss: Faster and Better Learning for Bounding B |
| WEAK | MEDIUM | STRONG | N | `0.4` | Robot Navigation with Map-Based Deep Reinforcement Learning |
| WEAK | MEDIUM | STRONG | N | `0.4` | FSSD: Feature Fusion Single Shot Multibox Detector |
| WEAK | MEDIUM | STRONG | N | `0.4` | Efficient Ladder-style DenseNets for Semantic Segmentation o |
| WEAK | MEDIUM | STRONG | N | `0.4` | Instant-Teaching: An End-to-End Semi-Supervised Object Detec |
| WEAK | MEDIUM | STRONG | Y | `0.4` | Clustering of Big Data with Mixed Features |
| WEAK | MEDIUM | STRONG | N | `0.4` | A Note on Connecting Barlow Twins with Negative-Sample-Free  |
| WEAK | MEDIUM | STRONG | N | `0.4` | Bayesian Batch Active Learning as Sparse Subset Approximatio |
| WEAK | MEDIUM | STRONG | Y | `0.4` | Nested Sampling with Normalising Flows for Gravitational-Wav |
| WEAK | MEDIUM | STRONG | N | `0.4` | Few-Shot Learning with Graph Neural Networks |
| WEAK | MEDIUM | STRONG | N | `0.4` | Unsupervised Multiple Choices Question Answering: Start Lear |
| WEAK | MEDIUM | STRONG | Y | `0.35` | One-shot World Models Using a Transformer Trained on a Synth |
| WEAK | MEDIUM | STRONG | Y | `0.35` | Sample Condensation in Online Continual Learning |
| WEAK | MEDIUM | STRONG | Y | `0.35` | Exploring the Determinants of Pedestrian Crash Severity Usin |
| WEAK | MEDIUM | STRONG | Y | `0.35` | FaceX: Understanding Face Attribute Classifiers through Summ |
| WEAK | MEDIUM | STRONG | N | `0.35` | SinGAN: Learning a Generative Model from a Single Natural Im |
| WEAK | MEDIUM | STRONG | N | `0.35` | Deep learning methods allow fully automated segmentation of  |
| WEAK | MEDIUM | STRONG | Y | `0.35` | The language of mental health problems in social media |
| WEAK | MEDIUM | STRONG | N | `0.35` | MIST: A Simple and Scalable End-To-End 3D Medical Imaging Se |
| WEAK | MEDIUM | STRONG | Y | `0.35` | A Blackbox Yield Estimation Workflow with Gaussian Process R |
| WEAK | MEDIUM | STRONG | N | `0.35` | G-Retriever: Retrieval-Augmented Generation for Textual Grap |
| WEAK | MEDIUM | STRONG | N | `0.35` | Hybrid Deep Network for Anomaly Detection |
| WEAK | MEDIUM | STRONG | N | `0.35` | Adaptive-Halting Policy Network for Early Classification |
| WEAK | MEDIUM | STRONG | Y | `0.35` | Differential Privacy Has Disparate Impact on Model Accuracy |
| WEAK | MEDIUM | STRONG | N | `0.35` | A Large-scale Dataset for Hate Speech Detection on Vietnames |
| WEAK | MEDIUM | STRONG | N | `0.35` | NeRF-Supervised Deep Stereo |
| WEAK | MEDIUM | STRONG | N | `0.35` | A C-LSTM Neural Network for Text Classification |
| WEAK | MEDIUM | STRONG | Y | `0.35` | MuJoCo MPC for Humanoid Control: Evaluation on HumanoidBench |
| WEAK | MEDIUM | STRONG | N | `0.35` | Semi-Supervised Learning with Ladder Networks |
| WEAK | MEDIUM | STRONG | N | `0.35` | node2vec: Scalable Feature Learning for Networks |
| WEAK | MEDIUM | STRONG | Y | `0.35` | Linear Causal Bandits: Unknown Graph and Soft Interventions |
| WEAK | MEDIUM | STRONG | N | `0.35` | Residual Correlation in Graph Neural Network Regression |
| WEAK | MEDIUM | STRONG | N | `0.35` | DeepBlindness: Fast Blindness Map Estimation and Blindness T |
| WEAK | MEDIUM | STRONG | N | `0.35` | Convolutional Neural Networks with Alternately Updated Cliqu |
| WEAK | MEDIUM | STRONG | N | `0.35` | Attention Is All You Need |
| WEAK | MEDIUM | STRONG | N | `0.35` | A Style-Aware Content Loss for Real-time HD Style Transfer |
| WEAK | MEDIUM | STRONG | Y | `0.35` | Split-PU: Hardness-aware Training Strategy for Positive-Unla |
| WEAK | MEDIUM | STRONG | Y | `0.35` | Secure Safety Filter: Towards Safe Flight Control under Sens |
| WEAK | MEDIUM | STRONG | N | `0.35` | Deformable ConvNets v2: More Deformable, Better Results |
| WEAK | MEDIUM | STRONG | N | `0.35` | A Novel Benchmark and Dataset for Efficient 3D Gaussian Spla |
| WEAK | MEDIUM | STRONG | N | `0.35` | Searching for Exoplanets Using Artificial Intelligence |
| WEAK | MEDIUM | STRONG | N | `0.35` | No Reason for No Supervision: Improved Generalization in Sup |
| WEAK | MEDIUM | STRONG | N | `0.35` | Free as in Free Word Order: An Energy Based Model for Word S |
| WEAK | MEDIUM | STRONG | N | `0.35` | Generalized Focal Loss: Learning Qualified and Distributed B |
| WEAK | MEDIUM | STRONG | N | `0.35` | Reverse Attention for Salient Object Detection |
| WEAK | MEDIUM | STRONG | N | `0.35` | Modeling Tabular data using Conditional GAN |
| WEAK | MEDIUM | STRONG | N | `0.35` | Low-effort place recognition with WiFi fingerprints using de |
| WEAK | MEDIUM | STRONG | Y | `0.35` | Topological Embedding of Human Brain Networks with Applicati |
| WEAK | MEDIUM | STRONG | N | `0.35` | Forget-free Continual Learning with Winning Subnetworks |
| WEAK | MEDIUM | STRONG | Y | `0.35` | Modeling chemistry during star formation: Water deuteration  |
| WEAK | MEDIUM | STRONG | N | `0.35` | FCOS: Fully Convolutional One-Stage Object Detection |
| WEAK | MEDIUM | STRONG | N | `0.35` | Hybrid Search for Efficient Planning with Completeness Guara |
| WEAK | MEDIUM | STRONG | N | `0.35` | Joint Face Detection and Alignment using Multi-task Cascaded |
| WEAK | MEDIUM | STRONG | N | `0.35` | Letter-Based Speech Recognition with Gated ConvNets |
| WEAK | MEDIUM | STRONG | N | `0.35` | Cascade Cost Volume for High-Resolution Multi-View Stereo an |
| WEAK | MEDIUM | STRONG | N | `0.35` | Learning K-way D-dimensional Discrete Codes for Compact Embe |
| WEAK | MEDIUM | STRONG | N | `0.35` | PPF-FoldNet: Unsupervised Learning of Rotation Invariant 3D  |
| WEAK | MEDIUM | STRONG | N | `0.35` | Character-level Convolutional Networks for Text Classificati |
| WEAK | MEDIUM | STRONG | N | `0.35` | Controlled abstention neural networks for identifying skillf |
| WEAK | MEDIUM | STRONG | N | `0.35` | Drawing Early-Bird Tickets: Towards More Efficient Training  |
| WEAK | MEDIUM | STRONG | N | `0.35` | Holistically-Nested Edge Detection |
| WEAK | MEDIUM | STRONG | N | `0.35` | Colorful Image Colorization |
| WEAK | MEDIUM | STRONG | N | `0.35` | The Design and Implementation of a Real Time Visual Search S |
| WEAK | MEDIUM | STRONG | Y | `0.35` | Natural Reference Frames within Video Analysis |
| WEAK | MEDIUM | STRONG | Y | `0.35` | Towards Exact Computation of Inductive Bias |
| WEAK | MEDIUM | STRONG | N | `0.35` | A joint separation-classification model for sound event dete |
| WEAK | MEDIUM | STRONG | N | `0.35` | AixBench: A Code Generation Benchmark Dataset |
| WEAK | MEDIUM | STRONG | N | `0.35` | Unsupervised Deep Learning for Structured Shape Matching |
| WEAK | MEDIUM | STRONG | Y | `0.35` | The dynamics and outcome of star formation with jets, radiat |
| WEAK | MEDIUM | STRONG | Y | `0.35` | Towards gaze-independent c-VEP BCI: A pilot study |
| WEAK | MEDIUM | STRONG | N | `0.35` | PaLM-E: An Embodied Multimodal Language Model |
| WEAK | MEDIUM | STRONG | Y | `0.35` | MVTec AD -- A Comprehensive Real-World Dataset for Unsupervi |
| WEAK | MEDIUM | STRONG | Y | `0.35` | Cluster-guided Asymmetric Contrastive Learning for Unsupervi |
| WEAK | MEDIUM | STRONG | N | `0.35` | Simple BERT Models for Relation Extraction and Semantic Role |
| WEAK | MEDIUM | STRONG | N | `0.35` | Potential Gap: Using Reactive Policies to Guarantee Safe Nav |
| WEAK | MEDIUM | STRONG | N | `0.35` | Speaking the Same Language: Matching Machine to Human Captio |
| WEAK | MEDIUM | STRONG | N | `0.35` | Robust Burned Area Delineation through Multitask Learning |
| WEAK | MEDIUM | STRONG | N | `0.35` | YOLO9000: Better, Faster, Stronger |
| WEAK | MEDIUM | STRONG | Y | `0.35` | Instantaneous PSD Estimation for Speech Enhancement based on |
| WEAK | MEDIUM | STRONG | N | `0.35` | Community-based Outlier Detection for Edge-attributed Graphs |
| WEAK | MEDIUM | STRONG | N | `0.35` | Single Shot Scene Text Retrieval |
| WEAK | MEDIUM | STRONG | N | `0.35` | Enhancing the Protein Tertiary Structure Prediction by Multi |
| WEAK | MEDIUM | STRONG | N | `0.35` | ns3-gym: Extending OpenAI Gym for Networking Research |
| WEAK | MEDIUM | STRONG | Y | `0.35` | The integration of angular velocity |
| WEAK | MEDIUM | STRONG | N | `0.35` | CodeGeeX: A Pre-Trained Model for Code Generation with Multi |
| WEAK | MEDIUM | STRONG | N | `0.35` | A large annotated medical image dataset for the development  |
| WEAK | MEDIUM | STRONG | N | `0.35` | Zero-Shot Learning -- A Comprehensive Evaluation of the Good |
| WEAK | MEDIUM | STRONG | N | `0.35` | GAMA: A Large Audio-Language Model with Advanced Audio Under |
| WEAK | MEDIUM | STRONG | N | `0.35` | Sound Event Localization and Detection of Overlapping Source |
| WEAK | MEDIUM | STRONG | N | `0.35` | Framing U-Net via Deep Convolutional Framelets: Application  |
| WEAK | MEDIUM | STRONG | Y | `0.35` | Toward Aligning Human and Robot Actions via Multi-Modal Demo |
| WEAK | MEDIUM | STRONG | N | `0.35` | SimCSE: Simple Contrastive Learning of Sentence Embeddings |
| WEAK | MEDIUM | STRONG | N | `0.35` | Multi-Anchor Active Domain Adaptation for Semantic Segmentat |
| WEAK | MEDIUM | STRONG | Y | `0.35` | Supercomputing tensor networks for U(1) symmetric quantum ma |
| WEAK | MEDIUM | STRONG | N | `0.35` | SIDA: Social Media Image Deepfake Detection, Localization an |
| WEAK | MEDIUM | STRONG | N | `0.35` | R$^2$-Gaussian: Rectifying Radiative Gaussian Splatting for  |
| WEAK | MEDIUM | STRONG | N | `0.35` | ChamNet: Towards Efficient Network Design through Platform-A |
| WEAK | MEDIUM | STRONG | N | `0.35` | RobustTP: End-to-End Trajectory Prediction for Heterogeneous |
| WEAK | MEDIUM | STRONG | N | `0.35` | Hierarchical Graph Representation Learning with Differentiab |
| WEAK | MEDIUM | STRONG | N | `0.35` | Sparse eigenbasis approximation: multiple feature extraction |
| WEAK | MEDIUM | STRONG | N | `0.35` | High-Resolution Image Inpainting with Iterative Confidence F |
| WEAK | MEDIUM | STRONG | N | `0.35` | GloDyNE: Global Topology Preserving Dynamic Network Embeddin |
| WEAK | MEDIUM | STRONG | N | `0.35` | Physical Attack on Monocular Depth Estimation with Optimal A |
| WEAK | MEDIUM | STRONG | N | `0.35` | Fast unfolding of communities in large networks |
| WEAK | MEDIUM | STRONG | N | `0.35` | Multi-Object Representation Learning with Iterative Variatio |
| WEAK | MEDIUM | STRONG | N | `0.35` | Panther: Fast Top-k Similarity Search in Large Networks |
| WEAK | MEDIUM | STRONG | N | `0.35` | Aerial Map-Based Navigation Using Semantic Segmentation and  |
| WEAK | MEDIUM | STRONG | N | `0.35` | GroupCDL: Interpretable Denoising and Compressed Sensing MRI |
| WEAK | MEDIUM | STRONG | Y | `0.35` | Winner-takes-all learners are geometry-aware conditional den |
| WEAK | MEDIUM | STRONG | N | `0.35` | Neural AMR: Sequence-to-Sequence Models for Parsing and Gene |
| WEAK | MEDIUM | STRONG | Y | `0.35` | Probabilistic Decomposed Linear Dynamical Systems for Robust |
| WEAK | MEDIUM | STRONG | N | `0.35` | A Sensitivity Analysis of (and Practitioners' Guide to) Conv |
| WEAK | MEDIUM | STRONG | N | `0.35` | HOME: Heatmap Output for future Motion Estimation |
| WEAK | MEDIUM | STRONG | Y | `0.35` | Graph Anomaly Detection with Unsupervised GNNs |
| WEAK | MEDIUM | STRONG | Y | `0.35` | AI Expands Scientists' Impact but Contracts Science's Focus |
| WEAK | MEDIUM | STRONG | N | `0.35` | Spatiotemporal Emotion Recognition using Deep CNN Based on E |
| WEAK | MEDIUM | STRONG | N | `0.35` | Chain-of-Thought Reasoning Without Prompting |
| WEAK | MEDIUM | STRONG | N | `0.35` | Reconstructive Visual Instruction Tuning |
| WEAK | MEDIUM | STRONG | N | `0.35` | HUSE: Hierarchical Universal Semantic Embeddings |
| WEAK | MEDIUM | STRONG | N | `0.35` | The CLRS-Text Algorithmic Reasoning Language Benchmark |
| WEAK | MEDIUM | STRONG | N | `0.35` | Towards AI-Complete Question Answering: A Set of Prerequisit |
| WEAK | MEDIUM | STRONG | N | `0.35` | Singularity-free Guiding Vector Field for Robot Navigation |
| WEAK | MEDIUM | STRONG | N | `0.35` | Blind Adversarial Pruning: Balance Accuracy, Efficiency and  |
| WEAK | MEDIUM | STRONG | N | `0.35` | FaceNet: A Unified Embedding for Face Recognition and Cluste |
| WEAK | MEDIUM | STRONG | N | `0.35` | Learning Dynamic Routing for Semantic Segmentation |
| WEAK | MEDIUM | STRONG | N | `0.35` | A Multi-Objective Anytime Rule Mining System to Ease Iterati |
| WEAK | MEDIUM | STRONG | N | `0.35` | FaceNet: A Unified Embedding for Face Recognition and Cluste |
| WEAK | MEDIUM | STRONG | N | `0.35` | StateSpaceModels.jl: a Julia Package for Time-Series Analysi |
| WEAK | MEDIUM | STRONG | N | `0.35` | Representation Tradeoffs for Hyperbolic Embeddings |
| WEAK | MEDIUM | STRONG | N | `0.35` | Temporally smooth online action detection using cycle-consis |
| WEAK | MEDIUM | STRONG | Y | `0.35` | Spectral Regularization: an Inductive Bias for Sequence Mode |
| WEAK | MEDIUM | STRONG | N | `0.35` | Augmented CycleGAN: Learning Many-to-Many Mappings from Unpa |
| WEAK | MEDIUM | STRONG | N | `0.35` | Reasoning in complex environments with the SelectScript decl |
| WEAK | MEDIUM | STRONG | N | `0.35` | ORB-SLAM3: An Accurate Open-Source Library for Visual, Visua |
| WEAK | MEDIUM | STRONG | N | `0.35` | Investigating Self-Attention Network for Chinese Word Segmen |
| WEAK | MEDIUM | STRONG | N | `0.35` | pyBART: Evidence-based Syntactic Transformations for IE |


---

## 6. Contradiction Cases

**95 contradictions detected.**

| Score | Level | Conf | Official | Note | Title |
|---|---|---|---|---|---|
| `0.65` | MEDIUM | LOW | Y | surface signals fired but LLM returned weak | UnSegGNet: Unsupervised Image Segmentation using G |
| `0.65` | MEDIUM | LOW | Y | surface signals fired but LLM returned weak | Just Jump: Dynamic Neighborhood Aggregation in Gra |
| `0.65` | MEDIUM | LOW | Y | surface signals fired but LLM returned weak | When and why vision-language models behave like ba |
| `0.65` | MEDIUM | LOW | Y | surface signals fired but LLM returned weak | Link Prediction without Graph Neural Networks |
| `0.65` | MEDIUM | LOW | Y | surface signals fired but LLM returned weak | Generalizable Low-Resource Activity Recognition wi |
| `0.65` | MEDIUM | LOW | Y | surface signals fired but LLM returned weak | MMIDR: Teaching Large Language Model to Interpret  |
| `0.6` | MEDIUM | LOW | Y | surface signals fired but LLM returned weak | Global Entity Disambiguation with BERT |
| `0.6` | MEDIUM | LOW | Y | no surface signals but LLM returned strong | Deep Graph Infomax |
| `0.6` | MEDIUM | LOW | Y | surface signals fired but LLM returned weak | Learning SO(3) Equivariant Representations with Sp |
| `0.6` | MEDIUM | LOW | Y | surface signals fired but LLM returned weak | Neural Speech Synthesis on a Shoestring: Improving |
| `0.6` | MEDIUM | LOW | Y | surface signals fired but LLM returned weak | Neurosymbolic Reasoning Shortcuts under the Indepe |
| `0.6` | MEDIUM | LOW | Y | surface signals fired but LLM returned weak | Machine Learning & Wi-Fi: Unveiling the Path Towar |
| `0.55` | MEDIUM | LOW | Y | no surface signals but LLM returned strong | Universal heavy-ball method for nonconvex optimiza |
| `0.55` | MEDIUM | LOW | Y | surface signals fired but LLM returned weak | NuPS: A Parameter Server for Machine Learning with |
| `0.55` | MEDIUM | LOW | Y | no surface signals but LLM returned strong | Exploring weight initialization, diversity of solu |
| `0.55` | MEDIUM | LOW | Y | surface signals fired but LLM returned weak | MC-UNet Multi-module Concatenation based on U-shap |
| `0.55` | MEDIUM | LOW | Y | surface signals fired but LLM returned weak | CNTS: Cooperative Network for Time Series |
| `0.55` | MEDIUM | LOW | Y | no surface signals but LLM returned strong | Uncertainty Quantification of Nonlinear Lagrangian |
| `0.55` | MEDIUM | LOW | Y | surface signals fired but LLM returned weak | How do Large Language Models Understand Relevance? |
| `0.5` | MEDIUM | LOW | N | surface signals fired but LLM returned weak | Conditional Image Synthesis With Auxiliary Classif |
| `0.5` | MEDIUM | LOW | Y | no surface signals but LLM returned strong | Interpretable Concept Bottlenecks to Align Reinfor |
| `0.5` | MEDIUM | LOW | N | surface signals fired but LLM returned weak | Diffusion Models Beat GANs on Image Synthesis |
| `0.5` | MEDIUM | LOW | Y | surface signals fired but LLM returned weak | Three things everyone should know about Vision Tra |
| `0.5` | MEDIUM | LOW | Y | surface signals fired but LLM returned weak | Max-Margin Token Selection in Attention Mechanism |
| `0.5` | MEDIUM | LOW | Y | surface signals fired but LLM returned weak | MatrixNet: Learning over symmetry groups using lea |
| `0.5` | MEDIUM | LOW | Y | surface signals fired but LLM returned weak | Few-shot Personalized Scanpath Prediction |
| `0.5` | MEDIUM | LOW | Y | surface signals fired but LLM returned weak | Do LLMs Implicitly Determine the Suitable Text Dif |
| `0.5` | MEDIUM | LOW | Y | surface signals fired but LLM returned weak | BigDL 2.0: Seamless Scaling of AI Pipelines from L |
| `0.5` | MEDIUM | LOW | Y | no surface signals but LLM returned strong | One Law, Many Languages: Benchmarking Multilingual |
| `0.45` | MEDIUM | LOW | Y | no surface signals but LLM returned strong | One-shot World Models Using a Transformer Trained  |
| `0.45` | MEDIUM | LOW | Y | no surface signals but LLM returned strong | Sample Condensation in Online Continual Learning |
| `0.45` | MEDIUM | LOW | N | surface signals fired but LLM returned weak | Feature Pyramid Networks for Object Detection |
| `0.45` | MEDIUM | LOW | Y | surface signals fired but LLM returned weak | DG-Trans: Dual-level Graph Transformer for Spatiot |
| `0.45` | MEDIUM | LOW | Y | no surface signals but LLM returned strong | Split-PU: Hardness-aware Training Strategy for Pos |
| `0.45` | MEDIUM | LOW | Y | no surface signals but LLM returned strong | Topological Embedding of Human Brain Networks with |
| `0.45` | MEDIUM | LOW | Y | no surface signals but LLM returned strong | Modeling chemistry during star formation: Water de |
| `0.45` | MEDIUM | LOW | N | surface signals fired but LLM returned weak | Road Extraction by Deep Residual U-Net |
| `0.45` | MEDIUM | LOW | Y | no surface signals but LLM returned strong | The dynamics and outcome of star formation with je |
| `0.45` | MEDIUM | LOW | N | surface signals fired but LLM returned weak | StackGAN: Text to Photo-realistic Image Synthesis  |
| `0.45` | MEDIUM | LOW | Y | no surface signals but LLM returned strong | Towards gaze-independent c-VEP BCI: A pilot study |
| `0.45` | MEDIUM | LOW | Y | surface signals fired but LLM returned weak | Schema2QA: High-Quality and Low-Cost Q&A Agents fo |
| `0.45` | MEDIUM | LOW | Y | surface signals fired but LLM returned weak | Theoretical analysis and computation of the sample |
| `0.45` | MEDIUM | LOW | Y | surface signals fired but LLM returned weak | UCC: Uncertainty guided Cross-head Co-training for |
| `0.45` | MEDIUM | LOW | Y | no surface signals but LLM returned strong | Supercomputing tensor networks for U(1) symmetric  |
| `0.45` | MEDIUM | LOW | N | surface signals fired but LLM returned weak | HGRN2: Gated Linear RNNs with State Expansion |
| `0.45` | MEDIUM | LOW | Y | no surface signals but LLM returned strong | Graph Anomaly Detection with Unsupervised GNNs |
| `0.45` | MEDIUM | LOW | N | surface signals fired but LLM returned weak | A Fixed-Point Model for Pancreas Segmentation in A |
| `0.4` | WEAK | LOW | N | surface signals fired but LLM returned weak | NAFSSR: Stereo Image Super-Resolution Using NAFNet |
| `0.4` | WEAK | LOW | N | surface signals fired but LLM returned weak | Effective LSTMs for Target-Dependent Sentiment Cla |
| `0.4` | WEAK | LOW | N | surface signals fired but LLM returned weak | The Lottery Ticket Hypothesis: Finding Sparse, Tra |
| `0.4` | WEAK | LOW | N | surface signals fired but LLM returned weak | Qwen2.5-VL Technical Report |
| `0.4` | WEAK | LOW | N | surface signals fired but LLM returned weak | Deep Residual Learning for Image Recognition |
| `0.4` | WEAK | LOW | N | surface signals fired but LLM returned weak | Faster R-CNN: Towards Real-Time Object Detection w |
| `0.4` | WEAK | LOW | N | surface signals fired but LLM returned weak | Text-Only Training for Image Captioning using Nois |
| `0.4` | WEAK | LOW | N | surface signals fired but LLM returned weak | AIM: An Adaptive and Iterative Mechanism for Diffe |
| `0.4` | WEAK | LOW | N | surface signals fired but LLM returned weak | Learning Filter Basis for Convolutional Neural Net |
| `0.4` | WEAK | LOW | N | surface signals fired but LLM returned weak | WaveGlow: A Flow-based Generative Network for Spee |
| `0.4` | WEAK | LOW | N | surface signals fired but LLM returned weak | HumanSD: A Native Skeleton-Guided Diffusion Model  |
| `0.4` | WEAK | LOW | N | surface signals fired but LLM returned weak | Free-Form Image Inpainting with Gated Convolution |
| `0.4` | WEAK | LOW | N | surface signals fired but LLM returned weak | Judging LLM-as-a-Judge with MT-Bench and Chatbot A |
| `0.4` | WEAK | LOW | N | surface signals fired but LLM returned weak | How Do Vision Transformers Work? |
| `0.4` | WEAK | LOW | N | surface signals fired but LLM returned weak | Understanding Black-box Predictions via Influence  |
| `0.4` | WEAK | LOW | N | surface signals fired but LLM returned weak | Towards Robust Monocular Depth Estimation: Mixing  |
| `0.4` | WEAK | LOW | N | surface signals fired but LLM returned weak | GraphGAN: Graph Representation Learning with Gener |
| `0.4` | WEAK | LOW | N | surface signals fired but LLM returned weak | GAN-QP: A Novel GAN Framework without Gradient Van |
| `0.4` | WEAK | LOW | N | surface signals fired but LLM returned weak | Making Monolingual Sentence Embeddings Multilingua |
| `0.4` | WEAK | LOW | N | surface signals fired but LLM returned weak | Learning Face Representation from Scratch |
| `0.4` | WEAK | LOW | N | surface signals fired but LLM returned weak | Esophageal Tumor Segmentation in CT Images using D |
| `0.35` | WEAK | LOW | N | surface signals fired but LLM returned weak | Value Iteration Networks |
| `0.35` | WEAK | LOW | N | surface signals fired but LLM returned weak | Improved Distribution Matching for Dataset Condens |
| `0.35` | WEAK | LOW | N | surface signals fired but LLM returned weak | U-Net v2: Rethinking the Skip Connections of U-Net |
| `0.35` | WEAK | LOW | N | surface signals fired but LLM returned weak | Large Scale GAN Training for High Fidelity Natural |
| `0.35` | WEAK | LOW | N | surface signals fired but LLM returned weak | Deep Anomaly Detection with Deviation Networks |
| `0.35` | WEAK | LOW | N | surface signals fired but LLM returned weak | Bridging the Gap to Real-World Object-Centric Lear |
| `0.35` | WEAK | LOW | N | surface signals fired but LLM returned weak | Encoder-Decoder with Atrous Separable Convolution  |
| `0.35` | WEAK | LOW | N | surface signals fired but LLM returned weak | QFAST: Quantum Synthesis Using a Hierarchical Cont |
| `0.35` | WEAK | LOW | N | surface signals fired but LLM returned weak | Single Channel Audio Source Separation using Convo |
| `0.35` | WEAK | LOW | N | surface signals fired but LLM returned weak | DGL-KE: Training Knowledge Graph Embeddings at Sca |
| `0.35` | WEAK | LOW | N | surface signals fired but LLM returned weak | Semi-supervised Left Atrium Segmentation with Mutu |
| `0.35` | WEAK | LOW | N | surface signals fired but LLM returned weak | Hindsight Experience Replay |
| `0.35` | WEAK | LOW | Y | surface signals fired but LLM returned weak | Improve Object Detection with Feature-based Knowle |
| `0.35` | WEAK | LOW | N | surface signals fired but LLM returned weak | Global Unifying Intrinsic Calibration for Spinning |
| `0.35` | WEAK | LOW | N | surface signals fired but LLM returned weak | DiffWave: A Versatile Diffusion Model for Audio Sy |
| `0.35` | WEAK | LOW | N | surface signals fired but LLM returned weak | Revisiting Semi-Supervised Learning with Graph Emb |
| `0.35` | WEAK | LOW | N | surface signals fired but LLM returned weak | All Tokens Matter: Token Labeling for Training Bet |
| `0.35` | WEAK | LOW | N | surface signals fired but LLM returned weak | Transformer-XL: Attentive Language Models Beyond a |
| `0.35` | WEAK | LOW | N | surface signals fired but LLM returned weak | Persuasion for Good: Towards a Personalized Persua |
| `0.35` | WEAK | LOW | N | surface signals fired but LLM returned weak | Multi-attention Recurrent Network for Human Commun |
| `0.35` | WEAK | LOW | N | surface signals fired but LLM returned weak | PraNet: Parallel Reverse Attention Network for Pol |
| `0.35` | WEAK | LOW | Y | surface signals fired but LLM returned weak | Bidirectional-Convolutional LSTM Based Spectral-Sp |
| `0.3` | WEAK | LOW | Y | no surface signals but LLM returned strong | Learning to Perceive in Deep Model-Free Reinforcem |
| `0.3` | WEAK | LOW | N | surface signals fired but LLM returned weak | Meta Pseudo Labels |
| `0.25` | WEAK | LOW | N | no surface signals but LLM returned strong | SpeedySpeech: Efficient Neural Speech Synthesis |
| `0.2` | WEAK | LOW | N | no surface signals but LLM returned strong | BERT: Pre-training of Deep Bidirectional Transform |
| `0.15` | WEAK | LOW | N | surface signals fired but LLM returned weak | Light-Head R-CNN: In Defense of Two-Stage Object D |
