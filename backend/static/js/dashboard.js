/**
 * Dashboard Page Interactions
 * Displays recent scans, navigation, and user profile
 */

document.addEventListener('DOMContentLoaded', function() {
  console.log('Dashboard page initialized');

  // Check if user is logged in
  if (!RiskBiteAPI.isLoggedIn()) {
    window.location.href = '/login';
    return;
  }

  // Display user info
  displayUserInfo();

  // Load recent scans for user
  loadRecentScans();

  // Setup button handlers
  setupButtonHandlers();

  /**
   * Display user information in the dashboard
   */
  function displayUserInfo() {
    const email = RiskBiteAPI.getUserEmail();
    const userNameElements = document.querySelectorAll('p[class*="text-sm font-700 text-slate-900"]');
    
    if (userNameElements.length > 0 && email) {
      const name = email.split('@')[0].charAt(0).toUpperCase() + email.split('@')[0].slice(1);
      userNameElements[0].textContent = name;
    }

    const userEmail = document.querySelectorAll('p[class*="text-xs text-slate-500"]');
    if (userEmail.length > 0 && email) {
      userEmail[0].textContent = email;
    }
  }

  /**
   * Setup all button and link event handlers
   */
  function setupButtonHandlers() {
    // New Scan button
    const newScanButton = document.querySelector('a[href="/scan"]');
    if (newScanButton) {
      newScanButton.addEventListener('click', function(e) {
        // On first click in this session, show inline scan modal and stay on dashboard
        const firstShown = sessionStorage.getItem('firstScanShown');
        if (!firstShown) {
          e.preventDefault();
          sessionStorage.setItem('firstScanShown', 'true');
          openInlineScanModal();
          return;
        }

        // Otherwise, follow the original navigation
        // allow default behaviour to navigate to /scan
      });
    }

    // Recent Scans links
    const recentScanLinks = document.querySelectorAll('div.group a[href="scan.html"]');
    recentScanLinks.forEach(link => {
      link.addEventListener('click', function(e) {
        e.preventDefault();
        // Store which scan was clicked and navigate
        window.location.href = '/scan-results';
      });
    });

    // Health History link
    const healthHistoryLink = document.querySelector('#healthHistoryLink');
    if (healthHistoryLink) {
      healthHistoryLink.addEventListener('click', function(e) {
        e.preventDefault();
        showHealthHistory();
      });
    }

    // Constraints link - NEW FUNCTIONALITY
    const constraintsLink = document.querySelector('#constraintsLink');
    if (constraintsLink) {
      constraintsLink.addEventListener('click', function(e) {
        e.preventDefault();
        showConstraints();
      });
    }

    // Settings link
    const settingsLink = document.querySelector('a[href*="settings"], a[href="#"]');
    if (settingsLink) {
      settingsLink.addEventListener('click', function(e) {
        if (this.textContent.includes('Settings')) {
          e.preventDefault();
          showSettings();
        }
      });
    }

    // Upgrade button
    const upgradeButton = document.querySelector('button.bg-primary[class*="w-full"]');
    if (upgradeButton) {
      upgradeButton.addEventListener('click', function(e) {
        e.preventDefault();
        showUpgradePrompt();
      });
    }

    // Filters button
    const filtersButton = document.querySelector('button[class*="px-4 py-2"] span.material-icons-round:first-child')?.closest('button');
    if (filtersButton) {
      filtersButton.addEventListener('click', function() {
        toggleFilters();
      });
    }

    // Notifications button
    const notificationsButton = document.querySelector('button.w-10.h-10.rounded-full[class*="primary"]');
    if (notificationsButton) {
      notificationsButton.addEventListener('click', function() {
        showNotifications();
      });
    }

    // Logout button - if exists in sidebar
    const logoutButton = document.querySelector('a[href*="logout"]') || 
                        document.querySelector('a[class*="hover:text-red"]');
    if (logoutButton) {
      logoutButton.addEventListener('click', function(e) {
        e.preventDefault();
        if (confirm('Are you sure you want to logout?')) {
          RiskBiteAPI.logout();
          window.location.href = '/login';
        }
      });
    }

    // Search functionality
    const searchInput = document.querySelector('input[placeholder*="Search"]');
    if (searchInput) {
      searchInput.addEventListener('input', handleSearch);
    }

    // Dynamically add click handlers to scan cards
    setupScanCardHandlers();
  }

  /**
   * Setup handlers for scan result cards
   */
  function setupScanCardHandlers() {
    const scanCards = document.querySelectorAll('[class*="group bg-white"]');
    scanCards.forEach(card => {
      card.addEventListener('click', function() {
        const productName = this.querySelector('h3')?.textContent || 'Unknown Product';
        const riskLevel = this.querySelector('[class*="text-sm uppercas"]')?.textContent || 'MODERATE';
        
        // Store selected scan info and navigate
        sessionStorage.setItem('selectedScan', JSON.stringify({
          product: productName,
          riskLevel: riskLevel,
          date: new Date().toLocaleString()
        }));
        
        window.location.href = '/scan-results';
      });
    });
  }


    /**
     * Load recent scans from the backend and render cards
     */
    async function loadRecentScans() {
      const userId = RiskBiteAPI.getUserId();
      const grid = document.getElementById('scansGrid');
      if (!grid) return;

      // Show loading state
      grid.innerHTML = `<div class="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 overflow-hidden p-6 text-center text-slate-500">Loading recent scans...</div>`;

      if (!userId) {
        grid.innerHTML = `<div class="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 overflow-hidden p-4 text-center text-slate-500">Please login to view your scans.</div>`;
        return;
      }

      try {
        const res = await RiskBiteAPI.getScans(userId);
        if (!res.ok) {
          grid.innerHTML = `<div class="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 overflow-hidden p-4 text-center text-slate-500">No scans available.</div>`;
          return;
        }

        const scans = res.scans || [];
        if (scans.length === 0) {
          grid.innerHTML = `<div class="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 overflow-hidden p-4 text-center text-slate-500">No scans yet. Start by uploading a product label!</div>`;
          return;
        }

        // Build cards
        grid.innerHTML = '';
        scans.forEach(s => {
          const scan = s.scan || {};
          const created = new Date(s.created_at).toLocaleString();
          const riskLevel = scan.risk_level || 'UNKNOWN';
          const riskScore = scan.risk_score !== undefined ? scan.risk_score : '';
          const title = (scan.ingredients && scan.ingredients.length>0) ? scan.ingredients[0] : (scan.summary || 'Scanned Product');

          const card = document.createElement('div');
          card.className = 'group bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 overflow-hidden p-4 cursor-pointer hover:shadow-lg transition-shadow';
          card.innerHTML = `
            <div class="flex items-start justify-between">
              <div class="text-left">
                <h3 class="text-lg font-700 text-slate-900 dark:text-white">${escapeHtml(title)}</h3>
                <p class="text-xs text-slate-500 mt-1">${created}</p>
              </div>
              <div class="text-right">
                <div class="text-sm uppercase text-slate-700 dark:text-slate-200 font-bold">${riskLevel}</div>
                <div class="text-xs text-slate-400 mt-1">Score: ${riskScore}</div>
              </div>
            </div>
            <p class="text-sm text-slate-500 mt-3 truncate">${escapeHtml(scan.summary || '')}</p>
          `;

          card.addEventListener('click', () => {
            sessionStorage.setItem('selectedScan', JSON.stringify(s));
            window.location.href = '/scan-results';
          });

          grid.appendChild(card);
        });

      } catch (err) {
        console.error('Failed to load scans', err);
        grid.innerHTML = `<div class="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 overflow-hidden p-4 text-center text-slate-500">Error loading scans.</div>`;
      }
    }

    function escapeHtml(unsafe) {
      if (!unsafe) return '';
      return String(unsafe).replace(/[&<>"'`]/g, function (s) {
        return ({
          '&': '&amp;',
          '<': '&lt;',
          '>': '&gt;',
          '"': '&quot;',
          "'": '&#39;',
          '`': '&#96;'
        })[s];
      });
    }

  /**
   * Handle search input
   */
  function handleSearch(e) {
    const query = e.target.value.toLowerCase();
    const scanCards = document.querySelectorAll('[class*="group bg-white"]');
    
    scanCards.forEach(card => {
      const productName = card.querySelector('h3')?.textContent.toLowerCase() || '';
      const visible = productName.includes(query);
      card.style.display = visible ? 'block' : 'none';
    });
  }


  /**
   * Open inline scan modal (simple uploader) and handle scanning
   */
  function openInlineScanModal() {
    // Remove existing modal if present
    const existing = document.getElementById('inline-scan-modal');
    if (existing) existing.remove();

    const modal = document.createElement('div');
    modal.id = 'inline-scan-modal';
    modal.style.cssText = `position:fixed;inset:0;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,0.45);z-index:12000;`;

    const panel = document.createElement('div');
    panel.className = 'bg-white dark:bg-slate-800 rounded-xl p-6 w-full max-w-2xl shadow-lg';
    panel.innerHTML = `
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-bold text-slate-900 dark:text-white">Scan Product Label</h3>
        <button id="inline-scan-close" class="text-slate-500 hover:text-slate-700">×</button>
      </div>
      <div class="space-y-4">
        <p class="text-sm text-slate-600">Upload a product label image to scan it here without leaving the dashboard.</p>
        <input id="inlineScanFile" type="file" accept="image/*,.pdf" class="w-full" />
        <div class="flex gap-2 justify-end">
          <button id="inlineScanCancel" class="px-4 py-2 bg-white border rounded">Cancel</button>
          <button id="inlineScanSubmit" class="px-4 py-2 bg-primary text-[#0d1b12] rounded font-bold">Scan</button>
        </div>
        <div id="inlineScanStatus" class="text-sm text-slate-500 mt-2"></div>
      </div>
    `;

    modal.appendChild(panel);
    document.body.appendChild(modal);

    const fileInput = document.getElementById('inlineScanFile');
    const submitBtn = document.getElementById('inlineScanSubmit');
    const cancelBtn = document.getElementById('inlineScanCancel');
    const closeBtn = document.getElementById('inline-scan-close');
    const status = document.getElementById('inlineScanStatus');

    function closeModal() {
      const m = document.getElementById('inline-scan-modal');
      if (m) m.remove();
    }

    cancelBtn.addEventListener('click', closeModal);
    closeBtn.addEventListener('click', closeModal);

    submitBtn.addEventListener('click', async function() {
      const files = fileInput.files;
      if (!files || files.length === 0) {
        status.textContent = 'Please choose an image file first.';
        return;
      }

      const file = files[0];
      status.textContent = 'Scanning...';

      try {
        const userId = RiskBiteAPI.getUserId();
        let userConditions = [];
        try {
          const hh = await RiskBiteAPI.getHealthHistory(userId);
          if (hh.ok && hh.history && hh.history.conditions) userConditions = hh.history.conditions;
        } catch (e) {
          // ignore
        }

        const result = await RiskBiteAPI.scanProduct(file, userConditions, userId);
        // Persist quick preview in session and refresh grid
        sessionStorage.setItem('selectedScan', JSON.stringify({ scan: result, created_at: new Date().toISOString() }));
        sessionStorage.setItem('scanResult', JSON.stringify(result));
        sessionStorage.setItem('scanImageName', file.name);

        status.textContent = 'Scan complete! Refreshing recent scans...';
        showNotification('Scan complete!', 'success');
        // refresh grid to include the new scan
        await loadRecentScans();
        setTimeout(closeModal, 800);
      } catch (err) {
        console.error('Inline scan failed', err);
        status.textContent = 'Scan failed: ' + (err.message || 'Unknown error');
        showNotification('Scan failed: ' + (err.message || ''), 'error');
      }
    });
  }

  /**
   * Show health history modal
   */
  async function showHealthHistory() {
    const userId = RiskBiteAPI.getUserId();
    if (!userId) {
      showNotification('Please login to manage health history', 'error');
      return;
    }

    // Fetch existing health history
    let existingHistory = null;
    let parsedConditions = [];
    try {
      const res = await RiskBiteAPI.getHealthHistory(userId);
      if (res.ok && res.history) {
        existingHistory = res.history;
        parsedConditions = existingHistory.conditions || [];
      }
    } catch (e) {
      console.log('No existing health history');
    }

    // Common health conditions and allergies
    const commonConditions = [
      { id: 'diabetes', label: 'Diabetes', category: 'Medical' },
      { id: 'high_blood_pressure', label: 'High Blood Pressure', category: 'Medical' },
      { id: 'heart_disease', label: 'Heart Disease', category: 'Medical' },
      { id: 'kidney_disease', label: 'Kidney Disease', category: 'Medical' },
      { id: 'liver_disease', label: 'Liver Disease', category: 'Medical' },
      { id: 'peanut_allergy', label: 'Peanut Allergy', category: 'Allergy' },
      { id: 'tree_nut_allergy', label: 'Tree Nut Allergy', category: 'Allergy' },
      { id: 'shellfish_allergy', label: 'Shellfish Allergy', category: 'Allergy' },
      { id: 'fish_allergy', label: 'Fish Allergy', category: 'Allergy' },
      { id: 'egg_allergy', label: 'Egg Allergy', category: 'Allergy' },
      { id: 'milk_allergy', label: 'Milk/Dairy Allergy', category: 'Allergy' },
      { id: 'soy_allergy', label: 'Soy Allergy', category: 'Allergy' },
      { id: 'wheat_allergy', label: 'Wheat/Gluten Allergy', category: 'Allergy' },
      { id: 'sesame_allergy', label: 'Sesame Allergy', category: 'Allergy' },
      { id: 'gluten_sensitivity', label: 'Gluten Sensitivity/Celiac', category: 'Dietary' },
      { id: 'lactose_intolerance', label: 'Lactose Intolerance', category: 'Dietary' },
      { id: 'vegetarian', label: 'Vegetarian', category: 'Dietary' },
      { id: 'vegan', label: 'Vegan', category: 'Dietary' },
      { id: 'kosher', label: 'Kosher', category: 'Dietary' },
      { id: 'halal', label: 'Halal', category: 'Dietary' },
    ];

    // Group conditions by category
    const categories = {};
    commonConditions.forEach(c => {
      if (!categories[c.category]) categories[c.category] = [];
      categories[c.category].push(c);
    });

    // Build checkbox HTML
    let checkboxesHtml = '';
    Object.keys(categories).forEach(cat => {
      checkboxesHtml += `<div class="mb-4"><h4 class="font-bold text-sm text-slate-700 mb-2">${cat}</h4><div class="grid grid-cols-2 gap-2">`;
      categories[cat].forEach(c => {
        const isChecked = parsedConditions.includes(c.id) ? 'checked' : '';
        checkboxesHtml += `
          <label class="flex items-center gap-2 text-sm cursor-pointer">
            <input type="checkbox" value="${c.id}" ${isChecked} class="health-checkbox w-4 h-4 rounded border-gray-300 text-primary focus:ring-primary">
            <span>${c.label}</span>
          </label>
        `;
      });
      checkboxesHtml += `</div></div>`;
    });

    // Get natural language description if exists
    const naturalLanguage = existingHistory?.natural_language || '';

    const modal = createModal(
      'Your Health History',
      `
        <div class="space-y-4">
          <p class="text-sm text-slate-600">Save your health conditions, allergies, and dietary preferences to get personalized risk assessments when scanning products.</p>
          
          <!-- Natural Language Input -->
          <div>
            <label class="block text-sm font-bold mb-2">Describe your health conditions</label>
            <textarea id="healthTextInput" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm" rows="3" placeholder="e.g., I have diabetes, allergic to peanuts and shellfish, lactose intolerant">${escapeHtml(naturalLanguage)}</textarea>
            <button id="parseHealthBtn" class="mt-2 text-xs bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600">
              Parse & Extract Conditions
            </button>
            <p id="parseStatus" class="text-xs text-slate-500 mt-1"></p>
          </div>

          <!-- Quick Select Conditions -->
          <div id="conditionsSection">
            <label class="block text-sm font-bold mb-2">Or select your conditions:</label>
            ${checkboxesHtml}
          </div>

          <div class="flex gap-2 mt-4">
            <button id="saveHealthBtn" class="flex-1 bg-primary text-[#0d1b12] font-bold py-2 px-4 rounded-lg hover:opacity-90">
              Save Health Profile
            </button>
            <button id="clearHealthBtn" class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
              Clear All
            </button>
          </div>
          
          <p class="text-xs text-gray-500 mt-4">Your health information is kept private and encrypted on our servers. It will be used to personalize your product risk assessments.</p>
        </div>
      `
    );
    modal.style.display = 'block';

    // Parse health button handler
    const parseBtn = document.getElementById('parseHealthBtn');
    const parseStatus = document.getElementById('parseStatus');
    const healthTextInput = document.getElementById('healthTextInput');
    
    if (parseBtn) {
      parseBtn.addEventListener('click', async function() {
        const text = healthTextInput.value.trim();
        if (!text) {
          parseStatus.textContent = 'Please enter your health conditions first.';
          return;
        }

        parseBtn.disabled = true;
        parseBtn.textContent = 'Parsing...';
        parseStatus.textContent = 'Analyzing your health conditions...';

        try {
          const result = await RiskBiteAPI.parseHealth(text);
          if (result.ok && result.parsed) {
            const parsed = result.parsed;
            const conditions = parsed.conditions || {};
            
            // Check the checkboxes based on parsed conditions
            const checkboxes = document.querySelectorAll('.health-checkbox');
            checkboxes.forEach(cb => {
              const conditionKey = cb.value;
              if (conditions[conditionKey] === true) {
                cb.checked = true;
              } else {
                // Also check for partial matches
                Object.keys(conditions).forEach(key => {
                  if (key.includes(conditionKey) || conditionKey.includes(key)) {
                    cb.checked = true;
                  }
                });
              }
            });

            parseStatus.textContent = `Found ${Object.values(conditions).filter(v => v).length} conditions!`;
            parseStatus.className = 'text-xs text-green-600 mt-1';
          } else {
            parseStatus.textContent = 'Could not parse health conditions. Please select manually.';
          }
        } catch (e) {
          console.error('Parse error:', e);
          parseStatus.textContent = 'Error parsing. Please select conditions manually.';
        } finally {
          parseBtn.disabled = false;
          parseBtn.textContent = 'Parse & Extract Conditions';
        }
      });
    }

    // Save health button handler
    const saveBtn = document.getElementById('saveHealthBtn');
    if (saveBtn) {
      saveBtn.addEventListener('click', async function() {
        // Collect checked conditions
        const checkboxes = document.querySelectorAll('.health-checkbox:checked');
        const conditions = Array.from(checkboxes).map(cb => cb.value);
        
        const healthData = {
          conditions: conditions,
          natural_language: healthTextInput.value.trim(),
          updated_at: new Date().toISOString()
        };

        saveBtn.disabled = true;
        saveBtn.textContent = 'Saving...';

        try {
          const result = await RiskBiteAPI.saveHealthHistory(userId, healthData);
          if (result.ok) {
            showNotification('Health profile saved successfully!', 'success');
            // Close modal after short delay
            setTimeout(() => {
              const modal = document.getElementById('modal-overlay');
              if (modal) {
                modal.style.display = 'none';
                setTimeout(() => modal.remove(), 300);
              }
            }, 1000);
          } else {
            showNotification('Failed to save health profile', 'error');
          }
        } catch (e) {
          console.error('Save error:', e);
          showNotification('Error saving health profile', 'error');
        } finally {
          saveBtn.disabled = false;
          saveBtn.textContent = 'Save Health Profile';
        }
      });
    }

// Clear button handler
    const clearBtn = document.getElementById('clearHealthBtn');
    if (clearBtn) {
      clearBtn.addEventListener('click', function() {
        const checkboxes = document.querySelectorAll('.health-checkbox');
        checkboxes.forEach(cb => cb.checked = false);
        healthTextInput.value = '';
        parseStatus.textContent = '';
      });
    }
  }

  /**
   * Show constraints modal - displays all diseases from database for selection
   * These constraints are used for risk calculation when scanning ingredients
   */
  async function showConstraints() {
    const userId = RiskBiteAPI.getUserId();
    if (!userId) {
      showNotification('Please login to manage constraints', 'error');
      return;
    }

    // Fetch existing health history to get current constraints
    let existingHistory = null;
    let parsedConditions = [];
    try {
      const res = await RiskBiteAPI.getHealthHistory(userId);
      if (res.ok && res.history) {
        existingHistory = res.history;
        parsedConditions = existingHistory.conditions || [];
      }
    } catch (e) {
      console.log('No existing health history');
    }

    // All diseases from the database (from health_parser_service.py)
    const allConditions = [
      // ===== COMMON DISEASES =====
      { id: 'diabetes', label: 'Diabetes', category: 'Diseases', description: 'Blood sugar management' },
      { id: 'cold', label: 'Cold', category: 'Diseases', description: 'Common cold, nasal congestion' },
      { id: 'fever', label: 'Fever', category: 'Diseases', description: 'High temperature, febrile condition' },
      { id: 'hypertension', label: 'High Blood Pressure (Hypertension)', category: 'Diseases', description: 'Elevated blood pressure' },
      { id: 'heart_disease', label: 'Heart Disease', category: 'Diseases', description: 'Cardiac conditions, coronary artery disease' },
      
      // ===== METABOLIC & HORMONAL =====
      { id: 'thyroid', label: 'Thyroid Disorder', category: 'Diseases', description: 'Hypothyroid, hyperthyroid conditions' },
      { id: 'pcos', label: 'PCOS', category: 'Diseases', description: 'Polycystic Ovarian Syndrome' },
      { id: 'obesity', label: 'Obesity', category: 'Diseases', description: 'Weight management concerns' },
      
      // ===== DIGESTIVE =====
      { id: 'ibs', label: 'IBS', category: 'Diseases', description: 'Irritable Bowel Syndrome' },
      { id: 'crohn_disease', label: "Crohn's Disease", category: 'Diseases', description: 'Inflammatory bowel disease' },
      { id: 'gerd', label: 'GERD/Acid Reflux', category: 'Diseases', description: 'Gastroesophageal reflux disease' },
      
      // ===== ALLERGIES =====
      { id: 'peanut_allergy', label: 'Peanut Allergy', category: 'Allergies', description: 'Peanut allergen' },
      { id: 'nut_allergy', label: 'Tree Nut Allergy', category: 'Allergies', description: 'Tree nut allergen (almond, cashew, walnut)' },
      { id: 'shellfish_allergy', label: 'Shellfish Allergy', category: 'Allergies', description: 'Shellfish allergen (shrimp, crab, lobster)' },
      { id: 'gluten_sensitivity', label: 'Gluten Sensitivity/Celiac', category: 'Allergies', description: 'Gluten intolerance, celiac disease' },
      { id: 'lactose_intolerance', label: 'Lactose Intolerance', category: 'Allergies', description: 'Dairy/lactose intolerance' },
      { id: 'egg_allergy', label: 'Egg Allergy', category: 'Allergies', description: 'Egg allergen' },
      { id: 'soy_allergy', label: 'Soy Allergy', category: 'Allergies', description: 'Soy allergen' },
      
      // ===== DIETARY PREFERENCES =====
      { id: 'vegan', label: 'Vegan', category: 'Dietary', description: 'No animal products' },
      { id: 'pescatarian', label: 'Pescatarian', category: 'Dietary', description: 'No meat except fish' },
      { id: 'vegetarian', label: 'Vegetarian', category: 'Dietary', description: 'No meat' },
    ];

    // Group conditions by category
    const categories = {};
    allConditions.forEach(c => {
      if (!categories[c.category]) categories[c.category] = [];
      categories[c.category].push(c);
    });

    // Build checkbox HTML with descriptions
    let checkboxesHtml = '';
    Object.keys(categories).forEach(cat => {
      checkboxesHtml += `<div class="mb-6"><h4 class="font-bold text-sm text-slate-700 mb-3 pb-2 border-b border-slate-200">${cat}</h4><div class="grid grid-cols-1 gap-2">`;
      categories[cat].forEach(c => {
        const isChecked = parsedConditions.includes(c.id) ? 'checked' : '';
        checkboxesHtml += `
          <label class="flex items-start gap-3 text-sm cursor-pointer p-2 rounded-lg hover:bg-slate-50 transition-colors">
            <input type="checkbox" value="${c.id}" ${isChecked} class="constraint-checkbox w-5 h-5 rounded border-gray-300 text-primary focus:ring-primary mt-0.5">
            <div class="flex flex-col">
              <span class="font-medium">${c.label}</span>
              <span class="text-xs text-slate-500">${c.description}</span>
            </div>
          </label>
        `;
      });
      checkboxesHtml += `</div></div>`;
    });

    const modal = createModal(
      'Disease Constraints',
      `
        <div class="space-y-4">
          <div class="bg-blue-50 p-4 rounded-lg border-l-4 border-blue-500">
            <p class="text-sm text-blue-800">
              <span class="font-bold">Select your health conditions:</span> 
              These constraints will be used to calculate personalized risk assessments when scanning product ingredients.
            </p>
          </div>
          
          <!-- Quick Select All by Category -->
          <div class="flex flex-wrap gap-2 mb-4">
            <button id="selectAllDiseases" class="text-xs bg-slate-100 hover:bg-slate-200 px-3 py-1 rounded transition-colors">
              Select All Diseases
            </button>
            <button id="selectAllAllergies" class="text-xs bg-slate-100 hover:bg-slate-200 px-3 py-1 rounded transition-colors">
              Select All Allergies
            </button>
            <button id="selectAllDietary" class="text-xs bg-slate-100 hover:bg-slate-200 px-3 py-1 rounded transition-colors">
              Select All Dietary
            </button>
            <button id="clearAllConstraints" class="text-xs bg-red-50 hover:bg-red-100 text-red-600 px-3 py-1 rounded transition-colors">
              Clear All
            </button>
          </div>

          <!-- Constraints Checkboxes -->
          <div id="constraintsSection" class="max-h-96 overflow-y-auto pr-2">
            ${checkboxesHtml}
          </div>

          <div class="flex gap-2 mt-4 pt-4 border-t">
            <button id="saveConstraintsBtn" class="flex-1 bg-primary text-[#0d1b12] font-bold py-2 px-4 rounded-lg hover:opacity-90">
              Save Constraints
            </button>
          </div>
          
          <p class="text-xs text-gray-500 mt-2">
            Your constraints are saved and automatically used when scanning ingredients for personalized risk assessment.
          </p>
        </div>
      `
    );
    modal.style.display = 'block';

    // Select All Diseases button
    const selectDiseasesBtn = document.getElementById('selectAllDiseases');
    if (selectDiseasesBtn) {
      selectDiseasesBtn.addEventListener('click', function() {
        const checkboxes = document.querySelectorAll('.constraint-checkbox');
        checkboxes.forEach(cb => {
          // Find the condition to check its category
          const condition = allConditions.find(c => c.id === cb.value);
          if (condition && condition.category === 'Diseases') {
            cb.checked = true;
          }
        });
      });
    }

    // Select All Allergies button
    const selectAllergiesBtn = document.getElementById('selectAllAllergies');
    if (selectAllergiesBtn) {
      selectAllergiesBtn.addEventListener('click', function() {
        const checkboxes = document.querySelectorAll('.constraint-checkbox');
        checkboxes.forEach(cb => {
          const condition = allConditions.find(c => c.id === cb.value);
          if (condition && condition.category === 'Allergies') {
            cb.checked = true;
          }
        });
      });
    }

    // Select All Dietary button
    const selectDietaryBtn = document.getElementById('selectAllDietary');
    if (selectDietaryBtn) {
      selectDietaryBtn.addEventListener('click', function() {
        const checkboxes = document.querySelectorAll('.constraint-checkbox');
        checkboxes.forEach(cb => {
          const condition = allConditions.find(c => c.id === cb.value);
          if (condition && condition.category === 'Dietary') {
            cb.checked = true;
          }
        });
      });
    }

    // Clear All button
    const clearAllBtn = document.getElementById('clearAllConstraints');
    if (clearAllBtn) {
      clearAllBtn.addEventListener('click', function() {
        const checkboxes = document.querySelectorAll('.constraint-checkbox');
        checkboxes.forEach(cb => cb.checked = false);
      });
    }

    // Save constraints button handler
    const saveBtn = document.getElementById('saveConstraintsBtn');
    if (saveBtn) {
      saveBtn.addEventListener('click', async function() {
        // Collect checked constraints
        const checkboxes = document.querySelectorAll('.constraint-checkbox:checked');
        const constraints = Array.from(checkboxes).map(cb => cb.value);
        
        const healthData = {
          conditions: constraints,
          updated_at: new Date().toISOString()
        };

        saveBtn.disabled = true;
        saveBtn.textContent = 'Saving...';

        try {
          const result = await RiskBiteAPI.saveHealthHistory(userId, healthData);
          if (result.ok) {
            showNotification('Constraints saved successfully! They will be used in future risk calculations.', 'success');
            // Close modal after short delay
            setTimeout(() => {
              const modal = document.getElementById('modal-overlay');
              if (modal) {
                modal.style.display = 'none';
                setTimeout(() => modal.remove(), 300);
              }
            }, 1000);
          } else {
            showNotification('Failed to save constraints', 'error');
          }
        } catch (e) {
          console.error('Save error:', e);
          showNotification('Error saving constraints', 'error');
        } finally {
          saveBtn.disabled = false;
          saveBtn.textContent = 'Save Constraints';
        }
      });
    }
  }

  /**
   * Show settings modal
   */
  function showSettings() {
    const modal = createModal(
      'Settings',
      `
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-bold mb-2">Account Email</label>
            <input type="email" value="${RiskBiteAPI.getUserEmail()}" disabled class="w-full px-3 py-2 border border-gray-300 rounded-lg bg-gray-100"/>
          </div>
          <div>
            <label class="block text-sm font-bold mb-2">Dark Mode</label>
            <input type="checkbox" id="darkModeToggle" class="w-4 h-4"/>
            <label for="darkModeToggle" class="ml-2">Enable dark mode</label>
          </div>
          <button class="w-full bg-red-500 text-white font-bold py-2 px-4 rounded-lg hover:opacity-90">
            Change Password
          </button>
        </div>
      `
    );
    modal.style.display = 'block';
  }

  /**
   * Show upgrade prompt
   */
  function showUpgradePrompt() {
    const modal = createModal(
      'Upgrade to Pro',
      `
        <div class="space-y-4">
          <div class="bg-gradient-to-r from-primary/20 to-primary/10 p-4 rounded-lg">
            <h3 class="font-bold text-lg text-primary mb-2">Pro Plan Benefits</h3>
            <ul class="space-y-2 text-sm">
              <li>✓ Unlimited scans</li>
              <li>✓ Deep chemical insights</li>
              <li>✓ Priority support</li>
              <li>✓ Advanced health tracking</li>
            </ul>
          </div>
          <button class="w-full bg-primary text-[#0d1b12] font-bold py-3 px-4 rounded-lg hover:opacity-90">
            Upgrade Now - \$9.99/month
          </button>
          <p class="text-xs text-center text-gray-500">7-day free trial. Cancel anytime.</p>
        </div>
      `
    );
    modal.style.display = 'block';
  }

  /**
   * Show notifications
   */
  function showNotifications() {
    const modal = createModal(
      'Notifications',
      `
        <div class="space-y-3">
          <div class="bg-blue-50 p-3 rounded-lg border-l-4 border-blue-500">
            <p class="font-bold text-sm">New ingredient added</p>
            <p class="text-xs text-gray-600">High-risk additive 'Tartrazine' flagged - 2 hours ago</p>
          </div>
          <div class="bg-green-50 p-3 rounded-lg border-l-4 border-green-500">
            <p class="font-bold text-sm">Health milestone</p>
            <p class="text-xs text-gray-600">You've completed 50 scans! - 1 day ago</p>
          </div>
          <div class="bg-yellow-50 p-3 rounded-lg border-l-4 border-yellow-500">
            <p class="font-bold text-sm">Pro trial ending</p>
            <p class="text-xs text-gray-600">Your trial expires in 4 days - upgrade now</p>
          </div>
        </div>
      `
    );
    modal.style.display = 'block';
  }

  /**
   * Toggle filters
   */
  function toggleFilters() {
    showNotification('Filter options will appear here', 'info');
  }

  /**
   * Create a modal dialog
   */
  function createModal(title, content) {
    // Remove existing modal if any
    const existingModal = document.getElementById('modal-overlay');
    if (existingModal) existingModal.remove();

    // Create modal HTML
    const modal = document.createElement('div');
    modal.id = 'modal-overlay';
    modal.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background-color: rgba(0, 0, 0, 0.5);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 10000;
    `;

    const modalContent = document.createElement('div');
    modalContent.style.cssText = `
      background: white;
      border-radius: 12px;
      padding: 24px;
      max-width: 500px;
      width: 90%;
      max-height: 80vh;
      overflow-y: auto;
      box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    `;

    modalContent.innerHTML = `
      <div class="flex justify-between items-center mb-4 pb-4 border-b">
        <h2 class="text-xl font-bold">${title}</h2>
        <button class="text-gray-500 hover:text-gray-700 text-2xl leading-none">×</button>
      </div>
      <div>${content}</div>
    `;

    modal.appendChild(modalContent);

    // Close button
    const closeBtn = modalContent.querySelector('button');
    closeBtn.addEventListener('click', () => {
      modal.style.display = 'none';
      setTimeout(() => modal.remove(), 300);
    });

    // Click outside to close
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        modal.style.display = 'none';
        setTimeout(() => modal.remove(), 300);
      }
    });

    document.body.appendChild(modal);
    return modal;
  }

  /**
   * Show notification message
   */
  function showNotification(message, type = 'info') {
    let notification = document.getElementById('notification');
    if (!notification) {
      notification = document.createElement('div');
      notification.id = 'notification';
      notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 16px 24px;
        border-radius: 8px;
        color: white;
        z-index: 9999;
        font-weight: 600;
      `;
      document.body.appendChild(notification);
    }

    const colors = {
      'success': { bg: '#13ec5b', text: '#0d1b12' },
      'error': { bg: '#ef4444', text: 'white' },
      'info': { bg: '#3b82f6', text: 'white' },
    };

    const color = colors[type] || colors['info'];
    notification.style.backgroundColor = color.bg;
    notification.style.color = color.text;
    notification.textContent = message;
    notification.style.display = 'block';

    setTimeout(() => {
      notification.style.display = 'none';
    }, 5000);
  }
});
