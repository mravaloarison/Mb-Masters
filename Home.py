import streamlit as st
from google import genai
from google.genai import types
import tempfile

# Initialize Gemini client
client = genai.Client(api_key="")  # Replace with actual key

st.title("AI Grading Assistant")

student_file = st.file_uploader("Upload student file", type=["pdf"])
instruction_file = st.file_uploader("Upload instruction file", type=["pdf"])
grading_rubrics = st.file_uploader("Upload grading rubrics", type=["pdf"])

if st.button("Submit"):
    if student_file and instruction_file and grading_rubrics:
        st.success("Files uploaded successfully!")

        # Save uploaded files temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_student:
            temp_student.write(student_file.read())
            student_path = temp_student.name

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_instruction:
            temp_instruction.write(instruction_file.read())
            instruction_path = temp_instruction.name

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_rubric:
            temp_rubric.write(grading_rubrics.read())
            rubric_path = temp_rubric.name

        # Read PDF bytes
        with open(student_path, "rb") as f:
            student_bytes = f.read()
        with open(instruction_path, "rb") as f:
            instruction_bytes = f.read()
        with open(rubric_path, "rb") as f:
            rubric_bytes = f.read()

        # Create prompt
        prompt = "Grade the student work based on the provided instructions and rubric. Provide detailed feedback and suggestions for improvement."

        student_ = client.files.upload(
            # You can pass a path or a file-like object here
            file=student_path, 
            config=dict(
                # It will guess the mime type from the file extension, but if you pass
                # a file-like object, you need to set the
                mime_type='application/pdf')
        )

        instruction_ = client.files.upload(
            # You can pass a path or a file-like object here
            file=instruction_path, 
            config=dict(
                # It will guess the mime type from the file extension, but if you pass
                # a file-like object, you need to set the
                mime_type='application/pdf')
        )

        rubric_ = client.files.upload(
            # You can pass a path or a file-like object here
            file=rubric_path, 
            config=dict(
                # It will guess the mime type from the file extension, but if you pass
                # a file-like object, you need to set the
                mime_type='application/pdf')
        )

        # Generate response
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[student_, 
                instruction_, 
                rubric_,
                prompt
            ])


        # Display feedback
        st.write("### AI Feedback:")
        st.write(response.text)

    else:
        st.error("Please upload all three files.")
