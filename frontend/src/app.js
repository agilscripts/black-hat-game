import React, { useState } from "react";
import axios from "axios";

function App() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [token, setToken] = useState(null);
  const [challengeInput, setChallengeInput] = useState("");
  const [challengeResult, setChallengeResult] = useState(null);

  const handleRegister = async () => {
    try {
      await axios.post("http://127.0.0.1:5000/register", { username, password });
      alert("User registered successfully");
    } catch (error) {
      alert("Registration failed: " + error.response.data.error);
    }
  };

  const handleLogin = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:5000/login", { username, password });
      setToken(response.data.token);
      alert("Login successful");
    } catch (error) {
      alert("Login failed: " + error.response.data.message);
    }
  };

  const handleSQLInjection = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:5000/challenge/sql_injection", { input: challengeInput });
      setChallengeResult(response.data.message);
    } catch (error) {
      setChallengeResult("Failed attempt: " + error.response.data.message);
    }
  };

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h1>Black Hat Game</h1>
      {!token ? (
        <div>
          <h2>Register / Login</h2>
          <input type="text" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} /><br/>
          <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} /><br/>
          <button onClick={handleRegister}>Register</button>
          <button onClick={handleLogin}>Login</button>
        </div>
      ) : (
        <div>
          <h2>SQL Injection Challenge</h2>
          <input type="text" placeholder="Enter SQL Input" value={challengeInput} onChange={(e) => setChallengeInput(e.target.value)} /><br/>
          <button onClick={handleSQLInjection}>Submit</button>
          {challengeResult && <p>{challengeResult}</p>}
        </div>
      )}
    </div>
  );
}

export default App;
