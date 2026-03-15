# 🚀 Gemini UI Navigator:  Edition

An autonomous AI agent powered by **Gemini 1.5 Flash** and the **Gemini Agent Development Kit (ADK)** that interprets **Figma prototypes through computer vision** and generates **production-ready React Native code**, automatically deployed to **Google Cloud**.

---

# 🏗️ Architecture Overview

The system follows a **Hybrid Edge-Cloud Architecture**:

### Local Edge (Gemini ADK)
Orchestrates physical automation (**Playwright / PyAutoGUI**) to navigate Figma, handle UI state, and capture high-resolution screenshots.

### Multimodal Reasoning
**Gemini 1.5 Flash** analyzes visual input to extract exact branding, colors *( Red #EC111A)*, and layout hierarchies.

### Cloud Persistence
Generated code is persisted in **Google Cloud Storage**.

### Live Presentation
A **Google Cloud Run microservice** fetches and renders the latest build for stakeholders.

---

# 📐 System Architecture

```mermaid
graph TD
    subgraph Local_Edge [Local Machine - Gemini ADK]
        User((User)) --> |Project Name| ADK[Gemini Agent Development Kit]
        ADK --> |Figma Vision| Model[Gemini 1.5 Flash]
        Model --> |Physical Control| Automation[Playwright & PyAutoGUI]
        Automation --> |Capture| Screenshot[debug_figma.png]
    end

    subgraph Storage_Layer [Data Persistence]
        Model --> |Generated Code| GCS_Tool[Google Cloud Storage Tool]
        GCS_Tool --> |Upload| Bucket[(GCS Bucket: bucket_gem_challenge)]
    end

    subgraph Presentation_Layer [Google Cloud Run]
        Bucket --> |Fetch .tsx| CR[Cloud Run: ui-navigator-web]
        CR --> |Render| Web((Web Landing Page))
    end