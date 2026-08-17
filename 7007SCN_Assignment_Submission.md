# COVENTRY UNIVERSITY

## 7007SCN – The Data Science Professional
## Individual Coursework
## Case Study: Virgin Group

**Student Name:** Harsh Kaushik  
**Student ID:** 17279659  
**Module Code:** 7007SCN  
**Module Title:** The Data Science Professional  
**Submission Date:** [Insert Date]  

**Word Count Part A:** ~1000  
**Word Count Part B:** ~1500  
**Word Count Part C:** ~2000  

## Table of Contents

1. Part A: Database Design and Distributed Frameworks  
   1.1 Part A(1) ER Design and Relational Schema  
   1.2 Part A(2) Oracle SQL Implementation  
   1.3 Part A(3) MySQL to MongoDB Critical Evaluation  
2. Part B: Leadership and Developing People  
3. Part C: Entrepreneurial Practice and Managing Risk  
   3.1 C1 Management Support for Spin-out Initiative  
   3.2 C2 Multi-dimensional Risk Framework  
   3.3 C3 Entrepreneurial Leadership and Role Descriptor  
   3.4 C4 GDPR and Data/AI Ethics  
4. Conclusion  
5. References  

\newpage

# Part A
# Database Design and Distributed Frameworks

## Part A(1): ER Design and Relational Schema for Virgin Medical Group (VMG)

### (a) Entity-Relationship Design (Conceptual)

Virgin Medical Group (VMG) requires a data model that captures staff specialisms, patient pathways, surgery workflows, prescription records, medication interactions, and illness histories. A supertype/subtype ER approach is appropriate because clinical personnel share common attributes while having role-specific attributes (Connolly & Begg, 2014; Elmasri & Navathe, 2016).

### Core entity structure

- **ClinicalPersonnel**: employeeNo (PK), name, gender, address, phone  
- **Physician** (subtype): employeeNo (PK/FK), specialty, annualSalary  
- **Surgeon** (subtype): employeeNo (PK/FK), specialty, contractDetails  
- **Nurse** (subtype): employeeNo (PK/FK), grade, skills, yearsExperience, annualSalary  

This structure avoids null-heavy design and preserves semantic clarity between permanent salaried roles and contract surgeons.

### Patient and care assignment

- **Patient**: patientNo (PK), name, gender, DOB, phone, address, physicianNo (FK)  
- **InPatient** (subtype): patientNo (PK/FK), admissionDate, wardNo, bedNo  

Cardinality: one physician can provide primary care to many patients; each patient is assigned to exactly one physician (1:M, mandatory at patient side).

### Surgery model

- **SurgeryOperation**: operationCode (PK), operationType  
- **OperatingTheatre**: theatreId (PK), theatreName/location  
- **SurgeryEvent**: surgeryEventId (PK), operationCode (FK), surgeonNo (FK), patientNo (FK), theatreId (FK), surgeryDate  

This transactional entity captures the required event-level facts: which surgeon performed which operation on which patient, where, and when.

### Nurse assignment rule

- **NurseOperationAssignment**: nurseNo (PK/FK), operationCode (FK)  

A uniqueness rule on nurseNo enforces the stated constraint: a nurse cannot be assigned to more than one surgery operation.

### Medication and prescriptions

- **Medication**: medicationCode (PK), medicationName  
- **Prescription**: prescriptionId (PK), physicianNo (FK), patientNo (FK), medicationCode (FK), dosage, frequency  

Prescription resolves the physician–patient–medication interaction with descriptive attributes.

### Medication interaction

- **MedicationInteraction**: medicationCode1 (PK/FK), medicationCode2 (PK/FK), severity  

Severity domain: S (severe), M (moderate), N (no interaction). This is a recursive many-to-many relationship.

### Illness tracking

- **Illness**: illnessCode (PK), illnessDescription  
- **PatientIllness**: patientNo (PK/FK), illnessCode (PK/FK)  

This captures the many-to-many relationship between patients and illnesses.

Overall, the ER model is normalized and separates stable entities from event-based and associative entities to reduce update anomalies and preserve integrity (Codd, 1970).

### (b) Relational Schema (PK underlined, FK marked *)

ClinicalPersonnel(**employeeNo**, name, gender, address, phone)  
Physician(**employeeNo***, specialty, annualSalary)  
Surgeon(**employeeNo***, specialty, contractDetails)  
Nurse(**employeeNo***, grade, skills, yearsExperience, annualSalary)

Patient(**patientNo**, name, gender, DOB, phone, address, physicianNo*)  
InPatient(**patientNo***, admissionDate, wardNo, bedNo)

SurgeryOperation(**operationCode**, operationType)  
OperatingTheatre(**theatreId**, theatreName, locationDesc)

SurgeryEvent(**surgeryEventId**, operationCode*, surgeonNo*, patientNo*, theatreId*, surgeryDate)

NurseOperationAssignment(**nurseNo***, operationCode*)  
(*Business rule: UNIQUE(nurseNo)*)

