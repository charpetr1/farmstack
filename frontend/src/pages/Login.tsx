import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import type { FormEvent } from "react";
import authApi from "../api/auth";
import { useAuth } from "../auth/useAuth";
import styles from "./Login.module.css";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();
  const { login } = useAuth();

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);

    try {
      const res = await authApi.login({ email, password });
      login(res.access_token);
      navigate("/lists");
    } catch {
      setError("Invalid email or password");
    }
  };

  return (
    <div className={styles.page}>
      <form className={styles.card} onSubmit={submit}>
        <h1>Login</h1>
        <p>Sign in to your account</p>

        {error && <p className={styles.error}>{error}</p>}

        <input
          value={email}
          onChange={e => setEmail(e.target.value)}
          placeholder="Email"
          type="email"
          required
        />

        <input
          value={password}
          onChange={e => setPassword(e.target.value)}
          type="password"
          placeholder="Password"
          required
        />

        <button type="submit">Login</button>

        <p className={styles.footer}>
          Not registered? <Link to="/register">Register</Link>
        </p>
      </form>
    </div>
  );
}
