import { useState } from 'react';

const GarminLogin = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        // Mock Action: Console log the credentials
        console.log('Sync Data Clicked');
        console.log('Email:', email);
        console.log('Password:', password);
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
