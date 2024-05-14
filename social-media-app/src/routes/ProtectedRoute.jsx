import { Navigate } from "react-router-dom";

function ProtectedRoute({ children }) { // componente que verifica se o usuário está logueado
  const auth = localStorage.getItem("auth"); // se obtiene el token de autenticación del localStorage
  const { user } = auth && auth.user // se obtiene el usuario del localStorage
    ? JSON.parse(localStorage.getItem("auth")).user // si existe, se convierte a un objeto
    : { user: null }; // si no existe, se le asigna null
  // si el usuario existe, se renderiza el children, si no, se redirige a la página de inicio de sesión
  return user ? <>{children}</> : <Navigate to="/login/" />;
}
export default ProtectedRoute;
