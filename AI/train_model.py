
import json
import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import (
    preprocess_input,
)

# ==========================================
# ECO-VISION AI - MODEL TRAINING
# ==========================================

# Configuration
TRAIN_DIR = "dataset/train"
VAL_DIR = "dataset/validation"
MODEL_DIR = "models"

MODEL_PATH = os.path.join(MODEL_DIR, "eco_vision_model.keras")
CLASS_PATH = os.path.join(MODEL_DIR, "class_names.json")

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
INITIAL_EPOCHS = 10
FINE_TUNE_EPOCHS = 5
SEED = 42

os.makedirs(MODEL_DIR, exist_ok=True)

# Check dataset paths
if not os.path.isdir(TRAIN_DIR):
    raise FileNotFoundError(
        f"Training dataset not found: {TRAIN_DIR}"
    )

if not os.path.isdir(VAL_DIR):
    raise FileNotFoundError(
        f"Validation dataset not found: {VAL_DIR}"
    )

# ==========================================
# LOAD DATASET
# ==========================================

train_ds = keras.utils.image_dataset_from_directory(
    TRAIN_DIR,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="int",
    shuffle=True,
    seed=SEED,
)

val_ds = keras.utils.image_dataset_from_directory(
    VAL_DIR,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="int",
    shuffle=False,
)

class_names = train_ds.class_names
num_classes = len(class_names)

if num_classes < 2:
    raise ValueError("At least two waste categories are required.")

if class_names != val_ds.class_names:
    raise ValueError(
        "Training and validation categories do not match."
    )

print("\nEco-Vision AI")
print("Waste categories:", class_names)
print("Number of classes:", num_classes)

# Save class names for prediction
with open(CLASS_PATH, "w", encoding="utf-8") as file:
    json.dump(class_names, file, indent=4)

# Improve data pipeline performance
AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.prefetch(AUTOTUNE)
val_ds = val_ds.prefetch(AUTOTUNE)

# ==========================================
# DATA AUGMENTATION
# ==========================================

data_augmentation = keras.Sequential(
    [
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.08),
        layers.RandomZoom(0.10),
        layers.RandomContrast(0.10),
    ],
    name="data_augmentation",
)

# ==========================================
# BUILD TRANSFER LEARNING MODEL
# ==========================================

base_model = MobileNetV2(
    input_shape=(*IMAGE_SIZE, 3),
    include_top=False,
    weights="imagenet",
)

# Initially freeze pretrained layers
base_model.trainable = False

inputs = keras.Input(shape=(*IMAGE_SIZE, 3))

x = data_augmentation(inputs)
x = layers.Lambda(preprocess_input, name="preprocessing")(x)

x = base_model(x, training=False)
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dropout(0.30)(x)

outputs = layers.Dense(
    num_classes,
    activation="softmax",
    name="waste_classification",
)(x)

model = keras.Model(
    inputs=inputs,
    outputs=outputs,
    name="EcoVisionAI",
)

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=1e-3),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)

model.summary()

# ==========================================
# CALLBACKS
# ==========================================

callbacks = [
    keras.callbacks.ModelCheckpoint(
        MODEL_PATH,
        monitor="val_accuracy",
        save_best_only=True,
        mode="max",
        verbose=1,
    ),
    keras.callbacks.EarlyStopping(
        monitor="val_loss",
        patience=4,
        restore_best_weights=True,
        verbose=1,
    ),
    keras.callbacks.ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.2,
        patience=2,
        min_lr=1e-7,
        verbose=1,
    ),
]

# ==========================================
# PHASE 1: TRAIN CLASSIFICATION HEAD
# ==========================================

print("\nPhase 1: Training Eco-Vision AI...")

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=INITIAL_EPOCHS,
    callbacks=callbacks,
)

# ==========================================
# PHASE 2: FINE-TUNE PRETRAINED LAYERS
# ==========================================

print("\nPhase 2: Fine-tuning MobileNetV2...")

base_model.trainable = True

# Freeze earlier layers and fine-tune later layers
fine_tune_at = max(0, len(base_model.layers) - 30)

for layer in base_model.layers[:fine_tune_at]:
    layer.trainable = False

# Keep BatchNormalization layers frozen for stability
for layer in base_model.layers:
    if isinstance(layer, layers.BatchNormalization):
        layer.trainable = False

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=1e-5),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)

model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=FINE_TUNE_EPOCHS,
    callbacks=callbacks,
)

# ==========================================
# EVALUATE MODEL
# ==========================================

print("\nEvaluating Eco-Vision AI...")

best_model = keras.models.load_model(MODEL_PATH)

loss, accuracy = best_model.evaluate(
    val_ds,
    verbose=1,
)

print(f"\nValidation Loss: {loss:.4f}")
print(f"Validation Accuracy: {accuracy * 100:.2f}%")

# Save final best model
best_model.save(MODEL_PATH)

print("\nTraining completed successfully!")
print(f"Model saved to: {MODEL_PATH}")
print(f"Class names saved to: {CLASS_PATH}")