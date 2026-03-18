# LLM Institution Example

This example demonstrates how to use the Google GenAI SDK (Gemini 3) to simulate a policymaker role in an "agriculture and rural development" context. It showcases the powerful combination of **Thinking Mode** and **Structured Output** to perform complex reasoning and return valid JSON data.

## Project Overview

In this simulation, the LLM acts as a policymaker who receives historical data on land use and ecosystem services. The goal is to achieve specific policy targets (e.g., increasing agroforestry area, enhancing high-diversity landscape features) by adjusting subsidies and taxes.

## Prerequisites

- **Python**: Version 3.9 or higher is recommended.
- **Gemini API Key**: You must have a valid API key from [Google AI Studio](https://aistudio.google.com/).

## Setup

1. **Clone or Download** the repository to your local machine.

2. **Create a Virtual Environment (venv)**
   Open a terminal in the project folde and run:
   ```
   python -m venv myenv
   ```
   You can replace 'myenv' with the your desired venv name. Then, activate the venv by running:
   On macOS / Linux:
   ```
   source myenv/bin/activate
   ```
   On Windows (Command Prompt):
   ```
   myenv\Scripts\activate
   ```
   On Windows (PowerShell):
   ```
   myenv\Scripts\Activate.ps1
   ```
2. **Install Dependencies**:
   Open a terminal in the root directory (where `requirements.txt` is located) and run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables (very important)**:
   - Create a `.env` file in the root directory of the project.
   - Add your Gemini API key to the file:
     ```env
     GEMINI_API_KEY=your_actual_api_key_here
     ```

## Running the Example

Navigate to the `LLM_institution_example` directory and execute the main script:

```bash
cd LLM_institution_example
python llm_inst.py
```

The script will:
1. Load historical simulation data.
2. Formulate a prompt for Gemini.
3. Call the Gemini API with thinking mode enabled.
4. Print the model's internal reasoning (thoughts) and the final structured JSON decision.

## Core Logic

### 1. Role-Play & Reasoning
The example uses a sophisticated prompt (`prompts.py`) that defines:
- **Role**: A policymaker in agriculture and rural development.
- **Instruments**: 11 levels of subsidies and taxes.
- **Targets**: Specific ecological and agricultural goals.
- **Thinking Mode**: The model is configured to "think step-by-step" before making decisions, ensuring evidence-informed and logically-sound policies.

### 2. Technical Implementation
The core functionality is in `llm_inst.py`:
- **Pydantic Schemas**: Defines `OutputSchema` and `PolicyDecisions` to enforce a strict JSON structure for the model's response.
- **Thinking Configuration**: Uses `types.ThinkingConfig` to enable the model's internal reasoning process.
- **Structured Output**: Uses `response_mime_type="application/json"` and `response_schema` to ensure the final output is machine-readable.

### 3. I/O Schema
The model receives:
- `model_historical_output`: JSON-like string of land use trends.
- `policy_historical`: JSON-like string of previous policy levels.

The model produces:
- `reasoning`: A text description of the logic.
- `policy_decisions`: A dictionary of 6 specific policy instruments and their assigned levels (-5 to 5).

## File Structure

- `llm_inst.py`: Main execution script containing the API client setup and logic.
- `prompts.py`: Contains the detailed system prompt used for the simulation.
- `requirements.txt`: (In root) List of necessary Python packages.
- `.env`: (In root) Stores your API key securely.
