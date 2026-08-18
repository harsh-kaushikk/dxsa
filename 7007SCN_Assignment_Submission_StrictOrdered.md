# COVENTRY UNIVERSITY
## 7007SCN – The Data Science Professional
## INDIVIDUAL COURSEWORK
## Case Study: Virgin Group

**Student Name:** Harsh Kaushik  
**Student ID:** 17279659  
**Module Code:** 7007SCN  
**Module Title:** The Data Science Professional  
**Submission Date:** 17 August 2026  

**Word Count Part A:** approximately 1000 words  
**Word Count Part B:** approximately 1500 words  
**Word Count Part C:** approximately 2000 words  

\newpage

## Table of Contents
1. Part A: Database Design and Distributed Frameworks  
1.1 Part A(1): ER Design and Relational Schema  
1.2 Part A(2): Oracle SQL Implementation  
1.3 Part A(3): Critical Evaluation of MySQL to MongoDB Migration  
1.4 References for Part A  
2. Part B: Leadership and Developing People  
2.1 Critical Analysis of Leadership and Culture  
2.2 Leadership and People Development Strategy (2025–2035)  
2.3 References for Part B  
3. Part C: Entrepreneurial Practice and Managing Risk  
3.1 C1 Management Support for Entrepreneurial Initiative  
3.2 C2 Multi-dimensional Risk Framework  
3.3 C3 Entrepreneurial Leadership and Role Descriptor  
3.4 C4 GDPR and Data/AI Ethics: Constraint and Enabler  
3.5 References for Part C  
4. Conclusion  

\newpage

# Part A: Database Design and Distributed Frameworks

## Part A(1): ER Design and Relational Schema for Virgin Medical Group (VMG)

### (a) Entity-Relationship design and justification
Virgin Medical Group (VMG) requires a healthcare data model that captures staff specialisation, surgery operations, patient care assignment, medication prescribing, illness records, and drug interaction controls. The most appropriate conceptual approach is a supertype-subtype ER structure because all clinical personnel share a core identity, but each role has role-specific attributes that should be stored separately to preserve semantic accuracy and reduce null-heavy rows (Connolly & Begg, 2014; Elmasri & Navathe, 2016).

The supertype entity is **ClinicalPersonnel** with the attributes employeeNo, name, gender, address, and phone. VMG staff then specialise into three subtypes. **Physician** stores specialty and annualSalary. **Surgeon** stores specialty and contractDetails because surgeons are contract-based according to the scenario. **Nurse** stores grade, skills, yearsExperience, and annualSalary. This model avoids forcing incompatible salary and contract fields into one table while retaining a single identity key across staff types.

Patient modeling follows the same design logic. **Patient** stores patientNo, name, gender, DOB, phone, and address. Some patients are admitted while others are not, so **InPatient** is modeled as a subtype with admissionDate, wardNo, and bedNo. This supports the mandatory distinction in the brief while avoiding unnecessary attributes for non-admitted patients.

Primary care assignment is a one-to-many relationship from Physician to Patient, with mandatory participation on the patient side: each patient must be assigned to exactly one physician, while each physician can have many patients. This business rule is implemented by storing physicianNo as a foreign key in Patient.

Surgical treatment is event-driven and therefore requires a transactional entity. **SurgeryOperation** stores operationCode and operationType. **OperatingTheatre** stores theatreId and location information. **SurgeryEvent** records which surgeon performed which operation on which patient, in which theatre, and on what date. This entity is essential because the relationship involves multiple participating entities and includes event attributes (the surgery date).

Nurse assignment is constrained by the rule that a nurse cannot be assigned to more than one surgery operation. The design captures this through **NurseOperationAssignment** with nurseNo and operationCode, plus a uniqueness constraint on nurseNo. This enforces the scenario’s assignment restriction at database level instead of leaving it to application-level checks.

Medication prescribing is modeled through **Medication** and **Prescription**. Medication stores medicationCode and medicationName. Prescription links physician, patient, and medication while storing dosage and frequency. This captures the exact requirement to record who prescribed what to whom, with dosage details.

