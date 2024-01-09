# rebus
REBUS: A Robust Evaluation Benchmark of Understanding Symbols

## Introduction

Recent advances in large language models have led to the development of multimodal LLMs (MLLMs), which take both image data and text as an input. Virtually all of these models have been announced within the past year, leading to a significant need for benchmarks evaluating the abilities of these models to reason truthfully and accurately on a diverse set of tasks. When Google announced Gemini Pro \citep{geminiteam2023gemini}, they displayed its ability to solve rebuses---wordplay puzzles which involve creatively adding and subtracting letters from words derived from text and images. The diversity of rebuses allows for a broad evaluation of multimodal reasoning capabilities, including image recognition, multi-step  %vs "multi-part puzzles"%
reasoning, and understanding the human creator's intent.

We present REBUS: a collection of 333 hand-crafted rebuses spanning 13 diverse categories, and including both hand-drawn and digitally created puzzles from nine people. The dataset contains a large set of challenges, with samples presented in **Table 1**. Notably, GPT-4V, the most powerful model we evaluated, got only 24% of the puzzles correct, highlighting the lack of capabilities that MLLMs have in new and unexpected domains that human reasoning is able to generalize to with comparative ease. Open-source models perform even worse, with a median accuracy of less than 1%, underscoring their relative incompetence at out-of-distribution tasks, and serving as a warning against immediately relying on them for real-world applications.

![image](https://github.com/cvndsh/rebus/assets/10122030/131bde1a-9a09-44cc-abc3-efe874b95b23)

