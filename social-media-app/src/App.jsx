import { Route, Routes } from "react-router-dom";
import ProtectedRoute from "./routes/ProtectedRoute";
import Home from "./pages/Home";
import Registration from "./pages/Registration";
import Login from "./pages/Login";

function App() {
  return (
    <Routes>
      <Route
        path="/"
        element={
          <ProtectedRoute> {/* aqui estoy protegiendo esta vista, osea que le digo que debe iniciar sesión para logran ingresar, gracias a la comprobacin de ese componente */}
            <Home />
          </ProtectedRoute>
        }
      />
      <Route path="/register/" element={<Registration />} />
      <Route path="/login/" element={<Login />} />
      </Routes>
  );
}
export default App;
