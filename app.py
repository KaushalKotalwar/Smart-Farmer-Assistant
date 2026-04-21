from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import time

app = Flask(__name__)
CORS(app)

# ---------------- DATA ----------------
DISEASE_DATA = {
    "Yellow Leaves": {
        "en": {
            "disease": "Nitrogen Deficiency",
            "cause": "Lack of nitrogen in soil",
            "chemical": "Urea (46% Nitrogen), Ammonium Nitrate",
            "herbal": "Compost, cow dung manure",
            "prevention": "Maintain soil nutrients"
        },
        "mr": {
            "disease": "नायट्रोजनची कमतरता",
            "cause": "मातीमध्ये नायट्रोजन कमी आहे",
            "chemical": "युरिया (46% N), अमोनियम नायट्रेट",
            "herbal": "कंपोस्ट, शेणखत",
            "prevention": "मातीची सुपीकता राखा"
        },
        "hi": {
            "disease": "नाइट्रोजन की कमी",
            "cause": "मिट्टी में नाइट्रोजन की कमी",
            "chemical": "यूरिया (46% N), अमोनियम नाइट्रेट",
            "herbal": "कम्पोस्ट, गोबर खाद",
            "prevention": "मिट्टी की उर्वरता बनाए रखें"
        },
        "link": "https://amzn.in/d/0aHzcbdx"
    },

    "Black Spots": {
        "en": {
            "disease": "Early Blight",
            "cause": "Fungal infection",
            "chemical": "Mancozeb, Chlorothalonil",
            "herbal": "Neem spray",
            "prevention": "Avoid moisture"
        },
        "mr": {
            "disease": "अर्ली ब्लाइट",
            "cause": "बुरशीजन्य संसर्ग",
            "chemical": "मॅन्कोझेब, क्लोरोथॅलोनील",
            "herbal": "नीम स्प्रे",
            "prevention": "जास्त ओलावा टाळा"
        },
        "hi": {
            "disease": "अर्ली ब्लाइट",
            "cause": "फंगल संक्रमण",
            "chemical": "मैनकोजेब, क्लोरोथालोनिल",
            "herbal": "नीम स्प्रे",
            "prevention": "अधिक नमी से बचें"
        },
        "link": "https://amzn.in/d/0fhUHwlr"
    },

    "Leaf Curl": {
        "en": {
            "disease": "Leaf Curl Virus",
            "cause": "Whiteflies",
            "chemical": "Imidacloprid",
            "herbal": "Neem oil spray",
            "prevention": "Control insects"
        },
        "mr": {
            "disease": "लीफ कर्ल व्हायरस",
            "cause": "पांढऱ्या माशीमुळे",
            "chemical": "इमिडाक्लोप्रिड",
            "herbal": "नीम तेल स्प्रे",
            "prevention": "किड नियंत्रण करा"
        },
        "hi": {
            "disease": "लीफ कर्ल वायरस",
            "cause": "सफेद मक्खी",
            "chemical": "इमिडाक्लोप्रिड",
            "herbal": "नीम तेल स्प्रे",
            "prevention": "कीट नियंत्रण करें"
        },
        "link": "https://www.bighaat.com/products/geolife-no-virus-organic-viricide"
    },

    "White Powder": {
        "en": {
            "disease": "Powdery Mildew",
            "cause": "High humidity",
            "chemical": "Sulfur fungicide",
            "herbal": "Milk spray",
            "prevention": "Air circulation"
        },
        "mr": {
            "disease": "पावडरी मिल्ड्यू",
            "cause": "जास्त आर्द्रता",
            "chemical": "सल्फर फंगीसाइड",
            "herbal": "दूध स्प्रे",
            "prevention": "हवेची देवाणघेवाण ठेवा"
        },
        "hi": {
            "disease": "पाउडरी मिल्ड्यू",
            "cause": "अधिक आर्द्रता",
            "chemical": "सल्फर फंगीसाइड",
            "herbal": "दूध स्प्रे",
            "prevention": "हवा का प्रवाह बनाए रखें"
        },
        "link": "https://www.bighaat.com/products/geolife-no-virus-organic-viricide"
    },

    "Brown Rot": {
        "en": {
            "disease": "Late Blight",
            "cause": "Wet conditions",
            "chemical": "Copper fungicide",
            "herbal": "Ginger spray",
            "prevention": "Avoid water stagnation"
        },
        "mr": {
            "disease": "लेट ब्लाइट",
            "cause": "ओलसर वातावरण",
            "chemical": "कॉपर फंगीसाइड",
            "herbal": "आले स्प्रे",
            "prevention": "पाणी साचू देऊ नका"
        },
        "hi": {
            "disease": "लेट ब्लाइट",
            "cause": "गीली परिस्थितियाँ",
            "chemical": "कॉपर फंगीसाइड",
            "herbal": "अदरक स्प्रे",
            "prevention": "पानी जमा न होने दें"
        },
        "link": "https://www.bighaat.com/products/geolife-no-virus-organic-viricide"
    }
}

IMAGE_DATA = {
    "Leaf Spot Disease": {
        "chemical": "Mancozeb",
        "herbal": "Neem spray",
        "prevention": "Remove infected leaves"
    },
    "Powdery Mildew": {
        "chemical": "Sulfur",
        "herbal": "Milk spray",
        "prevention": "Improve airflow"
    },
    "Healthy Plant": {
        "chemical": "No need",
        "herbal": "Compost",
        "prevention": "Regular care"
    }
}

# ---------------- API ----------------
@app.route('/api/symptom', methods=['POST'])
def symptom():
    data = request.json
    symptom = data.get("symptom")
    lang = data.get("lang", "en")

    if symptom not in DISEASE_DATA:
        return jsonify({"error": "Invalid symptom"}), 400

    d = DISEASE_DATA[symptom]

    return jsonify({
        "disease": d[lang]["disease"],
        "cause": d[lang]["cause"],
        "chemical": d[lang]["chemical"],
        "herbal": d[lang]["herbal"],
        "prevention": d[lang]["prevention"],
        "link": d["link"],
        "severity": random.choice(["Low","Medium","High"])
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({"error": "No image"}), 400

    disease = random.choice(list(IMAGE_DATA.keys()))
    d = IMAGE_DATA[disease]

    return jsonify({
        "disease": disease,
        "cause": "Detected using image analysis",
        "chemical": d["chemical"],
        "link": "https://example.com",
        "herbal": d["herbal"],
        "prevention": d["prevention"],
        "severity": random.choice(["Low","Medium","High"])
    })


if __name__ == '__main__':
    app.run(debug=True)