import os
import subprocess
from excel_generator import generate_excel_report

def grade_all_submissions(language):
    submissions_folder = "uploads/submissions"
    inputs_folder = "uploads/inputs"
    expected_folder = "uploads/expected_outputs"
    outputs_folder = "uploads/student_outputs"
    os.makedirs(outputs_folder, exist_ok=True)

    submissions = os.listdir(submissions_folder)
    inputs = sorted(os.listdir(inputs_folder))

    results = []

    for sub in submissions:
        student_result = {
            "filename": sub,
            "results": []
        }

        sub_path = os.path.join(submissions_folder, sub)
        compiled = False
        exec_path = None

        if language == "c":
            exec_path = sub_path.replace(".c", ".exe")
            compile_cmd = ["gcc", sub_path, "-o", exec_path]
        elif language == "cpp":
            exec_path = sub_path.replace(".cpp", ".exe")
            compile_cmd = ["g++", sub_path, "-o", exec_path]
        elif language == "python":
            compiled = True
            student_result["results"].append("Interpreted Language")
        else:
            student_result["results"].append("Unsupported Language")
            results.append(student_result)
            continue

        if not compiled and language != "python":
            try:
                subprocess.run(compile_cmd, check=True)
                compiled = True
                student_result["results"].append("Compilation Success")
            except subprocess.CalledProcessError as e:
                student_result["results"].append("Compilation Error")
                results.append(student_result)
                continue

        for inp in inputs:
            input_path = os.path.join(inputs_folder, inp)
            output_file = os.path.join(outputs_folder, f"{sub}_{inp}_out.txt")

            if language in ["c", "cpp"]:
                run_cmd = [exec_path]
            elif language == "python":
                run_cmd = ["python", sub_path]
            else:
                continue

            try:
                with open(input_path, "r") as infile, open(output_file, "w") as outfile:
                    subprocess.run(run_cmd, stdin=infile, stdout=outfile, stderr=subprocess.PIPE, timeout=5)
            except subprocess.TimeoutExpired:
                student_result["results"].append(f"{inp}: Timeout")
                continue

            expected_output_file = os.path.join(expected_folder, inp.replace("input", "output"))
            if os.path.exists(expected_output_file):
                with open(output_file, "r") as student_out, open(expected_output_file, "r") as expected_out:
                    student_lines = [line.strip() for line in student_out.readlines()]
                    expected_lines = [line.strip() for line in expected_out.readlines()]
                    if student_lines == expected_lines:
                        student_result["results"].append(f"{inp}: Pass")
                    else:
                        student_result["results"].append(f"{inp}: Fail")
            else:
                student_result["results"].append(f"{inp}: No Expected Output")

        results.append(student_result)

    print("DEBUG RESULTS:", results)  # This will appear in your terminal
    report_path = generate_excel_report(results)
    print("Excel saved at:", report_path)
    return report_path
