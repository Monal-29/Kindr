let currentCardIndex = 0;
let cards = [];
let currentCard = null;
let refreshInterval = null;
let lastCardCount = 0;

document.addEventListener('DOMContentLoaded', async function () {
    const token = checkAuth();
    if (!token) return;

    console.log('Initializing swipe page...');
    await loadCards();

    // Set up periodic refresh to check for newly verified requests
    // Check every 30 seconds for new verified requests
    refreshInterval = setInterval(async () => {
        console.log('Periodic check for new cards...');
        await checkForNewCards();
    }, 30000);

    // Reload cards when page becomes visible (user switches back to tab)
    document.addEventListener('visibilitychange', async () => {
        if (!document.hidden) {
            console.log('Page visible, checking for new cards...');
            await checkForNewCards();
        }
    });
});

async function loadCards() {
    try {
        console.log('Loading cards from API...');
        const newCards = await apiCall(API_CONFIG.ENDPOINTS.HELP_REQUESTS.GET_VERIFIED);
        console.log('API returned cards:', newCards);
        console.log('Number of cards:', newCards ? newCards.length : 0);

        // Ensure newCards is an array
        if (!Array.isArray(newCards)) {
            console.error('API did not return an array:', newCards);
            if (cards.length === 0) {
                document.getElementById('no-cards').style.display = 'block';
            }
            return;
        }

        // If we have no current cards but new cards are available, show them
        if (cards.length === 0 && newCards.length > 0) {
            console.log('No current cards, showing new cards');
            cards = newCards;
            currentCardIndex = 0;
            lastCardCount = newCards.length;
            document.getElementById('no-cards').style.display = 'none';
            showCard(0);
        } else if (newCards.length > 0) {
            // Update cards list, preserving current position if possible
            const currentCardId = currentCard ? currentCard.id : null;
            const previousLength = cards.length;
            cards = newCards;
            lastCardCount = newCards.length;

            console.log(`Cards updated: ${previousLength} -> ${newCards.length}, current index: ${currentCardIndex}`);

            // If we're at the end and new cards are available, show the first new one
            if (currentCardIndex >= previousLength && cards.length > 0) {
                console.log('At end of cards, showing first new card');
                currentCardIndex = 0;
                document.getElementById('no-cards').style.display = 'none';
                showCard(0);
            }
            // If we had a current card, try to maintain position
            else if (currentCardId && cards.length > 0) {
                const cardIndex = cards.findIndex(c => c.id === currentCardId);
                if (cardIndex >= 0) {
                    console.log(`Maintaining position at index ${cardIndex}`);
                    currentCardIndex = cardIndex;
                    showCard(cardIndex);
                } else if (currentCardIndex < cards.length) {
                    console.log(`Showing card at current index ${currentCardIndex}`);
                    showCard(currentCardIndex);
                }
            }
        } else {
            // No new cards available
            console.log('No cards available');
            lastCardCount = 0;
            if (cards.length === 0) {
                document.getElementById('no-cards').style.display = 'block';
            }
        }
    } catch (error) {
        console.error('Failed to load cards:', error);
        console.error('Error details:', error.message, error.stack);
        if (cards.length === 0) {
            document.getElementById('no-cards').style.display = 'block';
        }
    }
}

async function checkForNewCards() {
    try {
        const newCards = await apiCall(API_CONFIG.ENDPOINTS.HELP_REQUESTS.GET_VERIFIED);

        if (!Array.isArray(newCards)) {
            console.error('checkForNewCards: API did not return an array:', newCards);
            return;
        }

        console.log(`checkForNewCards: Current cards: ${cards.length}, New cards: ${newCards.length}, Last count: ${lastCardCount}`);

        // If we have no cards currently but new cards are available, reload
        if (cards.length === 0 && newCards.length > 0) {
            console.log('checkForNewCards: No current cards, new cards available - reloading');
            cards = newCards;
            lastCardCount = newCards.length;
            currentCardIndex = 0;
            document.getElementById('no-cards').style.display = 'none';
            showCard(0);
            return;
        }
        // If new cards were added (more than before), reload to show them
        else if (newCards.length > lastCardCount) {
            console.log(`checkForNewCards: New cards detected (${lastCardCount} -> ${newCards.length})`);
            // If we're currently showing "no cards", reload immediately
            if (currentCardIndex >= cards.length || !currentCard) {
                console.log('checkForNewCards: Currently at end, showing new cards immediately');
                cards = newCards;
                lastCardCount = newCards.length;
                currentCardIndex = 0;
                document.getElementById('no-cards').style.display = 'none';
                showCard(0);
            } else {
                // Otherwise, just update the cards list for next time
                console.log('checkForNewCards: Updating cards list');
                await loadCards();
            }
        } else {
            // Update the count even if no new cards
            lastCardCount = newCards.length;
        }
    } catch (error) {
        console.error('Failed to check for new cards:', error);
        console.error('Error details:', error.message);
    }
}

const SWIPE_THRESHOLD = 100;

