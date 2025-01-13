# Ml_chatbot

# Threat Generation Model

## Overview

This project focuses on training a **threat generation model** using **GPT-2 (medium)** for Natural Language Processing (NLP). The model is designed to generate realistic cybersecurity threat descriptions based on a comprehensive dataset compiled from multiple sources, including **MITRE ATT&CK tactics, Common Vulnerabilities and Exposures (CVEs) from 1999-2024, and various cyber threat types** (e.g., SQL Injection, XSS, Ransomware, etc.).

## Dataset

The dataset consists of  **259,743 rows** , combining structured and unstructured threat intelligence data. It integrates:

* **MITRE ATT&CK tactics** : Each tactic represents a category of threats with descriptions.
* **CVEs (Common Vulnerabilities and Exposures)** : Includes CVE IDs with corresponding descriptions from 1999 to 2024.
* **General Cyber Threats** : Contains named cyber threats such as SQL Injection, Ransomware, XSS, along with their detailed descriptions.

### Example Data Structure

| Threat Name          | Description Threat                                                                                                  |
| -------------------- | ------------------------------------------------------------------------------------------------------------------- |
| SQL Injection Attack | SQL injection is a type of attack where an attacker injects malicious SQL code into a web application's database... |
| CVE-2008-4031        | Microsoft Office Word 2000 SP3, 2002 SP3, 2003 SP3, and 2007 Gold and SP1...                                        |
| Reconnaissance       | Adversaries may gather information about identities and roles within the victim organization...                     |
| Initial Access       | Adversaries may introduce computer accessories, networking hardware, or other computing devices...                  |

## Model Training

### Model: `gpt2-medium`

* The model was trained on the compiled dataset to learn cybersecurity threat patterns and generate new threat descriptions.
* **Training duration:** Each epoch took approximately 3 **hours** due to the dataset size.
* **Hardware:** The training process was conducted on a high-performance computing setup to handle the extensive data.

## Training Process

1. **Data Preprocessing:**
   * Cleaned and formatted data to ensure consistency.
   * Tokenized text and prepared input sequences for GPT-2.
2. **Fine-Tuning GPT-2:**
   * Used **transfer learning** on `gpt2-medium` with a  **causal language modeling objective** .
   * Employed **gradient accumulation** to manage memory usage.
3. **Evaluation:**
   * Evaluated generated text based on coherence, relevance, and accuracy.
   * Compared generated outputs with real-world threat descriptions.

## Results & Observations

* The model successfully learned patterns in cybersecurity threat descriptions and generated meaningful threat reports.
* Some challenges included:
  * Handling rare or complex threat descriptions.
  * Avoiding redundant threat explanations.
  * Ensuring descriptions remained realistic and did not generate misleading information.
* The generated threats closely resembled real-world cybersecurity threats from the dataset.

## Applications

This model can be useful for:

* **Cybersecurity Research** : Generating synthetic cybersecurity threats for testing and training purposes.
* **Threat Intelligence Automation** : Assisting in generating new threat descriptions for security analysts.
* **Adversarial Simulation** : Developing realistic threat scenarios for cybersecurity training exercises.

## Future Improvements

* Experimenting with **larger transformer models** (e.g., GPT-3, Llama) for improved threat description accuracy.
* Integrating **adversarial training** to detect and mitigate model-generated hallucinations.
* Enhancing **dataset diversity** by incorporating more structured threat intelligence sources.

## Installation & Usage

### Prerequisites

* Python 3.8+
* PyTorch
* Hugging Face Transformers
* Pandas, NumPy, and other dependencies

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/linataataa/Ml_chatbot.git
   cd ML_chatbot
   ```
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Run model inference:

   ```bash
   python generative_AI/app_gen_ai.py --input "SQL Injection Attack"
   ```

## Acknowledgments

* **MITRE ATT&CK** for providing structured threat intelligence.
* **CVE Database** for cybersecurity vulnerability data.
* **Hugging Face** for pre-trained NLP models and libraries.