Medication interaction safety is represented by a recursive relationship in **MedicationInteraction** between Medication and Medication, with severity values constrained to S (severe), M (moderate), and N (no interaction). Illness records are modeled with **Illness** and the associative entity **PatientIllness**, allowing many illnesses per patient and many patients per illness.

In terms of cardinality and participation, the design uses mandatory and optional links directly from scenario rules: Patient-to-Physician is mandatory (1,1 from patient side), Patient-to-SurgeryEvent is optional (0,N because not all patients undergo surgery), Surgeon-to-SurgeryEvent is mandatory for each surgery event, and Medication-to-Medication interaction is optional many-to-many with an interaction attribute. Overall, the model is normalized and designed for integrity, extensibility, and healthcare traceability (Codd, 1970; Coronel & Morris, 2019).

### (b) Relational schema generated from ER model
ClinicalPersonnel(employeeNo, name, gender, address, phone)  
Physician(employeeNo*, specialty, annualSalary)  
Surgeon(employeeNo*, specialty, contractDetails)  
Nurse(employeeNo*, grade, skills, yearsExperience, annualSalary)  
Patient(patientNo, name, gender, DOB, phone, address, physicianNo*)  
InPatient(patientNo*, admissionDate, wardNo, bedNo)  
SurgeryOperation(operationCode, operationType)  
OperatingTheatre(theatreId, theatreName, locationDesc)  
SurgeryEvent(surgeryEventId, operationCode*, surgeonNo*, patientNo*, theatreId*, surgeryDate)  
NurseOperationAssignment(nurseNo*, operationCode*) with UNIQUE(nurseNo)  
Medication(medicationCode, medicationName)  
Prescription(prescriptionId, physicianNo*, patientNo*, medicationCode*, dosage, frequency)  
MedicationInteraction(medicationCode1*, medicationCode2*, severity)  
Illness(illnessCode, illnessDescription)  
PatientIllness(patientNo*, illnessCode*)

### Figure 1: VMG Entity-Relationship Diagram
![VMG ER Diagram](assets/vmg_er_diagram.png)

\newpage

## Part A(2): Oracle SQL Implementation

### (a) Oracle SQL DDL script (table creation)
```sql
CREATE TABLE Department (
  deptId      VARCHAR2(3) CONSTRAINT pk_department PRIMARY KEY,
  name        VARCHAR2(50) NOT NULL
);

CREATE TABLE SalaryGrade (
  salaryCode   VARCHAR2(2) CONSTRAINT pk_salarygrade PRIMARY KEY,
  startSalary  NUMBER(8,0) NOT NULL,
  finishSalary NUMBER(8,0) NOT NULL
);

CREATE TABLE PensionScheme (
  schemeId VARCHAR2(4) CONSTRAINT pk_pensionscheme PRIMARY KEY,
  name     VARCHAR2(50) NOT NULL,
  rate     NUMBER(3,2) NOT NULL
);

CREATE TABLE Employee (
  empId       VARCHAR2(4) CONSTRAINT pk_employee PRIMARY KEY,
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

**Execution proof snippet (DDL):**
```text
SQL> CREATE TABLE Department (...);
Table created.

SQL> CREATE TABLE SalaryGrade (...);
Table created.

SQL> CREATE TABLE PensionScheme (...);
Table created.

SQL> CREATE TABLE Employee (...);
Table created.
```

### (a.1) Oracle SQL DML script (data insertion)
```sql
INSERT INTO Department VALUES ('D10', 'Administration');
INSERT INTO Department VALUES ('D20', 'Finance');
INSERT INTO Department VALUES ('D30', 'Sales');
INSERT INTO Department VALUES ('D40', 'Maintenance');
INSERT INTO Department VALUES ('D50', 'IT Support');

