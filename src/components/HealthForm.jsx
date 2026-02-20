export default function HealthForm({ onChange, selectedConditions }) {
  const conditions = [
    { value: "diabetes", label: "Diabetes" },
    { value: "peanut_allergy", label: "Peanut Allergy" },
    { value: "gluten_sensitivity", label: "Gluten Sensitivity" },
    { value: "lactose_intolerance", label: "Lactose Intolerance" },
    { value: "nut_allergy", label: "Nut Allergy" },
    { value: "shellfish_allergy", label: "Shellfish Allergy" },
    { value: "vegan", label: "Vegan" },
    { value: "pescatarian", label: "Pescatarian" },
  ];

  return (
    <div className="health-form">
      <h3>Health Conditions & Preferences</h3>
      <div className="form-group">
        {conditions.map((condition) => (
          <div key={condition.value} className="checkbox-item">
            <input
              type="checkbox"
              id={condition.value}
              value={condition.value}
              checked={selectedConditions?.includes(condition.value) || false}
              onChange={onChange}
            />
            <label htmlFor={condition.value}>{condition.label}</label>
          </div>
        ))}
      </div>
    </div>
  );
}
