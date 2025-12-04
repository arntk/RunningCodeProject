import { useState } from 'react';

const GarminLogin = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        console.log('Sync Data Clicked');

        try {
            const response = await fetch('http://localhost:5000/api/sync', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password }),
            });

            if (response.ok) {
                alert('Sync Successful!');
            } else {
                alert('Sync Failed. Check credentials.');
            }
        } catch (error) {
            console.error('Error syncing:', error);
            alert('Sync Failed. Check credentials.');
        }
    };

    return (
        <div className="card login-card">
            <h2>Connect your Garmin</h2>
            <form onSubmit={handleSubmit} className="login-form">
                <div className="form-group">
                    <label>Email:</label>
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                        placeholder="Enter your email"
                    />
                </div>
                <div className="form-group">
                    <label>Password:</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        placeholder="Enter your password"
                    />
                </div>
                <button type="submit">
                    Sync Data
                </button>
            </form>
        </div>
    );
};

export default GarminLogin;