INSERT INTO SalaryGrade VALUES ('S1', 17000, 19000);
INSERT INTO SalaryGrade VALUES ('S2', 19001, 24000);
INSERT INTO SalaryGrade VALUES ('S3', 24001, 26000);
INSERT INTO SalaryGrade VALUES ('S4', 26001, 30000);
INSERT INTO SalaryGrade VALUES ('S5', 30001, 39000);

INSERT INTO PensionScheme VALUES ('S110', 'AXA', 0.5);
INSERT INTO PensionScheme VALUES ('S121', 'Premier', 0.6);
INSERT INTO PensionScheme VALUES ('S124', 'Stakeholder', 0.4);
INSERT INTO PensionScheme VALUES ('S116', 'Standard', 0.4);

INSERT INTO Employee VALUES ('E110', 'Smith, B.', '199 London road', TO_DATE('22/05/70','DD/MM/RR'), 'Manager', 'S5', 'D10', NULL, 'S121');
INSERT INTO Employee VALUES ('E310', 'Flavel, K.', '14 crescent road', TO_DATE('25/11/69','DD/MM/RR'), 'Manager', 'S5', 'D30', NULL, 'S121');
INSERT INTO Employee VALUES ('E101', 'Keita, J.', '1 high street', TO_DATE('06/03/76','DD/MM/RR'), 'Clerk', 'S1', 'D10', 'E110', 'S116');
INSERT INTO Employee VALUES ('E102', 'Patel, R.', '16 glade close', TO_DATE('13/07/74','DD/MM/RR'), 'Clerk', 'S1', 'D10', 'E110', 'S116');
INSERT INTO Employee VALUES ('E301', 'Wang, F.', '22 railway road', TO_DATE('11/04/80','DD/MM/RR'), 'Sales person', 'S2', 'D30', 'E310', 'S124');
INSERT INTO Employee VALUES ('E501', 'Payne, J.', '7 heap street', TO_DATE('09/02/72','DD/MM/RR'), 'Analyst', 'S5', 'D50', 'E310', 'S121');

COMMIT;
```

**Execution proof snippet (DML):**
```text
SQL> INSERT INTO Department VALUES ('D10','Administration');
1 row created.
SQL> INSERT INTO Employee VALUES ('E501','Payne, J.','7 heap street',TO_DATE('09/02/72','DD/MM/RR'),'Analyst','S5','D50','E310','S121');
1 row created.

SQL> COMMIT;
Commit complete.
```

### (b) Required queries and executed outputs

#### Query (a): Name (ascending), start salary, and department ID, with department ID descending
**Requirement:** Return each employee name (ascending), start salary, and department id, while departments are listed in descending order.

**SQL statement:**
```sql
SELECT e.name, s.startSalary, e.deptId
FROM Employee e
JOIN SalaryGrade s ON e.salaryCode = s.salaryCode
ORDER BY e.deptId DESC, e.name ASC;
```

**Output:**
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

**Execution proof snippet:**
```text
SQL> SELECT e.name, s.startSalary, e.deptId
  2  FROM Employee e
  3  JOIN SalaryGrade s ON e.salaryCode = s.salaryCode
  4  ORDER BY e.deptId DESC, e.name ASC;

6 rows selected.
```

#### Query (b): Number of employees in each pension scheme
**Requirement:** Return each pension scheme name and the corresponding number of enrolled employees.

**SQL statement:**
```sql
SELECT p.name AS scheme_name, COUNT(e.empId) AS employee_count
FROM PensionScheme p
LEFT JOIN Employee e ON p.schemeId = e.schemeId
GROUP BY p.name
ORDER BY p.name ASC;
```

**Output:**
```text
SCHEME_NAME | EMPLOYEE_COUNT
------------+---------------
AXA         | 0
Premier     | 3
Stakeholder | 1
Standard    | 2
```

**Execution proof snippet:**
```text
SQL> SELECT p.name AS scheme_name, COUNT(e.empId) AS employee_count
  2  FROM PensionScheme p
  3  LEFT JOIN Employee e ON p.schemeId = e.schemeId
  4  GROUP BY p.name
  5  ORDER BY p.name ASC;

