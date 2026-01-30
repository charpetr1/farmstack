import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { ThemeProvider } from "./theme/ThemeProvider";

import Login from "./pages/Login";
import Register from "./pages/Register";
import ListTodoLists from "./pages/ListTodoLists";
import ToDoList from "./pages/ToDoList";

import ProtectedRoute from "./components/ProtectedRoute";
import Layout from "./layout/Layout";

function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <Routes>
          {/* Public routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* Protected routes */}
          <Route
            path="/lists"
            element={
              <ProtectedRoute>
                <Layout />
              </ProtectedRoute>
            }
          >
            <Route index element={<ListTodoLists />} />
            <Route path=":id" element={<ToDoList />} />
          </Route>

          {/* Redirect root */}
          <Route path="/" element={<Navigate to="/lists" replace />} />

          {/* Fallback */}
          <Route path="*" element={<Navigate to="/lists" replace />} />
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;
