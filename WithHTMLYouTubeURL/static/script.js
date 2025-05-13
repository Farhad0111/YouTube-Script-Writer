// Handle form toggling between regular and channel-based script generation
document.addEventListener('DOMContentLoaded', function() {
    const regularForm = document.getElementById('regular-form');
    const channelForm = document.getElementById('channel-form');
    const formToggle = document.getElementById('form-toggle');
    const loadingSpinner = document.getElementById('loading-spinner');
    const channelIdInput = document.getElementById('channel-id');
    const channelInfoSection = document.getElementById('channel-info');
    const detectedTone = document.getElementById('detected-tone');
    
    // Toggle between forms
    if (formToggle) {
        formToggle.addEventListener('change', function() {
            if (this.checked) {
                regularForm.classList.add('hidden');
                channelForm.classList.remove('hidden');
            } else {
                regularForm.classList.remove('hidden');
                channelForm.classList.add('hidden');
            }
        });
    }
    
    // Channel form submission
    if (channelForm) {
        channelForm.addEventListener('submit', function() {
            loadingSpinner.classList.remove('hidden');
        });
    }
    
    // Regular form submission
    if (regularForm) {
        regularForm.addEventListener('submit', function() {
            loadingSpinner.classList.remove('hidden');
        });
    }
    
    // Channel lookup function
    if (channelIdInput) {
        channelIdInput.addEventListener('blur', async function() {
            if (this.value.trim().length > 0) {
                try {
                    loadingSpinner.classList.remove('hidden');
                    const response = await fetch(`/api/channel-info/${encodeURIComponent(this.value.trim())}`);
                    
                    if (response.ok) {
                        const data = await response.json();
                        // Update channel info display
                        detectedTone.textContent = data.tones.primary;
                        
                        // Display channel info 
                        channelInfoSection.innerHTML = `
                            <div class="channel-preview">
                                <h3>${data.channel.title}</h3>
                                <p><strong>Subscribers:</strong> ${data.channel.subscribers.toLocaleString()}</p>
                                <p><strong>Videos:</strong> ${data.channel.videos}</p>
                                <div class="tone-info">
                                    <p><strong>Primary Tone:</strong> ${data.tones.primary}</p>
                                    <p><strong>Secondary Tones:</strong> ${data.tones.secondary.join(', ')}</p>
                                </div>
                            </div>
                        `;
                        channelInfoSection.classList.remove('hidden');
                    } else {
                        const errorData = await response.json();
                        channelInfoSection.innerHTML = `<p class="error">${errorData.detail || 'Error fetching channel info'}</p>`;
                        channelInfoSection.classList.remove('hidden');
                    }
                } catch (error) {
                    console.error('Error:', error);
                    channelInfoSection.innerHTML = `<p class="error">Error connecting to server</p>`;
                    channelInfoSection.classList.remove('hidden');
                } finally {
                    loadingSpinner.classList.add('hidden');
                }
            }
        });
    }
    
    // Copy button for script
    const copyButton = document.getElementById('copy-script');
    if (copyButton) {
        copyButton.addEventListener('click', function() {
            const scriptContent = document.getElementById('script-content');
            if (scriptContent) {
                navigator.clipboard.writeText(scriptContent.textContent)
                    .then(() => {
                        this.textContent = 'Copied!';
                        setTimeout(() => {
                            this.textContent = 'Copy Script';
                        }, 2000);
                    })
                    .catch(err => {
                        console.error('Failed to copy: ', err);
                    });
            }
        });
    }
});