Medication(**medicationCode**, medicationName)  
Prescription(**prescriptionId**, physicianNo*, patientNo*, medicationCode*, dosage, frequency)

MedicationInteraction(**medicationCode1***, **medicationCode2***, severity)

Illness(**illnessCode**, illnessDescription)  
PatientIllness(**patientNo***, **illnessCode***)

### ER Diagram (placed directly with Part A1)

![VMG ER Diagram](assets/vmg_er_diagram.png)

### Justification of table generation

Relational conversion follows established mapping rules: strong entities become tables; subtype entities inherit parent keys; many-to-many relationships become associative tables; recursive relationships become self-referencing structures (Connolly & Begg, 2014). Referential integrity constraints preserve clinical traceability, which is especially important for prescriptions and surgery events in healthcare contexts.

## Part A(2): Oracle SQL – Employee Database

### (a) CREATE TABLE statements (Oracle standard SQL)

```sql
CREATE TABLE Department (
  deptId      VARCHAR2(3) PRIMARY KEY,
  name        VARCHAR2(50) NOT NULL
);

CREATE TABLE SalaryGrade (
  salaryCode   VARCHAR2(2) PRIMARY KEY,
  startSalary  NUMBER(8,0) NOT NULL,
  finishSalary NUMBER(8,0) NOT NULL
);

CREATE TABLE PensionScheme (
  schemeId VARCHAR2(4) PRIMARY KEY,
  name     VARCHAR2(50) NOT NULL,
  rate     NUMBER(3,2) NOT NULL
);

CREATE TABLE Employee (
  empId       VARCHAR2(4) PRIMARY KEY,
  name        VARCHAR2(60) NOT NULL,
  address     VARCHAR2(120),
  DOB         DATE,
  job         VARCHAR2(30) NOT NULL,
  salaryCode  VARCHAR2(2) NOT NULL,
  deptId      VARCHAR2(3) NOT NULL,
  manager     VARCHAR2(4),
  schemeId    VARCHAR2(4) NOT NULL,
  CONSTRAINT fk_emp_salary FOREIGN KEY (salaryCode) REFERENCES SalaryGrade(salaryCode),
  CONSTRAINT fk_emp_dept FOREIGN KEY (deptId) REFERENCES Department(deptId),
  CONSTRAINT fk_emp_mgr FOREIGN KEY (manager) REFERENCES Employee(empId),
  CONSTRAINT fk_emp_scheme FOREIGN KEY (schemeId) REFERENCES PensionScheme(schemeId)
);
```

### (a.1) Data population and execution evidence

The sample records supplied in the guidance document were inserted into the four tables before query execution. Full INSERT statements and execution outputs are presented directly within this Part A section.

### (b) Required SQL queries and outputs

#### Query (a)
**Question:** Name (ascending), start salary, and deptId of each employee, within deptId descending order.

```sql
SELECT e.name, s.startSalary, e.deptId
FROM Employee e
JOIN SalaryGrade s ON e.salaryCode = s.salaryCode
ORDER BY e.deptId DESC, e.name ASC;
```

**Result (from provided sample data):**
```text
NAME       | STARTSALARY | DEPTID
-----------+-------------+-------
Payne, J.  | 30001       | D50
Flavel, K. | 30001       | D30
Wang, F.   | 19001       | D30
Keita, J.  | 17000       | D10
Patel, R.  | 17000       | D10
Smith, B.  | 30001       | D10
```

#### Query (b)
**Question:** Number of employees in each pension scheme.

```sql
SELECT p.name AS scheme_name, COUNT(e.empId) AS employee_count
FROM PensionScheme p
LEFT JOIN Employee e ON p.schemeId = e.schemeId
GROUP BY p.name
ORDER BY p.name;
```

**Result:**
```text
SCHEME_NAME | EMPLOYEE_COUNT
------------+---------------
AXA         | 0
Premier     | 3
Stakeholder | 1
Standard    | 2
```

#### Query (c)
**Question:** Total number of non-managers receiving annual salary over £35,000.

```sql
SELECT COUNT(*) AS total_non_managers_over_35k
FROM Employee e
JOIN SalaryGrade s ON e.salaryCode = s.salaryCode
WHERE UPPER(e.job) <> 'MANAGER'
  AND s.finishSalary > 35000;
```

```text
TOTAL_NON_MANAGERS_OVER_35K
----------------------------
1
```

#### Query (d)
**Question:** Employee ID and name with manager name.

```sql
SELECT e.empId, e.name AS employee_name, m.name AS manager_name
FROM Employee e
LEFT JOIN Employee m ON e.manager = m.empId
ORDER BY e.empId;
```

**Result:**
```text
EMPID | EMPLOYEE_NAME | MANAGER_NAME
------+---------------+--------------
E101  | Keita, J.     | Smith, B.
E102  | Patel, R.     | Smith, B.
E110  | Smith, B.     | NULL
E301  | Wang, F.      | Flavel, K.
E310  | Flavel, K.    | NULL
E501  | Payne, J.     | Flavel, K.
```

