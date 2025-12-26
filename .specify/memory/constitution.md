# Todo Evolution Project – Constitution

## 1. Purpose

This project implements a progressively evolving **Todo Application** across five structured phases using **Spec-Kit Plus** and **Qwen**.  
All functionality must be derived from **formal specifications**, refined until **Qwen** generates correct implementations without any manual code writing.

The project also integrates a **conversational AI agent**, deployed locally and to the cloud, capable of managing todos via natural language.

---

## 2. Core Principles

### 2.1 Spec-Driven Development (Mandatory)

- Every feature **must begin with a written Specification**
- No implementation may exist without an approved Spec
- Specs are refined iteratively until Qwen generates correct output
- Manual code writing is **strictly prohibited**

### 2.2 Constitution-First Workflow

- This Constitution defines **non-negotiable rules**
- All Specs and implementations must comply with this document
- Any conflict between code and the Constitution is resolved in favor of the Constitution

### 2.3 AI-Generated Implementation Only

- All application code must be generated using **Qwen**
- Humans may:
  - Write or refine Specs
  - Evaluate output
  - Request regeneration
- Humans may **not**:
  - Hand-edit generated source code
  - Patch bugs manually
  - Add logic outside of spec regeneration

---

## 3. Required Core Functionality (All Phases)

Every applicable phase must support the following Todo essentials:

1. **Add Task** – Create new todo items  
2. **Delete Task** – Remove tasks from the list  
3. **Update Task** – Modify task details (title, description, due date, etc.)  
4. **View Task List** – Display all tasks  
5. **Mark as Complete** – Toggle task completion state  

These capabilities must be accessible programmatically and, in later phases, via natural language.

---

## 4. Five-Phase Evolution Model

### Phase I – Core Todo Engine
- Local, non-AI Todo system
- CRUD operations only
- Spec-defined data model and behavior
- No chatbot, no deployment

### Phase II – Persistence & Validation
- Persistent storage (file or database)
- Input validation rules defined in Specs
- Error handling specified formally

### Phase III – Conversational AI Interface
- Natural language Todo management
- Integration with:
  - OpenAI Chatkit
  - OpenAI Agents SDK
  - Official MCP SDK
- AI must interpret user intent (e.g., “Move my unfinished tasks to tomorrow”)

### Phase IV – Local Cloud-Native Deployment
- Containerized application
- Deployed locally using **Minikube**
- Kubernetes manifests generated from Specs
- AI chatbot fully functional in cluster

### Phase V – Cloud Deployment & Scaling
- Deployment to **DigitalOcean Kubernetes (DOKS)**
- Environment configuration via Specs
- Scalable AI chatbot service
- Production-ready architecture

---

## 5. Specification Requirements

Every feature spec **must include**:

- Feature intent and user goal
- Inputs and outputs
- State changes
- Validation rules
- Error cases
- AI interpretation rules (where applicable)
- Deployment expectations (Phases IV–V)

Each phase must have:
- A **Phase Specification**
- Individual **Feature Specifications**

---

## 6. AI Chatbot Rules (Phases III–V)

- The chatbot is the **primary interface** for advanced interaction
- Must support:
  - Task creation
  - Task updates
  - Task deletion
  - Rescheduling
  - Completion toggling
- Must respond deterministically based on Specs
- Must not hallucinate tasks or states

---

## 7. Deployment & Infrastructure Rules

### Local Deployment (Phase IV)
- Minikube required
- Kubernetes manifests must be AI-generated
- No manual YAML editing

### Cloud Deployment (Phase V)
- DigitalOcean Kubernetes (DOKS) only
- Secrets and environment variables defined in Specs
- Infrastructure behavior must be reproducible

---

## 8. Quality & Acceptance Criteria

A phase is considered complete only when:

- All Specs are written and approved
- Qwen generates the implementation
- All required features function as specified
- No manual code changes exist
- AI chatbot behavior matches Spec definitions
- Deployment targets function successfully (Phases IV–V)

---

## 9. Prohibited Actions

The following are strictly forbidden:

- Writing or editing source code by hand
- Skipping Specs
- Bypassing Qwen for implementation
- Deploying without Spec-defined manifests
- Adding features not defined in Specs

---

## 10. Amendment Policy

- This Constitution may evolve
- Amendments must be documented, versioned, and justified
- No amendment may remove the requirement for Spec-Driven Development

---

**This Constitution governs the entire lifecycle of the Todo Evolution Project and is binding for all contributors, humans and AI alike.**
