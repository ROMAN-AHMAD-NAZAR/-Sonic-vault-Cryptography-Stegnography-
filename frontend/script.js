/**
 * SonicVault - Frontend JavaScript
 * Interactive functionality for the web interface
 */

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', () => {
    initParticles();
    initTabs();
    initEncode();
    initDecode();
    initKeyGeneration();
    initThemeCards();
    initNavbar();
    initMobileMenu();
});

/**
 * Create floating particles in background
 */
function initParticles() {
    const container = document.getElementById('particles');
    const particleCount = 30;
    
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        particle.style.animationDelay = Math.random() * 15 + 's';
        particle.style.animationDuration = (10 + Math.random() * 20) + 's';
        container.appendChild(particle);
    }
}

/**
 * Initialize tab switching functionality
 */
function initTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const panels = document.querySelectorAll('.demo-panel');
    
    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabName = btn.dataset.tab;
            
            // Update active tab button
            tabButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            // Update active panel
            panels.forEach(panel => {
                panel.classList.remove('active');
                if (panel.id === `${tabName}-panel`) {
                    panel.classList.add('active');
                }
            });
        });
    });
}

/**
 * Initialize encode functionality
 */
function initEncode() {
    const encodeBtn = document.getElementById('encodeBtn');
    const messageInput = document.getElementById('encodeMessage');
    const passwordInput = document.getElementById('encodePassword');
    const themeSelect = document.getElementById('encodeTheme');
    const signatureCheckbox = document.getElementById('addSignature');
    const outputDiv = document.getElementById('encodeOutput');
    
    encodeBtn.addEventListener('click', () => {
        const message = messageInput.value.trim();
        const password = passwordInput.value;
        const theme = themeSelect.value;
        const addSignature = signatureCheckbox.checked;
        
        // Validation
        if (!message) {
            showOutput(outputDiv, 'error', 'Please enter a message to encode.');
            return;
        }
        
        if (!password) {
            showOutput(outputDiv, 'error', 'Please enter an encryption password.');
            return;
        }
        
        if (password.length < 8) {
            showOutput(outputDiv, 'error', 'Password must be at least 8 characters long.');
            return;
        }
        
        // Simulate encoding process
        showOutput(outputDiv, 'loading', 'Encoding message...');
        
        setTimeout(() => {
            const result = simulateEncode(message, password, theme, addSignature);
            showOutput(outputDiv, 'success', result);
        }, 1500);
    });
}

/**
 * Simulate encoding process
 */
function simulateEncode(message, password, theme, addSignature) {
    const themeNames = {
        'sine': 'Sine Wave',
        'rain': 'Rain Drops',
        'birds': 'Bird Chirps',
        'synth': 'Synth Tones',
        'digital': 'Digital Beeps'
    };
    
    const encodedLength = Math.ceil(message.length * 0.5 + 2);
    
    return `
        <div class="encode-result">
            <div class="result-header">
                <i class="fas fa-check-circle"></i>
                <h4>Message Encoded Successfully!</h4>
            </div>
            <div class="result-details">
                <div class="detail-item">
                    <span class="detail-label">Audio Theme:</span>
                    <span class="detail-value">${themeNames[theme]}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Encryption:</span>
                    <span class="detail-value">AES-256-GCM</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Digital Signature:</span>
                    <span class="detail-value">${addSignature ? 'Yes (DSA)' : 'No'}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Audio Duration:</span>
                    <span class="detail-value">~${encodedLength} seconds</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Message Length:</span>
                    <span class="detail-value">${message.length} characters</span>
                </div>
            </div>
            <div class="result-cli">
                <p><i class="fas fa-terminal"></i> Run locally for actual audio file:</p>
                <code>python cli.py encode "${message.substring(0, 30)}${message.length > 30 ? '...' : ''}" output.wav --password YOUR_PASSWORD --theme ${theme}${addSignature ? ' --sign' : ''}</code>
            </div>
        </div>
    `;
}

/**
 * Initialize decode functionality
 */
