from gpt_2 import generate_text
import os
import re


def extract_ruby_methods(code):
    methods = []
    method_pattern = re.compile(r'^\s*def\s+(\w+)', re.MULTILINE)
    
    for match in method_pattern.finditer(code):
        method_name = match.group(1)
        method_start = match.start()
        method_code = code[method_start:]
        
        method_end = re.search(r'(\n\s*\w)|(^\s*$)', method_code, re.MULTILINE).start()
        method_code = method_code[:method_end].strip()

        methods.append({
            'name': method_name,
            'code': method_code,
        })
    return methods


def find_method_info(project_data, method_name):
    for file_data in project_data:
        for method in file_data['methods']:
            if method['name'] == method_name:
                return method
    return None

def answer_method_question(question, method_name, project_data):
    method_info = find_method_info(project_data, method_name)
    if method_info:
        context = ' '.join(method_info['comments'])
        answer = generate_text(prompt=f"{question}\n\nContext: {context}")
        return answer[0]
    else:
        return "Method not found in the project."


def handle_user_question(question, method_name, project_data):
    return answer_method_question(question, method_name, project_data)




def generate_comments_for_method(function_data):
    signature = f"def {function_data['name']}"
    code = function_data['code']
    
    prompt = f"Generate comments for the following Ruby method:\n\n{signature}\n{code}\n\nComments:"
    comments_response = generate_text(prompt)
    comments = comments_response[0]
    
    return comments


def generate_test_cases(method_data):
    signature = f"def {method_data['name']}"
    code = method_data['code']
    
    prompt = f"Generate test cases for the following Ruby method:\n\n{signature}\n{code}\n\nTest cases:"
    test_cases_response = generate_text(prompt)
    test_cases = test_cases_response[0]
    
    return test_cases



def preprocess_ruby_project(project_path):
    project_data = []

    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith('.rb'):
                file_path = os.path.join(root, file)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()

                methods = extract_ruby_methods(code)

                for method in methods:
                    comments = generate_comments_for_method(method)
                    method['comments'] = comments.split('\n')
                    
                    test_cases = generate_test_cases(method)
                    method['test_cases'] = test_cases.split('\n')

                project_data.append({
                    'file_path': file_path,
                    'methods': methods
                })

    return project_data




def get_test_cases(method_name, project_data):
    method_info = find_method_info(project_data, method_name)
    if method_info:
        return method_info['test_cases']
    else:
        return None