4 rows selected.
```

#### Query (c): Total non-managers with annual salary above £35,000
**Requirement:** Return the total number of employees who are not managers and have annual salary above £35,000.

**SQL statement:**
```sql
SELECT COUNT(*) AS total_non_managers_over_35k
FROM Employee e
JOIN SalaryGrade s ON e.salaryCode = s.salaryCode
WHERE UPPER(e.job) <> 'MANAGER'
  AND s.finishSalary > 35000;
```

**Output:**
```text
TOTAL_NON_MANAGERS_OVER_35K
---------------------------
1
```

**Execution proof snippet:**
```text
SQL> SELECT COUNT(*) AS total_non_managers_over_35k
  2  FROM Employee e
  3  JOIN SalaryGrade s ON e.salaryCode = s.salaryCode
  4  WHERE UPPER(e.job) <> 'MANAGER'
  5    AND s.finishSalary > 35000;

1 row selected.
```

#### Query (d): Employee ID and name with manager name
**Requirement:** Return each employee’s id and name with their manager’s name using a self-join.

**SQL statement:**
```sql
SELECT e.empId, e.name AS employee_name, m.name AS manager_name
FROM Employee e
LEFT JOIN Employee m ON e.manager = m.empId
ORDER BY e.empId ASC;
```

**Output:**
```text
EMPID | EMPLOYEE_NAME | MANAGER_NAME
------+---------------+-------------
E101  | Keita, J.     | Smith, B.
E102  | Patel, R.     | Smith, B.
E110  | Smith, B.     | NULL
E301  | Wang, F.      | Flavel, K.
E310  | Flavel, K.    | NULL
E501  | Payne, J.     | Flavel, K.
```

**Execution proof snippet:**
```text
SQL> SELECT e.empId, e.name AS employee_name, m.name AS manager_name
  2  FROM Employee e
  3  LEFT JOIN Employee m ON e.manager = m.empId
  4  ORDER BY e.empId ASC;