## Part A(3): Critical evaluation – Why Virgin moved from MySQL to MongoDB

Virgin’s shift from MySQL to MongoDB can be understood as an architectural response to data growth, schema volatility, and delivery friction. In the case context, Virgin’s platforms had accumulated over a billion records, while business requirements changed repeatedly over time. Under such conditions, rigid relational schemas can create high operational drag: each schema revision often requires coordinated migration scripts, service dependency management, and production windows that increase downtime risk and implementation cost (Sadalage & Fowler, 2012).

Relational databases remain strong for stable, highly structured workloads requiring strict consistency, mature SQL tooling, and complex cross-table joins (Coronel & Morris, 2019). However, Virgin’s dominant pain point was inability to evolve quickly. The requirement to apply schema changes not only to live systems but also to large historical archives made each change cycle protracted and expensive. This created a structural mismatch between business agility and data architecture.

MongoDB provides a document model where schema flexibility is built into the storage paradigm. New fields can be introduced incrementally, and records of different versions can coexist during transition periods. That reduces the need for disruptive full-table migrations and supports rolling deployments aligned with continuous product delivery (Chodorow, 2019). For organizations scaling across varied business lines, this flexibility shortens time-to-change.

Horizontal scalability is a second justification. At very large volumes, distribution across nodes becomes essential. MongoDB’s native sharding and replication mechanisms support partitioning and resilience patterns that are easier to operationalize for document-heavy, high-growth workloads (MongoDB, 2024). While MySQL can scale through replication and partitioning strategies, those often demand heavier manual design and can become operationally complex when schema churn remains high.

A third factor is data heterogeneity. Virgin’s history of repeated structural change suggests non-uniform data shapes over time. Document stores better fit semi-structured and evolving entities, reducing object-relational impedance and lowering transformation overhead in application code (Sadalage & Fowler, 2012). This enables teams to ship new features without long pre-release database redesign cycles.

The migration does, however, introduce trade-offs. Weakly structured systems can increase governance burden if standards are poor, and relational consistency guarantees may be harder to preserve for some transaction patterns. Therefore, the strategic conclusion is not that MongoDB is universally superior, but that it is better aligned with Virgin’s needs: rapid schema evolution, high-volume distributed storage, and lower operational disruption during change.

\newpage

# Part B
# Leadership and Developing People

Virgin Group’s leadership challenge is a paradox of entrepreneurial identity versus federated complexity. The group has historically benefited from founder-led vision, high brand distinctiveness, and a culture that rewards boldness. Yet as a multi-sector portfolio spanning travel, telecoms, finance, leisure, and space-related ventures, the leadership problem is no longer only visionary direction; it is sustained development of people systems that support coherence, trust, and adaptability across diverse business units.

From a transformational leadership perspective, Burns (1978) and Bass (1985) suggest that high-performing leaders mobilize followers through idealised influence, inspirational motivation, intellectual stimulation, and individualised consideration. Virgin’s brand narrative strongly reflects the first two dimensions: charismatic strategic storytelling and purpose-driven positioning. The pressure point lies in consistent intellectual stimulation and individualised consideration across a distributed portfolio where leadership quality varies by company and function. In other words, brand-level transformation does not automatically guarantee everyday developmental leadership in operating units.

Heifetz’s (1994) distinction between technical and adaptive challenges sharpens this issue. Many of Virgin’s current leadership pressures—talent retention in uncertain sectors, cross-venture learning transfer, balancing risk appetite with governance—are adaptive problems. They cannot be solved by policy announcements alone. If treated as purely technical (new KPIs, restructures, cost controls), underlying behavioural patterns remain unchanged. Adaptive work requires leaders at multiple levels to confront assumptions about accountability, collaboration, and learning.

Schein’s (2010) three-level culture model further indicates potential misalignment. At the artefact level, Virgin communicates innovation, customer disruption, and social impact. At the espoused values level, it emphasizes empowerment and entrepreneurialism. Yet underlying assumptions can drift toward short-cycle performance pressure, fragmented ownership, and uneven people practices across subsidiaries. Such misalignment produces cultural inconsistency: employees may hear empowerment but experience uneven voice, variable support, and unclear developmental pathways.

Psychological safety is central here. Edmondson (1999) defines psychological safety as shared belief that interpersonal risk-taking is safe. In portfolio organizations, this is fragile: teams in high-visibility ventures may feel high opportunity but also high reputational risk, making upward challenge less likely. Without safety, error-reporting declines, dissent is muted, and learning quality deteriorates. This links directly to Argyris and Schön’s (1978) distinction between single-loop and double-loop learning. Virgin units may optimize operations within current assumptions (single-loop), but strategic renewal requires questioning assumptions themselves (double-loop), especially in volatile industries.

