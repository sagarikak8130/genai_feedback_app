#### 🧠 Generative AI-Powered Customer Feedback Analyzer
This project uses a **Generative AI (LLM)** to analyze customer feedback messages in real time and infer:
* **Intent**: Whether the message is a Complaint, Suggestion, or Routine Inquiry.
* **Urgency**: How critical the issue is — High, Medium, or Low.

#### 🔍 How it Works
When a user submits feedback through the web interface:
1. The feedback is passed to an **LLM (like OpenAI GPT)** via a carefully designed prompt.
2. The LLM responds with structured JSON containing the *intent* and *urgency*.
3. Based on this:
     * **Complaints** with high urgency are escalated to customer support agents.
     * **Suggestions** are routed to the product or engineering team.
     * **Routine inquiries** are assigned to general support or self-service.

#### 🔧 Technologies Used
* Python & Flask
* OpenAI GPT (LLM) API
* MongoDB (for storing feedback history)
* Bootstrap (UI styling)