document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('research-form');
    const input = document.getElementById('company-input');
    const submitBtn = document.getElementById('submit-btn');
    const chatHistory = document.getElementById('chat-history');
    const aiModelSelect = document.getElementById('ai-model');
    const chatContainer = document.getElementById('chat-container');

    // Discord Modal Elements
    const discordBtn = document.getElementById('discord-settings-btn');
    const discordModal = document.getElementById('discord-modal');
    const closeModalBtn = document.getElementById('close-modal-btn');
    const discordForm = document.getElementById('discord-settings-form');

    // Load saved Discord settings
    const savedDiscordSettings = JSON.parse(localStorage.getItem('discordSettings') || '{}');
    if (savedDiscordSettings.applicantName) document.getElementById('discord-applicant-name').value = savedDiscordSettings.applicantName;
    if (savedDiscordSettings.applicantEmail) document.getElementById('discord-applicant-email').value = savedDiscordSettings.applicantEmail;
    if (savedDiscordSettings.botToken) document.getElementById('discord-bot-token').value = savedDiscordSettings.botToken;
    if (savedDiscordSettings.channelId) document.getElementById('discord-channel-id').value = savedDiscordSettings.channelId;

    // Modal toggles
    const openModal = () => {
        discordModal.classList.remove('hidden');
        setTimeout(() => discordModal.classList.remove('opacity-0'), 10);
    };
    const closeModal = () => {
        discordModal.classList.add('opacity-0');
        setTimeout(() => discordModal.classList.add('hidden'), 300);
    };

    discordBtn.addEventListener('click', openModal);
    closeModalBtn.addEventListener('click', closeModal);
    discordModal.addEventListener('click', (e) => {
        if (e.target === discordModal) closeModal();
    });

    discordForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const settings = {
            applicantName: document.getElementById('discord-applicant-name').value,
            applicantEmail: document.getElementById('discord-applicant-email').value,
            botToken: document.getElementById('discord-bot-token').value,
            channelId: document.getElementById('discord-channel-id').value
        };
        localStorage.setItem('discordSettings', JSON.stringify(settings));
        closeModal();
        
        // Show temporary toast or feedback
        const btn = e.target.querySelector('button');
        const originalText = btn.innerText;
        btn.innerText = 'Saved!';
        btn.classList.add('bg-green-600');
        setTimeout(() => {
            btn.innerText = originalText;
            btn.classList.remove('bg-green-600');
        }, 2000);
    });

    function scrollToBottom() {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    function addUserMessage(text) {
        const div = document.createElement('div');
        div.className = 'flex justify-end mb-6 animate-fade-in';
        div.innerHTML = `
            <div class="bg-blue-600 text-white rounded-2xl p-4 shadow-sm border border-blue-500 max-w-2xl">
                <p>${text}</p>
            </div>
        `;
        chatHistory.appendChild(div);
        scrollToBottom();
    }

    function addLoadingMessage() {
        const id = 'msg-' + Date.now();
        const div = document.createElement('div');
        div.className = 'flex gap-4 mb-6 animate-fade-in';
        div.id = id;
        div.innerHTML = `
            <div class="w-10 h-10 rounded-full bg-blue-600 flex-shrink-0 flex items-center justify-center">
                <i class="fa-solid fa-robot text-white text-sm"></i>
            </div>
            <div class="bg-gray-800 rounded-2xl p-4 md:p-5 shadow-sm border border-gray-700/50 flex-1 max-w-3xl">
                <div class="flex items-center gap-2 text-gray-400 text-sm mb-2">
                    <i class="fa-solid fa-circle-notch fa-spin"></i> Researching...
                </div>
                <div class="typing-indicator mt-2">
                    <span></span><span></span><span></span>
                </div>
            </div>
        `;
        chatHistory.appendChild(div);
        scrollToBottom();
        return id;
    }

    function replaceMessageWithReport(id, data) {
        const div = document.getElementById(id);
        if (!div) return;

        let competitorsHtml = '';
        if (data.competitors && data.competitors.length > 0) {
            competitorsHtml = `
                <h3 class="text-white font-semibold mt-4 mb-2"><i class="fa-solid fa-users mr-2 text-blue-400"></i>Competitors</h3>
                <ul class="space-y-2">
                    ${data.competitors.map(c => `
                        <li class="bg-gray-700 rounded-lg p-3 border border-gray-600 flex justify-between items-center">
                            <span class="font-medium text-gray-200">${c.name}</span>
                            <a href="${c.website}" target="_blank" class="text-blue-400 hover:text-blue-300 text-sm truncate max-w-[200px]"><i class="fa-solid fa-arrow-up-right-from-square mr-1"></i>${c.website}</a>
                        </li>
                    `).join('')}
                </ul>
            `;
        } else {
            competitorsHtml = `<p class="text-gray-400 text-sm mt-4 italic">No direct competitors found.</p>`;
        }

        const reportHtml = `
            <div class="w-10 h-10 rounded-full bg-blue-600 flex-shrink-0 flex items-center justify-center">
                <i class="fa-solid fa-robot text-white text-sm"></i>
            </div>
            <div class="bg-gray-800 rounded-2xl p-4 md:p-5 shadow-sm border border-gray-700/50 flex-1 max-w-3xl">
                <div class="flex justify-between items-start mb-4 border-b border-gray-700 pb-4">
                    <div>
                        <h2 class="text-2xl font-bold text-white">${data.companyName || 'Unknown Company'}</h2>
                        <a href="${data.website}" target="_blank" class="text-blue-400 hover:text-blue-300 text-sm"><i class="fa-solid fa-globe mr-1"></i>${data.website || 'No website found'}</a>
                    </div>
                    <button class="download-btn bg-gray-700 hover:bg-gray-600 text-white p-2 rounded-lg text-sm transition-colors border border-gray-600" data-company='${JSON.stringify(data).replace(/'/g, "&#39;")}'>
                        <i class="fa-solid fa-download mr-1"></i> PDF
                    </button>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                    ${data.phoneNumber ? `<div class="bg-gray-700/50 p-3 rounded-lg"><i class="fa-solid fa-phone mr-2 text-gray-400"></i><span class="text-gray-300">${data.phoneNumber}</span></div>` : ''}
                    ${data.address ? `<div class="bg-gray-700/50 p-3 rounded-lg"><i class="fa-solid fa-location-dot mr-2 text-gray-400"></i><span class="text-gray-300">${data.address}</span></div>` : ''}
                </div>

                <div class="space-y-4">
                    <div>
                        <h3 class="text-white font-semibold mb-2"><i class="fa-solid fa-cube mr-2 text-blue-400"></i>Products & Services</h3>
                        <p class="text-gray-300 text-sm leading-relaxed">${data.productsServices || 'Not available.'}</p>
                    </div>
                    <div>
                        <h3 class="text-white font-semibold mb-2"><i class="fa-solid fa-bolt mr-2 text-blue-400"></i>AI-Generated Pain Points</h3>
                        <p class="text-gray-300 text-sm leading-relaxed">${data.painPoints || 'Not available.'}</p>
                    </div>
                    ${competitorsHtml}
                </div>
            </div>
        `;
        
        div.innerHTML = reportHtml;
        
        // Attach download event
        const downloadBtn = div.querySelector('.download-btn');
        if (downloadBtn) {
            downloadBtn.addEventListener('click', async () => {
                downloadBtn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin mr-1"></i> Generating...';
                downloadBtn.disabled = true;
                
                try {
                    const response = await fetch('/api/pdf', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(data)
                    });
                    
                    const result = await response.json();
                    if (result.success) {
                        // In a real app, this would return a blob or url to download
                        // Since it's a demo, we might trigger a virtual download or redirect
                        window.location.href = result.pdfUrl;
                        
                        // Check if we need to send to Discord
                        const ds = JSON.parse(localStorage.getItem('discordSettings') || '{}');
                        if (ds.botToken && ds.channelId) {
                            // Send discord notification in background
                            fetch('/api/discord', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({
                                    reportData: data,
                                    pdfUrl: result.pdfUrl,
                                    settings: ds
                                })
                            }).catch(e => console.error("Discord error:", e));
                        }
                    } else {
                        alert('Error generating PDF');
                    }
                } catch (err) {
                    alert('Error generating PDF');
                } finally {
                    downloadBtn.innerHTML = '<i class="fa-solid fa-download mr-1"></i> PDF';
                    downloadBtn.disabled = false;
                }
            });
        }
        scrollToBottom();
    }

    function addErrorMessage(id, errorText) {
        const div = document.getElementById(id);
        if (!div) return;
        div.innerHTML = `
            <div class="w-10 h-10 rounded-full bg-red-600 flex-shrink-0 flex items-center justify-center">
                <i class="fa-solid fa-exclamation text-white text-sm"></i>
            </div>
            <div class="bg-gray-800 rounded-2xl p-4 md:p-5 shadow-sm border border-red-500/50 flex-1 text-red-400">
                <p><strong>Error:</strong> ${errorText}</p>
            </div>
        `;
        scrollToBottom();
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const companyInput = input.value.trim();
        if (!companyInput) return;

        const aiModel = aiModelSelect.value;
        
        addUserMessage(companyInput);
        input.value = '';
        input.disabled = true;
        submitBtn.disabled = true;

        const msgId = addLoadingMessage();

        try {
            const response = await fetch('/api/research', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ companyInput, aiModel })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                replaceMessageWithReport(msgId, data);
            } else {
                addErrorMessage(msgId, data.error || 'Failed to fetch research data.');
            }
        } catch (error) {
            addErrorMessage(msgId, 'Network error occurred. Please try again.');
        } finally {
            input.disabled = false;
            submitBtn.disabled = false;
            input.focus();
        }
    });
});