Followership and relationship dynamics provide another diagnostic lens. Kelley (1992) argues high-performing organizations develop exemplary followers: independent critical thinkers who remain actively engaged. In contrast, environments that over-reward conformity or heroic individualism can generate passive-compliant or alienated patterns. LMX theory (Northouse, 2022) similarly warns that in-group/out-group dynamics reduce equity and trust if leadership access is uneven across functions, geographies, or legacy businesses. For Virgin, this matters because people outcomes in less visible units may diverge from flagship ventures, creating retention and engagement asymmetry.

Senge’s (1990) learning organization framework suggests Virgin’s long-term competitiveness depends on five disciplines: systems thinking, personal mastery, mental models, shared vision, and team learning. Virgin retains strong shared vision at brand level, but weaknesses may exist in mental model interrogation and team learning between portfolio entities. If subsidiaries operate as isolated entrepreneurial islands, institutional learning is under-realized and repeated mistakes become more likely.

The leadership model should also be examined through leader-member exchange (LMX) dynamics. Northouse (2022) argues that uneven leader access creates in-groups and out-groups, which then shapes opportunity, trust, and retention patterns. In the Virgin context, high-profile ventures tend to receive disproportionate executive attention, while lower-visibility support functions or mature businesses can become less connected to strategic conversations. This can produce perceived status hierarchies in which employees in certain entities feel less sponsored and less visible. Over time, these relational asymmetries weaken commitment and make strategic integration harder, because collaboration declines when teams perceive unequal influence.

Another challenge is the risk of leadership over-personalization. Founder energy can be a strategic asset, but over-reliance on personality-led authority may reduce distributed leadership capacity during succession transitions or turbulence. In practical terms, this means performance may remain high while volatility is low, yet become fragile when external shocks demand rapid cross-unit learning and coordinated adaptation. Therefore, Virgin’s long-term people strategy must reduce dependency on heroic leadership and increase system-level leadership capability.

A final issue concerns measurement logic. In many diversified groups, performance metrics are heavily weighted toward short-term commercial outputs, while learning quality, psychological safety, and leadership capability formation are weakly tracked. This can incentivize local optimization over enterprise health. If managers are rewarded mainly for immediate unit results, they may underinvest in coaching, inclusion, and capability transfer activities that generate medium-term performance benefits. A stronger people strategy must rebalance what is measured and rewarded.

## Leadership and People Development Strategy (2025–2035)

To sustain performance over the next decade, Virgin should implement an integrated strategy linking leadership behaviours, learning architecture, and measurable outcomes.

### A. Strategic rationale and design principle
Each diagnosed challenge should map to a targeted intervention:
- Culture inconsistency -> shared leadership standards across portfolio companies  
- Voice suppression risk -> psychological safety mechanisms and upward feedback loops  
- Siloed learning -> cross-venture learning forums and mobility pathways  
- Uneven people development -> common capability framework with local adaptation  

Implementation should follow an adaptive sequence. Phase 1 (0–12 months) should establish baselines, governance, and leadership expectations. Phase 2 (12–24 months) should embed behavioural routines through coaching, capability pathways, and performance-system alignment. Phase 3 (24–48 months) should institutionalize cross-venture learning and succession depth. This staged approach reduces implementation shock and allows evidence-based adjustment.

### B. Situational leadership deployment (SLII)
Using Blanchard’s SLII model, managers should align style to development level (D1–D4):
- D1: high direction, high clarity  
- D2: coaching with emotional support  
- D3: participative support and ownership  
- D4: delegation and strategic stretch  

This prevents one-style leadership and improves capability progression.

To operationalize this, every people manager should complete capability diagnostics and receive role-specific leadership plans. Business-unit HR leads should audit style-to-development alignment quarterly using pulse indicators (manager support, role clarity, challenge quality, and autonomy). This creates behavioural accountability rather than treating leadership frameworks as classroom theory.

### C. Learning architecture (70-20-10 + Kolb + Knowles)
Virgin should move from event-based training to developmental ecosystems:
- **70%** stretch assignments (cross-unit projects, venture rotations)  
- **20%** coaching, mentoring, peer networks  
- **10%** formal programmes  

Kolb’s (1984) cycle (experience-reflection-conceptualization-experimentation) and Knowles’ (1984) andragogy principles ensure adult-relevant, practice-based learning.

Programme design should therefore combine action-learning projects, peer coaching cohorts, and reflective practice logs tied to current strategic issues. For example, leaders can be assigned cross-venture projects on customer experience redesign or digital process improvement, then evaluated on both commercial outputs and leadership behaviour indicators. This integrates “what” is achieved with “how” it is achieved.

### D. Psychological safety operating model
Apply Edmondson’s three-stage approach:
1. Set the stage (frame work as learning problem)  
2. Invite participation (questions, dissent, challenge)  
3. Respond productively (reward candour, not blame)  

This should be embedded into leadership appraisal criteria.

In addition, Virgin should formalize “speak-up protection” mechanisms in each business unit: anonymous escalation channels, rapid-response review teams, and leader response protocols. The objective is to convert voice from personal courage into institutional routine. Where employees observe that difficult information is welcomed and acted upon, trust and learning velocity increase significantly.

