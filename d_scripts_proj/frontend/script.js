document.addEventListener('DOMContentLoaded', () => {
    lucide.createIcons();
    fetchScripts();
});

const API_URL = '/api/scripts/';

async function fetchScripts() {
    const loader = document.getElementById('loader');
    const scriptsContainer = document.getElementById('scripts-container');
    const errorMessage = document.getElementById('error-message');

    loader.style.display = 'flex';
    scriptsContainer.innerHTML = '';
    errorMessage.classList.add('hidden');

    try {
        const response = await fetch(API_URL);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const scripts = await response.json();

        loader.style.display = 'none';

        if (scripts.length === 0) {
            scriptsContainer.innerHTML = `
                <div class="col-span-full text-center py-20">
                    <i data-lucide="inbox" class="mx-auto h-16 w-16 text-slate-500"></i>
                    <h2 class="mt-4 text-2xl font-bold text-white">No scripts yet</h2>
                    <p class="mt-2 text-slate-400">Check back later for new additions to the catalog.</p>
                </div>
            `;
            lucide.createIcons();
            return;
        }

        scripts.forEach(script => {
            const card = createScriptCard(script);
            scriptsContainer.appendChild(card);
        });

        lucide.createIcons();

    } catch (error) {
        console.error('Error fetching scripts:', error);
        loader.style.display = 'none';
        errorMessage.classList.remove('hidden');
    }
}

function createScriptCard(script) {
    const card = document.createElement('div');
    card.className = 'bg-slate-800/50 rounded-xl overflow-hidden shadow-lg hover:shadow-cyan-500/20 transition-all duration-300 flex flex-col border border-slate-700/50';

    const priceTag = script.is_free ?
        `<span class="bg-green-500 text-white px-3 py-1 text-sm font-semibold rounded-full">Free</span>` :
        `<span class="bg-cyan-500 text-white px-3 py-1 text-sm font-semibold rounded-full">$${parseFloat(script.price).toFixed(2)}</span>`;

    let videoEmbed = '';
    if (script.video_url) {
        const videoId = getYouTubeID(script.video_url);
        if (videoId) {
            videoEmbed = `
            <div class="aspect-w-16 aspect-h-9">
                <iframe src="https://www.youtube.com/embed/${videoId}" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen class="w-full h-full"></iframe>
            </div>`;
        } else {
             videoEmbed = `
             <div class="aspect-w-16 aspect-h-9 bg-slate-900 flex items-center justify-center">
                <a href="${script.video_url}" target="_blank" class="text-cyan-400 hover:text-cyan-300 flex items-center gap-2">
                    <i data-lucide="video"></i> View Demo
                </a>
             </div>`;
        }
    } else {
        videoEmbed = `
        <div class="aspect-w-16 aspect-h-9 bg-slate-900 flex items-center justify-center">
            <i data-lucide="image-off" class="h-12 w-12 text-slate-600"></i>
        </div>`;
    }

    card.innerHTML = `
        ${videoEmbed}
        <div class="p-6 flex flex-col flex-grow">
            <div class="flex justify-between items-start mb-2">
                <h3 class="text-xl font-bold text-white pr-4">${script.title}</h3>
                ${priceTag}
            </div>
            <p class="text-slate-400 flex-grow mb-6">${script.description}</p>
            <div class="mt-auto pt-4 border-t border-slate-700/50">
                 <button class="w-full bg-slate-700 hover:bg-cyan-600 text-white font-bold py-2 px-4 rounded-lg transition-colors flex items-center justify-center gap-2">
                    <i data-lucide="shopping-cart" class="h-5 w-5"></i>
                    Add to Cart
                </button>
            </div>
        </div>
    `;

    return card;
}

function getYouTubeID(url) {
    const regExp = new RegExp('^.*(youtu.be\\/|v\\/|u\\/\\w\\/|embed\\/|watch\\?v=|&v=)([^#&?]*).*', 'i');
    const match = url.match(regExp);
    return (match && match[2].length === 11) ? match[2] : null;
}