function initDecode() {
    const decodeBtn = document.getElementById('decodeBtn');
    const fileInput = document.getElementById('decodeFile');
    const passwordInput = document.getElementById('decodePassword');
    const outputDiv = document.getElementById('decodeOutput');
    const fileLabel = document.querySelector('.file-upload-label span');
    
    // Update label when file is selected
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            fileLabel.textContent = e.target.files[0].name;
        } else {
            fileLabel.textContent = 'Drop audio file here or click to browse';
        }
    });
    
    decodeBtn.addEventListener('click', () => {
        const file = fileInput.files[0];
        const password = passwordInput.value;
        
        // Validation
        if (!file) {
            showOutput(outputDiv, 'error', 'Please select an audio file to decode.');
            return;
        }
        
        if (!password) {
            showOutput(outputDiv, 'error', 'Please enter the decryption password.');
            return;
        }
        
        // Simulate decoding process
        showOutput(outputDiv, 'loading', 'Decoding audio...');
        
        setTimeout(() => {
            const result = simulateDecode(file.name, password);
            showOutput(outputDiv, 'success', result);
        }, 2000);
    });
}

/**
 * Simulate decoding process
 */
function simulateDecode(filename, password) {
    return `
        <div class="decode-result">
            <div class="result-header">
                <i class="fas fa-unlock"></i>
                <h4>Audio Analysis Complete</h4>
            </div>
            <div class="result-details">
                <div class="detail-item">
                    <span class="detail-label">File:</span>
                    <span class="detail-value">${filename}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Status:</span>
                    <span class="detail-value">Demo Mode</span>
                </div>
            </div>
            <div class="result-note">
                <i class="fas fa-info-circle"></i>
                <p>To decode actual messages, run the Python CLI locally:</p>
            </div>
            <div class="result-cli">
                <code>python cli.py decode ${filename} --password YOUR_PASSWORD</code>
            </div>
        </div>
    `;
}

/**
 * Initialize key generation functionality
 */
function initKeyGeneration() {
    const generateBtn = document.getElementById('generateKeysBtn');
    const keyNameInput = document.getElementById('keyName');
    const keyPasswordInput = document.getElementById('keyPassword');
    const outputDiv = document.getElementById('keysOutput');
    
    generateBtn.addEventListener('click', () => {
        const keyName = keyNameInput.value.trim() || 'sonic_vault_keys';
        const keyPassword = keyPasswordInput.value;
        
        // Simulate key generation
        showOutput(outputDiv, 'loading', 'Generating key pair...');
        
        setTimeout(() => {
            const result = simulateKeyGeneration(keyName, keyPassword);
            showOutput(outputDiv, 'success', result);
        }, 1500);
    });
}

/**
 * Simulate key generation process
 */
function simulateKeyGeneration(keyName, keyPassword) {
    return `
        <div class="keys-result">
            <div class="result-header">
                <i class="fas fa-key"></i>
                <h4>Key Pair Generated!</h4>
            </div>
            <div class="result-details">
                <div class="detail-item">
                    <span class="detail-label">Private Key:</span>
                    <span class="detail-value">${keyName}_private.pem</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Public Key:</span>
                    <span class="detail-value">${keyName}_public.pem</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Algorithm:</span>
                    <span class="detail-value">DSA (2048-bit)</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Password Protected:</span>
                    <span class="detail-value">${keyPassword ? 'Yes' : 'No'}</span>
                </div>
            </div>
            <div class="result-warning">
                <i class="fas fa-exclamation-triangle"></i>
                <p><strong>Important:</strong> Never share your private key!</p>
            </div>
            <div class="result-cli">
                <p><i class="fas fa-terminal"></i> Generate real keys locally:</p>
                <code>python cli.py generate-keys --output ${keyName}${keyPassword ? ' --password YOUR_PASSWORD' : ''}</code>
            </div>
        </div>
    `;
}

/**
 * Show output in panel
 */