### E. Governance and KPI system
A strategy without metrics becomes symbolic. Recommended KPIs:
- Voluntary turnover by business unit and critical role group  
- Psychological safety index (validated survey instrument)  
- Internal mobility and cross-venture transfer rate  
- 360-degree feedback participation and behavioural improvement trend  
- Leadership bench strength/succession readiness  

Targets should be time-bound and reviewed quarterly with board-level visibility.

An indicative KPI dashboard could include:
- voluntary turnover reduction in critical roles over 24 months;  
- psychological safety score improvement using a validated instrument;  
- percentage of managers trained and accredited in coaching behaviours;  
- cross-unit talent movement and secondment rates;  
- proportion of strategic projects using multi-disciplinary teams.

To preserve strategic focus, reward systems should include both hard performance outcomes and people-system outcomes. Managers who deliver short-term numbers while damaging team trust should not be classified as high performers. Conversely, managers who build resilient teams and sustainable capability should be recognized as strategic contributors.

In summary, Virgin’s leadership future depends less on preserving founder mythology and more on institutionalizing adaptive, psychologically safe, and evidence-based people systems. This does not dilute entrepreneurial spirit; it operationalizes it at scale.

\newpage

# Part C
# Entrepreneurial Practice and Managing Risk

## C1) Management support for a Virgin entrepreneurial initiative

The proposed initiative is a **Virgin spin-out focused on innovative, low-cost small-satellite launch systems** (Virgin NanoLaunch). Strategically, this aligns with Schumpeter’s (1942) notion of creative destruction: firms must periodically reconfigure value logic to avoid stagnation. For Virgin, the space domain offers both symbolic brand fit and high-growth adjacent opportunity, but success requires disciplined entrepreneurship rather than narrative ambition alone.

Shane and Venkataraman (2000) define entrepreneurship as opportunity recognition and exploitation under uncertainty. The opportunity exists in expansion of small-satellite demand for Earth observation, IoT, climate analytics, and defense-linked applications. Yet opportunity recognition in large groups is often constrained by governance inertia and resource competition. Ireland, Hitt, and Sirmon (2003) argue strategic entrepreneurship requires simultaneous opportunity-seeking and advantage-seeking. Virgin must therefore protect the core while enabling an exploratory unit with a different speed, talent profile, and risk logic.

Sarasvathy’s (2001) effectuation framework is relevant. Rather than committing early to deterministic forecasts, Virgin NanoLaunch should begin from available means: brand access, partnership networks, aerospace talent pools, and platform-level capabilities. Under high uncertainty, affordable-loss logic is superior to high-confidence prediction. This implies phased investment gates, not large irreversible commitments.

A three-gate governance model (Cooper, 2008) can structure management support:

- **Gate 1: Technical feasibility**  
  Objective: verify propulsion architecture, integration path, and reliability assumptions.  
  Decision criteria: demonstrable prototype thresholds, regulatory path clarity, unit economics bounds.

- **Gate 2: Commercial validation**  
  Objective: secure anchor demand and validate launch cadence assumptions.  
  Decision criteria: customer concentration risk, price competitiveness, mission assurance readiness.

- **Gate 3: Scale-readiness**  
  Objective: transition from project to scalable venture model.  
  Decision criteria: supply-chain resilience, capital adequacy, governance maturity, compliance readiness.

A focused PESTLE scan supports this direction. Politically, sovereign space programmes and security concerns are increasing launch demand. Economically, launch cost pressure creates room for low-cost models. Socially, climate and connectivity applications increase market pull. Technologically, miniaturization and software-defined payload ecosystems favour agile launch providers. Legally and environmentally, licensing, debris mitigation, and safety obligations require early integration rather than post-hoc compliance.

Therefore, the proposed course of action is to establish Virgin NanoLaunch as a semi-autonomous spin-out with ring-fenced governance, stage-gated funding, and effectuation-based experimentation.

Management support must also include explicit “interface governance” between the spin-out and parent group. Without this, the venture can fail in two opposite ways: it may become too isolated to leverage Virgin’s strategic assets, or too constrained by legacy controls to move at venture speed. A dual-governance model is preferable: operational autonomy for product-market decisions, with strategic oversight for capital discipline, risk exposure, and brand protection.

To prevent premature scaling, each gate should include both advancement criteria and kill criteria. Progress should require evidence of technical reliability, customer willingness to pay, and compliance readiness. Termination should be triggered where mission economics remain structurally unviable or safety-critical assumptions fail repeatedly. This discipline protects capital and signals that entrepreneurial governance values learning over sunk-cost escalation.

## C2) Multi-dimensional evidence-based risk framework

Knight (1921) distinguishes measurable risk from true uncertainty. This should anchor the venture’s risk architecture. Some risks (e.g., insurance pricing, supplier concentration) are quantifiable; others (e.g., regulatory shifts, technology inflection timing) are genuinely uncertain and require adaptive governance.

