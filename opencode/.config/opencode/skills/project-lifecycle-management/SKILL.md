---
name: Project Lifecycle Management  
version: 1.0.3
description: End-to-end project lifecycle management with Jira integration, design documentation, and multi-repository coordination
author: GlossGenius
keywords: [project, lifecycle, management, jira, design, documentation, workflow]
---

# Project Lifecycle Management

This skill provides comprehensive project lifecycle management from initial design phase through implementation completion, with integrated Jira tracking, documentation management, and multi-repository coordination.

## Overview

The Project Lifecycle Management skill orchestrates complex engineering projects through two distinct phases: **Design Phase** (planning and architecture) and **Implementation Phase** (execution and delivery). It acts as a project manager, delegating specific tasks to specialized sub-agents while maintaining overall project coherence and tracking.

## Project Lifecycle Phases

### Design Phase
**Focus**: Planning, architecture, and preparation

**Activities:**
- **Problem Analysis**: Analyzing project requirements and constraints
- **Scope Assessment**: Identifying impacted codebases and work scope
- **Design Documentation**: Writing comprehensive design documents (Google Docs integration)
- **Task Planning**: Creating detailed work breakdown with Jira initiatives/epics
- **Learning Documentation**: Capturing insights under `docs/learnings/`

### Implementation Phase  
**Focus**: Execution, verification, and delivery

**Activities:**
- **Parallel Implementation**: Multi-repository development coordination
- **Work Verification**: Quality assurance and testing coordination
- **Project Closure**: Final deliverable verification and handoff
- **Learning Capture**: Documenting lessons learned and best practices

## Available Commands

### /project-work
Initiates or resumes a project with comprehensive lifecycle management and task delegation.

**Usage:**
- `/project-work` - Interactive project initiation or continuation

**Capabilities:**
- **New Project Setup**: Creates Jira initiatives/epics with proper structure
- **Existing Project Resume**: Continues work on previously initiated projects  
- **Task Delegation**: Assigns specific work to specialized sub-agents
- **Progress Monitoring**: Tracks task completion and quality verification
- **Feedback Integration**: Handles feedback from Jira, GitHub, and direct user input

**Process:**
1. **Project Assessment**: Determines if creating new or continuing existing project
2. **Jira Integration**: Creates/updates initiatives, epics, and tasks
3. **Local Structure Setup**: Establishes organized project workspace
4. **Planning Documentation**: Creates and maintains implementation plans
5. **Repository Coordination**: Manages dependencies across multiple repos
6. **Execution Oversight**: Delegates and monitors specialized tasks
7. **Quality Assurance**: Verifies deliverables meet requirements

## Project Structure and Organization

### Local Project Structure
All projects organized under: `~/Development/projects/<TICKET-ID>/`

```
~/Development/projects/EN-123/
├── docs/
│   ├── plan.md              # Implementation plan (maintained)
│   └── learnings/           # Documentation of insights and lessons
│       ├── design-decisions.md
│       ├── technical-challenges.md
│       └── process-improvements.md
└── repos/                   # Cloned repositories for the project
    ├── core-services/
    ├── web-app/
    └── mobile-app/
```

### Documentation Standards
- **Implementation Plan**: `docs/plan.md` - Living document with current project status
- **Learning Capture**: `docs/learnings/` - Organized knowledge preservation
- **Design Documents**: External Google Docs integration for collaborative design
- **Progress Tracking**: Integrated with Jira for status visibility

## Jira Integration

### Project Hierarchy
- **Initiatives**: Large, strategic projects with multiple epics
- **Epics**: Smaller projects or grouped tasks under initiatives  
- **Tasks**: Specific work items with clear deliverables
- **Subtasks**: Granular work breakdown for complex tasks

### Workflow Management
- **Status Tracking**: Automatic status updates (`In Development`, `In Review`, `Done`)
- **Assignee Management**: Auto-assignment to current user when work begins
- **Atlassian Document Format**: Proper ADF formatting for descriptions
- **Command-Line Control**: Full management via `acli` command-line interface

### Jira Operations
```bash
# Create new initiative/epic
acli jira workitem create --project EN --type Initiative --title "Project Name"

# Update work items with structured JSON
acli jira workitem edit --from-json /path/to/update.json --yes

# Status transitions
acli jira workitem transition EN-123 "In Development"
```

## Git Integration and Branching Strategy

### Branch Naming Convention
Format: `<TICKET-ID>/<descriptive-title>`

**Examples:**
- `EN-123/implement-user-authentication`
- `EN-456/fix-payment-processing-bug`
- `EN-789/add-reporting-dashboard`

### Commit Message Format
```
[TICKET-ID] Descriptive commit message

Example: [EN-123] Add OAuth2 authentication flow
```

### Multi-Repository Coordination
- **Dependency Mapping**: Identifies required GlossGenius repositories
- **Parallel Development**: Coordinates work across multiple codebases
- **Branch Synchronization**: Manages inter-repository dependencies
- **Integration Testing**: Ensures compatibility across repositories

