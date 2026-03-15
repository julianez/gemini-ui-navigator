# 🚀 Figma to Code Powered by Gemini

An autonomous AI agent powered by **Gemini 3.1 Flash Lite Preview** and the **Gemini Agent Development Kit (ADK)** that interprets **Figma prototypes through computer vision** and generates **production-ready React Native code**, automatically deployed to **Google Cloud**.

---

# 🏗️ Architecture Overview

The system follows a **Hybrid Edge-Cloud Architecture**:

### Local Edge (Gemini ADK)
Orchestrates physical automation (**Playwright / PyAutoGUI**) to navigate Figma, handle UI state, and capture high-resolution screenshots.

### Multimodal Reasoning
**Gemini 3.1 Flash Lite Preview** analyzes visual input to extract exact branding, colors and layout hierarchies.

### Cloud Persistence
Generated code is persisted in **Google Cloud Storage**.

### Live Presentation
A **Google Cloud Run microservice** fetches and renders the latest build for stakeholders.

---

# 📐 System Architecture

```mermaid
%%{init: {
  "theme": "base",
  "flowchart": { "curve": "linear" },
  "themeVariables": {
    "fontFamily": "Inter, Arial, sans-serif",
    "primaryColor": "#F8FAFC",
    "primaryBorderColor": "#334155",
    "lineColor": "#475569",
    "secondaryColor": "#EEF2F7",
    "tertiaryColor": "#FFFFFF",
    "fontSize": "14px"
  }
}}%%

flowchart LR

%% USER
User((👤 User))

%% LOCAL AGENT
subgraph Agent["Local AI Agent"]
ADK["🧠 Gemini Agent Development Kit"]
Vision["👁️ UI Vision Analysis"]
Automation["🤖 Playwright + PyAutoGUI"]
Screenshot["📸 Figma Screenshot"]
end

%% AI MODEL
subgraph AI["Gemini Reasoning"]
Gemini["Gemini 3.1 Flash Lite"]
CodeGen["⚛️ React Native Code Generation"]
end

%% CLOUD STORAGE
subgraph Storage["Cloud Storage"]
GCS["📦 GCS Upload Tool"]
Bucket[("🪣 GCS Bucket\nbucket_gem_challenge")]
end

%% CLOUD RUNTIME
subgraph Runtime["Cloud Deployment"]
CloudRun["☁️ Cloud Run\nui-navigator-web"]
WebApp(("🌐 Demo Web App"))
end

%% JUDGES
Judges((🏆 Judges))

%% FLOWS
User -->|Project Name| ADK
ADK --> Vision
Vision --> Gemini
Gemini --> Automation
Automation --> Screenshot
Gemini --> CodeGen
CodeGen --> GCS
GCS --> Bucket
Bucket --> CloudRun
CloudRun --> WebApp
Judges -->|Open Demo URL| WebApp
