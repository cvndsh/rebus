# REBUS
REBUS: A Robust Evaluation Benchmark of Understanding Symbols

[**Paper**](https://arxiv.org/abs/2401.05604) | [**🤗 Dataset**](https://huggingface.co/datasets/cavendishlabs/rebus) | [**GitHub**](https://github.com/cvndsh/rebus) | [**Website**](https://cavendishlabs.org/rebus/)

## Introduction

Recent advances in large language models have led to the development of multimodal LLMs (MLLMs), which take both image data and text as an input. Virtually all of these models have been announced within the past year, leading to a significant need for benchmarks evaluating the abilities of these models to reason truthfully and accurately on a diverse set of tasks. When Google announced Gemini Pro (Gemini Team et al., 2023), they displayed its ability to solve rebuses—wordplay puzzles which involve creatively adding and subtracting letters from words derived from text and images. The diversity of rebuses allows for a broad evaluation of multimodal reasoning capabilities, including image recognition, multi-step reasoning, and understanding the human creator's intent.

We present REBUS: a collection of 333 hand-crafted rebuses spanning 13 diverse categories, including hand-drawn and digital images created by nine contributors. Samples are presented in the table below. Notably, GPT-4V, the most powerful model we evaluated, answered only 24% of puzzles correctly, highlighting the poor capabilities of MLLMs in new and unexpected domains to which human reasoning generalizes with comparative ease. Open-source models perform even worse, with a median accuracy below 1%. We notice that models often give faithless explanations, fail to change their minds after an initial approach doesn't work, and remain highly uncalibrated on their own abilities.

![image](https://github.com/cvndsh/rebus/assets/10122030/131bde1a-9a09-44cc-abc3-efe874b95b23)

## Evaluation results

| Model             | Overall       | Easy          | Medium        | Hard         |
| ----------------- | ------------- | ------------- | ------------- | ------------ |
| GPT-4o            | **41.7**      | **52.4**      | **32.5**      | **7.1**      |
| GPT-4V            | 24.0          | 33.0          | 13.2          | **7.1**      |
| Claude 3 Opus     | 18.9          | 29.3          | 6.1           | 0.0          |
| Gemini 1.5 Pro    | 17.4          | 23.0          | 11.4          | 3.6          |
| Gemini 1.0 Pro    | 13.2          | 19.4          | 5.3           | 3.6          |
| Claude 3 Sonnet   | 7.5           | 11.5          | 2.7           | 0.0          |
| Gemini 1.5 Flash  | 6.0           | 8.9           | 1.8           | 3.6          |
| Reka Core         | 5.4           | 7.9           | 1.8           | 3.6          |
| Claude 3 Haiku    | 4.5           | 6.3           | 1.8           | 3.6          |
| LLaVa-1.6-34B     | 2.7           | 3.7           | 1.8           | 0.0          |
| LLaVa-1.5-13B     | 1.8           | 2.6           | 0.9           | 0.0          |
| LLaVa-1.5-7B      | 1.5           | 2.6           | 0.0           | 0.0          |
| BLIP2-FLAN-T5-XXL | 0.9           | 0.5           | 1.8           | 0.0          |
| CogVLM            | 0.9           | 1.6           | 0.0           | 0.0          |
| QWEN              | 0.9           | 1.6           | 0.0           | 0.0          |
| InstructBLIP      | 0.6           | 0.5           | 0.9           | 0.0          |

## Steps to Reproduce

1. Install [Python](https://www.python.org).

1. Install the [package installer for Python](https://pypi.org/project/pip/) (pip).

1. Install the necessary packages: `pip install torch requests Pillow transformers openai matplotlib tiktoken transformers_stream_generator einops torchvision`

1. Run the scripts in `eval_scripts/`, for example `blip.py`:

   - `python ./eval_scripts/blip.py`


## Attribution

This dataset was created by Andrew Gritsevskiy, Arjun Panickssery, Derik Kauffman, Joe Cavanagh, Jonathan Chiang, Aaron Kirtland, Hans Gundlach, Irina Gritsevskaya, Lydia La Roux, and Michelle Hung. Attributions for images used within rebuses are individially available in data.csv.


## Citation

If you use this dataset, please cite

```
@misc{gritsevskiy2024rebus,
      title={REBUS: A Robust Evaluation Benchmark of Understanding Symbols}, 
      author={Andrew Gritsevskiy and Arjun Panickssery and Aaron Kirtland and Derik Kauffman and Hans Gundlach and Irina Gritsevskaya and Joe Cavanagh and Jonathan Chiang and Lydia La Roux and Michelle Hung},
      year={2024},
      eprint={2401.05604},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

