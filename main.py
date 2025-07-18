from flask import Flask, request, render_template_string
import pandas as pd
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load plant dataset
df = pd.read_excel("sample.xlsx")

# HTML Template
template = """
<!DOCTYPE html>
<html>
<head>
    <title>Apartment Plant Recommender</title>
    <style>
        body {
       background-image: url(C:/Users/swath/Desktop/project/bg.png);
       background-size: cover;

            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #87A96B, #f1f8e9);
            color: #2e7d32;
            padding: 30px;
            margin: 0;
        }
        .container {
            background-color: #FFF6D2;
            max-width: 600px;
            margin: auto;
            padding: 25px 40px;
            border-radius: 20px;
            box-shadow: 0 8px 16px rgba(0, 100, 0, 0.2);
        }
        h2 {
            text-align: center;
            color: #1b5e20;
        }
        label {
            font-weight: bold;
            display: block;
            margin: 12px 0 6px;
        }
        input[type="text"], input[type="file"] {
            width: 100%;
            padding: 10px;
            border: 2px solid #a5d6a7;
            border-radius: 8px;
            font-size: 14px;
        }
        input[type="submit"] {
            background-color: #388e3c;
            color: white;
            font-weight: bold;
            padding: 12px 20px;
            border: none;
            border-radius: 8px;
            margin-top: 20px;
            cursor: pointer;
            width: 100%;
            transition: background 0.3s;
        }
        input[type="submit"]:hover {
            background-color: #2e7d32;
        }
        .result {
            margin-top: 30px;
            padding: 20px;
            background: #e8f5e9;
            border-left: 6px solid #66bb6a;
            border-radius: 10px;
            font-color: #2e7d32;
        }
        img {
            margin-top: 15px;
            max-width: 100%;
            border-radius: 12px;
            border: 2px solid #a5d6a7;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>🌱 Apartment-Friendly Plant Recommendation</h2>
        <form method="POST" enctype="multipart/form-data">
            <label>City:</label>

             <select name="city">
        <option value="">--Select--</option>
        <option value="Chennai">Chennai</option>
        <option value="Mumbai">Mumbai</option>
        <option value="Bengaluru">Bengaluru</option>
        <option value="Delhi">Delhi</option>
        <option value="Kolkata">Kolkata</option>
        <option value="Jaipur">Jaipur</option>
        <option value="Hyderabad">Hyderabad</option>
        <option value="Ahmedabad">Ahmedabad</option>
        <option value="Lucknow">Lucknow</option>
        <option value="Bhopal">Bhopal</option>
        <option value="Patna">Patna</option>
        <option value="Surat">Surat</option>
        <option value="Nagpur">Nagpur</option>
        <option value="Visakhapatnam">Visakhapatnam</option>
        <option value="Itanagar">Itanagar</option>
        <option value="Guwahati">Guwahati</option>
        <option value="Raipur">Raipur</option>
        <option value="Panaji">Panaji</option>
        <option value="Gurugram">Gurugram</option>
        <option value="Shimla">Shimla</option>
        <option value="Ranchi">Ranchi</option>
        <option value="Thiruvananthapuram">Thiruvananthapuram</option>
        <option value="Imphal">Imphal</option>
        <option value="Shillong">Shillong</option>
        <option value="Aizawl">Aizawl</option>
        <option value="Kohima">Kohima</option>
        <option value="Bhubaneswar">Bhubaneswar</option>
        <option value="Gangtok">Gangtok</option>
        <option value="Agartala">Agartala</option>
        <option value="Dehradun">Dehradun</option>

    </select><br><br>

            <label>State:</label>
             <select name="state">
        <option value="">--Select--</option>
        <option value="Tamil Nadu">Tamil Nadu</option>
        <option value="Maharashtra">Maharashtra</option>
        <option value="Karnataka">Karnataka</option>
        <option value="Delhi">Delhi</option>
        <option value="West Bengal">West Bengal</option>
        <option value="Telangana">Telangana</option>
        <option value="Gujarat">Gujarat</option>
        <option value="Rajasthan">Rajasthan</option>
        <option value="Uttar Pradesh">Uttar Pradesh</option>
        <option value="Madhya Pradesh">Madhya Pradesh</option>
        <option value="Bihar">Bihar</option>
        <option value="Andhra Pradesh">Andhra Pradesh</option>
        <option value="Arunachal Pradesh">Arunachal Pradesh</option>
        <option value="Assam">Assam/option>
        <option value="Chhattisgarh">Chhattisgarh</option>
        <option value="Goa">Goa</option>
        <option value="Haryana">Haryana</option>
        <option value="Himachal Pradesh">Himachal Pradesh</option>
        <option value="Jharkhand">Jharkhand</option>
        <option value="Kerala">Kerala</option>
        <option value="Manipur">Manipur</option>
        <option value="Meghalaya">Meghalaya</option>
        <option value="Mizoram">Mizoram</option>
        <option value="Nagaland">Nagaland</option>
        <option value="Odisha">Odisha</option>
        <option value="Sikkim">Sikkim</option>
        <option value="Tripura">Tripura</option>
        <option value="Uttarakhand">Uttarakhand</option>
    </select><br><br>

            <label>Upload Soil Image:</label>
            <input type="file" name="soil_image" required>

            <input type="submit" value="Get Recommendation">
        </form>

        {% if detected_soil %}
            <div class="result">
                <p><strong>Detected Soil Type:</strong> {{ detected_soil }}</p>
            </div>
        {% endif %}

        {% if recommendation %}
            <div class="result">
                <h3>🌿 Recommended Plant: {{ recommendation }}</h3>
                <p><strong>Care Tips:</strong> {{ care_tips }}</p>
                <p><strong>Light Needs:</strong> {{ light_needs }}</p>
                <p><strong>Water Needs:</strong> {{ water_needs }}</p>
                {% if image_url %}
                    <img src="{{ image_url }}" alt="{{ recommendation }}">
                {% endif %}
            </div>
        {% endif %}
    </div>
</body>
</html>

"""


