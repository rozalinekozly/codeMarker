@app.post("/upload")
async def upload_files(
    submissions: list[UploadFile] = File(...),
    inputs: list[UploadFile] = File(...),
    expected_outputs: list[UploadFile] = File(...),
    language: str = Form(...)
):
    os.makedirs("uploads/submissions", exist_ok=True)
    os.makedirs("uploads/inputs", exist_ok=True)
    os.makedirs("uploads/expected_outputs", exist_ok=True)

    print("FILES UPLOADED")

    # Save submissions
    for file in submissions:
        with open(f"uploads/submissions/{file.filename}", "wb") as f:
            f.write(await file.read())
    # Save inputs
    for file in inputs:
        with open(f"uploads/inputs/{file.filename}", "wb") as f:
            f.write(await file.read())
    # Save expected outputs
    for file in expected_outputs:
        with open(f"uploads/expected_outputs/{file.filename}", "wb") as f:
            f.write(await file.read())

    print("FILES SAVED, CALLING GRADER")

    from grader import grade_all_submissions
    report_path = grade_all_submissions(language)

    print("RETURNING RESPONSE")

    return {"status": "done", "report_url": report_path}
