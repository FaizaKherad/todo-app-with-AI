---

description: "Task list for Web Application & Database Persistence feature implementation"
---

# Tasks: Web Application & Database Persistence

**Input**: Design documents from `/specs/002-web-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are included as per feature specification requirements.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: Following the Next.js structure from plan.md
- All paths are relative to repository root

<!--
  ============================================================================
  Generated tasks based on:
  - User stories from spec.md (with their priorities P1, P2, P3...)
  - Feature requirements from plan.md
  - Entities from data-model.md
  - Endpoints from contracts/
  ============================================================================

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create Next.js project structure in repository root
- [X] T002 Install dependencies: next, react, react-dom, typescript, @types/react, @types/node, tailwindcss, postgresql client
- [X] T003 [P] Configure Tailwind CSS following official Next.js setup guide
- [X] T004 Setup TypeScript configuration with Next.js recommended settings
- [X] T005 Create initial directory structure: src/app/, src/components/, src/lib/, src/types/, public/, styles/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 Setup NeonDB PostgreSQL connection in src/lib/db.ts
- [X] T007 [P] Create database initialization function that checks/creates tasks table in src/lib/db.ts
- [X] T008 Create Task type definition in src/types/task.ts based on data model
- [X] T009 [P] Create task data access functions in src/lib/tasks.ts (get all, create, update, delete, toggle completion)
- [X] T010 [P] Setup API route handlers structure in src/app/api/
- [X] T011 Configure environment variables handling for database connection
- [X] T012 Setup error handling middleware for API responses

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - View Task List in Web Interface (Priority: P1) 🎯 MVP

**Goal**: Allow users to view their tasks in a web browser with clear completion status and empty state message

**Independent Test**: System can be tested by accessing the web application in a browser and verifying that tasks are displayed correctly, delivering the core value of web-based task viewing.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

- [X] T013 [P] [US1] Contract test for GET /api/tasks endpoint in tests/contract/test_tasks_api.py
- [X] T014 [P] [US1] Integration test for viewing task list in tests/integration/test_view_tasks.py

### Implementation for User Story 1

- [X] T015 [P] [US1] Create TaskList component in src/components/TaskList/TaskList.tsx
- [X] T016 [P] [US1] Create TaskItem component in src/components/TaskItem/TaskItem.tsx
- [X] T017 [US1] Implement GET /api/tasks endpoint in src/app/api/tasks/route.ts
- [X] T018 [US1] Create page to display task list in src/app/page.tsx
- [X] T019 [US1] Add UI for empty state message when no tasks exist
- [X] T020 [US1] Style components with Tailwind CSS following design requirements
- [X] T021 [US1] Add loading states and error handling for task retrieval

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Add Tasks via Web Interface (Priority: P1)

**Goal**: Enable users to create new tasks through the web interface by entering title and optional description

**Independent Test**: System can be tested by entering a title in the web form and submitting it, then verifying the task appears in the list, delivering the value of task creation through the web interface.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [X] T022 [P] [US2] Contract test for POST /api/tasks endpoint in tests/contract/test_tasks_api.py
- [X] T023 [P] [US2] Integration test for adding tasks in tests/integration/test_add_tasks.py

### Implementation for User Story 2

- [X] T024 [P] [US2] Create TaskForm component in src/components/TaskForm/TaskForm.tsx
- [X] T025 [US2] Implement POST /api/tasks endpoint in src/app/api/tasks/route.ts
- [X] T026 [US2] Add form validation for title (1-255 chars) and description (0-1000 chars)
- [X] T027 [US2] Integrate TaskForm with the main page to add new tasks
- [X] T028 [US2] Add client-side error handling for validation failures
- [X] T029 [US2] Update UI to show newly added tasks immediately

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 5 - Toggle Task Completion via Web Interface (Priority: P1)

**Goal**: Allow users to mark tasks as complete/incomplete through the web interface with UI updates

**Independent Test**: System can be tested by toggling a task's completion status and verifying the change persists, delivering the value of completion tracking through the web interface.

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [X] T030 [P] [US5] Contract test for PATCH /api/tasks/{id}/complete endpoint in tests/contract/test_tasks_api.py
- [X] T031 [P] [US5] Integration test for toggling task completion in tests/integration/test_toggle_completion.py

### Implementation for User Story 5

- [X] T032 [P] [US5] Implement PATCH /api/tasks/{id}/complete endpoint in src/app/api/tasks/[id]/complete/route.ts
- [X] T033 [US5] Update TaskItem component to include completion toggle UI in src/components/TaskItem/TaskItem.tsx
- [X] T034 [US5] Add client-side logic to toggle completion status
- [X] T035 [US5] Update UI to visually distinguish completed vs incomplete tasks
- [X] T036 [US5] Add error handling for completion toggle operations

**Checkpoint**: At this point, User Stories 1, 2, AND 5 should all work independently

---

## Phase 6: User Story 3 - Update Tasks via Web Interface (Priority: P2)

**Goal**: Allow users to edit their tasks through the web interface by modifying title and description

**Independent Test**: System can be tested by editing a task's title or description and verifying the changes persist, delivering the value of task modification through the web interface.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [X] T037 [P] [US3] Contract test for PUT /api/tasks/{id} endpoint in tests/contract/test_tasks_api.py
- [X] T038 [P] [US3] Integration test for updating tasks in tests/integration/test_update_tasks.py

### Implementation for User Story 3

- [X] T039 [P] [US3] Implement PUT /api/tasks/{id} endpoint in src/app/api/tasks/[id]/route.ts
- [X] T040 [US3] Extend TaskForm component to support editing existing tasks in src/components/TaskForm/TaskForm.tsx
- [X] T041 [US3] Add edit functionality to TaskItem component
- [X] T042 [US3] Add client-side validation for update operations
- [X] T043 [US3] Update UI to reflect changes after successful updates

**Checkpoint**: At this point, User Stories 1, 2, 5, AND 3 should all work independently

---

## Phase 7: User Story 4 - Delete Tasks via Web Interface (Priority: P2)

**Goal**: Allow users to delete tasks through the web interface with appropriate confirmation

**Independent Test**: System can be tested by selecting a task for deletion and confirming the action, then verifying the task is removed, delivering the value of task deletion through the web interface.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [X] T044 [P] [US4] Contract test for DELETE /api/tasks/{id} endpoint in tests/contract/test_tasks_api.py
- [X] T045 [P] [US4] Integration test for deleting tasks in tests/integration/test_delete_tasks.py

### Implementation for User Story 4

- [X] T046 [P] [US4] Implement DELETE /api/tasks/{id} endpoint in src/app/api/tasks/[id]/route.ts
- [X] T047 [US4] Add delete functionality to TaskItem component with confirmation dialog
- [X] T048 [US4] Add client-side logic for task deletion
- [X] T049 [US4] Add error handling for deletion operations
- [X] T050 [US4] Update UI to remove deleted tasks from the list

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T051 [P] Documentation updates in README.md and docs/
- [X] T052 Code cleanup and refactoring across all components
- [X] T053 Performance optimization for API calls and UI rendering
- [X] T054 [P] Additional unit tests in tests/unit/
- [X] T055 Security hardening of API endpoints and validation
- [X] T056 Run quickstart.md validation to ensure setup instructions work
- [X] T057 Add comprehensive error boundary handling
- [X] T058 Implement responsive design for all screen sizes

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 5 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US5 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for GET /api/tasks endpoint in tests/contract/test_tasks_api.py"
Task: "Integration test for viewing task list in tests/integration/test_view_tasks.py"

# Launch all components for User Story 1 together:
Task: "Create TaskList component in src/components/TaskList/TaskList.tsx"
Task: "Create TaskItem component in src/components/TaskItem/TaskItem.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 5 → Test independently → Deploy/Demo
5. Add User Story 3 → Test independently → Deploy/Demo
6. Add User Story 4 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 5
   - Developer D: User Story 3
   - Developer E: User Story 4
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence