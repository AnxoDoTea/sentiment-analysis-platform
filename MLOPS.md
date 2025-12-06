# MLOps & Fine-Tuning Pipeline

## Overview
This document describes the lifecycle of the LLMs used for sentiment classification and crisis detection.

## Model Details
- **Base Model**: Gemma 2B-it or Phi-2.
- **Task**: Sequence Classification (Sentiment) + Text Generation (Crisis explanation).
- **Format**: 4-bit Quantized (BNB4bit).

## Pipeline Steps

### 1. Data Collection & Labeling
- Raw tweets and news are stored in a "Silver" layer in Data Lake (or S3-compatible MinIO).
- Periodic jobs select high-variance samples for human/GPT-4 review to create a "Gold" dataset.

### 2. Fine-Tuning (Training)
We use a **PEFT (Parameter-Efficient Fine-Tuning)** approach with **QLoRA**.

**Script**: `train/finetune.py`
- Loads base model + tokenizer.
- Applies LoRA adapters (Target modules: `q_proj`, `v_proj`).
- Training on "Gold" dataset.
- Tracks metrics (Loss, Perplexity) to **Weights & Biases (W&B)**.

### 3. Versioning & Registry
- **MLflow**: Used as the Model Registry.
- Upon successful training run, the adapter weights (`adapter_model.bin`) are versioned in MLflow.
- Tags: `production`, `staging`, `archived`.

### 4. Deployment (Inference Service)
- The Inference Pod pulls the latest `production` adapter from MLflow/S3 on startup.
- Uses **vLLM** or **HuggingFace Pipeline** to serve requests.
- **Dynamic Adapter Loading**: (Advanced) Switch adapters on the fly for different brands without restarting the service.

## Experiment Tracking
All experiments logs to W&B:
- Hyperparameters (learning rate, batch size, r, alpha).
- Evaluation metrics (Accuracy, F1-Score on test set).
