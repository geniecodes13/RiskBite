"""
Comprehensive ingredient knowledge base
Maps ingredients to risk levels, health tags, and alternatives
"""

# Risk levels: low, medium, high
INGREDIENTS_DB = {
    # ==================== SUGARS & SWEETENERS ====================
    "sugar": {
        "risk_level": "high",
        "health_tags": ["diabetes", "weight_gain", "cavities", "pcos", "insulin_resistance", "high_calorie"],
        "description": "Added sugar causes rapid blood glucose spikes",
        "safe_alternative": "Stevia, Erythritol, Monk Fruit",
        "why": "High glycemic index increases diabetes risk and problematic for PCOS"
    },
    "high fructose corn syrup": {
        "risk_level": "high",
        "health_tags": ["diabetes", "fatty_liver", "weight_gain", "pcos", "obesity", "insulin_resistance"],
        "description": "Metabolized differently than regular sugar, linked to fatty liver disease",
        "safe_alternative": "Stevia or natural honey",
        "why": "Associated with metabolic syndrome, type 2 diabetes, and PCOS"
    },
    "glucose": {
        "risk_level": "medium",
        "health_tags": ["diabetes"],
        "description": "Simple sugar that raises blood glucose",
        "safe_alternative": "Complex carbohydrates",
        "why": "Rapid absorption affects blood sugar levels"
    },
    "fructose": {
        "risk_level": "medium",
        "health_tags": ["diabetes", "weight_gain"],
        "description": "Fruit sugar that may contribute to weight gain",
        "safe_alternative": "Whole fruits instead of extracted fructose",
        "why": "Doesn't trigger satiation hormones like other sugars"
    },
    "maltose": {
        "risk_level": "medium",
        "health_tags": ["diabetes"],
        "description": "Malt sugar with high glycemic index",
        "safe_alternative": "Complex carbs",
        "why": "Rapidly absorbed, impacts blood sugar"
    },
    "dextrose": {
        "risk_level": "medium",
        "health_tags": ["diabetes"],
        "description": "Another name for glucose",
        "safe_alternative": "Stevia or Erythritol",
        "why": "Fast-acting sugar that spikes glucose"
    },
    "sucrose": {
        "risk_level": "high",
        "health_tags": ["diabetes", "cavities"],
        "description": "Common table sugar",
        "safe_alternative": "Monk Fruit Sweetener",
        "why": "High glycemic index food"
    },
    "sorbitol": {
        "risk_level": "low",
        "health_tags": ["digestive"],
        "description": "Sugar alcohol that may cause digestive issues in large amounts",
        "safe_alternative": "Erythritol",
        "why": "Can cause bloating and laxative effects"
    },
    "xylitol": {
        "risk_level": "low",
        "health_tags": ["teeth_friendly"],
        "description": "Sugar alcohol beneficial for teeth",
        "safe_alternative": "Safe for most people",
        "why": "Lower calorie, doesn't spike blood sugar"
    },
    "aspartame": {
        "risk_level": "low",
        "health_tags": ["diet_friendly"],
        "description": "Artificial sweetener",
        "safe_alternative": "Stevia",
        "why": "Zero calories, no blood sugar impact"
    },
    "saccharin": {
        "risk_level": "low",
        "health_tags": ["diet_friendly"],
        "description": "Artificial sweetener",
        "safe_alternative": "Stevia or Erythritol",
        "why": "Zero calories, no sugar impact"
    },

    # ==================== FATS & OILS ====================
    "palm oil": {
        "risk_level": "high",
        "health_tags": ["heart_disease", "hypertension", "saturated_fat", "environmental"],
        "description": "High in saturated fat, linked to heart disease and hypertension",
        "safe_alternative": "Olive oil, Coconut oil, Sunflower oil",
        "why": "Increases LDL cholesterol and blood pressure"
    },
    "palm kernel oil": {
        "risk_level": "high",
        "health_tags": ["saturated_fat"],
        "description": "Even higher in saturated fat than palm oil",
        "safe_alternative": "Unsaturated oils",
        "why": "Most saturated fat content"
    },
    "hydrogenated oil": {
        "risk_level": "high",
        "health_tags": ["trans_fat", "heart_disease", "hypertension", "inflammation"],
        "description": "Contains trans fats linked to heart disease and hypertension",
        "safe_alternative": "Non-hydrogenated oils",
        "why": "Trans fats raise LDL, lower HDL, increase inflammation"
    },
    "partially hydrogenated oil": {
        "risk_level": "high",
        "health_tags": ["trans_fat", "inflammation"],
        "description": "Source of dangerous trans fats",
        "safe_alternative": "Natural oils",
        "why": "Creates trans fats that promote inflammation"
    },
    "shortening": {
        "risk_level": "high",
        "health_tags": ["saturated_fat"],
        "description": "Usually highly saturated and processed",
        "safe_alternative": "Butter or coconut oil",
        "why": "Often contains trans fats"
    },

    # ==================== SODIUM ====================
    "sodium": {
        "risk_level": "medium",
        "health_tags": ["hypertension", "heart_disease", "high_blood_pressure"],
        "description": "Excess sodium increases blood pressure",
        "safe_alternative": "Reduce sodium intake",
        "why": "Contributes to hypertension"
    },
    "sodium chloride": {
        "risk_level": "medium",
        "health_tags": ["hypertension", "high_blood_pressure", "heart_disease"],
        "description": "Table salt - in excess increases blood pressure",
        "safe_alternative": "Use sparingly, try sea salt",
        "why": "Excess salt leads to hypertension and heart disease"
    },
    "sodium benzoate": {
        "risk_level": "medium",
        "health_tags": ["preservative", "hyperactivity"],
        "description": "Preservative that may trigger hyperactivity in children",
        "safe_alternative": "Naturally preserved foods",
        "why": "Linked to behavioral issues in some children"
    },
    "sodium nitrate": {
        "risk_level": "high",
        "health_tags": ["carcinogenic", "preservative"],
        "description": "Preservative linked to increased cancer risk",
        "safe_alternative": "Fresh meats without nitrates",
        "why": "Forms carcinogenic compounds in stomach"
    },
    "sodium nitrite": {
        "risk_level": "high",
        "health_tags": ["carcinogenic"],
        "description": "Similar to sodium nitrate with cancer concerns",
        "safe_alternative": "Nitrate-free cured meats",
        "why": "Potential carcinogen"
    },
    "monosodium glutamate": {
        "risk_level": "medium",
        "health_tags": ["flavor_enhancer", "hyperactivity"],
        "description": "Flavor enhancer (MSG) may cause headaches or hyperactivity",
        "safe_alternative": "Natural seasonings and spices",
        "why": "Can trigger migraines and restlessness"
    },

    # ==================== ALLERGENS ====================
    "peanuts": {
        "risk_level": "high",
        "health_tags": ["peanut_allergy", "allergen"],
        "description": "Common allergen - can cause severe reactions",
        "safe_alternative": "Tree nuts or seed butters",
        "why": "Major food allergen"
    },
    "peanut": {
        "risk_level": "high",
        "health_tags": ["peanut_allergy", "allergen"],
        "description": "Peanut allergy trigger",
        "safe_alternative": "Sunflower seed butter",
        "why": "Can cause anaphylaxis"
    },
    "tree nuts": {
        "risk_level": "high",
        "health_tags": ["nut_allergy", "allergen"],
        "description": "Includes almonds, cashews, walnuts - common allergen",
        "safe_alternative": "Sunflower seeds or pumpkin seeds",
        "why": "Major allergen group"
    },
    "almonds": {
        "risk_level": "high",
        "health_tags": ["nut_allergy", "allergen"],
        "description": "Tree nut - allergenic",
        "safe_alternative": "Sunflower seeds",
        "why": "Common tree nut allergen"
    },
    "cashews": {
        "risk_level": "high",
        "health_tags": ["nut_allergy", "allergen"],
        "description": "Tree nut - allergenic",
        "safe_alternative": "Seeds",
        "why": "TreeNut allergen"
    },
    "walnuts": {
        "risk_level": "high",
        "health_tags": ["nut_allergy", "allergen"],
        "description": "Tree nut - allergenic",
        "safe_alternative": "Seeds",
        "why": "Tree nut allergen"
    },
    "shellfish": {
        "risk_level": "high",
        "health_tags": ["shellfish_allergy", "allergen"],
        "description": "Shellfish - can cause severe allergic reactions",
        "safe_alternative": "Fish or other proteins",
        "why": "Major allergen - can cause anaphylaxis"
    },
    "shrimp": {
        "risk_level": "high",
        "health_tags": ["shellfish_allergy", "allergen"],
        "description": "Crustacean - shellfish allergen",
        "safe_alternative": "Fish",
        "why": "Shellfish allergen"
    },
    "crab": {
        "risk_level": "high",
        "health_tags": ["shellfish_allergy", "allergen"],
        "description": "Crustacean - shellfish allergen",
        "safe_alternative": "Fish",
        "why": "Shellfish allergen"
    },
    "milk": {
        "risk_level": "high",
        "health_tags": ["lactose_intolerance", "milk_allergy", "allergen"],
        "description": "Contains lactose - unsuitable for lactose intolerant",
        "safe_alternative": "Almond milk, oat milk, coconut milk",
        "why": "Lactose causes digestion issues"
    },
    "lactose": {
        "risk_level": "high",
        "health_tags": ["lactose_intolerance", "digestive"],
        "description": "Milk sugar - causes bloating and digestive issues",
        "safe_alternative": "Lactose-free milk or non-dairy alternatives",
        "why": "Many people lack lactase enzyme"
    },
    "whey": {
        "risk_level": "medium",
        "health_tags": ["milk_allergy", "lactose_intolerance"],
        "description": "Milk protein - may cause issues for sensitive individuals",
        "safe_alternative": "Plant-based proteins",
        "why": "Contains lactose and milk proteins"
    },
    "casein": {
        "risk_level": "medium",
        "health_tags": ["milk_allergy"],
        "description": "Milk protein - allergenic",
        "safe_alternative": "Plant proteins",
        "why": "Can trigger milk allergy"
    },
    "eggs": {
        "risk_level": "high",
        "health_tags": ["egg_allergy", "allergen"],
        "description": "Common allergen",
        "safe_alternative": "Egg substitutes like flax or chia",
        "why": "Major allergen"
    },
    "sesame": {
        "risk_level": "high",
        "health_tags": ["sesame_allergy", "allergen"],
        "description": "Increasingly recognized allergen",
        "safe_alternative": "Sunflower seeds",
        "why": "Emerging major allergen"
    },
    "gluten": {
        "risk_level": "high",
        "health_tags": ["gluten_sensitivity", "celiac", "allergen"],
        "description": "Gluten - unsuitable for celiac and gluten-sensitive individuals",
        "safe_alternative": "Gluten-free alternatives",
        "why": "Causes intestinal damage in celiac disease"
    },
    "wheat": {
        "risk_level": "high",
        "health_tags": ["gluten_sensitivity", "wheat_allergy"],
        "description": "Contains gluten - problematic for sensitive individuals",
        "safe_alternative": "Rice, corn, or other gluten-free grains",
        "why": "Contains gluten and wheat allergens"
    },
    "barley": {
        "risk_level": "high",
        "health_tags": ["gluten_sensitivity"],
        "description": "Grain containing gluten",
        "safe_alternative": "Gluten-free grains",
        "why": "Contains gluten"
    },
    "rye": {
        "risk_level": "high",
        "health_tags": ["gluten_sensitivity"],
        "description": "Grain containing gluten",
        "safe_alternative": "Gluten-free alternatives",
        "why": "Contains gluten"
    },

    # ==================== ADDITIVES & PRESERVATIVES ====================
    "artificial colors": {
        "risk_level": "medium",
        "health_tags": ["hyperactivity", "additive"],
        "description": "Artificial dyes linked to hyperactivity in children",
        "safe_alternative": "Natural color from vegetables and fruits",
        "why": "Can trigger hyperactivity and behavioral issues"
    },
    "food coloring": {
        "risk_level": "medium",
        "health_tags": ["additive", "hyperactivity"],
        "description": "Artificial colorants",
        "safe_alternative": "Natural food coloring",
        "why": "Linked to behavior problems"
    },
    "red 40": {
        "risk_level": "medium",
        "health_tags": ["artificial_color", "hyperactivity"],
        "description": "Artificial red dye",
        "safe_alternative": "Beet juice or carmine",
        "why": "Banned in some countries due to hyperactivity concerns"
    },
    "yellow 5": {
        "risk_level": "medium",
        "health_tags": ["artificial_color", "allergies"],
        "description": "Artificial yellow dye",
        "safe_alternative": "Turmeric or annatto",
        "why": "Can trigger allergies"
    },
    "yellow 6": {
        "risk_level": "medium",
        "health_tags": ["artificial_color"],
        "description": "Artificial yellow dye",
        "safe_alternative": "Natural colorants",
        "why": "Artificial dye"
    },
    "blue 1": {
        "risk_level": "low",
        "health_tags": ["artificial_color"],
        "description": "Artificial blue dye",
        "safe_alternative": "Spirulina or blue butterfly pea",
        "why": "Generally considered safe by FDA"
    },
    "bha": {
        "risk_level": "high",
        "health_tags": ["preservative", "carcinogenic"],
        "description": "Butylated hydroxyanisole - potential carcinogen",
        "safe_alternative": "Vitamin E or citric acid",
        "why": "Animal studies showed cancer risk"
    },
    "bht": {
        "risk_level": "high",
        "health_tags": ["preservative", "carcinogenic"],
        "description": "Butylated hydroxytoluene - potential carcinogen",
        "safe_alternative": "Natural preservatives",
        "why": "Possible carcinogen"
    },
    "tbhq": {
        "risk_level": "high",
        "health_tags": ["preservative", "carcinogenic"],
        "description": "Tert-butylhydroquinone - linked to health issues",
        "safe_alternative": "Vitamin E or rosemary extract",
        "why": "May cause immune system issues"
    },
    "propylene glycol": {
        "risk_level": "medium",
        "health_tags": ["additive", "preservative"],
        "description": "Used in cosmetics and food - may cause allergies",
        "safe_alternative": "Natural preservatives",
        "why": "Can trigger allergic reactions"
    },
    "potassium sorbate": {
        "risk_level": "low",
        "health_tags": ["preservative"],
        "description": "Preservative generally considered safe",
        "safe_alternative": "Natural preservation methods",
        "why": "Safe in small amounts"
    },

    # ==================== ANIMAL PRODUCTS (for vegans/vegetarians) ====================
    "gelatin": {
        "risk_level": "high",
        "health_tags": ["vegan", "vegetarian", "animal_product"],
        "description": "Animal-derived protein from collagen",
        "safe_alternative": "Agar or pectin",
        "why": "Not suitable for vegan/vegetarian diets"
    },
    "carmine": {
        "risk_level": "high",
        "health_tags": ["vegan", "animal_product"],
        "description": "Red dye from crushed insects",
        "safe_alternative": "Beetroot juice",
        "why": "Not vegan - from insects"
    },
    "beeswax": {
        "risk_level": "high",
        "health_tags": ["vegan", "animal_product"],
        "description": "Coating from bees",
        "safe_alternative": "Vegetable wax",
        "why": "Not vegan"
    },
    "honey": {
        "risk_level": "medium",
        "health_tags": ["vegan", "high_sugar"],
        "description": "Bee product - not suitable for vegans",
        "safe_alternative": "Maple syrup or agave",
        "why": "Not vegan; high sugar content"
    },
    "beef": {
        "risk_level": "high",
        "health_tags": ["vegetarian", "vegan", "animal_product"],
        "description": "Beef - not suitable for vegetarians/vegans",
        "safe_alternative": "Plant-based proteins",
        "why": "Animal product"
    },
    "chicken": {
        "risk_level": "high",
        "health_tags": ["vegetarian", "vegan", "animal_product"],
        "description": "Chicken - not suitable for vegetarians/vegans",
        "safe_alternative": "Legumes or tofu",
        "why": "Animal product"
    },
    "pork": {
        "risk_level": "high",
        "health_tags": ["vegetarian", "vegan", "animal_product"],
        "description": "Pork - not suitable for vegetarians/vegans",
        "safe_alternative": "Plant proteins",
        "why": "Animal product"
    },
    "fish": {
        "risk_level": "high",
        "health_tags": ["vegan", "animal_product"],
        "description": "Fish - not suitable for vegans (pescatarians ok)",
        "safe_alternative": "Algae or plant-based",
        "why": "Not vegan"
    },

    # ==================== TRANS FATS ====================
    "trans fat": {
        "risk_level": "high",
        "health_tags": ["trans_fat", "heart_disease"],
        "description": "Trans fats increase heart disease and stroke risk",
        "safe_alternative": "Replace with unsaturated fats",
        "why": "Raises LDL, lowers HDL cholesterol"
    },

    # ==================== MISC ADDITIVES ====================
    "monodiglyceride": {
        "risk_level": "low",
        "health_tags": ["emulsifier"],
        "description": "Emulsifier - generally safe",
        "safe_alternative": "Natural emulsifiers",
        "why": "Safe in food amounts"
    },
    "potassium phosphate": {
        "risk_level": "low",
        "health_tags": ["additive"],
        "description": "Additive and preservative",
        "safe_alternative": "Natural alternatives",
        "why": "GRAS ingredient"
    },
    "lecithin": {
        "risk_level": "low",
        "health_tags": ["emulsifier"],
        "description": "Natural emulsifier from eggs or soy",
        "safe_alternative": "Other emulsifiers",
        "why": "Generally safe but note soy/egg content"
    },
    "guar gum": {
        "risk_level": "low",
        "health_tags": ["thickener"],
        "description": "Natural thickener from guar beans",
        "safe_alternative": "Other thickeners",
        "why": "Safe and natural"
    },
    "xanthan gum": {
        "risk_level": "low",
        "health_tags": ["thickener"],
        "description": "Thickener - safe for most people",
        "safe_alternative": "Other thickeners",
        "why": "Safe and widely used"
    },
    "citric acid": {
        "risk_level": "low",
        "health_tags": ["preservative", "natural"],
        "description": "Natural preservative from citrus",
        "safe_alternative": "Safe natural choice",
        "why": "Natural and safe"
    },

    # ==================== COMMON DAILY LIFE INGREDIENTS ====================
    "soy": {
        "risk_level": "medium",
        "health_tags": ["allergen", "soy_allergy"],
        "description": "Soy is a common allergen - can trigger allergic reactions",
        "safe_alternative": "Legumes like lentils or peas",
        "why": "Soy allergy is increasingly common"
    },
    "soybeans": {
        "risk_level": "medium",
        "health_tags": ["allergen", "soy_allergy"],
        "description": "Soybean - common allergen",
        "safe_alternative": "Other legumes",
        "why": "Contains soy proteins that trigger allergies"
    },
    "tofu": {
        "risk_level": "low",
        "health_tags": ["soy_product", "vegetarian"],
        "description": "Soy curd - good plant protein, safe for most people but contains soy allergen",
        "safe_alternative": "Tempeh or legume-based proteins",
        "why": "Nutritious but contains soy"
    },
    "soy sauce": {
        "risk_level": "medium",
        "health_tags": ["soy_product", "high_sodium"],
        "description": "Soy sauce is high in sodium and contains soy allergen",
        "safe_alternative": "Coconut aminos or low-sodium alternatives",
        "why": "High salt content and soy allergen"
    },
    "rice": {
        "risk_level": "low",
        "health_tags": ["gluten_free", "grain"],
        "description": "Rice is a safe, gluten-free grain suitable for most diets",
        "safe_alternative": "Safe choice for sensitive individuals",
        "why": "Hypoallergenic and easily digestible"
    },
    "white rice": {
        "risk_level": "low",
        "health_tags": ["gluten_free", "grain"],
        "description": "White rice - safe gluten-free grain with low fiber",
        "safe_alternative": "Brown rice for more nutrients",
        "why": "Easy to digest"
    },
    "brown rice": {
        "risk_level": "low",
        "health_tags": ["gluten_free", "grain", "fiber"],
        "description": "Whole grain rice - nutritious and gluten-free",
        "safe_alternative": "Safe whole grain choice",
        "why": "Rich in fiber and minerals"
    },
    "oats": {
        "risk_level": "low",
        "health_tags": ["gluten_free", "grain", "fiber"],
        "description": "Oats are naturally gluten-free and high in fiber",
        "safe_alternative": "Safe for most people but may contain traces of gluten",
        "why": "Healthful whole grain"
    },
    "corn": {
        "risk_level": "low",
        "health_tags": ["gluten_free", "grain"],
        "description": "Corn - gluten-free grain, generally safe",
        "safe_alternative": "Safe alternative for gluten-sensitive individuals",
        "why": "Naturally gluten-free"
    },
    "cornstarch": {
        "risk_level": "low",
        "health_tags": ["thickener", "gluten_free"],
        "description": "Starch from corn used for thickening",
        "safe_alternative": "Tapioca starch or potato starch",
        "why": "Pure starch with no gluten"
    },
    "potato": {
        "risk_level": "low",
        "health_tags": ["gluten_free", "vegetable"],
        "description": "Potatoes are gluten-free and nutritious",
        "safe_alternative": "Safe natural choice",
        "why": "Safe for most diets"
    },
    "vegetable oil": {
        "risk_level": "medium",
        "health_tags": ["oil", "refined"],
        "description": "Generic vegetable oil - often refined and may contain unhealthy fats",
        "safe_alternative": "Olive oil or coconut oil",
        "why": "Highly processed, higher omega-6 ratio"
    },
    "olive oil": {
        "risk_level": "low",
        "health_tags": ["oil", "heart_healthy"],
        "description": "Olive oil - heart-healthy oil rich in antioxidants",
        "safe_alternative": "Safe and healthy choice",
        "why": "High in monounsaturated fats"
    },
    "coconut oil": {
        "risk_level": "low",
        "health_tags": ["oil", "saturated_fat"],
        "description": "Coconut oil - natural oil with medium chain triglycerides",
        "safe_alternative": "Good alternative to vegetable oil",
        "why": "Natural and less processed"
    },
    "sunflower oil": {
        "risk_level": "low",
        "health_tags": ["oil", "seed_oil"],
        "description": "Sunflower oil - light oil good for cooking",
        "safe_alternative": "Safe alternative oil",
        "why": "Contains vitamin E and linoleic acid"
    },
    "butter": {
        "risk_level": "medium",
        "health_tags": ["dairy", "saturated_fat"],
        "description": "Butter - dairy product high in saturated fat",
        "safe_alternative": "Olive oil or vegan butter",
        "why": "Contains lactose and saturated fat"
    },
    "coffee": {
        "risk_level": "low",
        "health_tags": ["caffeine", "beverage"],
        "description": "Coffee contains caffeine - generally safe, may cause jitters or sleep issues",
        "safe_alternative": "Decaf coffee or herbal tea",
        "why": "Caffeine can affect sleep patterns"
    },
    "caffeine": {
        "risk_level": "low",
        "health_tags": ["stimulant"],
        "description": "Caffeine is a stimulant - safe in moderation",
        "safe_alternative": "Reduce intake if sensitive",
        "why": "Can cause anxiety or insomnia"
    },
    "tea": {
        "risk_level": "low",
        "health_tags": ["caffeine", "antioxidants"],
        "description": "Tea contains moderate caffeine and beneficial antioxidants",
        "safe_alternative": "Green tea for lighter caffeine",
        "why": "Healthy beverage with antioxidants"
    },
    "chocolate": {
        "risk_level": "medium",
        "health_tags": ["sugar", "caffeine", "high_fat"],
        "description": "Chocolate contains sugar, caffeine, and fat - enjoy in moderation",
        "safe_alternative": "Dark chocolate or cocoa powder",
        "why": "High in sugar and calories"
    },
    "cocoa": {
        "risk_level": "low",
        "health_tags": ["antioxidants", "chocolate"],
        "description": "Cocoa powder - antioxidant-rich, natural chocolate flavor",
        "safe_alternative": "Safe natural choice",
        "why": "Rich in polyphenols and antioxidants"
    },
    "salt": {
        "risk_level": "medium",
        "health_tags": ["high_sodium", "seasoning"],
        "description": "Salt in excess increases blood pressure",
        "safe_alternative": "Reduce salt intake, use herbs for flavoring",
        "why": "Excess sodium contributes to hypertension"
    },
    "sea salt": {
        "risk_level": "medium",
        "health_tags": ["high_sodium", "seasoning"],
        "description": "Sea salt - still contains sodium, use sparingly",
        "safe_alternative": "Herbs and spices for flavoring",
        "why": "High sodium content"
    },
    "cumin": {
        "risk_level": "low",
        "health_tags": ["spice", "seasoning"],
        "description": "Cumin is a safe spice with potential health benefits",
        "safe_alternative": "Safe natural choice",
        "why": "Natural and antioxidant-rich"
    },
    "turmeric": {
        "risk_level": "low",
        "health_tags": ["spice", "anti_inflammatory"],
        "description": "Turmeric - anti-inflammatory spice with curcumin",
        "safe_alternative": "Safe natural choice",
        "why": "Known for anti-inflammatory properties"
    },
    "black pepper": {
        "risk_level": "low",
        "health_tags": ["spice", "seasoning"],
        "description": "Black pepper is a safe spice with no known allergens",
        "safe_alternative": "Safe natural choice",
        "why": "Safe seasoning"
    },
    "garlic": {
        "risk_level": "low",
        "health_tags": ["vegetable", "seasoning"],
        "description": "Garlic is safe and has antimicrobial properties",
        "safe_alternative": "Safe natural choice",
        "why": "Beneficial for immune system"
    },
    "onion": {
        "risk_level": "low",
        "health_tags": ["vegetable", "seasoning"],
        "description": "Onions are safe and contain beneficial compounds",
        "safe_alternative": "Safe natural choice",
        "why": "Good source of antioxidants"
    },
    "tomato": {
        "risk_level": "low",
        "health_tags": ["vegetable", "antioxidant"],
        "description": "Tomatoes are safe and rich in lycopene antioxidant",
        "safe_alternative": "Safe natural choice",
        "why": "Rich in beneficial nutrients"
    },
    "carrot": {
        "risk_level": "low",
        "health_tags": ["vegetable", "beta_carotene"],
        "description": "Carrots are safe and rich in beta-carotene and vitamins",
        "safe_alternative": "Safe natural choice",
        "why": "Nutritious and healthy"
    },
    "broccoli": {
        "risk_level": "low",
        "health_tags": ["vegetable", "cruciferous"],
        "description": "Broccoli is a nutritious cruciferous vegetable",
        "safe_alternative": "Safe natural choice",
        "why": "Rich in vitamins and fiber"
    },
    "spinach": {
        "risk_level": "low",
        "health_tags": ["vegetable", "iron"],
        "description": "Spinach is nutrient-dense leafy green safe for most",
        "safe_alternative": "Safe natural choice",
        "why": "High in iron and antioxidants"
    },
    "apple": {
        "risk_level": "low",
        "health_tags": ["fruit", "fiber"],
        "description": "Apples are safe, nutritious fruits with dietary fiber",
        "safe_alternative": "Safe natural choice",
        "why": "Good source of fiber and vitamin C"
    },
    "banana": {
        "risk_level": "low",
        "health_tags": ["fruit", "potassium"],
        "description": "Bananas are safe and rich in potassium",
        "safe_alternative": "Safe natural choice",
        "why": "Good source of potassium and B vitamins"
    },
    "orange": {
        "risk_level": "low",
        "health_tags": ["fruit", "vitamin_c"],
        "description": "Oranges are safe citrus fruits rich in vitamin C",
        "safe_alternative": "Safe natural choice",
        "why": "Excellent source of vitamin C"
    },
    "lemon": {
        "risk_level": "low",
        "health_tags": ["fruit", "vitamin_c"],
        "description": "Lemons are safe citrus for flavoring and vitamin C",
        "safe_alternative": "Safe natural choice",
        "why": "Good source of vitamin C and antioxidants"
    },
    "almond milk": {
        "risk_level": "low",
        "health_tags": ["milk_alternative", "dairy_free"],
        "description": "Almond milk is a dairy-free alternative suitable for lactose-intolerant",
        "safe_alternative": "Safe for most people, except nut allergies",
        "why": "No lactose or dairy"
    },
    "oat milk": {
        "risk_level": "low",
        "health_tags": ["milk_alternative", "dairy_free", "gluten_free"],
        "description": "Oat milk is dairy-free and gluten-free alternative",
        "safe_alternative": "Safe natural choice",
        "why": "Good for dairy and gluten-free diets"
    },
    "coconut milk": {
        "risk_level": "low",
        "health_tags": ["milk_alternative", "dairy_free"],
        "description": "Coconut milk is creamy dairy-free alternative",
        "safe_alternative": "Safe natural choice",
        "why": "No lactose or dairy"
    },
    "yeast": {
        "risk_level": "low",
        "health_tags": ["additive", "leavening"],
        "description": "Yeast is used for leavening in baking - safe for most people",
        "safe_alternative": "Baking powder or baking soda",
        "why": "Safe natural ingredient"
    },
    "baking powder": {
        "risk_level": "low",
        "health_tags": ["leavening", "additive"],
        "description": "Baking powder is a leavening agent - safe for baking",
        "safe_alternative": "Safe natural choice",
        "why": "Standard baking ingredient"
    },
    "baking soda": {
        "risk_level": "low",
        "health_tags": ["leavening", "additive"],
        "description": "Baking soda is sodium bicarbonate used for leavening",
        "safe_alternative": "Safe natural choice",
        "why": "Non-toxic leavening agent"
    },
    "vinegar": {
        "risk_level": "low",
        "health_tags": ["preservative", "condiment"],
        "description": "Vinegar is a natural preservative and condiment",
        "safe_alternative": "Safe natural choice",
        "why": "Natural and safe"
    },
    "apple cider vinegar": {
        "risk_level": "low",
        "health_tags": ["preservative", "condiment"],
        "description": "Apple cider vinegar - natural vinegar with potential health benefits",
        "safe_alternative": "Safe natural choice",
        "why": "Natural and may have health benefits"
    },
    "honey": {
        "risk_level": "medium",
        "health_tags": ["vegan", "high_sugar"],
        "description": "Bee product - not suitable for vegans, high in sugar",
        "safe_alternative": "Maple syrup or agave",
        "why": "Not vegan; high sugar content"
    },
    "maple syrup": {
        "risk_level": "low",
        "health_tags": ["natural_sweetener", "vegan"],
        "description": "Natural sweetener from maple tree sap",
        "safe_alternative": "Safe natural choice",
        "why": "Natural sweetener with trace minerals"
    },
    "agave": {
        "risk_level": "low",
        "health_tags": ["natural_sweetener", "vegan"],
        "description": "Agave nectar - natural vegan sweetener",
        "safe_alternative": "Safe natural choice",
        "why": "Lower glycemic index than sugar"
    },
    "honey bee product": {
        "risk_level": "high",
        "health_tags": ["bee_allergy", "allergen"],
        "description": "Honey - bee product not safe for those with bee allergies",
        "safe_alternative": "Plant-based sweeteners",
        "why": "Can trigger bee allergy reactions"
    },
    "almond": {
        "risk_level": "high",
        "health_tags": ["nut_allergy", "allergen"],
        "description": "Tree nut - allergenic for those with tree nut allergies",
        "safe_alternative": "Sunflower seeds or pumpkin seeds",
        "why": "Common tree nut allergen"
    },
    "hazelnut": {
        "risk_level": "high",
        "health_tags": ["nut_allergy", "allergen"],
        "description": "Tree nut - allergenic",
        "safe_alternative": "Sunflower seed spread",
        "why": "Tree nut allergen"
    },
    "pistachio": {
        "risk_level": "high",
        "health_tags": ["nut_allergy", "allergen"],
        "description": "Tree nut - allergenic",
        "safe_alternative": "Seeds or legumes",
        "why": "Tree nut allergen"
    },
    "lentil": {
        "risk_level": "low",
        "health_tags": ["legume", "protein", "vegan"],
        "description": "Lentils are safe legumes high in protein and fiber",
        "safe_alternative": "Safe natural choice",
        "why": "Nutritious plant protein"
    },
    "chickpea": {
        "risk_level": "low",
        "health_tags": ["legume", "protein", "vegan"],
        "description": "Chickpeas are nutritious legumes safe for most diets",
        "safe_alternative": "Safe natural choice",
        "why": "Good source of protein and fiber"
    },
    "beans": {
        "risk_level": "low",
        "health_tags": ["legume", "protein", "vegan"],
        "description": "Beans are nutritious legumes safe for vegetarians and vegans",
        "safe_alternative": "Safe natural choice",
        "why": "Rich in protein and fiber"
    },
    "pea": {
        "risk_level": "low",
        "health_tags": ["legume", "vegetable"],
        "description": "Peas are safe legumes rich in protein and nutrients",
        "safe_alternative": "Safe natural choice",
        "why": "Good plant-based protein"
    },
    "quinoa": {
        "risk_level": "low",
        "health_tags": ["grain", "gluten_free", "complete_protein"],
        "description": "Quinoa is a complete protein and gluten-free grain",
        "safe_alternative": "Safe natural choice",
        "why": "Complete protein with all amino acids"
    },
    "plain yogurt": {
        "risk_level": "medium",
        "health_tags": ["dairy", "probiotics"],
        "description": "Yogurt contains probiotics but also lactose",
        "safe_alternative": "Dairy-free yogurt or lactose-free yogurt",
        "why": "Contains lactose despite probiotics"
    },
    "greek yogurt": {
        "risk_level": "medium",
        "health_tags": ["dairy", "high_protein"],
        "description": "Greek yogurt is higher in protein but contains dairy",
        "safe_alternative": "Dairy-free protein alternatives",
        "why": "Contains lactose"
    },
    
    # ==================== DIGESTIVE & INFLAMMATORY ====================
    "spicy sauce": {
        "risk_level": "medium",
        "health_tags": ["acid_forming", "gerd", "digestive", "inflammatory"],
        "description": "Spicy foods can trigger acid reflux and inflammation",
        "safe_alternative": "Mild seasonings",
        "why": "Can aggravate GERD and digestive disorders"
    },
    "chili pepper": {
        "risk_level": "medium",
        "health_tags": ["acid_forming", "gerd", "inflammatory"],
        "description": "Capsaicin can irritate digestive tract",
        "safe_alternative": "Mild spices",
        "why": "Triggers acid reflux in susceptible individuals"
    },
    "caffeine": {
        "risk_level": "medium",
        "health_tags": ["acid_forming", "gerd", "inflammatory"],
        "description": "Can relax esophageal sphincter triggering reflux",
        "safe_alternative": "Decaffeinated beverages",
        "why": "Worsens acid reflux"
    },
    "coffee": {
        "risk_level": "medium",
        "health_tags": ["acid_forming", "gerd", "digestive"],
        "description": "Acidic and can trigger reflux",
        "safe_alternative": "Herbal tea",
        "why": "Common GERD trigger"
    },
    "chocolate": {
        "risk_level": "medium",
        "health_tags": ["acid_forming", "gerd", "digestive", "high_calorie"],
        "description": "Fat and theobromine can trigger reflux",
        "safe_alternative": "Dark chocolate in moderation",
        "why": "Worsens GERD symptoms"
    },
    "alcohol": {
        "risk_level": "high",
        "health_tags": ["inflammatory", "liver_health", "digestive", "gerd"],
        "description": "Alcohol irritates digestive tract and impairs health",
        "safe_alternative": "Non-alcoholic beverages",
        "why": "Triggers inflammation and digestive issues"
    },
    
    # ==================== IMMUNE SUPPORT (for cold/fever) ====================
    "vitamin c rich": {
        "risk_level": "low",
        "health_tags": ["immune_support", "healthy"],
        "description": "Supports immune system",
        "safe_alternative": "Safe and beneficial",
        "why": "Boosts immunity"
    },
    "zinc rich": {
        "risk_level": "low",
        "health_tags": ["immune_support", "healthy"],
        "description": "Zinc supports immune function",
        "safe_alternative": "Safe and beneficial",
        "why": "Essential for immune response"
    },
    "ginger": {
        "risk_level": "low",
        "health_tags": ["immune_support", "anti_inflammatory", "healthy"],
        "description": "Natural anti-inflammatory and immune booster",
        "safe_alternative": "Safe and beneficial",
        "why": "Reduces inflammation and supports immunity"
    },
    "honey": {
        "risk_level": "low",
        "health_tags": ["immune_support", "anti_inflammatory", "healthy"],
        "description": "Natural antibacterial and soothes throat",
        "safe_alternative": "Safe and beneficial",
        "why": "Helps with cough and immune support"
    },
    
    # ==================== THYROID SUPPORT ====================
    "iodine rich": {
        "risk_level": "low",
        "health_tags": ["thyroid", "healthy"],
        "description": "Iodine essential for thyroid function",
        "safe_alternative": "Safe and beneficial for thyroid",
        "why": "Prevents thyroid disorders"
    },
    "seaweed": {
        "risk_level": "low",
        "health_tags": ["thyroid", "iodine", "healthy"],
        "description": "Rich in iodine for thyroid health",
        "safe_alternative": "Safe source of iodine",
        "why": "Natural thyroid support"
    },
    "cruciferous vegetables": {
        "risk_level": "medium",
        "health_tags": ["thyroid", "goitrogenic"],
        "description": "Raw cruciferous vegetables contain goitrogens that can affect thyroid",
        "safe_alternative": "Cook vegetables to reduce goitrogens",
        "why": "Goitrogens interfere with iodine absorption if raw"
    },
    
    # ==================== EMULSIFIERS ====================
    "soy lecithin": {
        "risk_level": "medium",
        "health_tags": ["emulsifier", "soy_allergy", "allergen"],
        "description": "Soy-derived emulsifier used to prevent ingredient separation. May contain allergens.",
        "safe_alternative": "Sunflower lecithin, egg lecithin",
        "why": "Common allergen; can trigger soy allergy"
    },
    "polysorbate 80": {
        "risk_level": "low",
        "health_tags": ["emulsifier", "additive"],
        "description": "Polysorbate 80 is a synthetic emulsifier used in many processed foods and cosmetics to achieve smooth texture and consistency.",
        "safe_alternative": "Natural emulsifiers like egg lecithin",
        "why": "Generally recognized as safe (GRAS) but some sensitivity reported"
    },
    "polysorbate 60": {
        "risk_level": "low",
        "health_tags": ["emulsifier", "additive"],
        "description": "Synthetic polysorbate used as emulsifier in ice cream and baked goods. Helps mix oil and water-based ingredients.",
        "safe_alternative": "Lecithin or natural gums",
        "why": "GRAS approved but may cause digestive issues in sensitive individuals"
    },
    "mono- and diglycerides": {
        "risk_level": "low",
        "health_tags": ["emulsifier", "additive"],
        "description": "Emulsifiers derived from fats used in bread, baked goods, and peanut butter to improve texture and extend shelf life.",
        "safe_alternative": "Natural emulsifiers",
        "why": "Generally safe but highly processed"
    },
    "sodium stearoyl lactylate": {
        "risk_level": "low",
        "health_tags": ["emulsifier", "additive"],
        "description": "Sodium stearoyl lactylate (SSL) strengthens dough and improves texture in baked goods. Used as dough conditioner.",
        "safe_alternative": "Natural dough conditioners",
        "why": "Generally recognized as safe but synthetic"
    },
    "potassium sorbate": {
        "risk_level": "low",
        "health_tags": ["preservative", "additive"],
        "description": "Preservative that inhibits mold and yeast growth. Commonly used in dairy products and baked goods.",
        "safe_alternative": "Natural preservatives like citric acid",
        "why": "Generally safe but may cause reactions in sensitive individuals"
    },
    "sorbic acid": {
        "risk_level": "low",
        "health_tags": ["preservative", "additive"],
        "description": "Sorbic acid is a naturally-derived preservative that prevents mold, yeast, and bacterial growth in foods.",
        "safe_alternative": "Citric acid or natural alternatives",
        "why": "Safe alternative to sodium benzoate"
    },
    "calcium disodium edta": {
        "risk_level": "low",
        "health_tags": ["chelating_agent", "additive"],
        "description": "Chelating agent (EDTA) used to preserve color and flavor by binding trace metals. Found in salad dressings and sauces.",
        "safe_alternative": "Natural antioxidants",
        "why": "GRAS but metal-binding concerns for some individuals"
    },
    
    # ==================== CATALYSTS & PROCESSING AIDS ====================
    "enzymes": {
        "risk_level": "low",
        "health_tags": ["processing_aid", "additive"],
        "description": "Natural or GMO-derived enzymes used in food processing to speed up reactions like cheese-making or bread fermentation.",
        "safe_alternative": "Traditional processing methods",
        "why": "Generally safe but may contain GMO sources"
    },
    "amylase": {
        "risk_level": "low",
        "health_tags": ["enzyme", "processing_aid"],
        "description": "Enzyme that breaks down starches into sugars. Used in bread-making and brewing for texture and fermentation.",
        "safe_alternative": "Traditional fermentation",
        "why": "Natural enzyme but may come from GMO sources"
    },
    "protease": {
        "risk_level": "low",
        "health_tags": ["enzyme", "processing_aid"],
        "description": "Protein-breaking enzyme used in cheese production, meat tenderizing, and brewing to improve texture and flavor.",
        "safe_alternative": "Traditional processing",
        "why": "Safe but may be derived from GMO organisms"
    },
    "lipase": {
        "risk_level": "low",
        "health_tags": ["enzyme", "processing_aid"],
        "description": "Fat-breaking enzyme used in cheese-making to develop flavor. Creates characteristic tang in aged cheeses.",
        "safe_alternative": "Traditional aged cheese methods",
        "why": "Safe enzyme but may originate from GMO sources"
    },
    "glucose oxidase": {
        "risk_level": "low",
        "health_tags": ["enzyme", "processing_aid"],
        "description": "Enzyme that oxidizes glucose. Used in baking as flour improver and in food preservation to remove oxygen.",
        "safe_alternative": "Natural aging methods",
        "why": "GRAS but highly processed"
    },
    
    # ==================== THICKENERS & GELLING AGENTS ====================
    "sodium carboxymethyl cellulose": {
        "risk_level": "low",
        "health_tags": ["thickener", "additive"],
        "description": "Synthetic cellulose derivative used as thickener in ice cream, yogurt, and sauces for smooth consistency.",
        "safe_alternative": "Gelatin, agar-agar",
        "why": "Generally safe but may cause digestive issues in large amounts"
    },
    "carrageenan": {
        "risk_level": "medium",
        "health_tags": ["thickener", "additive", "digestive"],
        "description": "Carrageenan is a seaweed-derived thickener used in dairy alternatives and processed foods. May cause inflammation.",
        "safe_alternative": "Gelatin or guar gum",
        "why": "Some studies link to digestive inflammation"
    },
    "agar-agar": {
        "risk_level": "low",
        "health_tags": ["thickener", "natural"],
        "description": "Natural seaweed-derived gelling agent used in desserts and plant-based products. Vegetarian-friendly.",
        "safe_alternative": "Safe natural choice",
        "why": "Natural and vegetarian alternative to gelatin"
    },
    "gelatin": {
        "risk_level": "medium",
        "health_tags": ["gelling_agent", "animal_product", "vegan"],
        "description": "Animal-derived protein used as gelling agent in desserts and marshmallows. Not suitable for vegetarians/vegans.",
        "safe_alternative": "Agar-agar or pectin",
        "why": "Animal product; not vegan"
    },
    "pectin": {
        "risk_level": "low",
        "health_tags": ["gelling_agent", "natural"],
        "description": "Natural pectin from fruits used as thickener in jams and jellies. No significant health risks.",
        "safe_alternative": "Safe natural choice",
        "why": "Natural and generally beneficial"
    },
    
    # ==================== ANTIOXIDANTS ====================
    "sodium ascorbate": {
        "risk_level": "low",
        "health_tags": ["antioxidant", "additive"],
        "description": "Sodium form of vitamin C used to prevent oxidation and browning. Used in cured meats and frozen products.",
        "safe_alternative": "Natural vitamin C (ascorbic acid)",
        "why": "Generally safe but sodium content to consider"
    },
    "sodium bisulfite": {
        "risk_level": "medium",
        "health_tags": ["preservative", "sulfite", "asthma"],
        "description": "Sulfite preservative that prevents browning and spoilage. Can trigger asthma in sensitive individuals.",
        "safe_alternative": "Citric acid or ascorbic acid",
        "why": "Known allergen for asthmatics; must be labeled"
    },
    "sulfur dioxide": {
        "risk_level": "medium",
        "health_tags": ["preservative", "sulfite", "asthma"],
        "description": "Preservative used in wine, dried fruit, and processed foods. May cause respiratory issues in sensitive individuals.",
        "safe_alternative": "Natural preservation methods",
        "why": "Sulfite allergen; can trigger asthma attacks"
    },
    "bha": {
        "risk_level": "medium",
        "health_tags": ["antioxidant", "potentially_harmful"],
        "description": "Butylated hydroxyanisole - synthetic antioxidant used in oils and processed meats. Under study for potential health risks.",
        "safe_alternative": "Vitamin E or natural antioxidants",
        "why": "Potential endocrine disruptor; being phased out"
    },
    "bht": {
        "risk_level": "medium",
        "health_tags": ["antioxidant", "potentially_harmful"],
        "description": "Butylated hydroxytoluene - synthetic antioxidant used to prevent fat rancidity. Potential health concerns.",
        "safe_alternative": "Vitamin E (tocopherols)",
        "why": "Possible carcinogen; restricted in EU"
    },
    "vitamin e": {
        "risk_level": "low",
        "health_tags": ["antioxidant", "healthy"],
        "description": "Natural antioxidant (tocopherol) derived from oils or seeds. Used to prevent rancidity without health risks.",
        "safe_alternative": "Safe natural choice",
        "why": "Natural and beneficial antioxidant"
    },
    
    # ==================== FLAVORING COMPOUNDS ====================
    "vanillin": {
        "risk_level": "low",
        "health_tags": ["flavoring", "additive"],
        "description": "Synthetic vanilla flavoring derived from wood pulp or through chemical synthesis. Cost-effective alternative to natural vanilla.",
        "safe_alternative": "Natural vanilla extract",
        "why": "Generally safe but synthetic; may contain traces from petroleum"
    },
    "ethylvanillin": {
        "risk_level": "low",
        "health_tags": ["flavoring", "additive"],
        "description": "Synthetic flavoring compound 3x stronger than vanillin. Used in desserts, beverages, and confections.",
        "safe_alternative": "Natural vanilla or vanillin",
        "why": "Safe but synthetic; stronger concentration needed"
    },
    "natural flavors": {
        "risk_level": "low",
        "health_tags": ["flavoring", "natural"],
        "description": "Natural flavors derived from plant or animal sources. Exact composition not always disclosed on labels.",
        "safe_alternative": "Whole ingredient flavors",
        "why": "Generally safe but composition may include allergens"
    },
    "artificial flavors": {
        "risk_level": "low",
        "health_tags": ["flavoring", "additive"],
        "description": "Lab-synthesized flavors chemically engineered to replicate tastes. Cost-effective but less complex than natural flavors.",
        "safe_alternative": "Natural flavors",
        "why": "Generally recognized as safe but highly processed"
    },
    
    # ==================== MODIFIED STARCHES ====================
    "modified food starch": {
        "risk_level": "low",
        "health_tags": ["starch", "additive"],
        "description": "Chemically modified starch used as thickener to improve texture in sauces, gravies, and processed foods.",
        "safe_alternative": "Cornstarch or tapioca starch",
        "why": "Generally safe but highly processed"
    },
    "tapioca starch": {
        "risk_level": "low",
        "health_tags": ["starch", "natural"],
        "description": "Natural starch extracted from cassava root. Used as thickener in gluten-free products.",
        "safe_alternative": "Safe natural choice",
        "why": "Natural and widely used in gluten-free cooking"
    },
    "cornstarch": {
        "risk_level": "low",
        "health_tags": ["starch", "natural"],
        "description": "Natural starch from corn used as thickener. May be from GMO corn without organic certification.",
        "safe_alternative": "Tapioca or potato starch",
        "why": "Natural but check for GMO/organic status"
    },
    
    # ==================== COLORANTS & DYES ====================
    "titanium dioxide": {
        "risk_level": "low",
        "health_tags": ["colorant", "additive"],
        "description": "White pigment used in candies, frosting, and supplements for bright white color. Nano particles concerns exist.",
        "safe_alternative": "Natural colorants",
        "why": "Generally safe but nano-particle inhalation concerns"
    },
    "fd&c red no. 40": {
        "risk_level": "medium",
        "health_tags": ["colorant", "artificial_dye", "hyperactivity"],
        "description": "Synthetic red food dye used in candies and beverages. May trigger hyperactivity in children.",
        "safe_alternative": "Beet juice or carmine",
        "why": "Linked to behavioral issues in some children"
    },
    "fd&c yellow no. 5": {
        "risk_level": "medium",
        "health_tags": ["colorant", "artificial_dye", "allergen"],
        "description": "Synthetic yellow food dye. Known allergen for some individuals; must be labeled when present.",
        "safe_alternative": "Turmeric or natural colorants",
        "why": "Can trigger allergic reactions in sensitive individuals"
    },
    "tartrazine": {
        "risk_level": "medium",
        "health_tags": ["colorant", "fd&c_yellow_5", "allergen"],
        "description": "Yellow synthetic dye (FD&C Yellow #5) used in processed foods. Common allergen trigger.",
        "safe_alternative": "Turmeric or annatto",
        "why": "Known allergen; linked to asthma and hives"
    },
    "annatto": {
        "risk_level": "low",
        "health_tags": ["colorant", "natural"],
        "description": "Natural orange-red colorant derived from achiote seeds. Safe and widely used in organic products.",
        "safe_alternative": "Safe natural choice",
        "why": "Natural and generally well-tolerated"
    },
    "carmine": {
        "risk_level": "low",
        "health_tags": ["colorant", "natural", "animal_product"],
        "description": "Natural red dye derived from cochineal insects. Not suitable for vegans but rare allergen.",
        "safe_alternative": "Beet juice or synthetic alternatives",
        "why": "Natural but animal-derived"
    },
    
    # ==================== COATINGS & RELEASE AGENTS ====================
    "soy": {
        "risk_level": "medium",
        "health_tags": ["allergen", "soy_allergy", "processing_aid"],
        "description": "Soy-based processing aid or ingredient. Common allergen that can trigger allergic reactions.",
        "safe_alternative": "Sunflower oil or other alternatives",
        "why": "Major allergen; increasingly common in food products"
    },
    "canola oil": {
        "risk_level": "low",
        "health_tags": ["oil", "additive"],
        "description": "Rapeseed oil used as coating and release agent. Usually highly processed and potentially GMO.",
        "safe_alternative": "Olive oil or coconut oil",
        "why": "Often GMO; check for organic certification"
    },
    "sunflower oil": {
        "risk_level": "low",
        "health_tags": ["oil", "healthy"],
        "description": "Sunflower oil used as natural coating and release agent. Generally healthier than canola.",
        "safe_alternative": "Safe natural choice",
        "why": "Natural and generally safe"
    },
    "carnauba wax": {
        "risk_level": "low",
        "health_tags": ["coating", "natural"],
        "description": "Natural wax from carnauba palm leaves used to coat candies and pills for shine and protection.",
        "safe_alternative": "Safe natural choice",
        "why": "Natural and food-grade"
    },
    
    # ==================== HUMECTANTS & MOISTURE RETENTION ====================
    "glycerin": {
        "risk_level": "low",
        "health_tags": ["humectant", "additive"],
        "description": "Glycerin retains moisture in processed foods and maintains softness in baked goods. Generally well-tolerated.",
        "safe_alternative": "Safe natural choice",
        "why": "Generally recognized as safe"
    },
    "propylene glycol": {
        "risk_level": "low",
        "health_tags": ["humectant", "preservative"],
        "description": "Synthetic humectant used in processed foods to retain moisture. Also used in anti-freeze (different grade).",
        "safe_alternative": "Glycerin or honey",
        "why": "GRAS but synthetic; consumer confusion with anti-freeze"
    },
    "sorbitol": {
        "risk_level": "low",
        "health_tags": ["humectant", "sugar_alcohol", "digestive"],
        "description": "Sugar alcohol that retains moisture in foods. Can cause digestive issues and bloating in large amounts.",
        "safe_alternative": "Glycerin or erythritol",
        "why": "May cause laxative effect in sensitive individuals"
    },
}



