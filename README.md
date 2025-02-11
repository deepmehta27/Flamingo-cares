# 🥩 Flamingo Cares - Patient Simulator  
_A Virtual Patient Simulation System for Medical Training_

## 📌 Overview  
**Flamingo Cares** is an **AI-powered virtual patient simulator** designed for medical training. It helps practitioners improve **diagnostic reasoning, patient communication, and clinical decision-making**.

### 🔹 Built With:  
- **Python** 🐍  
- **Streamlit** (Web UI)  
- **AWS Bedrock** (Claude Sonnet 3.5 for AI responses)  
- **AWS Textract** (Extracting medical data from PDFs)  
- **AWS S3** (Storing patient records & documents)  
- **Boto3** (AWS SDK for Python)  

---

## ✨ Features  
✔️ **Realistic patient conversations** using **Claude Sonnet 3.5**  
✔️ **Context-aware responses** based on patient history & medical data  
✔️ **Feedback system** to evaluate doctor-patient interactions  
✔️ **PDF data extraction** (medical history, reports) using **AWS Textract**  
✔️ **Scalable architecture** powered by **AWS Bedrock**  

---

## 🏠 Tech Stack  

### 📌 Frontend:  
- **Streamlit** (UI Framework)  
- **Custom CSS** for chat design  

### 📌 Backend:  
- **Python** (Main language)  
- **AWS Bedrock** (Claude Sonnet 3.5 for intelligent responses)  
- **Boto3** (AWS SDK for API interactions)  

### 📌 AWS Services Used:  
1. **Amazon S3** - Storing patient records and extracted medical data  
2. **AWS Textract** - Extracting text from medical PDFs  
3. **AWS Bedrock (Claude Sonnet 3.5)** - AI-powered chatbot responses  
4. **AWS Knowledge Base** - Enhancing chatbot responses with context  
5. **Boto3** - AWS SDK for integrating services  

---

## 🛠️ Installation & Setup  

### 1⃣ Clone the Repository  
```sh  
git clone https://github.com/deepmehta27/Flamingo-cares.git 
```

### 2⃣ Install Dependencies  
Ensure you have **Python 3.8+** installed. Then, install the required libraries:  
```sh  
pip install -r requirements.txt  
```

### 3⃣ Set Up AWS Credentials  
Create a `.env` file and add your **AWS credentials**:  
```
AWS_ACCESS_KEY=your_access_key  
AWS_SECRET_KEY=your_secret_key  
AWS_SESSION_TOKEN=your_session_token  
AWS_DEFAULT_REGION=your_region  
```

### 4⃣ Run the Application  
```sh  
streamlit run app.py  
```

---

## 🛢️ How It Works  

### 🩺 Interacting with the Virtual Patient  
1️⃣ **Type your message** (as a doctor) in the chat interface.  
2️⃣ **Patient responds** with context-aware symptoms or history.  
3️⃣ **Type "END"** to receive feedback on your consultation.  

### 📝 Uploading Medical Documents  
- The system extracts key information from **PDF files** using **AWS Textract**.  
- Patient history is stored in **S3** and used for enhanced AI responses.  

---

## 🤖 Preventing AI Hallucinations  
To ensure **accurate** and **relevant** AI responses, we implement:  
✅ **AWS Knowledge Base** for factual grounding  
✅ **Retrieval-Augmented Generation (RAG)** to fetch relevant data  
✅ **Fine-tuned prompts** to guide AI behavior  
✅ **Temperature control (0.3 - 0.5)** for controlled creativity  

---

## 🚀 Future Enhancements  
💡 **Voice Interaction** (Speech-to-Text + AI response)  
💡 **Multi-language support**  
💡 **Integration with EHR systems**  

---

## 🤝 Contributing  
Want to improve **Flamingo Cares**? Follow these steps:  
1. **Fork** the repo  
2. **Create a branch** (`feature-1`)  
3. **Commit your changes**  
4. **Open a PR** 🚀  

---

## 🐟 License  
This project is **open-source** under the **MIT License**.  

---

### 🚀 Made with ❤️ by Team Flamingo Cares  