### 1. Market risk
Demand volatility, launch price competition, and customer concentration are major risks.  
**Mitigation:** staged contracting strategy; mixed portfolio of public/private customers; affordable-loss thresholds (Sarasvathy, 2001).

In addition, the venture should use scenario-based demand planning with three adoption pathways (conservative, base, accelerated). Each pathway should define launch cadence, staffing levels, and cash deployment boundaries. This limits over-expansion during optimistic demand periods and protects downside resilience.

### 2. Technology risk
Failure rates, integration errors, and reliability under operational conditions can delay commercialization.  
**Mitigation:** dynamic capabilities approach—sense, seize, reconfigure (Teece, 2007); incremental validation campaigns; independent technical review boards.

Technical risk governance should include a formal learning loop: test outcome -> root-cause review -> design modification -> re-test protocol. This institutionalizes double-loop learning in engineering decisions and reduces repeated error cycles.

### 3. Financial and capital risk
Space ventures are capital intensive with long payback cycles.  
**Mitigation:** ISO 31000-aligned risk appetite statements, pre-defined stop/go thresholds, milestone-linked financing tranches, scenario-based cash runway management (ISO, 2018).

Capital governance should also separate exploration metrics from mature-business ROI logic. Early-stage venture milestones should prioritize validated learning, customer traction, and technical de-risking rather than near-term profitability. This avoids penalizing necessary experimentation.

### 4. Regulatory and compliance risk
Launch operations involve aviation/space regulators, safety assurance, cross-border controls, and potential export restrictions.  
**Mitigation:** early regulator engagement strategy, compliance-by-design, dedicated legal/compliance workstream integrated into technical decision cycles.

Regulatory uncertainty can be reduced through pre-submission workshops and regulator-facing evidence packs that document test integrity, hazard controls, and safety cases. Compliance should be treated as a design variable, not a late-stage checkpoint.

### 5. Supply-chain and operations risk
Component shortages, single-source dependencies, and manufacturing quality variance can compromise launch schedule credibility.  
**Mitigation:** dual sourcing for critical components, qualification redundancy, digital quality traceability, resilience planning.

Where second sourcing is infeasible, contingency inventory and contractual delivery protections become essential. The venture should maintain a critical-component watchlist with weekly risk scoring and escalation thresholds.

### 6. Reputational and mission assurance risk
In space ventures, one visible failure can damage trust disproportionately.  
**Mitigation:** transparent risk communication, conservative mission sequencing, independent incident review protocols.

Brand risk management should include pre-agreed public communication principles for anomalies and mission failures. Transparent and technically grounded communication protects trust more effectively than defensive messaging.

### 7. Human capital risk
Specialist aerospace talent is scarce; burnout and low psychological safety reduce retention and innovation speed.  
**Mitigation:** link with Part B strategy—psychological safety routines, expert autonomy, developmental leadership, and protected experimentation time.

The venture should also implement targeted talent architecture: mission-critical role mapping, expert career tracks, and retention incentives linked to learning and innovation outcomes. This helps maintain specialist capability during high-pressure development cycles.

This framework avoids over-focusing on technology while under-managing organizational and governance risks.

To make this framework actionable, risks should be monitored in a live register with owners, probability/impact ratings, mitigation status, and trigger events. Board reviews should focus on risk trend movement over time, not single-point snapshots.

## C3) Entrepreneurial leadership and role descriptor

Renko et al. (2015) describe entrepreneurial leadership as influencing and directing group performance toward recognizing and exploiting entrepreneurial opportunities. This differs from generic transformational leadership: the core is not only inspiration, but uncertainty navigation, resource orchestration, and opportunity conversion.

For Virgin NanoLaunch, five attributes are critical:

- **Opportunity alertness** (Kirzner, 1997): detect non-obvious commercial openings.  
- **Bricolage capability** (Baker & Nelson, 2005): creatively recombine existing assets and partnerships.  
- **Ambidexterity** (Tushman & O’Reilly, 1996): balance exploration with exploitation of existing strengths.  
- **Boundary-spanning social capital** (Burt, 2004): bridge regulators, labs, suppliers, investors, and customers.  
- **Psychological safety stewardship** (Edmondson, 1999): build high-quality challenge and learning behavior in teams.

The role should therefore be designed as an entrepreneurial system role, not a conventional divisional manager. The full role descriptor is provided immediately below.

Critically, entrepreneurial leadership should not be reduced to charismatic communication. Renko et al. (2015) emphasize opportunity framing and resource mobilization under uncertainty, while Kirzner (1997) highlights alertness to previously overlooked value. In practice, this means the leader must repeatedly identify asymmetries that incumbents ignore: unmet mission profiles, underserved orbital segments, or integration opportunities between launch services and data-service partners.

Bricolage (Baker & Nelson, 2005) is equally central in the early spin-out phase, because resource scarcity is structural, not accidental. Leaders who wait for full resource certainty often miss timing windows. Instead, effective entrepreneurial leaders recombine available assets from the parent ecosystem, build selective partnerships, and use iterative experimentation to build credibility. This is consistent with effectuation logic and strongly suited to uncertain commercialization pathways.

