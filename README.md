# 📈 +EV Sports Betting Odds Finder

This project automates the discovery of profitable sports betting opportunities by comparing odds from multiple sportsbooks and identifying bets with **positive expected value (+EV)**. It is deployed on **AWS Lambda** and sends email notifications using **Amazon SES**.

---

## 🛠 Overview

The engine fetches real-time odds from a sports betting API and evaluates each betting line by comparing it to **Pinnacle's odds** which is known to have the 'sharpest' odds. When Pinnacle data is unavailable, the system uses the average of all available sportsbook odds for that event as a benchmark.

Using the **Kelly Criterion**, the engine calculates the optimal stake size and filters out bets below a **user-defined risk threshold**. This threshold represents the minimum expected value required for a bet to be considered worthwhile, allowing users to control how aggressive the system is with recommendations.

---

## ⚙️ Technical Details

- **Language:** Python
- **Infrastructure:** AWS Lambda (serverless execution), CloudWatch (scheduled trigger), Amazon SES (email delivery)
- **Odds Source:** External sports betting odds API
- **Data Handling:** Filters odds by event, market, and bookmaker; compares each to a calculated "true odds" benchmark
- **Expected Value Calculation:**  
  \[
  EV = (P_{\text{true}} \times \text{Odds}) - 1
  \]  
  where \(P_{\text{true}}\) is derived from Pinnacle or average market odds
- **Kelly Criterion Sizing:**  
  Calculates optimal stake as a proportion of bankroll based on the edge and probability
- **Thresholding:**  
  Only notifies the user if the expected value exceeds the configured risk threshold (e.g., +8%)

---

## 📬 Notifications

Qualified +EV betting opportunities are sent directly to the user via email, along with:

- Match details
- Bookmaker and odds
- Estimated edge and EV
- Suggested stake based on Kelly Criterion

---

## ☁️ Deployment

The entire system runs on **AWS Lambda**, triggered every 3 hours using **CloudWatch Events**. Deployment is handled by packaging the Python code and dependencies into a zipped Lambda-compatible archive. Email alerts are sent using **Amazon Simple Email Service (SES)**.

---

## 📄 License

This project is licensed under the MIT License.
