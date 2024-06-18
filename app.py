import streamlit as st
from DECIMER import predict_SMILES
import requests
from rdkit import Chem
from PIL import Image
from io import BytesIO

def get_common_name_from_inchikey(inchi_key):
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/inchikey/{inchi_key}/synonyms/JSON"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        synonyms = data.get("InformationList", {}).get("Information", [])[0].get("Synonym", [])
        return synonyms[0] if synonyms else None
    return None

def get_molecular_formula(inchi_key):
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/inchikey/{inchi_key}/property/MolecularFormula/JSON"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        formula = data.get("PropertyTable", {}).get("Properties", [])[0].get("MolecularFormula")
        return formula
    return None

st.title("SMILES Prediction from Chemical Structure Image")

uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    
    # Save the image to a temporary location
    with open("temp_image.png", "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.write("Predicting...")

    # Predict SMILES from image
    SMILES = predict_SMILES("temp_image.png")
    st.write(f'Predicted SMILES: {SMILES}')

    # Convert SMILES to InChIKey
    molecule = Chem.MolFromSmiles(SMILES)
    inchi_key = Chem.MolToInchiKey(molecule)
    st.write(f"InChIKey: {inchi_key}")

    # Get common name and molecular formula
    common_name = get_common_name_from_inchikey(inchi_key)
    formula = get_molecular_formula(inchi_key)
    st.write(f"Common Name: {common_name}")
    st.write(f"Molecular Formula: {formula}")
