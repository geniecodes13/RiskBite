import { useState } from "react";
import ImageUpload from "./components/ImageUpload";
import HealthForm from "./components/HealthForm";
import ResultCard from "./components/ResultCard";
import { scanProduct } from "./services/api";

function App() {
  const [conditions, setConditions] = useState([]);
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleConditionChange = e => {
    const value = e.target.value;
    setConditions(prev =>
      prev.includes(value)
        ? prev.filter(c => c !== value)
        : [...prev, value]
    );
    setError(null); // Clear error when user changes conditions
  };

  const handleUpload = async file => {
    if (!file) {
      setError("Please select an image first");
      return;
    }

    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const res = await scanProduct(file, conditions);
      
      if (!res.ok) {
        setError(res.error || "Failed to scan product. Please try again.");
      } else {
        setResult(res);
      }
    } catch (err) {
      setError(
        err.message ||
        "Unable to connect to the server. Make sure the backend is running."
      );
      console.error("Scan error:", err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setResult(null);
    setError(null);
  };

  return (
    <div className="app-container">
      <div className="app-header">
        <h1>🥗 RISKbite</h1>
        <p className="app-subtitle">
          Smart ingredient analysis for your health
        </p>
      </div>

      {error && <div className="error-message">{error}</div>}

      {!result ? (
        <>
          <HealthForm 
            onChange={handleConditionChange} 
            selectedConditions={conditions}
          />

          <ImageUpload 
            onUpload={handleUpload} 
            isLoading={isLoading}
          />

          {isLoading && (
            <div className="loading-message">
              <span className="loading-spinner"></span>
              Analyzing product...
            </div>
          )}
        </>
      ) : (
        <ResultCard data={result} onReset={handleReset} />
      )}
    </div>
  );
}
export default App;