function showOutput(container, type, content) {
    const styles = `
        <style>
            .encode-result, .decode-result, .keys-result {
                text-align: left;
                width: 100%;
            }
            .result-header {
                display: flex;
                align-items: center;
                gap: 12px;
                margin-bottom: 20px;
                color: #FF6D1F;
            }
            .result-header i {
                font-size: 1.5rem;
            }
            .result-header h4 {
                font-size: 1.1rem;
                margin: 0;
            }
            .result-details {
                background: rgba(255, 109, 31, 0.15);
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 15px;
            }
            .detail-item {
                display: flex;
                justify-content: space-between;
                padding: 8px 0;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }
            .detail-item:last-child {
                border-bottom: none;
            }
            .detail-label {
                color: #94a3b8;
            }
            .detail-value {
                color: #f8fafc;
                font-weight: 500;
            }
            .result-cli {
                background: #000;
                border-radius: 8px;
                padding: 15px;
                margin-top: 15px;
            }
            .result-cli p {
                color: #94a3b8;
                font-size: 0.875rem;
                margin-bottom: 10px;
                display: flex;
                align-items: center;
                gap: 8px;
            }
            .result-cli code {
                display: block;
                color: #FF6D1F;
                font-family: 'Fira Code', monospace;
                font-size: 0.85rem;
                word-break: break-all;
            }
            .result-note, .result-warning {
                display: flex;
                align-items: flex-start;
                gap: 10px;
                padding: 12px;
                border-radius: 8px;
                margin-top: 15px;
            }
            .result-note {
                background: rgba(255, 109, 31, 0.15);
                color: #ff8a4c;
            }
            .result-warning {
                background: rgba(245, 158, 11, 0.1);
                color: #f59e0b;
            }
            .result-note p, .result-warning p {
                margin: 0;
                font-size: 0.9rem;
            }
            .loading-spinner {
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 15px;
                color: #94a3b8;
            }
            .spinner {
                width: 40px;
                height: 40px;
                border: 3px solid rgba(255, 109, 31, 0.2);
                border-top-color: #FF6D1F;
                border-radius: 50%;
                animation: spin 1s linear infinite;
            }
            @keyframes spin {
                to { transform: rotate(360deg); }
            }
            .error-message {
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 10px;
                color: #ef4444;
                text-align: center;
            }
            .error-message i {
                font-size: 2rem;
            }
        </style>
    `;
    
    if (type === 'loading') {
        container.innerHTML = styles + `
            <div class="loading-spinner">
                <div class="spinner"></div>
                <p>${content}</p>
            </div>
        `;
    } else if (type === 'error') {
        container.innerHTML = styles + `
            <div class="error-message">
                <i class="fas fa-exclamation-circle"></i>
                <p>${content}</p>
            </div>
        `;
    } else {
        container.innerHTML = styles + content;
    }
}

/**
 * Initialize theme card interactions
 */
function initThemeCards() {
    const themeCards = document.querySelectorAll('.theme-card');
    
    themeCards.forEach(card => {
        card.addEventListener('click', () => {
            const theme = card.dataset.theme;
            
            // Switch to encode tab and select theme
            document.querySelector('[data-tab="encode"]').click();
            document.getElementById('encodeTheme').value = theme;
            
            // Scroll to demo section
            document.getElementById('demo').scrollIntoView({ behavior: 'smooth' });
        });
    });
}

/**
 * Initialize navbar scroll effect
 */
function initNavbar() {
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(42, 37, 32, 0.98)';
            navbar.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.2)';
        } else {
            navbar.style.background = 'rgba(42, 37, 32, 0.9)';
            navbar.style.boxShadow = 'none';
        }
    });
}

/**
 * Initialize mobile menu
 */
function initMobileMenu() {
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const navLinks = document.querySelector('.nav-links');
    
    mobileMenuBtn.addEventListener('click', () => {
        navLinks.classList.toggle('show');
    });
    
    // Close menu when clicking a link
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('show');
        });
    });
}

/**
 * Copy code to clipboard
 */
function copyCode(btn) {
    const codeBlock = btn.closest('.code-block');
    const code = codeBlock.querySelector('code').innerText;
    
    navigator.clipboard.writeText(code).then(() => {
        const originalIcon = btn.innerHTML;
        btn.innerHTML = '<i class="fas fa-check"></i>';
        btn.style.color = '#FF6D1F';
        
        setTimeout(() => {
            btn.innerHTML = originalIcon;
            btn.style.color = '';
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy:', err);
    });
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});
