// background.js - Service Worker for Chrome Extension
chrome.runtime.onInstalled.addListener((details) => {
    console.log('🎬 Bollywoodify Extension installed!', details);
    
    // Set default settings
    chrome.storage.local.set({
        extensionEnabled: true,
        installDate: Date.now(),
        version: chrome.runtime.getManifest().version
    });
});

chrome.runtime.onStartup.addListener(() => {
    console.log('🎬 Bollywoodify Extension started!');
});

// Handle extension icon click
chrome.action.onClicked.addListener((tab) => {
    console.log('🎬 Extension icon clicked for tab:', tab.url);
});

// Listen for tab updates to log supported sites
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === 'complete' && tab.url) {
        const supportedSites = [
            'timesofindia.com',
            'hindustantimes.com',
            'ndtv.com',
            'indianexpress.com',
            'indiatimes.com'
        ];
        
        const isSupported = supportedSites.some(site => tab.url.includes(site));
        
        if (isSupported) {
            console.log('🎬 Bollywoodify: Detected supported news site:', tab.url);
            
            // Update badge to show it's active
            chrome.action.setBadgeText({
                text: '🎬',
                tabId: tabId
            });
            
            chrome.action.setBadgeBackgroundColor({
                color: '#FF6B6B',
                tabId: tabId
            });
        }
    }
});

// Handle messages from content script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    console.log('🎬 Background received message:', request);
    
    if (request.type === 'transformation_complete') {
        console.log('✅ Bollywoodify transformation completed on:', sender.tab.url);
        
        // Update stats
        chrome.storage.local.get(['transformationCount'], (result) => {
            const count = (result.transformationCount || 0) + 1;
            chrome.storage.local.set({ transformationCount: count });
        });
    }
    
    if (request.type === 'transformation_error') {
        console.error('❌ Bollywoodify transformation error:', request.error);
    }
    
    sendResponse({ received: true });
});

// Cleanup on extension unload
chrome.runtime.onSuspend.addListener(() => {
    console.log('🎬 Bollywoodify Extension suspending...');
});