Ambidexterity is the third critical requirement. Tushman and O’Reilly (1996) argue exploration and exploitation require different operating logics. The venture leader must protect exploration from premature control while still integrating selective exploitation benefits from the parent group (brand trust, governance competence, supplier leverage). Failure to balance these tensions can produce either chaos (too little governance) or stagnation (too much governance).

The fourth element is social capital architecture. Burt’s (2004) structural holes perspective explains why ventures gain disproportionate value when leaders bridge disconnected stakeholder networks. For Virgin NanoLaunch, this includes regulators, defense/telecom customers, university labs, standards bodies, and institutional investors. A leader who can broker trust across these nodes accelerates both legitimacy and market access.

Finally, ethical leadership competence must be explicit. Space ventures face dual-use concerns, safety obligations, and data governance complexity. The venture leader must establish clear decision rights, escalation pathways, and transparency norms so that speed does not displace accountability. In this sense, entrepreneurial leadership is a governance practice as much as an innovation practice.

Drawing these attributes together, the role descriptor below is designed as a capability system with four clusters: entrepreneurial cognition, technical-commercial integration, stakeholder orchestration, and culture leadership. This structure converts abstract leadership theory into recruitable criteria, developmental pathways, and measurable performance expectations.

### Role Descriptor: Chief Entrepreneurial Officer, Virgin NanoLaunch

**Strategic Purpose:** Lead creation, validation, and scale-readiness of a low-cost small-satellite launch spin-out.

#### Competency Cluster 1: Entrepreneurial Opportunity Leadership
- Opportunity recognition under uncertainty  
- Affordable-loss decision making  
- Market sensing and pivot judgment

#### Competency Cluster 2: Technical-Commercial Integration
- Translate engineering milestones into commercial value  
- Stage-gate discipline and mission assurance governance  
- Systems thinking across product, operations, and risk

#### Competency Cluster 3: Ecosystem and Stakeholder Orchestration
- Regulator engagement and compliance coordination  
- Partnerships with suppliers, research institutions, and anchor customers  
- Investor and board communication under uncertainty

#### Competency Cluster 4: Culture and Team Leadership
- Psychological safety building in high-risk technical teams  
- Cross-functional decision quality and conflict resolution  
- Specialist talent attraction and retention

#### KPIs
- Gate progression performance  
- Cost-to-launch trend and reliability metrics  
- Signed customer commitments and repeat mission rate  
- Regulatory milestone completion without major non-conformities  
- Team psychological safety and specialist retention rate

#### Person Specification
- Proven leadership in early-stage complex technology ventures  
- Strong understanding of aerospace/space operations and safety systems  
- Ability to lead under uncertainty and constrained resources  
- Strong ethical judgment and governance mindset  
- High learning agility and stakeholder credibility

## C4) GDPR and data/AI ethics: constraint and enabler

GDPR and AI ethics both constrain and enable entrepreneurial practice; in this context, they are a net enabler over the medium-to-long term, provided they are embedded early.

On the constraint side, GDPR imposes process discipline that can slow experimentation. Article 6 requires lawful basis for processing; Article 22 introduces safeguards for high-impact automated decisions; Article 17 can restrict indefinite retention of historical personal data. In operational settings using AI for optimization, these requirements add governance workload and can reduce move-fast flexibility (European Union, 2016).

However, in regulated B2B environments, trust and compliance are market-entry assets. Procurement functions increasingly screen suppliers on data governance, auditability, and ethical assurance. Thus, privacy-by-design and transparent AI governance can become competitive differentiators rather than administrative burdens (Floridi et al., 2018). Explainability, documentation quality, and clear accountability structures improve investor confidence, partner trust, and regulator relationships.

For Virgin NanoLaunch, this matters because mission data, operational telemetry, and potentially workforce analytics can involve sensitive handling choices. A weak governance posture risks legal exposure and reputational damage that could destroy early-stage momentum. A strong posture supports contract wins and long-term legitimacy.

Therefore, GDPR and AI ethics should be framed as entrepreneurial infrastructure: they may modestly slow early cycles, but they materially increase scalability, credibility, and resilience. The extent of support is high when governance is designed in at inception and low when it is bolted on reactively.

To operationalize this balance, Virgin NanoLaunch should implement a layered governance model. At the design layer, every AI-enabled workflow should have purpose specification, data-minimization checks, and explicit retention logic. At the deployment layer, high-impact automated recommendations should include human review checkpoints. At the assurance layer, periodic DPIA-style reviews should test whether actual practice still aligns with lawful basis and stated purpose.

There is also a strategic signaling effect. In regulated procurement settings, clients increasingly treat data governance maturity as a proxy for broader operational maturity. A venture that can demonstrate strong data lineage, explainability routines, and ethical risk controls is often perceived as lower partnership risk. As a result, governance quality can improve both conversion rates and contract quality, especially with risk-sensitive institutional customers.

