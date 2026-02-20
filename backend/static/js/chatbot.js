/**
 * RiskBite AI Nutrientist Chatbot
 * A floating chatbot widget for nutritional advice
 */

(function() {
  'use strict';

  // Chatbot configuration
  const CHATBOT_CONFIG = {
    position: 'bottom-right',
    buttonText: 'your ai nutrientist',
    title: 'AI Nutrientist',
    subtitle: 'Ask me about nutrition',
    welcomeMessage: 'Hello! I\'m your AI Nutrientist. Ask me anything about food ingredients, nutrition, or healthy alternatives!'
  };

  // Simple nutrientist responses (can be enhanced with backend API)
  const responses = {
    'hello': 'Hello! I\'m your AI Nutrientist. How can I help you with your nutrition questions today?',
    'hi': 'Hi there! What would you like to know about food ingredients or nutrition?',
    'hey': 'Hey! I\'m here to help with any nutrition-related questions you might have.',
    'help': 'I can help you understand food ingredients, their health effects, and suggest healthier alternatives. Just ask!',
    'sugar': 'Sugar can be found in many forms in food. Watch out for: sucrose, high fructose corn syrup, maltose, dextrose, and other -ose endings. Natural alternatives include stevia, honey, or maple syrup in moderation.',
    'fat': 'Not all fats are bad! Focus on unsaturated fats (olive oil, nuts, avocado) while limiting saturated and trans fats. Omega-3 fatty acids are particularly beneficial for heart health.',
    'protein': 'Good protein sources include lean meats, fish, eggs, legumes, tofu, and dairy. Plant-based proteins are excellent for overall health.',
    'salt': 'High sodium intake can lead to hypertension. Check labels for sodium, salt, and compounds like monosodium glutamate (MSG). Herbs and spices are great alternatives.',
    'additive': 'Food additives include preservatives, colorings, flavorings, and texturizers. Some are safe while others may cause reactions in sensitive individuals. I can analyze specific ones if you have a product to scan!',
    'preservative': 'Common preservatives include BHA, BHT, sodium benzoate, and potassium sorbate. Some studies suggest potential health concerns with long-term consumption of certain preservatives.',
    'gluten': 'Gluten is a protein found in wheat, barley, and rye. Those with celiac disease or gluten sensitivity should avoid it. Many gluten-free alternatives exist.',
    'allergy': 'Common food allergens include peanuts, tree nuts, milk, eggs, wheat, soy, fish, and shellfish. Always check labels for allergen information.',
    'organic': 'Organic foods are grown without synthetic pesticides or fertilizers. They may have lower pesticide residues but nutritional content is similar to conventionally grown foods.',
    'default': 'That\'s a great question! I can help with information about specific ingredients, nutritional advice, or you can scan a food label with RiskBite for a detailed analysis. What would you like to know more about?'
  };

  let isOpen = false;
  let messageCount = 0;

  /**
   * Initialize the chatbot
   */
  function init() {
    createChatbotHTML();
    attachEventListeners();
  }

  /**
   * Create the chatbot HTML elements
   */
  function createChatbotHTML() {
    const chatbotHTML = `
      <!-- Chatbot Button -->
      <div id="nutrientist-chatbot" class="fixed z-[9998]">
        <button id="chatbot-toggle" class="flex items-center gap-3 px-4 py-3 bg-primary text-[#0d1b12] font-semibold text-sm rounded-full shadow-lg shadow-primary/30 hover:shadow-xl hover:shadow-primary/40 transition-all duration-300 hover:scale-105 cursor-pointer border-2 border-white">
          <span class="material-symbols-outlined text-xl">smart_toy</span>
          <span class="whitespace-nowrap">${CHATBOT_CONFIG.buttonText}</span>
        </button>
        
        <!-- Chat Window -->
        <div id="chatbot-window" class="hidden fixed bottom-20 right-6 w-[350px] max-w-[calc(100vw-48px)] h-[500px] max-h-[calc(100vh-120px)] bg-white rounded-2xl shadow-2xl border border-[#e7f3eb] flex flex-col overflow-hidden animate-slide-up">
          <!-- Header -->
          <div class="bg-primary px-4 py-3 flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-white rounded-full flex items-center justify-center shadow-sm">
                <span class="material-symbols-outlined text-primary text-xl">smart_toy</span>
              </div>
              <div>
                <h3 class="font-bold text-[#0d1b12] text-sm">${CHATBOT_CONFIG.title}</h3>
                <p class="text-xs text-[#0d1b12]/70">${CHATBOT_CONFIG.subtitle}</p>
              </div>
            </div>
            <button id="chatbot-close" class="w-8 h-8 rounded-full hover:bg-white/20 flex items-center justify-center transition-colors">
              <span class="material-symbols-outlined text-[#0d1b12]">close</span>
            </button>
          </div>
          
          <!-- Messages Container -->
          <div id="chatbot-messages" class="flex-1 overflow-y-auto p-4 space-y-4 custom-scrollbar bg-[#f8fcf9]">
            <!-- Welcome message -->
            <div class="flex justify-start">
              <div class="bg-white border border-[#e7f3eb] rounded-2xl rounded-tl-sm px-4 py-2 max-w-[80%] shadow-sm">
                <p class="text-sm text-[#0d1b12]">${CHATBOT_CONFIG.welcomeMessage}</p>
              </div>
            </div>
          </div>
          
          <!-- Input Area -->
          <div class="p-3 bg-white border-t border-[#e7f3eb]">
            <div class="flex items-center gap-2">
              <input 
                type="text" 
                id="chatbot-input" 
                class="flex-1 h-10 px-4 bg-[#f8fcf9] border border-[#e7f3eb] rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent placeholder:text-[#4c9a66]/50"
                placeholder="Type your question..."
              />
              <button id="chatbot-send" class="w-10 h-10 bg-primary rounded-full flex items-center justify-center hover:brightness-110 transition-all shadow-sm shadow-primary/30">
                <span class="material-symbols-outlined text-[#0d1b12]">send</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    `;

    // Insert chatbot HTML before the closing body tag
    document.body.insertAdjacentHTML('beforeend', chatbotHTML);

    // Add custom styles for animation
    addCustomStyles();
  }

  /**
   * Add custom CSS styles
   */
  function addCustomStyles() {
    const style = document.createElement('style');
    style.textContent = `
      @keyframes slide-up {
        from {
          opacity: 0;
          transform: translateY(20px) scale(0.95);
        }
        to {
          opacity: 1;
          transform: translateY(0) scale(1);
        }
      }
      
      .animate-slide-up {
        animation: slide-up 0.3s ease-out forwards;
      }
      
      #chatbot-toggle {
        animation: pulse-glow 2s ease-in-out infinite;
      }
      
      @keyframes pulse-glow {
        0%, 100% {
          box-shadow: 0 4px 15px rgba(19, 236, 91, 0.3);
        }
        50% {
          box-shadow: 0 4px 25px rgba(19, 236, 91, 0.5);
        }
      }
      
      #chatbot-messages .user-message {
        animation: message-in 0.3s ease-out;
      }
      
      @keyframes message-in {
        from {
          opacity: 0;
          transform: translateY(10px);
        }
        to {
          opacity: 1;
          transform: translateY(0);
        }
      }
    `;
    document.head.appendChild(style);
  }

  /**
   * Attach event listeners
   */
  function attachEventListeners() {
    const toggleBtn = document.getElementById('chatbot-toggle');
    const closeBtn = document.getElementById('chatbot-close');
    const sendBtn = document.getElementById('chatbot-send');
    const input = document.getElementById('chatbot-input');

    if (toggleBtn) {
      toggleBtn.addEventListener('click', toggleChat);
    }

    if (closeBtn) {
      closeBtn.addEventListener('click', closeChat);
    }

    if (sendBtn) {
      sendBtn.addEventListener('click', sendMessage);
    }

    if (input) {
      input.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
          sendMessage();
        }
      });
    }
  }

  /**
   * Toggle chat window
   */
  function toggleChat() {
    const window = document.getElementById('chatbot-window');
    const toggleBtn = document.getElementById('chatbot-toggle');
    
    if (isOpen) {
      window.classList.add('hidden');
      toggleBtn.classList.remove('hidden');
    } else {
      window.classList.remove('hidden');
      toggleBtn.classList.add('hidden');
      
      // Focus input when opening
      setTimeout(() => {
        document.getElementById('chatbot-input').focus();
      }, 100);
    }
    
    isOpen = !isOpen;
  }

  /**
   * Close chat window
   */
  function closeChat() {
    const window = document.getElementById('chatbot-window');
    const toggleBtn = document.getElementById('chatbot-toggle');
    
    window.classList.add('hidden');
    toggleBtn.classList.remove('hidden');
    isOpen = false;
  }

  /**
   * Send a message
   */
  function sendMessage() {
    const input = document.getElementById('chatbot-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Add user message
    addMessage(message, 'user');
    input.value = '';
    
    // Show typing indicator
    showTypingIndicator();
    
    // Simulate AI response delay
    setTimeout(() => {
      hideTypingIndicator();
      const response = getResponse(message);
      addMessage(response, 'bot');
    }, 800 + Math.random() * 500);
  }

  /**
   * Add a message to the chat
   */
  function addMessage(text, sender) {
    const container = document.getElementById('chatbot-messages');
    const messageDiv = document.createElement('div');
    
    if (sender === 'user') {
      messageDiv.className = 'flex justify-end';
      messageDiv.innerHTML = `
        <div class="user-message bg-primary text-[#0d1b12] rounded-2xl rounded-tr-sm px-4 py-2 max-w-[80%] shadow-sm">
          <p class="text-sm font-medium">${escapeHtml(text)}</p>
        </div>
      `;
    } else {
      messageDiv.className = 'flex justify-start';
      messageDiv.innerHTML = `
        <div class="bg-white border border-[#e7f3eb] rounded-2xl rounded-tl-sm px-4 py-2 max-w-[80%] shadow-sm">
          <p class="text-sm text-[#0d1b12]">${escapeHtml(text)}</p>
        </div>
      `;
    }
    
    container.appendChild(messageDiv);
    container.scrollTop = container.scrollHeight;
    messageCount++;
  }

  /**
   * Show typing indicator
   */
  function showTypingIndicator() {
    const container = document.getElementById('chatbot-messages');
    const typingDiv = document.createElement('div');
    typingDiv.id = 'chatbot-typing';
    typingDiv.className = 'flex justify-start';
    typingDiv.innerHTML = `
      <div class="bg-white border border-[#e7f3eb] rounded-2xl rounded-tl-sm px-4 py-3 shadow-sm">
        <div class="flex gap-1">
          <span class="w-2 h-2 bg-[#4c9a66] rounded-full animate-bounce" style="animation-delay: 0ms"></span>
          <span class="w-2 h-2 bg-[#4c9a66] rounded-full animate-bounce" style="animation-delay: 150ms"></span>
          <span class="w-2 h-2 bg-[#4c9a66] rounded-full animate-bounce" style="animation-delay: 300ms"></span>
        </div>
      </div>
    `;
    container.appendChild(typingDiv);
    container.scrollTop = container.scrollHeight;
  }

  /**
   * Hide typing indicator
   */
  function hideTypingIndicator() {
    const typing = document.getElementById('chatbot-typing');
    if (typing) {
      typing.remove();
    }
  }

  /**
   * Get response based on user input
   */
  function getResponse(message) {
    const lowerMessage = message.toLowerCase();
    
    // Check for keyword matches
    for (const [keyword, response] of Object.entries(responses)) {
      if (lowerMessage.includes(keyword)) {
        return response;
      }
    }
    
    // Check for common patterns
    if (lowerMessage.includes('?')) {
      // It's a question
      if (lowerMessage.includes('what') || lowerMessage.includes('how') || lowerMessage.includes('why')) {
        return responses.default;
      }
    }
    
    return responses.default;
  }

  /**
   * Escape HTML to prevent XSS
   */
  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
