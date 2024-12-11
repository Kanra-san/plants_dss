from flask import Flask, render_template, request
import sqlite3
import json
import skfuzzy as fuzz
import skfuzzy.control as ctrl
import numpy as np
from time import time

app = Flask(__name__)


def create_fuzzy_variable(symptom_name, membership_params):
    symptom = ctrl.Antecedent(np.arange(0, 11, 1), symptom_name)
    for function in membership_params["functions"]:
        label = function["label"]
        points = function["points"]
        if len(points) == 4:
            symptom[label] = fuzz.trapmf(symptom.universe, points)
        elif len(points) == 3:
            symptom[label] = fuzz.trimf(symptom.universe, points)
    return symptom


def create_disease_severity_variable(disease_name):

    print(f"Creating Consequent for disease: Original Name='{disease_name}'")

    severity = ctrl.Consequent(np.arange(0, 11, 1), disease_name)
    severity["Low"] = fuzz.trimf(severity.universe, [0, 0, 5])
    severity["Medium"] = fuzz.trimf(severity.universe, [3, 5, 7])
    severity["High"] = fuzz.trimf(severity.universe, [5, 10, 10])

    return severity


def construct_disease_rules(disease_data, antecedents, disease_consequent):
    rules = []
    grouped_conditions = {"High": [], "Medium": []}

    print("Constructing disease rules...")
    for condition in disease_data["conditions"]:
        symptom_name = condition["SymptomName"]
        symptom_condition = condition["Condition"]

        print(f"Checking condition: {symptom_name} - {symptom_condition}")

        if symptom_name in antecedents:
            antecedent = antecedents[symptom_name]
            print(f"Available labels in antecedent '{symptom_name}': {antecedent.terms.keys()}")

            if symptom_condition in antecedent.terms:
                symptom_rule = antecedent[symptom_condition]
                print(f"Adding rule for {symptom_name} - {symptom_condition}")
                grouped_conditions["High"].append(symptom_rule)
            else:
                print(f"Condition '{symptom_condition}' not found in antecedent '{symptom_name}' terms")
        else:
            print(f"Symptom '{symptom_name}' not found in antecedents")

    for severity, conditions in grouped_conditions.items():
        if severity == "High" and conditions:
            print(f"Creating {severity} severity rule with {len(conditions)} conditions.")
            combined_conditions = conditions[0]
            for condition in conditions[1:]:
                combined_conditions = combined_conditions & condition
            print(f"Final combined rule for {severity} severity: {combined_conditions}")
            rule = ctrl.Rule(combined_conditions, disease_consequent["High"])
            rules.append(rule)

        if severity == "High" and len(conditions) > 0:
            total_conditions = len(disease_data["conditions"])
            present_conditions = len(conditions)

            print(f"Total conditions: {total_conditions}, Present conditions: {present_conditions}")
            if present_conditions > total_conditions / 2:
                print(f"Creating Medium severity rule with {len(conditions)} conditions.")
                combined_conditions = conditions[0]
                for condition in conditions[1:]:
                    combined_conditions = combined_conditions & condition
                print(f"Final combined rule for Medium severity: {combined_conditions}")
                rule = ctrl.Rule(combined_conditions, disease_consequent["Medium"])
                rules.append(rule)

    if not rules:
        print("No rules were constructed.")
    else:
        print(f"Constructed {len(rules)} rules.")
        for rule in rules:
            print(f"Rule: {rule}")

    return rules


@app.route('/')
def home():
    conn = sqlite3.connect("plant_diseases.db")
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT FlowerName FROM flowers")
    flowers = [row[0] for row in cursor.fetchall()]
    conn.close()
    return render_template("home.html", flowers=flowers)


