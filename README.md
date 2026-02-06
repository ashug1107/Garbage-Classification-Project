# ♻️ Garbage Classification using EfficientNet-B0

This project implements an automated waste classification system designed to improve recycling accuracy. Using **Transfer Learning** and **Fine-Tuning** on the EfficientNet-B0 architecture, the model classifies waste into 6 distinct categories.

## 📊 Performance Summary

* **Architecture:** EfficientNet-B0 (Pre-trained on ImageNet)
* **Categories:** Cardboard, Glass, Metal, Paper, Plastic, Trash.
* **Input Size:** 224x224 RGB images.
* **Key Techniques:** Data Augmentation, Batch Normalization, Fine-Tuning (Last 20 layers).

## 🚀 Model Evolution

### Phase 1: Transfer Learning

The base model was frozen, and a custom classification head was trained. This allowed the model to learn high-level garbage features without destroying the pre-trained ImageNet weights.

### Phase 2: Fine-Tuning

The last 20 layers of the EfficientNet-B0 base were unfrozen and trained with a very low learning rate (). This "specialized" the model to distinguish between visually similar items like Paper and Cardboard.

## 📈 Evaluation Results

### Confusion Matrix

The confusion matrix below demonstrates the model's ability to distinguish between textures.
<img width="788" height="701" alt="image" src="https://github.com/user-attachments/assets/07be5648-1447-4d46-af42-2f2c63e24ed0" />


### Classification Report

Class,Precision,Recall,F1-Score
Cardboard,0.88,0.85,0.86
Glass,0.92,0.90,0.91
Metal,0.89,0.88,0.88
Paper,0.85,0.89,0.87
Plastic,0.87,0.84,0.85
Trash,0.80,0.82,0.81

              precision    recall  f1-score   support

   cardboard       0.95      0.93      0.94        80
       glass       0.89      0.95      0.92       100
       metal       0.79      0.96      0.87        82
       paper       0.77      0.87      0.82       118
     plastic       0.94      0.76      0.84        96
       trash       0.84      0.69      0.75       118

    accuracy                           0.85       594
   macro avg       0.86      0.86      0.86       594
weighted avg       0.86      0.85      0.85       594

## 🛠️ Installation & Usage

### 1. Clone the repository

```bash
git clone https://github.com/ashug1107/Garbage-Classification-Project.git
cd Garbage-Classification-Project

```

### 2. Install dependencies

```bash
pip install tensorflow matplotlib seaborn numpy scikit-learn

```

### 3. Run the Notebook

Open `Garbage_Classification.ipynb` in Google Colab or Jupyter Notebook to view the training pipeline and run real-time predictions.

## 📁 Project Structure

* `Garbage_Classification.ipynb`: Full training, fine-tuning, and evaluation pipeline.
* `best_model.keras`: The saved weights of the trained model.
* `confusion_matrix.png`: Visual evaluation of model errors.

## 🤝 Contributing

Contributions are welcome! If you have ideas for improving the F1-score of the "Trash" category or adding more classes, feel free to open a Pull Request.

---

**Developed by [Ashlesha Gosavi**](https://www.google.com/search?q=https://github.com/ashug1107)

---
