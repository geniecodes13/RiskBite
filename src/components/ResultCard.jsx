export default function ResultCard({ data, onReset }) {
  const getRiskColor = (level) => {
    switch (level?.toLowerCase()) {
      case "high":
        return "high";
      case "medium":
        return "medium";
      case "low":
        return "low";
      default:
        return "low";
    }
  };

  const getRiskBadge = (level) => {
    switch (level?.toLowerCase()) {
      case "high":
        return "🔴";
      case "medium":
        return "🟡";
      case "low":
        return "🟢";
      default:
        return "🟢";
    }
  };

  const getRiskMessage = (level) => {
    switch (level?.toLowerCase()) {
      case "high":
        return "High Risk - We recommend avoiding this product";
      case "medium":
        return "Moderate Risk - Check ingredients carefully";
      case "low":
        return "Safe to Consume - Great choice!";
      default:
        return "Product analysis complete";
    }
  };

  const getIngredientExplanation = (ingredient, reason) => {
    const explanations = {
      "high fructose corn syrup": "This sweetener causes rapid blood sugar spikes, which is problematic for diabetes management.",
      "sugar": "Added sugar can lead to blood sugar spikes and weight gain.",
      "peanuts": "Contains peanuts which trigger allergic reactions.",
      "tree nuts": "Tree nuts can cause severe allergic reactions.",
      "shellfish": "Shellfish can trigger shellfish allergies and cross-contamination risks.",
      "milk": "Contains dairy which is unsuitable for lactose intolerance.",
      "gluten": "Contains gluten which causes issues for gluten-sensitive individuals.",
      "artificial sweeteners": "Some people prefer to avoid artificial additives.",
      "high sodium": "High salt content can increase blood pressure.",
      "saturated fat": "Excessive saturated fat impacts heart health.",
    };

    // Try to find a matching explanation
    for (const [key, value] of Object.entries(explanations)) {
      if (ingredient.toLowerCase().includes(key) || reason.toLowerCase().includes(key)) {
        return value;
      }
    }
    return reason || "This ingredient may not be suitable for your conditions.";
  };

  return (
    <div className="result-card">
      <div className={`risk-summary ${getRiskColor(data.risk_level)}`}>
        <span className="risk-badge">{getRiskBadge(data.risk_level)}</span>
        <div className="risk-text">
          <h2>{data.risk_level} Risk</h2>
          <p>{getRiskMessage(data.risk_level)}</p>
        </div>
      </div>

      {data.warnings && data.warnings.length > 0 ? (
        <div className="warnings-section">
          <h3>⚠️ Issues Found</h3>
          <p style={{ fontSize: "13px", color: "#666", marginBottom: "15px", marginTop: "-5px" }}>
            We found {data.warnings.length} ingredient{data.warnings.length !== 1 ? "s" : ""} of concern:
          </p>
          {data.warnings.map((warning, i) => (
            <div key={i} className="warning-item">
              <div className="warning-ingredient">
                ⛔ {warning.ingredient || "Unknown Ingredient"}
                <span className="warning-badge">⚠️</span>
              </div>
              <div className="warning-reason">
                {getIngredientExplanation(
                  warning.ingredient || "",
                  warning.reason || ""
                )}
              </div>
              <div className="warning-alternative">
                <strong>✅ Better choice:</strong>&nbsp;
                {warning.alternative || "Look for alternatives without this ingredient"}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="no-warnings">
          🎉 Perfect! No issues found for your selected conditions. This product is safe for you!
        </div>
      )}

      {data.summary && (
        <div style={{
          background: "#f8f9fa",
          padding: "16px",
          borderRadius: "8px",
          marginTop: "16px",
          fontSize: "14px",
          color: "#555",
          lineHeight: "1.6",
          borderLeft: "4px solid #667eea"
        }}>
          <strong>📋 Summary:</strong> {data.summary}
        </div>
      )}

      <button
        className="btn btn-primary"
        onClick={onReset}
        style={{ marginTop: "20px" }}
      >
        🔄 Scan Another Product
      </button>
    </div>
  );
}