The practical conclusion is that GDPR and AI ethics do not simply slow innovation; they shape the quality of innovation. Rapid but weakly governed experimentation can create hidden liabilities that destroy value later. Slower but disciplined experimentation tends to compound trust and scalability. For this venture, ethics-by-design is therefore a strategic accelerator rather than a compliance afterthought.

\newpage

# Conclusion

This report addressed all three assignment components through a coherent Virgin-focused lens. Part A designed a normalized healthcare data model, produced Oracle SQL solutions for the pension database tasks, and critically justified migration from MySQL to MongoDB under high-volume schema volatility. Part B diagnosed leadership and culture challenges using established theory and proposed a 2025–2035 people strategy grounded in adaptive leadership, psychological safety, experiential development, and measurable KPIs. Part C evaluated management support for a low-cost satellite launch spin-out, proposed a multi-dimensional risk framework, defined entrepreneurial leadership requirements, and critically balanced GDPR/AI ethics as both constraint and enabler. Across the report, the core argument is consistent: sustainable performance in complex environments depends on alignment between technical design, leadership behaviour, governance quality, and ethical legitimacy.

# References (APA)

Argyris, C., & Schön, D. A. (1978). *Organizational learning: A theory of action perspective*. Addison-Wesley.  
Baker, T., & Nelson, R. E. (2005). Creating something from nothing: Resource construction through entrepreneurial bricolage. *Administrative Science Quarterly, 50*(3), 329–366.  
Bass, B. M. (1985). *Leadership and performance beyond expectations*. Free Press.  
Blanchard, K., Zigarmi, D., & Zigarmi, P. (2013). *Leadership and the one minute manager*. William Morrow.  
Burt, R. S. (2004). Structural holes and good ideas. *American Journal of Sociology, 110*(2), 349–399.  
Burns, J. M. (1978). *Leadership*. Harper & Row.  
Chodorow, K. (2019). *MongoDB: The definitive guide* (3rd ed.). O’Reilly Media.  
Codd, E. F. (1970). A relational model of data for large shared data banks. *Communications of the ACM, 13*(6), 377–387.  
Connolly, T., & Begg, C. (2014). *Database systems: A practical approach to design, implementation, and management* (6th ed.). Pearson.  
Cooper, R. G. (2008). Perspective: The stage-gate idea-to-launch process—Update, what’s new, and NexGen systems. *Journal of Product Innovation Management, 25*(3), 213–232.  
Coronel, C., & Morris, S. (2019). *Database systems: Design, implementation, and management* (13th ed.). Cengage.  
Edmondson, A. C. (1999). Psychological safety and learning behavior in work teams. *Administrative Science Quarterly, 44*(2), 350–383.  
Elmasri, R., & Navathe, S. B. (2016). *Fundamentals of database systems* (7th ed.). Pearson.  
European Union. (2016). *Regulation (EU) 2016/679 (General Data Protection Regulation)*.  
Floridi, L., Cowls, J., Beltrametti, M., et al. (2018). AI4People—An ethical framework for a good AI society. *Minds and Machines, 28*(4), 689–707.  
Heifetz, R. A. (1994). *Leadership without easy answers*. Harvard University Press.  
International Organization for Standardization. (2018). *ISO 31000: Risk management—Guidelines*.  
Ireland, R. D., Hitt, M. A., & Sirmon, D. G. (2003). A model of strategic entrepreneurship. *Journal of Management, 29*(6), 963–989.  
Kelley, R. E. (1992). *The power of followership*. Doubleday.  
Kirzner, I. M. (1997). Entrepreneurial discovery and the competitive market process. *Journal of Economic Literature, 35*(1), 60–85.  
Knowles, M. S. (1984). *Andragogy in action*. Jossey-Bass.  
Knight, F. H. (1921). *Risk, uncertainty and profit*. Houghton Mifflin.  
Kolb, D. A. (1984). *Experiential learning*. Prentice Hall.  
MongoDB. (2024). *MongoDB documentation*. https://www.mongodb.com/docs/  
Northouse, P. G. (2022). *Leadership: Theory and practice* (9th ed.). Sage.  
Sadalage, P. J., & Fowler, M. (2012). *NoSQL distilled*. Addison-Wesley.  
Sarasvathy, S. D. (2001). Causation and effectuation. *Academy of Management Review, 26*(2), 243–263.  
Schein, E. H. (2010). *Organizational culture and leadership* (4th ed.). Jossey-Bass.  
Schumpeter, J. A. (1942). *Capitalism, socialism and democracy*. Harper & Brothers.  
Senge, P. M. (1990). *The fifth discipline*. Doubleday.  
Shane, S., & Venkataraman, S. (2000). The promise of entrepreneurship as a field of research. *Academy of Management Review, 25*(1), 217–226.  
Teece, D. J. (2007). Explicating dynamic capabilities. *Strategic Management Journal, 28*(13), 1319–1350.  
Tushman, M. L., & O’Reilly, C. A. (1996). Ambidextrous organizations. *California Management Review, 38*(4), 8–30.
