/**
 * Scan Results Page Interactions
 * Displays analysis results, handles actions, and manages re-scans
 */

document.addEventListener('DOMContentLoaded', function() {
  console.log('Scan results page initialized');

  // Check if user is logged in
  if (!RiskBiteAPI.isLoggedIn()) {
    window.location.href = '/login';
    return;
  }

  // Display pending file if exists from landing page
  const pendingFile = sessionStorage.getItem('pendingFile');
  const pendingFileName = sessionStorage.getItem('pendingFileName');
  
  if (pendingFile && pendingFileName) {
    performPendingScan(pendingFile, pendingFileName);
    sessionStorage.removeItem('pendingFile');
    sessionStorage.removeItem('pendingFileName');
  } else {
    // Load scan result from session storage
    loadScanResult();
  }

  // Setup button handlers
  setupButtonHandlers();

  /**
   * Load and display scan result from session storage
   */
  function loadScanResult() {
    const resultJson = sessionStorage.getItem('scanResult');
    
    if (!resultJson) {
      showNotification('No scan results found. Redirecting...', 'error');
      setTimeout(() => window.location.href = '/landing', 2000);
      return;
    }

    const result = JSON.parse(resultJson);
    displayScanResult(result);
  }

  /**
   * Display scan results on the page
   */
  function displayScanResult(result) {
    // Update title with product name
    const title = document.querySelector('h1');
    if (title) {
      title.textContent = `Results: ${sessionStorage.getItem('scanImageName') || 'Product Scan'}`;
    }

    // Update scan date
    const dateElement = document.querySelector('p.flex.text-sm');
    if (dateElement) {
      const now = new Date().toLocaleString();
      dateElement.childNodes[1].textContent = ` Scanned on ${now}`;
    }

    // Update safety score
    const riskScore = result.risk_score || 0;
    const riskLevel = result.risk_level || 'MODERATE';
    displayRiskScore(riskScore, riskLevel);

    // Display ingredients
    displayIngredients(result.ingredients, result.explanations);

    // Display warnings
    displayWarnings(result.warnings);

    // Display summary
    if (result.summary) {
      displaySummary(result.summary);
    }
  }

  /**
   * Display risk/safety score
   */
  function displayRiskScore(score, riskLevel) {
    const scoreDisplay = document.querySelector('.w-24.h-24.rounded-full');
    if (scoreDisplay) {
      scoreDisplay.querySelector('span').textContent = Math.round(score);
    }

    // Update risk level indicator color
    const riskColorMap = {
      'LOW': { bg: '#13ec5b', text: 'green' },
      'MODERATE': { bg: '#eab308', text: 'yellow' },
      'HIGH': { bg: '#ef4444', text: 'red' },
    };

    const riskInfo = riskColorMap[riskLevel] || riskColorMap['MODERATE'];
    const colorElements = document.querySelectorAll('[style*="border-"]');
    colorElements.forEach(el => {
      el.style.borderColor = riskInfo.bg;
    });
  }

  /**
   * Display ingredients list
   */
  function displayIngredients(ingredients, explanations = {}) {
    const container = document.querySelector('[class*="grid"]');
    if (!container) return;

    // Create ingredients section
    let ingredientsHTML = '<div class="mb-8"><h3 class="font-bold text-lg mb-4">Ingredients Found</h3><div class="grid grid-cols-1 md:grid-cols-2 gap-4">';
    
    if (ingredients && Array.isArray(ingredients)) {
      ingredients.forEach(ingredient => {
        const explanation = explanations[ingredient] || 'No details available';
        ingredientsHTML += `
          <div class="bg-white rounded-lg border border-[#cfe7d7] p-4 hover:shadow-md transition-shadow">
            <h4 class="font-bold text-[#0d1b12]">${ingredient}</h4>
            <p class="text-sm text-[#4c9a66] mt-2">${explanation}</p>
          </div>
        `;
      });
    }
    
    ingredientsHTML += '</div></div>';
    container.innerHTML = ingredientsHTML;
  }

  /**
   * Display warnings in the prominent warnings section
   */
  function displayWarnings(warnings) {
    const warningsSection = document.getElementById('warningsSection');
    const warningsContainer = document.getElementById('warningsContainer');
    const warningCountBadge = document.getElementById('warningCountBadge');
    
    if (!warningsSection || !warningsContainer) return;
    
    // Check if there are warnings
    if (!warnings || warnings.length === 0) {
      warningsSection.style.display = 'none';
      return;
    }
    
    // Show the warnings section
    warningsSection.style.display = 'block';
    
    // Update warning count badge
    warningCountBadge.textContent = warnings.length;
    
    // Build warning cards
    let warningsHTML = '';
    
    warnings.forEach(warning => {
      // Determine severity based on risk level
      const isHighRisk = warning.risk_level === 'high';
      const borderColor = isHighRisk ? 'border-red-500' : 'border-yellow-500';
      const bgColor = isHighRisk ? 'bg-red-50' : 'bg-yellow-50';
      const textColor = isHighRisk ? 'text-red-700' : 'text-yellow-700';
      const iconColor = isHighRisk ? 'text-red-500' : 'text-yellow-500';
      
      warningsHTML += `
        <div class="${bgColor} border-l-4 ${borderColor} rounded-lg p-4 shadow-md hover:shadow-lg transition-shadow">
          <div class="flex items-start justify-between mb-2">
            <h4 class="font-bold text-lg ${textColor} flex items-center gap-2">
              <span class="material-symbols-outlined ${iconColor}">dangerous</span>
              ${warning.ingredient}
            </h4>
            <span class="bg-${isHighRisk ? 'red' : 'yellow'}-500 text-white text-xs font-bold px-2 py-1 rounded-full uppercase">
              ${warning.risk_level || 'Medium'} Risk
            </span>
          </div>
          
          <div class="mt-3">
            <p class="text-xs font-bold text-gray-500 uppercase tracking-wide mb-1">⚠️ Why It's Dangerous For You:</p>
            <p class="text-sm ${textColor} leading-relaxed">${warning.reason}</p>
          </div>
          
          <div class="mt-3 pt-3 border-t border-gray-200">
            <p class="text-xs font-bold text-green-600 uppercase tracking-wide mb-1">✅ Healthy Alternative:</p>
            <p class="text-sm text-green-700 font-medium flex items-center gap-2">
              <span class="material-symbols-outlined text-green-600">recommend</span>
              ${warning.alternative || 'N/A'}
            </p>
          </div>
        </div>
      `;
    });
    
    warningsContainer.innerHTML = warningsHTML;
  }

  /**
   * Display summary
   */
  function displaySummary(summary) {
    const container = document.querySelector('[class*="grid"]');
    if (!container) return;

    const summaryHTML = `
      <div class="mb-8 bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
        <h3 class="font-bold text-lg text-blue-700 mb-2">Summary</h3>
        <p class="text-sm text-blue-600">${summary}</p>
      </div>
    `;
    
    container.innerHTML += summaryHTML;
  }

  /**
   * Setup button event handlers
   */
  function setupButtonHandlers() {
    // Share button
    const shareButton = document.querySelector('button[onclick*="mailto"]') || 
                       document.querySelector('button[onclick*="share"]');
    if (shareButton) {
      shareButton.addEventListener('click', function(e) {
        if (!this.onclick) {
          e.preventDefault();
          handleShare();
        }
      });
    }

    // PDF Download button
    const pdfButton = document.querySelector('a[onclick*="PDF"]') || 
                     document.querySelector('button[onclick*="PDF"]');
    if (pdfButton) {
      pdfButton.addEventListener('click', function(e) {
        e.preventDefault();
        handlePDFDownload();
      });
    }

    // Re-scan button
    const rescanButton = document.querySelector('button[onclick*="rescan"]') || 
                        document.querySelector('button[title*="Scan another"]');
    if (rescanButton) {
      rescanButton.addEventListener('click', function(e) {
        e.preventDefault();
        document.getElementById('rescanFileInput').click();
      });
    }

    // Re-scan file input
    const rescanInput = document.getElementById('rescanFileInput');
    if (rescanInput) {
      rescanInput.addEventListener('change', handleRescan);
    }

    // Logout button
    const logoutButton = document.querySelector('a[href*="logout"]');
    if (logoutButton) {
      logoutButton.addEventListener('click', function(e) {
        e.preventDefault();
        if (confirm('Are you sure you want to logout?')) {
          RiskBiteAPI.logout();
          window.location.href = '/login';
        }
      });
    }

    // Navigation links
    const dashboardLink = document.querySelector('a[href*="dashboard"]');
    if (dashboardLink) {
      dashboardLink.addEventListener('click', function(e) {
        e.preventDefault();
        window.location.href = '/dashboard';
      });
    }
  }

  /**
   * Handle share button click
   */
  function handleShare() {
    const scanImageName = sessionStorage.getItem('scanImageName') || 'Food Analysis';
    
    // Create shareable text
    const text = `Check out my RiskBite analysis for ${scanImageName} - Know what's inside your food!`;
    
    if (navigator.share) {
      navigator.share({
        title: 'RiskBite Analysis Report',
        text: text,
        url: window.location.href
      }).catch(err => console.log('Share cancelled:', err));
    } else {
      // Fallback: copy to clipboard
      const shareUrl = `${window.location.origin}/scan-results`;
      navigator.clipboard.writeText(`${text}\n${shareUrl}`);
      showNotification('Report link copied to clipboard!', 'success');
    }
  }

  /**
   * Handle PDF download
   */
  function handlePDFDownload() {
    const result = JSON.parse(sessionStorage.getItem('scanResult'));
    const scanImageName = sessionStorage.getItem('scanImageName') || 'Product Scan';

    // Create a simple PDF representation
    const content = `
RiskBite Analysis Report
========================
Product: ${scanImageName}
Date: ${new Date().toLocaleString()}
Risk Level: ${result.risk_level}
Risk Score: ${Math.round(result.risk_score)}%

Ingredients Found:
${result.ingredients.join(', ')}

Warnings:
${result.warnings.map(w => `- ${w.ingredient}: ${w.reason}`).join('\n')}

Summary:
${result.summary}
    `;

    // Create blob and download
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `riskbite-${Date.now()}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    showNotification('Report downloaded!', 'success');
  }

  /**
   * Handle re-scan
   */
  async function handleRescan(e) {
    const files = e.target.files;
    if (files && files.length > 0) {
      processFile(files[0]);
    }
  }

  /**
   * Process file for re-scan
   */
  async function processFile(file) {
    if (!file.type.startsWith('image/') && file.type !== 'application/pdf') {
      showNotification('Please upload an image or PDF file', 'error');
      return;
    }

    try {
      showNotification('Processing new scan...', 'info');
      
      const userId = RiskBiteAPI.getUserId();
      let userConditions = [];

      try {
        const healthHistory = await RiskBiteAPI.getHealthHistory(userId);
        if (healthHistory.ok && healthHistory.history && healthHistory.history.conditions) {
          userConditions = healthHistory.history.conditions;
        }
      } catch (e) {
        console.log('Could not retrieve health history');
      }

      const scanResult = await RiskBiteAPI.scanProduct(file, userConditions, userId);
      sessionStorage.setItem('scanResult', JSON.stringify(scanResult));
      sessionStorage.setItem('scanImageName', file.name);
      
      showNotification('Scan complete!', 'success');
      setTimeout(() => location.reload(), 1000);

    } catch (error) {
      showNotification('Scan failed: ' + error.message, 'error');
    }
  }

  /**
   * Perform pending scan from landing page
   */
  async function performPendingScan(dataUrl, fileName) {
    try {
      showNotification('Processing pending scan...', 'info');
      
      // Convert data URL to file
      const arr = dataUrl.split(',');
      const mime = arr[0].match(/:(.*?);/)[1];
      const bstr = atob(arr[1]);
      const n = bstr.length;
      const u8arr = new Uint8Array(n);
      for (let i = 0; i < n; i++) {
        u8arr[i] = bstr.charCodeAt(i);
      }
      const file = new File([u8arr], fileName, { type: mime });

      const userId = RiskBiteAPI.getUserId();
      const scanResult = await RiskBiteAPI.scanProduct(file, [], userId);
      
      sessionStorage.setItem('scanResult', JSON.stringify(scanResult));
      sessionStorage.setItem('scanImageName', fileName);
      
      displayScanResult(scanResult);
      showNotification('Scan complete!', 'success');

    } catch (error) {
      showNotification('Scan failed: ' + error.message, 'error');
    }
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