function showCard(index) {
    if (index >= cards.length) {
        // Hide the no-cards message initially and check for new cards
        document.getElementById('no-cards').style.display = 'none';
        document.querySelector('.cards-container').innerHTML = '';

        // Check if there are new cards available
        checkForNewCards().then(() => {
            // After checking, if still no cards, show the message
            if (cards.length === 0) {
                document.getElementById('no-cards').style.display = 'block';
            }
        });
        return;
    }

    currentCardIndex = index;
    currentCard = cards[index];

    const container = document.querySelector('.cards-container');
    container.innerHTML = '';

    const card = document.createElement('div');
    card.className = 'card';
    card.id = 'current-card';
    card.innerHTML = `
        <div class="card-content">
            <div class="card-header-badge">${currentCard.category || 'Help Request'}</div>
            <h2>${currentCard.title}</h2>
            <p class="card-description">${currentCard.description}</p>
            <div class="card-details">
                <span class="badge urgency urgency-${currentCard.urgency}">${currentCard.urgency}</span>
                ${currentCard.location ? `<span class="badge location">📍 ${currentCard.location}</span>` : ''}
            </div>
            <div class="card-footer">
                <div class="user-info">
                    <div class="avatar-circle">${(currentCard.recipient_name || 'U').charAt(0).toUpperCase()}</div>
                    <span>${currentCard.recipient_name}</span>
                </div>
            </div>
        </div>
    `;

    container.appendChild(card);

    // Initialize Swipe Logic
    initSwipeGestures(card);
}

function initSwipeGestures(card) {
    let startX = 0;
    let startY = 0;
    let isDragging = false;
    let currentX = 0;
    let currentY = 0;

    const handleStart = (clientX, clientY) => {
        startX = clientX;
        startY = clientY;
        isDragging = true;

        // Reset transition during drag for responsiveness
        card.style.transition = 'none';
    };

    const handleMove = (clientX, clientY) => {
        if (!isDragging) return;
        currentX = clientX;
        currentY = clientY;
        const diffX = currentX - startX;
        const diffY = currentY - startY;

        // Calculate rotation based on X movement (max 30 degrees)
        const rotation = diffX * 0.1;

        card.style.transform = `translate(${diffX}px, ${diffY}px) rotate(${rotation}deg)`;

        // Visual feedback based on direction
        if (diffX > 50) {
            // Right swipe green hint
            card.style.boxShadow = '0 0 20px rgba(76, 175, 80, 0.4)';
            card.style.border = '2px solid rgba(76, 175, 80, 0.4)';
        } else if (diffX < -50) {
            // Left swipe red hint
            card.style.boxShadow = '0 0 20px rgba(244, 67, 54, 0.4)';
            card.style.border = '2px solid rgba(244, 67, 54, 0.4)';
        } else {
            card.style.boxShadow = '0 10px 40px rgba(0, 0, 0, 0.1)';
            card.style.border = 'none';
        }
    };

    const handleEnd = () => {
        if (!isDragging) return;
        isDragging = false;

        const diffX = currentX - startX;

        // Restore transition for smooth return or fly-off
        card.style.transition = 'transform 0.5s ease, opacity 0.5s ease, box-shadow 0.3s ease';
        card.style.boxShadow = '0 10px 40px rgba(0, 0, 0, 0.1)';
        card.style.border = 'none';

        if (Math.abs(diffX) > SWIPE_THRESHOLD) {
            if (diffX > 0) {
                swipeRight();
            } else {
                swipeLeft();
            }
        } else {
            // Reset position
            card.style.transform = 'translate(0, 0) rotate(0)';
        }
    };

    // Touch Events
    card.addEventListener('touchstart', (e) => handleStart(e.touches[0].clientX, e.touches[0].clientY));
    card.addEventListener('touchmove', (e) => handleMove(e.touches[0].clientX, e.touches[0].clientY));
    card.addEventListener('touchend', (e) => {
        // We rely on currentX which was updated in move.
        // If it was a tap without move, diffX is effectively 0 from last drag or uninitialized?
        // Let's rely on isDragging check and handleEnd logic using last positions
        handleEnd();
    });

    // Mouse Events
    card.addEventListener('mousedown', (e) => {
        handleStart(e.clientX, e.clientY);
        e.preventDefault(); // Prevent text selection/image drag
    });

    // Attach mouse move/up to document to handle dragging outside card
    document.addEventListener('mousemove', (e) => {
        if (isDragging) {
            handleMove(e.clientX, e.clientY);
        }
    });

    document.addEventListener('mouseup', () => {
        if (isDragging) {
            handleEnd();
        }
    });
}

async function swipeRight() {
    if (!currentCard) return;

    try {
        await apiCall(API_CONFIG.ENDPOINTS.SWIPES.CREATE, 'POST', {
            help_request_id: currentCard.id,
            action: 'like'
        });

        const card = document.getElementById('current-card');
        if (card) {
            card.style.transform = 'translateX(1000px) rotate(30deg)';
            card.style.opacity = '0';
            setTimeout(() => {
                showCard(currentCardIndex + 1);
            }, 300);
        }
    } catch (error) {
        console.error('Swipe failed:', error);
        alert('Failed to record swipe: ' + error.message);
    }
}

async function swipeLeft() {
    if (!currentCard) return;

    try {
        await apiCall(API_CONFIG.ENDPOINTS.SWIPES.CREATE, 'POST', {
            help_request_id: currentCard.id,
            action: 'pass'
        });

        const card = document.getElementById('current-card');
        if (card) {
            card.style.transform = 'translateX(-1000px) rotate(-30deg)';
            card.style.opacity = '0';
            setTimeout(() => {
                showCard(currentCardIndex + 1);
            }, 300);
        }
    } catch (error) {
        console.error('Swipe failed:', error);
        alert('Failed to record swipe: ' + error.message);
    }
}

async function refreshCards() {
    console.log('Manual refresh triggered');
    // Reset to start and reload all cards
    currentCardIndex = 0;
    cards = [];
    lastCardCount = 0;
    await loadCards();
    if (cards.length > 0) {
        document.getElementById('no-cards').style.display = 'none';
        showCard(0);
    } else {
        document.getElementById('no-cards').style.display = 'block';
    }
}