## Task Delegation and Sub-Agent Management

### Sub-Agent Coordination
The Project Lifecycle Management skill acts as an orchestrator, delegating specialized tasks to appropriate sub-agents:

- **Code Development**: Delegates to development specialists
- **Testing**: Assigns to testing and QA agents  
- **Documentation**: Routes to technical writing specialists
- **Review**: Coordinates code review processes
- **Deployment**: Manages release and deployment tasks

### Quality Assurance
- **Deliverable Verification**: Ensures all work meets project requirements
- **Progress Monitoring**: Tracks task completion and quality metrics
- **Risk Management**: Identifies and mitigates project risks
- **Stakeholder Communication**: Manages updates and reporting

## Feedback Handling and Adaptation

### Multi-Channel Feedback Integration
- **Direct User Feedback**: Immediate project adjustments
- **Jira Comments**: Contextual feedback on specific tasks
- **GitHub Reviews**: Code-level feedback and improvements
- **Stakeholder Input**: Business and technical stakeholder concerns

### Feedback Processing Workflow
1. **Feedback Distillation**: Understands underlying requirements and concerns
2. **Impact Assessment**: Evaluates effect on current plan and timeline
3. **Plan Adjustment**: Modifies project plan to address feedback
4. **Task Creation**: Creates new work items for substantial changes
5. **Communication**: Responds appropriately on the feedback channel
6. **Risk Evaluation**: Ensures changes don't contradict core requirements

### Feedback Categories
- **Clarification Requests**: Technical or business requirement clarification
- **Scope Changes**: Modifications to project scope or deliverables
- **Technical Corrections**: Code quality or architecture improvements
- **Process Improvements**: Workflow or methodology enhancements

## Project Phases and Transitions

### Phase Transition Criteria
**Design → Implementation:**
- Design document approved and shared
- All epics and tasks created in Jira
- Repository dependencies identified and accessible
- Implementation plan documented and reviewed

**Implementation → Closure:**
- All tasks completed and verified
- Quality assurance passed
- Documentation updated
- Stakeholder acceptance obtained

### Phase Management
- **Phase Gates**: Clear criteria for phase transitions
- **Milestone Tracking**: Regular progress checkpoints
- **Risk Assessment**: Continuous risk evaluation and mitigation
- **Resource Allocation**: Optimal distribution of effort across phases

## Advanced Features

### Learning Management System
- **Knowledge Capture**: Systematic documentation of insights
- **Best Practice Development**: Identifies and promotes successful patterns
- **Process Improvement**: Continuous workflow optimization
- **Knowledge Sharing**: Makes learnings available for future projects

### Multi-Project Coordination
- **Portfolio Management**: Handles multiple concurrent projects
- **Resource Conflicts**: Manages competing priorities and dependencies
- **Timeline Coordination**: Ensures project schedules don't conflict
- **Cross-Project Learning**: Shares insights across project boundaries

### Integration Ecosystem
- **Jira Integration**: Full lifecycle tracking and management
- **GitHub Integration**: Code repository management and coordination
- **Google Docs**: Collaborative design document creation
- **Slack/Teams**: Communication and notification integration

## Security and Compliance

### Data Management
- **Access Control**: Proper permission management for project resources
- **Sensitive Information**: Secure handling of confidential project data
- **Audit Trail**: Complete tracking of project decisions and changes
- **Compliance**: Adherence to organizational security policies

### Quality Standards
- **Code Quality**: Ensures high standards through review processes
- **Documentation Quality**: Maintains comprehensive and clear documentation
- **Process Compliance**: Follows established engineering workflows
- **Security Review**: Includes security considerations in all phases

## Performance and Scalability

### Efficient Project Management
- **Parallel Execution**: Maximizes concurrent work streams
- **Resource Optimization**: Efficient allocation of human and technical resources
- **Bottleneck Identification**: Proactive identification and resolution of constraints
- **Timeline Management**: Realistic scheduling with buffer management

### Scalability Features
- **Large Project Support**: Handles complex, multi-team projects
- **Repository Scalability**: Manages projects spanning many codebases
- **Team Coordination**: Supports large development teams
- **Stakeholder Management**: Handles multiple stakeholder groups

## Technical Requirements

### Dependencies
- **Atlassian CLI (`acli`)**: Jira integration and management
- **Git CLI**: Version control and branch management  
- **GitHub CLI (`gh`)**: GitHub repository operations
- **Node.js**: For Atlassian MCP server operations
- **Network Access**: API connectivity to Jira, GitHub, Google Docs

### System Integration
- **MCP Protocol**: Atlassian service integration
- **OAuth Authentication**: Secure service authentication
- **API Integration**: REST API connectivity for external services
- **File System Access**: Local project structure management

### Environment Setup
```bash
# Required tools installation
brew install atlassian-cli
npm install -g @atlassian/mcp-server

# Configuration
acli auth login
gh auth login
```

This skill transforms complex project management into an organized, efficient process that maintains high quality standards while maximizing development velocity and stakeholder satisfaction.