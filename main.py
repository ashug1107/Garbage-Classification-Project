import os
import io
import requests
import numpy as np
from PIL import Image
from fastapi import FastAPI, UploadFile, File, HTTPException

# This ensures we don't accidentally force the old legacy mode
os.environ["TF_USE_LEGACY_KERAS"] = "1" 

import tensorflow as tf
import tf_keras as keras

app = FastAPI(title="EcoScan AI - Integrated Backend")

import json
import zipfile


def deep_surgery_load(model_path):
    # 1. Open the .keras file (it's actually a ZIP)
    with zipfile.ZipFile(model_path, 'r') as zip_ref:
        config_str = zip_ref.read('config.json').decode('utf-8')
    
    # 2. PERFORM TEXT SURGERY ON THE CONFIG
    # Fix the InputLayer naming conflict
    config_str = config_str.replace('"batch_shape"', '"batch_input_shape"')
    
    # Fix the DTypePolicy conflict (convert object back to simple string)
    # We target the Rescaling layer's complex dtype config
    target_dtype_block = '"dtype": {"module": "keras", "class_name": "DTypePolicy", "config": {"name": "float32"}, "registered_name": null}'
    config_str = config_str.replace(target_dtype_block, '"dtype": "float32"')

    # 3. Rebuild the model structure
    config_dict = json.loads(config_str)
    model = keras.models.model_from_json(json.dumps(config_dict))
    
    # 4. Pour the weights in
    model.load_weights(model_path)
    return model

# --- EXECUTE LOADING ---
try:
    MODEL_PATH = "garbage_classifier_efficientnetb0_model.keras"
    model = deep_surgery_load(MODEL_PATH)
    print("✅ System: Model Surgery Successful. Weights loaded.")
except Exception as e:
    print(f"❌ Surgery Failed: {e}")

# --- 1. CONFIGURATION ---

#MODEL_PATH = "garbage_classifier_efficientnetb0_model.keras"
CLASS_NAMES = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']

# Directory to store user-uploaded images
UPLOAD_DIR = "user_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# GitHub Credentials (CHECK REPO NAME FOR HYPHENS)
GITHUB_TOKEN = "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" 
REPO_OWNER = "ashug1107"
REPO_NAME = "Garbage-Classification-Project" 

# --- 2. MODEL LOADING ---
try:
    from tf_keras.models import load_model
    model = keras.models.load_model(MODEL_PATH, compile=False, safe_mode=False)
    #model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    print("✅ System: AI Model loaded successfully.")
except Exception as e:
    print(f"❌ System: Failed to load model. Error: {e}")

# --- 3. HELPER FUNCTIONS ---
def preprocess_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    img = img.resize((224, 224))
    img_array = tf.keras.utils.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) 
    return img_array

# --- 4. API ENDPOINTS ---

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        content = await file.read()
        
        # SAVE THE IMAGE
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(content)
        
        processed_img = preprocess_image(content)
        predictions = model.predict(processed_img)
        pred_idx = np.argmax(predictions[0])
        confidence = float(np.max(predictions[0]))
        
        return {
            "prediction": CLASS_NAMES[pred_idx],
            "confidence": confidence,
            "saved_at": file_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/report-error")
async def report_error(predicted: str, actual: str):
    github_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    issue_payload = {
        "title": f"Mismatched Classification: {predicted} vs {actual}",
        "body": f"### Report\n- Predicted: `{predicted}`\n- Actual: `{actual}`",
        "labels": ["bug"]
    }
    response = requests.post(github_url, json=issue_payload, headers=headers)
    if response.status_code == 201:
        return {"status": "success"}
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
