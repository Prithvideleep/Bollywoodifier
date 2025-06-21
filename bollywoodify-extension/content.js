// content.js - Enhanced version with better error handling
(function() {
    'use strict';

    const API_BASE_URL = 'http://localhost:5000';
    let isProcessing = false;
    const transformedArticles = new Set();

    // Enhanced site selectors
    const siteSelectors = {
        'hindustantimes.com': {
            title: 'h1, .hdg1, .headline',
            content: '.detail p, .story-details p, p',
            article: '.detail, .story-details, .article-content',
            avoid: '.ad-container, .recommended-articles' // Elements to avoid
        },
        // Add other sites similarly...
    };

    function getCurrentSite() {
        return Object.keys(siteSelectors).find(site => 
            window.location.hostname.includes(site)
        );
    }

    function extractArticleData() {
        const site = getCurrentSite();
        if (!site) return null;

        const { title: titleSelector, content: contentSelector, article: articleSelector, avoid } = siteSelectors[site];
        
        // Get article elements
        const titleElement = document.querySelector(titleSelector);
        const contentElements = [...document.querySelectorAll(contentSelector)];
        const articleElement = document.querySelector(articleSelector) || document.body;

        // Filter out unwanted elements
        if (avoid) {
            document.querySelectorAll(avoid).forEach(el => {
                contentElements = contentElements.filter(ce => !el.contains(ce));
            });
        }

        // Extract and clean content
        const title = titleElement?.textContent.trim() || '';
        let content = contentElements
            .map(el => el.textContent.trim())
            .filter(text => text.length > 30) // Filter short paragraphs
            .join('\n\n')
            .substring(0, 2000); // Limit content length

        return {
            title,
            content,
            titleElement,
            articleElement
        };
    }

    async function transformArticle() {
        if (isProcessing) return;
        isProcessing = true;

        const articleData = extractArticleData();
        if (!articleData?.title || !articleData.content) {
            console.log('Could not extract article data');
            isProcessing = false;
            return;
        }

        // Create loading indicator
        const loadingDiv = document.createElement('div');
        loadingDiv.innerHTML = `
            <div style="padding: 20px; background: #FF6B6B; color: white; margin: 10px 0; border-radius: 5px;">
                🎬 Transforming into Bollywood magic... Please wait!
            </div>
        `;
        articleData.articleElement.prepend(loadingDiv);

        try {
            const response = await fetch(`${API_BASE_URL}/bollywoodify`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    title: articleData.title,
                    content: articleData.content
                })
            });

            if (!response.ok) throw new Error(`API Error: ${response.status}`);
            
            const result = await response.json();
            
            // Create Bollywood content
            const bollywoodContent = document.createElement('div');
            bollywoodContent.innerHTML = `
                <div style="background: linear-gradient(135deg, #FF6B6B, #4ECDC4); padding: 30px; margin: 20px 0; border-radius: 15px; color: white;">
                    <h1 style="color: gold; text-align: center;">🎬 ${result.movie_title} 🎬</h1>
                    <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin-top: 15px;">
                        <h3 style="color: gold;">🎵 The Song 🎵</h3>
                        <div style="white-space: pre-line;">${result.song}</div>
                    </div>
                    <div style="text-align: center; margin-top: 15px; font-size: 0.8em;">
                        ✨ Transformed by Bollywoodify ✨
                    </div>
                </div>
            `;

            // Replace loading indicator with transformed content
            loadingDiv.replaceWith(bollywoodContent);
            transformedArticles.add(articleData.title);

        } catch (error) {
            console.error('Transformation failed:', error);
            loadingDiv.innerHTML = `
                <div style="padding: 20px; background: #FF4444; color: white; margin: 10px 0; border-radius: 5px;">
                    ❌ Transformation failed. Please try again later.
                </div>
            `;
            setTimeout(() => loadingDiv.remove(), 5000);
        } finally {
            isProcessing = false;
        }
    }

    // Auto-transform on page load
    function initialize() {
        if (getCurrentSite()) {
            // Wait for content to load
            setTimeout(() => {
                if (!transformedArticles.size) {
                    transformArticle();
                }
            }, 2000);
            
            // Add click listeners to headlines
            document.querySelectorAll('h1, h2, h3, .headline').forEach(headline => {
                headline.style.cursor = 'pointer';
                headline.addEventListener('click', () => transformArticle());
            });
        }
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initialize);
    } else {
        initialize();
    }

})();