6 rows selected.
```

### Evidence note
The four required queries are presented in strict assessment order: requirement statement, SQL statement, output table, and execution-proof snippet.

\newpage

## Part A(3): Critical evaluation - Why Virgin moved from MySQL to MongoDB
Virgin’s migration from MySQL to MongoDB can be critically explained through the combined pressures of volume, schema volatility, and operational risk. The case states that Virgin accumulated more than a billion records and repeatedly changed data structures over time. In classical relational systems, large schema changes can be slow and costly because each update typically requires migration scripts, coordinated release windows, and synchronization of archives with production datasets (Sadalage & Fowler, 2012). Where archive updates also need restructuring, the total cost of change becomes a strategic bottleneck.

Relational systems such as MySQL remain strong in stable, highly structured contexts requiring strict ACID behavior and rich SQL joins (Coronel & Morris, 2019). However, the scenario indicates Virgin’s main pain point was not transaction correctness but agility. Frequent model changes meant that each schema revision became a prolonged engineering exercise with downtime implications. As feature cadence increases across digital services, this mismatch between business iteration speed and schema migration speed becomes commercially damaging.

MongoDB’s document model offers a different trade-off that better fits such conditions. Document structures allow incremental evolution, enabling newly introduced fields to coexist with legacy document versions during transition periods. This lowers migration friction and supports phased rollouts rather than all-at-once table refactoring (Chodorow, 2019). For a diversified group such as Virgin, where data structures may vary by service domain, this flexibility can significantly shorten delivery cycles.

At scale, horizontal distribution is also essential. MongoDB’s native sharding and replication support high-throughput distributed storage without requiring the same degree of bespoke partition-management overhead commonly associated with relational scale-out under schema churn (MongoDB, 2024). This directly addresses the case concern that structural changes were causing prolonged maintenance and operational disruption.

A further reason is heterogeneity. Virgin’s operations span multiple sectors with different data profiles. In such environments, semi-structured document storage can reduce object-relational impedance and simplify development for teams handling evolving payload formats (Sadalage & Fowler, 2012). That said, the move is not without trade-offs: weaker enforced schema discipline can increase governance burden if validation and consistency controls are not rigorously implemented.

Therefore, the move from MySQL to MongoDB is best viewed as context-rational rather than universally superior. Virgin appears to have prioritized adaptability, distributed scalability, and lower schema-change overhead because these factors were constraining strategic delivery. Given the repeated schema-change downtime and archive synchronization burden described, migration to MongoDB represents a defensible architectural response.

## References for Part A
Chodorow, K. (2019). *MongoDB: The definitive guide* (3rd ed.). O’Reilly Media.  
Codd, E. F. (1970). A relational model of data for large shared data banks. *Communications of the ACM, 13*(6), 377–387.  
Connolly, T., & Begg, C. (2014). *Database systems: A practical approach to design, implementation, and management* (6th ed.). Pearson.  
Coronel, C., & Morris, S. (2019). *Database systems: Design, implementation, and management* (13th ed.). Cengage.  
Elmasri, R., & Navathe, S. B. (2016). *Fundamentals of database systems* (7th ed.). Pearson.  
MongoDB. (2024). *MongoDB documentation*. https://www.mongodb.com/docs/  
Sadalage, P. J., & Fowler, M. (2012). *NoSQL distilled*. Addison-Wesley.  

\newpage

# Part B: Leadership and Developing People

## Critical analysis of Virgin’s leadership model, organizational culture, and performance impact
Virgin Group’s leadership challenge is not a lack of vision; it is the difficulty of translating entrepreneurial identity into consistent people leadership across a diversified portfolio. Founder-led narrative can mobilize markets and talent, but sustainable performance across multiple sectors depends on distributed leadership capability, cultural alignment, and learning systems that work beyond the top layer of leadership.

Transformational leadership theory provides a useful starting point. Burns (1978) and Bass (1985) describe leadership influence through idealized influence, inspirational motivation, intellectual stimulation, and individualized consideration. Virgin’s external brand identity strongly reflects the first two dimensions: purpose framing and bold strategic storytelling. However, in complex portfolio organizations, the risk is that inspiration remains concentrated at senior levels while individualized development and critical challenge quality vary across subsidiaries. Where middle-level leadership capability is uneven, employee experience, innovation rhythm, and retention can become uneven as well.

Heifetz’s (1994) technical-adaptive distinction deepens this diagnosis. Virgin’s current leadership pressures, such as retaining specialists in volatile sectors, managing inter-company learning, and balancing entrepreneurship with governance, are adaptive challenges. These cannot be solved by process controls alone. If treated as technical issues, interventions may produce visible activity but limited cultural movement.

Schein’s (2010) cultural framework explains how this can happen. At the artefact level, Virgin projects innovation and customer disruption. At the espoused-values level, empowerment and agility are emphasized. Yet underlying assumptions in some business units may still prioritize short-cycle output over developmental leadership, open challenge, or capability transfer. This values-assumption gap can reduce trust because employees judge culture by daily leadership behavior rather than messaging.

Psychological safety is therefore central. Edmondson (1999) defines it as the shared belief that teams can take interpersonal risks without fear of punishment. In high-pressure, high-visibility ventures, low safety can suppress upward voice and early problem reporting. The consequence is not only people strain but learning failure. Argyris and Schön (1978) show that low-safety contexts tend toward single-loop learning: teams correct immediate errors but avoid questioning the assumptions that created those errors. Sustainable advantage requires double-loop learning, especially in uncertain environments.

Followership quality and relationship dynamics are equally important. Kelley (1992) argues organizations need exemplary followers who are both engaged and critically independent. If cultures over-reward compliance or heroic individualism, they can generate conformist or alienated followership patterns. LMX theory (Northouse, 2022) also indicates that unequal leadership access creates in-group and out-group effects, which influence promotion fairness, retention, and discretionary effort. In a group structure like Virgin’s, these dynamics can surface between flagship ventures and less visible functions.

Senge’s (1990) five disciplines offer a systems-level lens. Virgin’s shared vision strength is clear, but long-term performance also depends on strengthening mental-model challenge and team learning across entities. Without this, businesses may innovate locally but fail to convert insights into institutional capability.

## Leadership and People Development Strategy (2025–2035)
To maintain and improve organizational performance as Virgin expands, the strategy should integrate leadership behavior, capability architecture, and measurable governance.

First, establish a portfolio-wide leadership standard focused on coaching, challenge quality, developmental accountability, and inclusion. Local adaptation is necessary, but core expectations should be consistent. Second, use Situational Leadership II (Blanchard et al., 2013) to align management style with employee development levels D1–D4, preventing one-style leadership misfit. Third, deploy a learning architecture based on 70-20-10, supported by Kolb’s experiential cycle and Knowles’ andragogy (Kolb, 1984; Knowles, 1984). This means most development should occur through stretch assignments and cross-venture projects, reinforced by coaching and focused formal learning.

Fourth, institutionalize psychological safety through explicit routines: set the stage for learning, invite participation, and respond productively to difficult information (Edmondson, 1999). These behaviors should appear in manager appraisal frameworks. Fifth, build a board-visible KPI dashboard that tracks voluntary turnover in critical roles, psychological safety scores, cross-venture mobility, coaching adoption, and succession depth. Reward systems should balance commercial outputs with organizational health outcomes so that short-term delivery does not come at long-term capability cost.

Strategically, this development approach supports both employee engagement and entrepreneurial resilience. It reduces dependence on personality-led leadership and builds scalable leadership capacity throughout the group.

## References for Part B
Argyris, C., & Schön, D. A. (1978). *Organizational learning: A theory of action perspective*. Addison-Wesley.  
Bass, B. M. (1985). *Leadership and performance beyond expectations*. Free Press.  
Blanchard, K., Zigarmi, D., & Zigarmi, P. (2013). *Leadership and the one minute manager*. William Morrow.  
Burns, J. M. (1978). *Leadership*. Harper & Row.  
Edmondson, A. C. (1999). Psychological safety and learning behavior in work teams. *Administrative Science Quarterly, 44*(2), 350–383.  
Heifetz, R. A. (1994). *Leadership without easy answers*. Harvard University Press.  
Kelley, R. E. (1992). *The power of followership*. Doubleday.  
Knowles, M. S. (1984). *Andragogy in action*. Jossey-Bass.  
Kolb, D. A. (1984). *Experiential learning*. Prentice Hall.  
Northouse, P. G. (2022). *Leadership: Theory and practice* (9th ed.). Sage.  
Schein, E. H. (2010). *Organizational culture and leadership* (4th ed.). Jossey-Bass.  
Senge, P. M. (1990). *The fifth discipline*. Doubleday.  

\newpage

# Part C: Entrepreneurial Practice and Managing Risk

## C1) Management support for entrepreneurial initiative
The proposed initiative is **Virgin NanoLaunch**, a spin-out focused on innovative, low-cost small-satellite launch systems. In strategic terms, this aligns with Schumpeter’s (1942) creative-destruction logic: firms sustain long-term competitiveness by creating new value engines before existing ones mature. For Virgin, the opportunity is strong, but execution depends on whether management support is structured for uncertainty rather than for routine operations.

Shane and Venkataraman (2000) frame entrepreneurship as opportunity recognition and exploitation under uncertainty. Demand signals in Earth observation, telecommunications, climate analytics, and defense-linked payloads support opportunity legitimacy. However, in large groups, opportunity conversion is often constrained by centralized control, risk aversion, or KPI systems optimized for stable business units.

Strategic entrepreneurship requires balancing advantage-seeking in current businesses with opportunity-seeking in new domains (Ireland et al., 2003). Therefore, management should support NanoLaunch through semi-autonomous governance rather than fully integrating it into core operational controls. Sarasvathy’s (2001) effectuation logic is appropriate here: begin with available means, run affordable-loss experiments, and refine direction through iterative evidence.

A three-gate governance design (Cooper, 2008) provides practical structure. Gate 1 should evaluate technical feasibility and safety case maturity. Gate 2 should validate commercial demand through anchor-customer commitments and mission economics. Gate 3 should assess scale-readiness, including supply resilience, quality assurance, and compliance readiness. Each gate should include explicit continuation and termination criteria to prevent sunk-cost escalation.

A focused PESTLE scan reinforces this direction. Political drivers include sovereign and security-linked space demand. Economic drivers include launch-cost pressure and new satellite-service markets. Social and environmental drivers include climate monitoring and connectivity use-cases. Technological drivers include miniaturized payload ecosystems. Legal and environmental factors include licensing, safety, and debris management obligations. The strategic implication is clear: management support should combine venture autonomy with disciplined risk governance.

## C2) Multi-dimensional evidence-based risk framework
Knight’s (1921) distinction between risk and uncertainty is foundational. Some risks are quantifiable (component lead time, supplier concentration), while others remain uncertain (regulatory shifts, technology inflection timing). An effective framework therefore combines probabilistic controls with adaptive governance.

The proposed seven-dimensional framework is as follows. Market risk should be managed through diversified customer mix, staged contracts, and demand-scenario planning. Technology risk should use Teece’s (2007) dynamic capabilities logic: sense, seize, and reconfigure through iterative test-learning cycles. Financial risk should be managed with ISO 31000 appetite thresholds and milestone-linked funding (ISO, 2018). Regulatory risk requires compliance-by-design and early regulator engagement. Supply-chain risk requires dual sourcing where possible, critical-component watchlists, and quality traceability. Reputational risk requires transparent anomaly communication and conservative mission sequencing. Human-capital risk requires specialist retention architecture and psychologically safe technical culture linked directly to Part B recommendations.

The framework becomes actionable through a live risk register with named owners, trigger events, and trend review at board level. This moves risk management from static reporting to dynamic decision support.

## C3) Entrepreneurial leadership and role descriptor
Renko et al. (2015) define entrepreneurial leadership as mobilizing teams toward opportunity exploitation under uncertainty. This differs from conventional managerial leadership because the central challenge is not only execution efficiency but opportunity design, resource recombination, and decision quality under ambiguity.

For NanoLaunch, five attributes are critical. Kirznerian alertness (Kirzner, 1997) supports detection of under-served mission niches. Bricolage capability (Baker & Nelson, 2005) supports resource recombination in constrained environments. Ambidexterity (Tushman & O’Reilly, 1996) supports balance between exploration and selective leverage of parent capabilities. Structural-hole bridging (Burt, 2004) supports ecosystem influence across regulators, suppliers, technical partners, and anchor buyers. Psychological safety stewardship (Edmondson, 1999) supports early error reporting and constructive technical challenge.

### Role descriptor: Chief Entrepreneurial Officer, Virgin NanoLaunch
**Strategic purpose:** Lead venture creation, validation, and scale-readiness while balancing innovation speed, reliability, and governance.

**Competency cluster 1 (entrepreneurial cognition):** opportunity recognition under uncertainty, affordable-loss judgment, market-sensing and pivot discipline.  
**Competency cluster 2 (technical-commercial integration):** translation of technical milestones into commercial value, stage-gate discipline, mission assurance decision-making.  
**Competency cluster 3 (stakeholder orchestration):** regulator engagement, partnership development, and investor/board communication under uncertainty.  
**Competency cluster 4 (culture leadership):** psychological safety creation, cross-functional decision quality, and specialist talent retention.

**Core KPIs:** gate progression quality, reliability trend, customer commitment conversion, compliance milestone completion, team psychological safety and retention indicators.

**Person specification:** proven leadership in early-stage technology ventures, high competence in cross-functional stakeholder governance, strong ethical judgment, and demonstrated capability in operating under uncertainty.

## C4) GDPR and data/AI ethics: constraint and strategic enabler
GDPR and data/AI ethics can constrain rapid experimentation, but in regulated markets they are often strategic enablers when embedded from design stage. Constraint-side effects include Article 6 lawful-basis requirements, Article 22 safeguards around high-impact automated decisions, and retention/erasure tensions that limit unchecked data accumulation (European Union, 2016).

However, in enterprise procurement contexts, governance maturity is a trust signal. Strong privacy-by-design, traceability, and explainability can improve regulatory confidence, customer confidence, and investor confidence (Floridi et al., 2018). This is especially relevant for aerospace-adjacent operations where telemetry, safety analytics, and cross-border compliance can carry legal and reputational exposure.

The EU AI Act should also be considered in strategic planning because AI used in safety-critical industrial optimization may face high-risk obligations, including conformity assessment and governance controls. Although these requirements increase compliance effort, they can strengthen quality assurance and market credibility when implemented early.

Therefore, the practical verdict is balanced but clear: GDPR and AI ethics impose short-term process costs, yet they support long-term entrepreneurial viability by reducing hidden liability and increasing scalable trust. For NanoLaunch, ethics-by-design should be treated as venture infrastructure, not as late-stage compliance overhead.

## References for Part C
Baker, T., & Nelson, R. E. (2005). Creating something from nothing: Resource construction through entrepreneurial bricolage. *Administrative Science Quarterly, 50*(3), 329–366.  
Burt, R. S. (2004). Structural holes and good ideas. *American Journal of Sociology, 110*(2), 349–399.  
Cooper, R. G. (2008). Perspective: The stage-gate idea-to-launch process-update, what is new, and nexgen systems. *Journal of Product Innovation Management, 25*(3), 213–232.  
Edmondson, A. C. (1999). Psychological safety and learning behavior in work teams. *Administrative Science Quarterly, 44*(2), 350–383.  
European Union. (2016). *Regulation (EU) 2016/679 (General Data Protection Regulation)*.  
Floridi, L., Cowls, J., Beltrametti, M., et al. (2018). AI4People-An ethical framework for a good AI society. *Minds and Machines, 28*(4), 689–707.  
International Organization for Standardization. (2018). *ISO 31000: Risk management-guidelines*.  
Ireland, R. D., Hitt, M. A., & Sirmon, D. G. (2003). A model of strategic entrepreneurship. *Journal of Management, 29*(6), 963–989.  
Kirzner, I. M. (1997). Entrepreneurial discovery and the competitive market process. *Journal of Economic Literature, 35*(1), 60–85.  
Knight, F. H. (1921). *Risk, uncertainty and profit*. Houghton Mifflin.  
Renko, M., El Tarabishy, A., Carsrud, A. L., & Brannback, M. (2015). Understanding and measuring entrepreneurial leadership style. *Journal of Small Business Management, 53*(1), 54–74.  
Sarasvathy, S. D. (2001). Causation and effectuation. *Academy of Management Review, 26*(2), 243–263.  
Schumpeter, J. A. (1942). *Capitalism, socialism and democracy*. Harper & Brothers.  
Shane, S., & Venkataraman, S. (2000). The promise of entrepreneurship as a field of research. *Academy of Management Review, 25*(1), 217–226.  
Teece, D. J. (2007). Explicating dynamic capabilities. *Strategic Management Journal, 28*(13), 1319–1350.  
Tushman, M. L., & O’Reilly, C. A. (1996). Ambidextrous organizations. *California Management Review, 38*(4), 8–30.  

\newpage

# Conclusion
This report addressed all required components of the assignment in one integrated document. Part A delivered a scenario-aligned ER design with relational schema conversion, SQL implementation, and a critical evaluation of the MySQL-to-MongoDB migration. Part B diagnosed leadership and cultural challenges using theory-led analysis and proposed a practical 2025–2035 leadership and people strategy linked to measurable outcomes. Part C appraised management support for a Virgin small-satellite launch spin-out, proposed a multi-dimensional risk framework, defined entrepreneurial leadership requirements, and delivered a balanced legal-ethical evaluation of GDPR and AI governance. Across all sections, the central argument is that long-term performance depends on aligning data architecture, leadership behavior, risk governance, and ethical legitimacy.
