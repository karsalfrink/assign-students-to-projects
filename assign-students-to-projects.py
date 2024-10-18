import random
from collections import defaultdict
import csv
from unidecode import unidecode

def load_students(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return [tuple(line.strip().split(',')) for line in f]

def load_projects(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return [tuple(line.strip().split(',')) for line in f]

def assign_projects(students, projects):
    student_groups = defaultdict(list)
    for student, group in students:
        student_groups[group].append(student)
    
    group_projects = {group: (project, case_study) for project, group, case_study in projects}
    
    assignments = []
    
    # Sort groups randomly to ensure fair distribution
    groups = list(student_groups.keys())
    random.shuffle(groups)
    
    for group in groups:
        group_students = student_groups[group]
        group_project, group_case_study = group_projects[group]
        
        available_projects = [
            (p, g, c) for p, g, c in projects
            if g != group and c != group_case_study
        ]
        
        if len(available_projects) < len(group_students):
            print(f"Warning: Not enough suitable projects for all students in {group}")
            available_projects = projects  # Fall back to all projects if necessary
        
        for student in group_students:
            if available_projects:
                project = random.choice(available_projects)
                assignments.append((student, group, group_case_study, project[0], project[2]))
            else:
                print(f"Error: No suitable project found for {student} from {group}")
    
    # Sort assignments by student name, considering accented characters
    assignments.sort(key=lambda x: unidecode(x[0].lower()))
    
    return assignments, group_projects

def save_assignments_csv(assignments, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Student', 'Original Group', 'Original Case Study', 'Assigned Project', 'Assigned Project Case Study'])
        writer.writerows(assignments)

def save_assignments_markdown(assignments, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("| Student | Original Group | Original Case Study | Assigned Project | Assigned Project Case Study |\n")
        f.write("|---------|----------------|---------------------|------------------|---------------------|\n")
        for student, orig_group, orig_case_study, assigned_project, assigned_case_study in assignments:
            f.write(f"| {student} | {orig_group} | {orig_case_study} | {assigned_project} | {assigned_case_study} |\n")

def main():
    students = load_students('students.csv')
    projects = load_projects('projects.csv')

    result, group_projects = assign_projects(students, projects)

    save_assignments_csv(result, 'assignments.csv')
    save_assignments_markdown(result, 'assignments.md')

    print("Student Project Assignments:")
    for student, orig_group, orig_case_study, assigned_project, assigned_case_study in result:
        print(f"{student} (Group: {orig_group}, Case Study: {orig_case_study}) is assigned to '{assigned_project}' (Case Study: {assigned_case_study})")

    project_counts = defaultdict(int)
    case_study_counts = defaultdict(int)
    for _, _, _, project, case_study in result:
        project_counts[project] += 1
        case_study_counts[case_study] += 1

    print("\nProject distribution:")
    for project, count in project_counts.items():
        print(f"'{project}': {count}")

    print("\nCase Study distribution:")
    for case_study, count in case_study_counts.items():
        print(f"'{case_study}': {count}")

    print("\nVerifying assignments:")
    for student, orig_group, orig_case_study, assigned_project, assigned_case_study in result:
        if orig_group == next(group for project, group, _ in projects if project == assigned_project):
            print(f"Error: {student} from {orig_group} was assigned their own group's project: {assigned_project}")
        elif orig_case_study == assigned_case_study:
            print(f"Error: {student} from {orig_group} was assigned a project with the same case study: {assigned_case_study}")
        else:
            print(f"OK: {student} from {orig_group} (Original Case Study: {orig_case_study}) was assigned {assigned_project} (Case Study: {assigned_case_study})")

if __name__ == "__main__":
    main()