# Dummy classifier based on filename
def dummy_soil_classifier(image_path):
    filename = os.path.basename(image_path).lower()
    if "clay" in filename:
        return "clay"
    elif "sandy" in filename:
        return "sandy"
    elif "loam" in filename:
        return "loamy"
    elif "black" in filename:
        return "black"
    elif "red" in filename:
        return "red"
    elif "alluvial" in filename:
        return "alluvial"
    else:
        return "loamy"  # default fallback

@app.route('/', methods=['GET', 'POST'])
def index():
    recommendation = care_tips = light_needs = water_needs = image_url = detected_soil = None

    if request.method == 'POST':
        city = request.form['city'].strip().lower()
        state = request.form['state'].strip().lower()

        # Require soil image
        if 'soil_image' in request.files:
            file = request.files['soil_image']
            if file and file.filename:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                detected_soil = dummy_soil_classifier(filepath)
                soil_type = detected_soil
            else:
                return "Please upload a valid soil image."
        else:
            return "Soil image is required."

        match = df[
            (df['city'].str.lower() == city) &
            (df['state'].str.lower() == state) &
            (df['soil_type'].str.lower() == soil_type)
        ]

        if not match.empty:
            recommendation = match.iloc[0]['recommended_plant']
            care_tips = match.iloc[0]['care_tips']
            light_needs = match.iloc[0]['light_needs']
            water_needs = match.iloc[0]['water_needs']
            image_url = match.iloc[0]['image_url']
        else:
            recommendation = "No apartment-suitable plant found for these inputs."

    return render_template_string(template,
                                  recommendation=recommendation,
                                  care_tips=care_tips,
                                  light_needs=light_needs,
                                  water_needs=water_needs,
                                  image_url=image_url,
                                  detected_soil=detected_soil)

if __name__ == '__main__':
    app.run(debug=True)