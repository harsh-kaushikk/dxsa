### Query a output
| name       |   startSalary | deptId   |
|------------|---------------|----------|
| Payne, J.  |         30001 | D50      |
| Flavel, K. |         30001 | D30      |
| Wang, F.   |         19001 | D30      |
| Keita, J.  |         17000 | D10      |
| Patel, R.  |         17000 | D10      |
| Smith, B.  |         30001 | D10      |

### Query b output
| scheme_name   |   employee_count |
|---------------|------------------|
| AXA           |                0 |
| Premier       |                3 |
| Stakeholder   |                1 |
| Standard      |                2 |

### Query c output
|   total_non_managers_over_35k |
|-------------------------------|
|                             1 |

### Query d output
| empId   | employee_name   | manager_name   |
|---------|-----------------|----------------|
| E101    | Keita, J.       | Smith, B.      |
| E102    | Patel, R.       | Smith, B.      |
| E110    | Smith, B.       | NULL           |
| E301    | Wang, F.        | Flavel, K.     |
| E310    | Flavel, K.      | NULL           |
| E501    | Payne, J.       | Flavel, K.     |