def get_ingredient_info(ingredient_name: str) -> dict:
    """
    Get information about an ingredient
    
    Args:
        ingredient_name: Name of ingredient to look up
        
    Returns:
        Dictionary with ingredient info or None if not found
    """
    # Normalize the input
    normalized = ingredient_name.lower().strip()
    return INGREDIENTS_DB.get(normalized)


def is_risky_ingredient(ingredient_name: str) -> bool:
    """Check if an ingredient has high or medium risk level"""
    info = get_ingredient_info(ingredient_name)
    if not info:
        return False
    return info["risk_level"] in ["high", "medium"]


def get_risk_score_for_ingredient(ingredient_name: str) -> int:
    """Get risk score for an ingredient (0-100)"""
    info = get_ingredient_info(ingredient_name)
    if not info:
        return 0
    
    risk_map = {"low": 10, "medium": 50, "high": 100}
    return risk_map.get(info["risk_level"], 0)



def get_ingredient_info(ingredient_name: str) -> dict:
    """
    Get information about an ingredient
    
    Args:
        ingredient_name: Name of ingredient to look up
        
    Returns:
        Dictionary with ingredient info or None if not found
    """
    # Normalize the input
    normalized = ingredient_name.lower().strip()
    return INGREDIENTS_DB.get(normalized)


def is_risky_ingredient(ingredient_name: str) -> bool:
    """Check if an ingredient has high or medium risk level"""
    info = get_ingredient_info(ingredient_name)
    if not info:
        return False
    return info["risk_level"] in ["high", "medium"]


def get_risk_score_for_ingredient(ingredient_name: str) -> int:
    """Get risk score for an ingredient (0-100)"""
    info = get_ingredient_info(ingredient_name)
    if not info:
        return 0
    
    risk_map = {"low": 10, "medium": 50, "high": 100}
    return risk_map.get(info["risk_level"], 0)
