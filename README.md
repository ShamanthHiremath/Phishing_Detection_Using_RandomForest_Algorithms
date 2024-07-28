# Phishing URL Detection Using RandomForest 

## Overview
This project aims to detect phishing URLs using a RandomForest classifier. The process involves two main steps: feature extraction from URLs and prediction using a custom trained RandomForest model.

### Feature Extraction

When a URL is input into the system, it undergoes a comprehensive feature extraction process. This process analyzes various characteristics of the URL and its associated website to create a feature vector.

The URL features extracted include:
- URL having IP: Checks if the URL contains an IP address instead of a domain name.
- URL length: Length of the URL string.
- URL shortening: Checks if the URL is shortened using services like Bit.ly or TinyURL.
- Presence of "@" symbol: Indicates if the URL contains the "@" symbol.
- Double slash redirecting: Checks for double slashes in the URL path.
- Prefix/suffix domains: Examines the prefix and suffix of the URL for common phishing indicators.
- Subdomain and domain features: Extracts features related to subdomains and domain characteristics.
- SSL certificate final state: Checks if the SSL certificate of the website is valid.
- Domain registration length: Duration since the domain was registered.
- Favicon presence: Determines if the website has a favicon.
- Port number in URL: Checks for unusual port numbers in the URL.
- HTTPS token in URL: Presence of "https" in the URL.
- Presence of request URL: Checks for the existence of an external URL request in the webpage.
- URL of anchor: Checks for the presence of an anchor element in the URL.
- Links in tags: Number of links present within HTML tags.
- Suspicious form handling (SFH): Checks if forms are handled securely on the webpage.
- Presence of email submission: Indicates if email submission is required.
- Abnormal URL redirection: Detects abnormal redirection behavior in the URL.
- Mouse over and right-click features: Checks if these features are enabled on the webpage.
- Presence of pop-up windows and iframes: Detects the presence of pop-up windows and iframes.
- Age of domain: Calculates the age of the domain.
- DNS checking: Checks the domain's DNS records.
- Web traffic data: Estimates web traffic to the domain.
- Google PageRank: Google's ranking of the webpage.
- Indexing in Google: Checks if the webpage is indexed by Google.
- Links pointing to page: Number of external links pointing to the webpage.
- Statistical features: Various statistical features extracted from the URL.


Each of these features is quantified and combined into a single feature vector that represents the URL.

### Prediction Using RandomForest

Once the feature vector is created, it's passed to the pre-trained RandomForest classifier:

1. RandomForest Structure: The classifier consists of multiple decision trees, each trained on a subset of the training data and features.
2. Decision Process: Each tree in the forest independently classifies the URL based on its feature vector.
3. Aggregation: The final classification is determined by majority voting among all trees.
4. Output: The model outputs a binary classification - either "Phishing" or "Legitimate" - along with a confidence score.

RandomForest is particularly effective for this task because:
- It can handle the high-dimensional feature space of URL characteristics.
- It's robust against overfitting, a common problem in phishing detection due to the constantly evolving nature of attacks.
- It can provide feature importance rankings, helping identify which URL characteristics are most indicative of phishing attempts.

By combining thorough feature extraction with the powerful RandomForest algorithm, this project aims to provide accurate and reliable phishing URL detection, helping to enhance online security for users.

### Model Performance
We achieved an accuracy of **97.31%** in detecting phishing URLs using our RandomForest classifier. This high accuracy demonstrates the effectiveness of our approach in distinguishing between legitimate and phishing websites.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/phishing-url-detection.git
   cd phishing-url-detection
2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
## Usage

### Python Script
1. To run a Python script from your command prompt or terminal, use the following format:
    ```bash
    python main.py/python3 main.py
2. When prompted, enter the URL you want to check.

The script will output whether the URL is classified as phishing or legitimate.

### React Web Application
1. Navigate to the React app directory:
    ```bash
    cd frontend
2. Install dependencies:
    ```bash
    npm install
3. Start the application:
    ```bash
    npm start
4. Open your web browser and go to http://localhost:3000.
5. Enter a URL in the input field and click the "Check" or "Predict" button.
6. The application will display whether the URL is classified as "Phishy URL" or "Legitimate URL".
7. To stop the React application, press Ctrl + C in the terminal where it's running.

## RandomForest Classifier
RandomForest is a robust ensemble learning method that constructs multiple decision trees during training and outputs the mode of the classes (for classification) or mean prediction (for regression) of the individual trees. It excels in handling large datasets with high dimensionality and provides insights into feature importance.

## Contributors
### [Shamanth M Hiremath](https://github.com/ShamanthHiremath)
Email: shamanth.hiremath.101@gmail.com
### [Sanchit Vijay](https://github.com/sanchiitvijay)
Email: sanchiitvijay@gmail.com
### [Trijal Shinde](https://github.com/trijal18)
Email: trijal18@gmail.com

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
Thanks to [Akash Kumar](https://www.kaggle.com/akashkr) for providing the [phishing URL dataset](https://www.kaggle.com/datasets/akashkr/phishing-website-dataset).

## Future Work
1. Implement real-time URL checking API
2. Enhance feature extraction for better accuracy
3. Develop a browser extension for instant phishing detection