@app.route('/symptoms', methods=['POST'])
def symptoms():
    flower_name = request.form.get("flower")
    conn = sqlite3.connect("plant_diseases.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT s.SymptomName, s.MembershipParameters
        FROM symptoms s
        JOIN rule_conditions rc ON s.SymptomID = rc.SymptomID
        JOIN rules r ON rc.RuleID = r.RuleID
        JOIN diseases d ON r.DiseaseID = d.DiseaseID
        JOIN flowers f ON d.FlowerID = f.FlowerID
        WHERE f.FlowerName = ?
    """, (flower_name,))
    symptoms_data = cursor.fetchall()
    if not symptoms_data:
        return f"No symptoms found for the selected flower: {flower_name}"

    symptoms = []
    for symptom_name, membership_params in symptoms_data:
        membership_params = json.loads(membership_params)
        symptoms.append({"name": symptom_name.strip(), "membership_params": membership_params})
    conn.close()
    return render_template("symptoms.html", flower=flower_name, symptoms=symptoms)


@app.route('/results', methods=['POST'])
def results():
    start_time = time()
    symptom_inputs = {key: float(value) for key, value in request.form.items() if key != "flower"}
    flower_name = request.form.get("flower")
    print(f"Symptom inputs received: {symptom_inputs}")

    conn = sqlite3.connect("plant_diseases.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT d.DiseaseName, d.Description
        FROM diseases d
        JOIN flowers f ON d.FlowerID = f.FlowerID
        WHERE f.FlowerName = ?
    """, (flower_name,))
    diseases_info = cursor.fetchall()

    results = {}
    highest_output = -1
    selected_disease = None

    medium_severity_diseases = []

    for disease_name, description_json in diseases_info:
        try:
            description_data = json.loads(description_json)  # Assuming the description is a JSON string
            description = description_data.get('description', 'Brak opisu')
            recommendation = description_data.get('recommendation', 'Brak rekomendacji')

            print(f"Processing disease: {disease_name}, Description: {description}")

            cursor.execute("""
                SELECT DISTINCT rc.Condition, s.SymptomName, s.MembershipParameters
                FROM rule_conditions rc
                JOIN symptoms s ON rc.SymptomID = s.SymptomID
                JOIN rules r ON rc.RuleID = r.RuleID
                JOIN diseases d ON r.DiseaseID = d.DiseaseID
                WHERE d.DiseaseName = ?
            """, (disease_name,))

            conditions = []
            antecedents = {}
            for row in cursor.fetchall():
                symptom_name = row[1].strip()
                condition_name = row[0].strip()
                membership_params = json.loads(row[2])
                if symptom_name not in antecedents:
                    antecedents[symptom_name] = create_fuzzy_variable(symptom_name, membership_params)
                conditions.append({"SymptomName": symptom_name, "Condition": condition_name})

            disease_consequent = create_disease_severity_variable(disease_name)
            rules = construct_disease_rules({"conditions": conditions}, antecedents, disease_consequent)
            print(f"Rules for {disease_name}:")
            for rule in rules:
                print(f" {rule}")
            control_system = ctrl.ControlSystem(rules)
            simulation = ctrl.ControlSystemSimulation(control_system)

            for antecedent in simulation.ctrl.antecedents:
                if antecedent.label in [condition["SymptomName"] for condition in conditions]:
                    if antecedent.label in symptom_inputs:
                        simulation.input[antecedent.label] = symptom_inputs[antecedent.label]
                    else:
                        simulation.input[antecedent.label] = 0

            simulation.compute()
            output_key = disease_consequent.label

            if output_key in simulation.output:
                severity = simulation.output[output_key]
                print(f"Calculated severity for {disease_name}: {severity}")

                if severity > highest_output:
                    highest_output = severity
                    selected_disease = {
                        "disease_name": disease_name,
                        "description": description,
                        "recommendation": recommendation
                    }

                if 3 <= severity <= 7:
                    medium_severity_diseases.append({
                        "disease_name": disease_name,
                        "description": description,
                        "recommendation": recommendation,
                        "severity": severity
                    })

        except json.JSONDecodeError:
            print(f"Error decoding JSON for disease: {disease_name}")
            continue

    conn.close()

    if medium_severity_diseases:
        most_probable_medium_disease = max(medium_severity_diseases, key=lambda x: x["severity"])
        selected_disease = most_probable_medium_disease

    # If no disease is found with high or medium severity
    if not selected_disease:
        print(f"No disease detected for the given symptoms in the database for {flower_name}.")
        return render_template("noresults.html", selected_disease=selected_disease, flower_name=flower_name)

    print(f"Selected disease: {selected_disease['disease_name']} with severity: {highest_output}")
    end_time = time()
    total_time = end_time - start_time
    print(f'TOTAL TIME OF THE DIAGNOSE PROCESS: {total_time}')
    return render_template("results3.html", selected_disease=selected_disease, flower_name=flower_name)



if __name__ == "__main__":
    app.run(debug=True)