import random
from collections import defaultdict
import csv

def load_students(filename):
    with open(filename, 'r') as f:
        return [tuple(line.strip().split(',')) for line in f]

def load_projects(filename):
    with open(filename, 'r') as f:
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
                assignments.append((student, group, project[0], project[2]))
            else:
                print(f"Error: No suitable project found for {student} from {group}")
    
    return assignments, group_projects

def save_assignments(assignments, filename):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Student', 'Student Group', 'Assigned Project', 'Project Case Study'])
        writer.writerows(assignments)

def main():
    students = load_students('students.csv')
    projects = load_projects('projects.csv')

    result, group_projects = assign_projects(students, projects)

    save_assignments(result, 'assignments.csv')

    print("Student Project Assignments:")
    for student, student_group, project, case_study in result:
        print(f"{student} (from {student_group}) is assigned to '{project}' (Case Study: {case_study})")

    project_counts = defaultdict(int)
    case_study_counts = defaultdict(int)
    for _, _, project, case_study in result:
        project_counts[project] += 1
        case_study_counts[case_study] += 1

    print("\nProject distribution:")
    for project, count in project_counts.items():
        print(f"'{project}': {count}")

    print("\nCase Study distribution:")
    for case_study, count in case_study_counts.items():
        print(f"'{case_study}': {count}")

    print("\nVerifying assignments:")
    for student, student_group, assigned_project, assigned_case_study in result:
        student_project, student_case_study = group_projects[student_group]
        if student_group == next(group for project, group, _ in projects if project == assigned_project):
            print(f"Error: {student} from {student_group} was assigned their own group's project: {assigned_project}")
        elif student_case_study == assigned_case_study:
            print(f"Error: {student} from {student_group} was assigned a project with the same case study: {assigned_case_study}")
        else:
            print(f"OK: {student} from {student_group} (Case study: {student_case_study}) was assigned {assigned_project} (Case study: {assigned_case_study})")

if __name__ == "__main__":
    main()