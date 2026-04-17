// admin_panel.js
        const roleSelect = document.getElementById('role');
        const yearLevelGroup = document.getElementById('yearLevelGroup');
        const form = document.getElementById('registerForm');
        const responseBox = document.getElementById('responseMessage');

        // Show year level only for students
        roleSelect.addEventListener('change', () => {
            if (roleSelect.value === 'student') {
                yearLevelGroup.style.display = 'block';
            } else {
                yearLevelGroup.style.display = 'none';
            }
        });

        // Hide year level initially
        yearLevelGroup.style.display = 'none';

        form.addEventListener('submit', async (event) => {
            event.preventDefault();

            const formData = {
                first_name: document.getElementById('first_name').value,
                middle_name: document.getElementById('middle_name').value,
                last_name: document.getElementById('last_name').value,
                suffix: document.getElementById('suffix').value,
                birth_date: document.getElementById('birth_date').value,
                gender: document.getElementById('gender').value,
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
                role: document.getElementById('role').value,
                year_level: document.getElementById('year_level').value
            };

            try {
                const response = await fetch('http://127.0.0.1:5000/api/auth/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });

                const result = await response.json();

                responseBox.classList.remove('hidden');

                if (response.ok) {
                    responseBox.className = 'response-box success';
                    responseBox.innerHTML = `
                        <strong>Success:</strong> ${result.message}<br>
                        <strong>Profile ID:</strong> ${result.id}
                    `;

                    form.reset();
                    yearLevelGroup.style.display = 'none';
                } else {
                    responseBox.className = 'response-box error';
                    responseBox.innerHTML = `
                        <strong>Error:</strong> ${result.message || 'Something went wrong'}
                    `;
                }
            } catch (error) {
                responseBox.className = 'response-box error';
                responseBox.innerHTML = `
                    <strong>Error:</strong> Unable to connect to server
                `;
            }
        });
