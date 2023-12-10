from flask import Flask, render_template, request
import email

app = Flask(__name__)

def analyze_email_header(msg):
    # Extract common header fields
    header_info = {
        "From": msg["From"],
        "To": msg["To"],
        "Subject": msg["Subject"],
        "Date": msg["Date"]
    }
    # Extract detailed header fields
    detailed_header = {}
    for key in msg.keys():
        if key not in ["From", "To", "Subject", "Date"]:
            detailed_header[key] = msg[key]
    return header_info, detailed_header

# Function to reconstruct the forwarding chain
def reconstruct_forwarding_chain(msg):
    # Initialize a list to store forwarding chain entries
    forwarding_chain = []
    # Extract the received headers
    received_headers = msg.get_all("Received")
    if received_headers:
        for received_header in received_headers:
            forwarding_chain.append(received_header)
    return forwarding_chain


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"

        file = request.files["file"]

        if file.filename == "":
            return "No selected file"

        if file:
            msg = email.message_from_binary_file(file)
            header_info, detailed_header = analyze_email_header(msg)
            forwarding_chain = reconstruct_forwarding_chain(msg)
            return render_template("result.html", header_info=header_info, detailed_header=detailed_header, forwarding_chain=forwarding_chain)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
