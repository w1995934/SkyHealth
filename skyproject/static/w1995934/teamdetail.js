document.addEventListener('DOMContentLoaded', () => {
    const setupMemberInteractions = () => {
        const memberCards = document.querySelectorAll('.member-card');
        const sessionContainer = document.getElementById('session-container');

        memberCards.forEach(card => {
            card.addEventListener('click', async () => {
                memberCards.forEach(c => c.classList.remove('active'));
                card.classList.add('active');
                
                const memberId = card.dataset.memberId; //add employee ids
                const response = await fetch(``); // add fetch
                const sessions = await response.json();
                renderSessions(sessions);
            });
        });

        const renderSessions = (sessions) => {
            sessionContainer.innerHTML = sessions.length 
                ? sessions.map(session => `
                    <div class="session-card" data-session-id="${session.id}">
                        <h3>${session.date}</h3>
                        <button class="delete-session">Remove Session</button>
                    </div>
                `).join('')
                : '<p class="empty-state">No sessions found</p>'; //add session id and date

            setupDeleteButtons();
        };

        const setupDeleteButtons = () => {
            document.querySelectorAll('.delete-session').forEach(button => {
                button.addEventListener('click', async (e) => {
                    const card = e.target.closest('.session-card');
                    const sessionId = card.dataset.sessionId; //add session ids

                    await fetch(`/api/sessions/${sessionId}/`, {
                        method: 'DELETE',
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken') //add toekn
                        }
                    });
                    card.remove();
                });
            });
        };

        const getCookie = (name) => {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let cookie of cookies) {
                    cookie = cookie.trim();
                    if (cookie.startsWith(name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        };};

    setupMemberInteractions();
});
